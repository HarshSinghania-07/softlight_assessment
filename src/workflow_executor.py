"""
Executes workflow steps defined in configuration.
"""

from loguru import logger
from src.state_detector import StateDetector
from src.state_capturer import StateCapturer

class WorkflowExecutor:
    """
    Coordinates the execution of workflow actions and state capture.
    """

    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.detector = StateDetector(page)

    def run_workflow(self, app_name: str, workflow_name: str):
        """
        Executes each step for a given workflow.
        """
        logger.info(f"Running workflow: {workflow_name} for {app_name}")
        app = next(app for app in self.config["apps"] if app["name"] == app_name)
        workflow = next(w for w in app["workflows"] if w["name"] == workflow_name)
        base_url = app.get("url")

        capturer = StateCapturer(f"datasets/{app_name}/{workflow_name}")
        steps = workflow["steps"]

        # Step 1: Open the base URL before beginning
        if base_url:
            logger.info(f"Navigating to base URL: {base_url}")
            self.page.goto(base_url, wait_until="load")
            capturer.capture(self.page, "initial_load", f"Opened {base_url}")

        # Step 2: Iterate through defined steps
        for step in steps:
            logger.info(f"Executing step: {step}")

            # Define basic step logic (extend later)
            if step == "wait_for_load":
                self.page.wait_for_timeout(2000)
            elif step.startswith("capture_"):
                # Capture UI after specific step
                self.detector.detect_state_change()
                capturer.capture(self.page, step, f"Captured UI for {step}")
            elif step == "open_homepage":
                # Optional redundancy, ensure URL is loaded
                self.page.goto(base_url, wait_until="load")
            else:
                # Placeholder for any other step action
                self.page.wait_for_timeout(1000)

        capturer.save_metadata()
