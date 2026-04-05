import os

from debug_agent.prompts.react_prompt import build_prompt

from debug_agent.tools.runner import run_code
from debug_agent.tools.patcher import apply_patch
from debug_agent.validation.fix_validator import validate_fix

from debug_agent.agent.parser import parse_llm_output

#### Changes added before Day 5
from debug_agent.core.error_classifier import ErrorClassifier
from debug_agent.utils.dependency_utils import extract_missing_module
from debug_agent.tools.installer import install_package, PACKAGE_MAPPING

from debug_agent.core.confidence_scorer import ConfidenceScorer

from debug_agent.tools.web_search import search_web

from debug_agent.observability.debug_trace import DebugTrace

class ReactAgent:

    def __init__(self, llm, logger, tracer, metrics):
        self.llm = llm
        self.logger = logger
        self.tracer = tracer
        self.metrics = metrics
        self.scorer = ConfidenceScorer()

    def map_file_to_sandbox(self, file_name, relevant_files):
        """
        Handles:
        - filename.py
        - /full/path/to/file.py
        - ./relative/path/file.py
        """

        self.logger.log(
                    message="Mapping file",
                    llm_file=file_name,
                    normalized=os.path.basename(file_name),
                    available_files=[os.path.basename(f) for f in relevant_files]
        )
        
        # Normalize LLM output
        normalized_name = os.path.basename(file_name)

        for f in relevant_files:
            if os.path.basename(f) == normalized_name:
                return f
        
        return None
    
    def get_relative_path(self, full_path, sandbox_path):
        """
        Convert sandbox path -> project relative path
        """
        try:
            return os.path.relpath(full_path, sandbox_path)
        except Exception:
            return os.path.basename(full_path)
    
    def run(self, context, entry_point, sandbox_path, initial_error):

        current_error = initial_error
        previous_attempts = []
        seen_errors = []
        trace = DebugTrace() ## debug trace
        trace.add("initial_error", current_error) ## debug trace

        for iteration in range(5):

            with self.tracer.start_span(f"iteration_{iteration}"):

                self.metrics.record_iteration()

                ### Web results
                if iteration >= 2:
                    self.logger.log(message="Triggering web search", error=current_error)

                    web_results = search_web(current_error)

                    context["web_results"] = web_results

                ### Build prompt ###
                prompt = build_prompt(context, previous_attempts, current_error)

                ### error classification before LLM call
                classifier = ErrorClassifier()
                error_type = classifier.classify(current_error)

                if error_type == "missing_dependency":

                    missing_pkg = extract_missing_module(current_error)

                    if missing_pkg:

                        install_name = PACKAGE_MAPPING.get(missing_pkg, missing_pkg)

                        self.logger.log(
                            message="Installing missing dependency",
                            package=install_name
                        )

                        install_result = install_package(install_name, sandbox_path)

                        if install_result["success"]:
                            result = run_code(entry_point, sandbox_path)

                            if result.get("success"):
                                return {
                                    "root_cause": f"Missing dependency: {install_name}",
                                    "action": f"Installed {install_name}",
                                    "status": "fixed"
                                }
                            
                            current_error = result.get("stderr", "")

                        else:
                            return {"error": f"Failed to install {install_name}"}

                ##############################
                response = self.llm.generate(prompt)

                parsed = parse_llm_output(response)
                trace.add("llm_output", parsed.dict()) ## debug trace

                ## smart retry
                if parsed.fixed_code in [d["fixed_code"] for d in previous_attempts]:
                    self.logger.log(message="Skipping repeated fix")
                    continue

                # previous_attempts.append({
                #     "iteration": iteration,
                #     "reason": parsed.reason,
                #     "status": status
                # })

                if not parsed:
                    self.logger.log("error", "Invalid LLM output", response=response)
                    continue

                target_file = self.map_file_to_sandbox(
                    parsed.file,
                    context["relevant_files"]
                )

                if not target_file:
                    self.logger.log(
                        "error",
                        "File mapping failed",
                        llm_output=parsed.file,
                        available=context["relevant_files"] 
                    )
                    return {"error": f"File {parsed.file} not found"}
                
                # Apply fix
                apply_patch(target_file, parsed.fixed_code)

                # Run code
                result = run_code(entry_point, sandbox_path)

                trace.add("execution_result", result) ## debug trace

                status = validate_fix(current_error, result)

                new_error = result.get("stderr", "") or result.get("error", "")

                previous_attempts.append({
                    "iteration": iteration,
                    "reason": parsed.reason,
                    "status": status,
                    "fixed_code": parsed.fixed_code, ## smart retry
                })

                self.logger.log(
                    message="Iteration result",
                    iteration=iteration,
                    status=status
                )

                seen_errors.append(new_error)

                relative_path = self.get_relative_path(target_file, sandbox_path)

                # condidence calculation
                confidence = self.scorer.score(initial_error, result, iteration + 1)

                # Success
                if status == "success":
                    self.metrics.mark_success()

                    return {
                        "root_cause": parsed.reason,
                        "file_to_change": relative_path,
                        "file_name": os.path.basename(target_file),
                        "fixed_code": parsed.fixed_code,
                        "confidence": confidence,
                        "debug_trace": trace.get() ## debug trace
                    }
                
                # Early stop: repeated error
                if seen_errors.count(new_error) >= 2:
                    return {"error": "Repeated error, stopping early"}
                
                # Early stop: no improvement
                if new_error == current_error:
                    return {"error": "No improvement, stopping"}
                
                current_error = new_error

        return {"error": "Max iterations reached"}