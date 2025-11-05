"""
Entry point for the Autonomous UI State Capture System (Agent B)
"""

import argparse
from loguru import logger
from src.config_loader import ConfigLoader
from src.browser_manager import BrowserManager
from src.workflow_executor import WorkflowExecutor
from src.task_interpreter import TaskInterpreter

def main():
    parser = argparse.ArgumentParser(description="Autonomous UI State Capture System")
    parser.add_argument("--app", type=str, help="Name of the app (e.g., Linear, Notion)")
    parser.add_argument("--workflow", type=str, help="Workflow name from YAML config")
    parser.add_argument("--query", type=str, help="Natural language query from Agent A")
    args = parser.parse_args()

    logger.info("=== Starting UI State Capture System ===")

    # Load configuration
    try:
        loader = ConfigLoader("config/tasks.yaml")
        config = loader.load_config()
        logger.info("Configuration loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return

    # Launch browser
    browser_manager = BrowserManager()
    page = browser_manager.launch_browser() 

    # Initialize workflow executor
    executor = WorkflowExecutor(page, config)

    # -------------------
    # Dynamic Query Mode 
    # -------------------
    if args.query:
        logger.info(f"Received dynamic query: {args.query}")
        try:
            interpreter = TaskInterpreter()
            app_name, dynamic_workflow = interpreter.interpret(args.query)
            executor.run_dynamic_workflow(app_name, dynamic_workflow)
        except Exception as e:
            logger.error(f"Error interpreting query: {e}")

    # ---------------------
    # Predefined YAML Mode 
    # ---------------------
    else:
        # If app/workflow not provided
        if not args.app or not args.workflow:
            print("\n No app or workflow provided. Let's choose one interactively!")
            print("Available apps:")
            for app in config["apps"]:
                print(f" - {app['name']}")
            app_choice = input("\nEnter the app name: ").strip()

            selected_app = next((app for app in config["apps"] if app["name"].lower() == app_choice.lower()), None)
            if not selected_app:
                logger.error(f"App '{app_choice}' not found in config.")
                browser_manager.close_browser(browser)
                return

            print(f"\nAvailable workflows for {selected_app['name']}:")
            for wf in selected_app["workflows"]:
                print(f" - {wf['name']}")
            workflow_choice = input("\nEnter the workflow name: ").strip()

            args.app = selected_app["name"]
            args.workflow = workflow_choice

        try:
            logger.info(f"Running predefined workflow: {args.workflow} for {args.app}")
            executor.run_workflow(args.app, args.workflow)
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")

    browser_manager.close_browser()
    logger.info("=== Workflow execution completed ===")

if __name__ == "__main__":
    main()