from debug_agent.sandbox.sandbox_manager import SandboxManager
from debug_agent.observability.logger import Logger
from debug_agent.observability.tracer import Tracer
from debug_agent.sandbox.sandbox_cleanup import cleanup_old_sandboxes

def main():

    cleanup_old_sandboxes()

    logger = Logger()
    tracer = Tracer()

    project_path = "/Users/ashishpal/Documents/GenAI_Projects/for_testing/example_project" # change this

    with tracer.start_span("debugger_run"):
        logger.log(message="Starting debugger", path=project_path)

        sandbox = SandboxManager(project_path)

        try:
            sandbox_path = sandbox.setup()

            # run agent here
        finally:
            sandbox.cleanup()

        logger.log(message="Sandbox created", sandbox_path=sandbox_path)

        print(f"Sandbox Path: {sandbox_path}")

if __name__ == "__main__":
    main()