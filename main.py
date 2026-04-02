from debug_agent.sandbox.sandbox_manager import SandboxManager
from debug_agent.observability.logger import Logger
from debug_agent.observability.tracer import Tracer
from debug_agent.sandbox.sandbox_cleanup import cleanup_old_sandboxes

from debug_agent.core.analyzer import ProjectAnalyzer
from debug_agent.core.dependency_graph import DependencyGraph
from debug_agent.core.traceback_parser import TracebackParser
from debug_agent.core.context_builder import ContextBuilder

from debug_agent.tools.runner import run_code
from debug_agent.tools.linter import lint_code
from debug_agent.tools.patcher import apply_patch

from debug_agent.validation.fix_validator import validate_fix

def main():

    cleanup_old_sandboxes()

    logger = Logger()
    tracer = Tracer()

    project_path = "/Users/ashishpal/Documents/GenAI_Projects/for_testing" # change this

    with tracer.start_span("debugger_run"):
        logger.log(message="Starting debugger", path=project_path)

        sandbox = SandboxManager(project_path)

        try:
            sandbox_path = sandbox.setup()

            traceback = """
            File "/example_project/main.py", line 1, in <module>
                from utils import printUtils
            File "/example_project/utils.py", line 1
                def printUtils()
                                ^
            SyntaxError: expected ':'
            """

            # File index and analyze
            analyzer = ProjectAnalyzer(sandbox_path)
            files = analyzer.build_file_index()
            print(files)

            # dependency graph
            graph = DependencyGraph().build(analyzer)
            print(graph.edges())

            # run_code tool call
            result = run_code("example_project/main.py", sandbox_path)
            print(result)

            # traceback parser
            parser = TracebackParser()
            trace_data = parser.parse(result["stderr"])
            print(trace_data)

            # context builder
            context_builder = ContextBuilder(files)
            context = context_builder.build(trace_data)
            print(context)
            
            
            for file in context["relevant_files"]:
                lint_result = lint_code(file)
                print(lint_result)

            # apply_path test
            print("Initial Run:", result)

            old_error = result.get("stderr", "")

            # Apply manual fix (simulate LLM fix)
            fixed_code = """def printUtils():
                print("utility code")
            """

            apply_patch(f"{sandbox_path}/example_project/utils.py",
                        fixed_code
            )

            # run again
            new_result = run_code("example_project/utils.py", sandbox_path)
            print("After Fix:", new_result)

            # Validate
            status = validate_fix(old_error, new_result)

            print("Validation:", status)

            # run agent here
        finally:
            sandbox.cleanup()

        logger.log(message="Sandbox created", sandbox_path=sandbox_path)

        print(f"Sandbox Path: {sandbox_path}")


if __name__ == "__main__":
    main()