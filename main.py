"""
main.py
Entry point for the UI State Capture agent.
"""

from src.browser_manager import BrowserManager
from src.config_loader import ConfigLoader
from src.workflow_executor import WorkflowExecutor
from src.dataset_manager import DatasetManager
from loguru import logger
import argparse

def main(app: str, workflow: str):
    logger.info("=== Starting UI State Capture System ===")

    # Load configuration
    config = ConfigLoader("config/tasks.yaml").load_config()

    # Initialize dataset structure
    DatasetManager().create_app_folder(app)

    # Launch browser
    browser_mgr = BrowserManager(headless=False)
    page = browser_mgr.launch_browser()

    # Execute workflow
    executor = WorkflowExecutor(page, config)
    executor.run_workflow(app, workflow)

    # Close browser
    browser_mgr.close_browser()
    logger.info("=== Workflow execution completed ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", required=True, help="Application name (e.g., Linear)")
    parser.add_argument("--workflow", required=True, help="Workflow name (e.g., create_project)")
    args = parser.parse_args()

    main(args.app, args.workflow)