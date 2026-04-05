import os
import shutil

import networkx as nx

from debug_agent.sandbox.sandbox_manager import SandboxManager
from debug_agent.sandbox.sandbox_cleanup import cleanup_old_sandboxes

from debug_agent.core.analyzer import ProjectAnalyzer
from debug_agent.core.dependency_graph import DependencyGraph
from debug_agent.core.traceback_parser import TracebackParser
from debug_agent.core.context_builder import ContextBuilder

from debug_agent.agent.react_agent import ReactAgent
from debug_agent.agent.llm import LLM

from debug_agent.observability.logger import Logger
from debug_agent.observability.tracer import Tracer
from debug_agent.observability.metrics import Metrics

from debug_agent.tools.runner import run_code

# -------------------------------
# Step 1: Run Debugger
# -------------------------------

def run_test():

    cleanup_old_sandboxes()

    logger = Logger()
    tracer = Tracer()
    metrics = Metrics()

    project_path = "/Users/ashishpal/Documents/GenAI_Projects/for_testing/example_project"

    # create sandbox
    sandbox = SandboxManager(project_path)

    try:
        sandbox_path = sandbox.setup()

        logger.log(message="Sandbox ready", sandbox=sandbox_path)

        # -------------------------------
        # Step A: Run initial code
        # -------------------------------
        entry_point = "main.py"

        initial_result = run_code(entry_point, sandbox_path, sandbox.venv_path)

        print("\n=== INITIAL RUN ===")
        print(initial_result)

        initial_error = initial_result.get("stderr", "") or initial_result.get("error", "")
        
        # -------------------------------
        # Step B: Static Analysis
        # -------------------------------
        analyzer = ProjectAnalyzer(sandbox_path)
        files = analyzer.build_file_index()

        graph = DependencyGraph().build(analyzer)

        parser = TracebackParser()
        traceback_data = parser.parse(initial_error)
        print("\n=== Traceback ===\n")
        print(traceback_data)

        context_builder = ContextBuilder(files, logger)
        context = context_builder.build(traceback_data)

        print("\n=== CONTEXT BUILT ===")
        print(context["snippets"])

        # -------------------------------
        # Step C: Run Agent
        # -------------------------------
        llm = LLM() # change the model if needed

        agent = ReactAgent(llm, logger, tracer, metrics)

        result = agent.run(
            context=context,
            entry_point=entry_point,
            sandbox_path=sandbox_path,
            initial_error=initial_error,
            venv_path=sandbox.venv_path
        )

        print("\n=== FINAL RESULT ===")
        print(result)

        print("\n=== METRICS ===")
        print(metrics.get_metrics())
    
    finally:
        sandbox.cleanup()

if __name__ == "__main__":
    run_test()