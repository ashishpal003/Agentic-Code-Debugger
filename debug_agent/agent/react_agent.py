import os

from debug_agent.prompts.react_prompt import build_prompt

from debug_agent.tools.runner import run_code
from debug_agent.tools.patcher import apply_patch
from debug_agent.validation.fix_validator import validate_fix

from debug_agent.agent.parser import parse_llm_output

class ReactAgent:

    def __init__(self, llm, logger, tracer, metrics):
        self.llm = llm
        self.logger = logger
        self.tracer = tracer
        self.metrics = metrics

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

        for iteration in range(5):

            with self.tracer.start_span(f"iteration_{iteration}"):

                self.metrics.record_iteration()

                # Build prompt
                prompt = build_prompt(context, previous_attempts, current_error)

                response = self.llm.generate(prompt)

                parsed = parse_llm_output(response)

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

                status = validate_fix(current_error, result)

                new_error = result.get("stderr", "") or result.get("error", "")

                previous_attempts.append({
                    "iteration": iteration,
                    "reason": parsed.reason,
                    "status": status
                })

                self.logger.log(
                    message="Iteration result",
                    iteration=iteration,
                    status=status
                )

                seen_errors.append(new_error)

                relative_path = self.get_relative_path(target_file, sandbox_path)

                # Success
                if status == "success":
                    self.metrics.mark_success()
                    return {
                        "root_cause": parsed.reason,
                        "file_to_change": relative_path,
                        "file_name": os.path.basename(target_file),
                        "fixed_code": parsed.fixed_code 
                    }
                
                # Early stop: repeated error
                if seen_errors.count(new_error) >= 2:
                    return {"error": "Repeated error, stopping early"}
                
                # Early stop: no improvement
                if new_error == current_error:
                    return {"error": "No improvement, stopping"}
                
                current_error = new_error

        return {"error": "Max iterations reached"}