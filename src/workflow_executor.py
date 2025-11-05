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

        if base_url:
            logger.info(f"Navigating to base URL: {base_url}")
            self.page.goto(base_url, wait_until="load")
            extra_wait = 5000  
            logger.debug(f"Waiting {extra_wait/1000}s for page assets to finish loading...")
            self.page.wait_for_timeout(extra_wait)
            capturer.capture(self.page, "initial_load", f"Opened {base_url} after stabilization delay")

        for step in steps:
            logger.info(f"Executing step: {step}")

            if step == "wait_for_load":
                self.page.wait_for_timeout(2000)

            elif step == "open_homepage":
                self.page.goto(base_url, wait_until="load")
                self.page.wait_for_timeout(1500)

            elif step == "click_login":
                logger.debug("Clicking 'Log in' on Linear...")
                self.page.click("text='Log in'", timeout=5000)
                self.page.wait_for_timeout(2000)

            elif step == "click_product":
                logger.debug("Clicking 'Product' on Linear...")
                self.page.click("text='Product'", timeout=5000)
                self.page.wait_for_load_state("load")
                self.page.wait_for_timeout(1500)

            elif step == "scroll_to_features":
                logger.debug("Scrolling down to Features section...")
                for i in range(3):
                    self.page.mouse.wheel(0, 1000)
                    self.page.wait_for_timeout(800)
                self.page.wait_for_timeout(1000)

            elif step == "click_pricing":
                logger.debug("Clicking 'Pricing' on Notion...")
                self.page.click("text='Pricing'", timeout=5000)
                self.page.wait_for_timeout(2000)

            elif step == "type_email_field":
                logger.debug("Typing into email field (Notion sign-up)...")
                try:
                    self.page.click("text='Log in'")
                    self.page.wait_for_selector("input[type='email']", timeout=4000)
                    self.page.fill("input[type='email']", "test@example.com")
                    self.page.wait_for_timeout(1500)
                except Exception as e:
                    logger.warning(f"Could not find email input: {e}")

            elif step.startswith("capture_"):
                self.detector.detect_state_change()
                capturer.capture(self.page, step, f"Captured UI for {step}")

            else:
                logger.warning(f"Unknown step: {step}. Waiting briefly.")
                self.page.wait_for_timeout(1000)
        capturer.save_metadata()
        logger.info(f"Workflow '{workflow_name}' completed successfully.")
    def run_dynamic_workflow(self, app_name, workflow):
        """
        Executes a workflow dynamically generated at runtime.
        """
        logger.info(f"Running dynamic workflow: {workflow['name']} for {app_name}")
        base_url = next(app["url"] for app in self.config["apps"] if app["name"] == app_name)
        capturer = StateCapturer(f"datasets/{app_name}/{workflow['name']}")

        self.page.goto(base_url, wait_until="load")
        self.page.wait_for_timeout(5000)
        capturer.capture(self.page, "initial_load", f"Opened {base_url}")

        for step in workflow["steps"]:
            logger.info(f"Executing step: {step}")
            self.execute_step(app_name, step, capturer)

        capturer.save_metadata()
