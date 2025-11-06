import os, time
from loguru import logger
from src.state_capturer import StateCapturer
from playwright.sync_api import Page


class WorkflowExecutor:
    def __init__(self, page: Page):
        self.page = page

    def run_dynamic_workflow(self, plan: dict):
        app = plan.get("app", "Unknown")
        workflow = plan.get("workflow", "Unnamed_Workflow").replace(" ", "_")
        steps = plan.get("steps", [])

        logger.info(f"Starting guided workflow for {app}: {workflow}")
        workflow_folder = f"datasets/{app}/{workflow}"
        os.makedirs(workflow_folder, exist_ok=True)
        capturer = StateCapturer(self.page, workflow_folder)
        base_urls = {"Notion": "https://www.notion.so", "Linear": "https://linear.app"}
        homepage_url = base_urls.get(app, "https://www.google.com")

        step_num = 1
        logger.info(f"Opening homepage for {app}: {homepage_url}")
        self.page.goto(homepage_url, timeout=60000)
        self.page.wait_for_load_state("networkidle")
        time.sleep(3)
        capturer.capture(app, f"{step_num:02d}_homepage")
        step_num += 1

        for step in steps:
            try:
                action = step.get("action", "").upper()
                url = step.get("url")
                name = step.get("name", f"step_{step_num:02d}")

                if action == "OPEN" and url != homepage_url:
                    logger.info(f"Navigating to: {url}")
                    self.page.goto(url, timeout=60000)
                    self.page.wait_for_load_state("networkidle")
                    time.sleep(3)
                    capturer.capture(app, f"{step_num:02d}_{name}")
                    step_num += 1

                elif action == "WAIT":
                    delay = step.get("seconds", 2)
                    logger.info(f"Waiting for {delay} seconds...")
                    time.sleep(delay)

                elif action == "CAPTURE":
                    logger.info(f"Capturing step: {name}")
                    capturer.capture(app, f"{step_num:02d}_{name}")
                    step_num += 1

            except Exception as e:
                logger.error(f"Error in step {step_num}: {e}")

        capturer.save_metadata(app, workflow)
        logger.info(f"Workflow completed for {app}: {workflow}")