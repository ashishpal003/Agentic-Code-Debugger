from debug_agent.sandbox.sandbox_manager import SandboxManager
from debug_agent.observability.logger import Logger
from debug_agent.observability.tracer import Tracer
from debug_agent.sandbox.sandbox_cleanup import cleanup_old_sandboxes

from debug_agent.core.analyzer import ProjectAnalyzer
from debug_agent.core.dependency_graph import DependencyGraph
from debug_agent.core.traceback_parser import TracebackParser
from debug_agent.core.context_builder import ContextBuilder

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

            parser = TracebackParser()
            trace_data = parser.parse(traceback)
            print(trace_data)

            context_builder = ContextBuilder(files)
            context = context_builder.build(trace_data)
            print(context)

            # run agent here
        finally:
            sandbox.cleanup()

        logger.log(message="Sandbox created", sandbox_path=sandbox_path)

        print(f"Sandbox Path: {sandbox_path}")

if __name__ == "__main__":
    main()