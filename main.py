from loguru import logger
from src.llm_manager import LLMManager
from src.browser_manager import BrowserManager
from src.workflow_executor import WorkflowExecutor

def main():
    logger.info("=== Starting UI State Capture ===")

    query = input("Enter your request: ")

    llm = LLMManager()
    plan = llm.generate_workflow_plan(query)
    logger.info(f"Generated Plan: {plan}")

    browser = BrowserManager()
    page = browser.launch_browser()

    executor = WorkflowExecutor(page)
    executor.run_dynamic_workflow(plan)

    browser.close_browser()
    logger.info("=== Done ===")


if __name__ == "__main__":
    main()