import os
import time
import re
from loguru import logger
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from src.state_capturer import StateCapturer


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
        step_num = 1
        for step in steps:
            try:
                action = step.get("action", "").upper()
                url = step.get("url")
                name = step.get("name", f"step_{step_num:02d}")
                if action == "OPEN" and url:
                    logger.info(f"Opening URL: {url}")
                    try:
                        self.page.goto(url, timeout=120000, wait_until="domcontentloaded")
                    except PlaywrightTimeoutError:
                        logger.warning(f"Timeout loading {url}, continuing.")
                    time.sleep(5)
                    capturer.capture(app, f"{step_num:02d}_{name}")
                    step_num += 1
                    if any(k in name.lower() for k in ["signup", "register", "get started", "create account"]):
                        self.navigate_to_auth_page(capturer, app, step_num, intent="signup")
                        step_num += 1
                    elif any(k in name.lower() for k in ["login", "log in", "sign in"]):
                        self.navigate_to_auth_page(capturer, app, step_num, intent="login")
                        step_num += 1

                elif action == "WAIT":
                    delay = step.get("seconds", 2)
                    logger.info(f"Waiting {delay} seconds...")
                    time.sleep(delay)

                elif action == "CAPTURE":
                    logger.info(f"Capturing step: {name}")
                    capturer.capture(app, f"{step_num:02d}_{name}")
                    step_num += 1

            except Exception as e:
                logger.error(f"Error in step {step_num}: {e}")

        capturer.save_metadata(app, workflow)
        logger.info(f"Workflow completed for {app}: {workflow}")

    def navigate_to_auth_page(self, capturer, app, step_num, intent="signup"):
        """Dynamic detection of signup/login modals and navigation."""
        logger.info(f"Attempting to detect {intent} page for {app}...")

        keywords = ["sign up", "get started", "create account", "register"] if intent == "signup" else ["log in", "sign in"]
        selectors = [f"text={k}" for k in keywords]

        for sel in selectors:
            try:
                el = self.page.wait_for_selector(sel, timeout=8000, state="visible")
                if el:
                    logger.info(f"Found {intent} element: {sel}")
                    el.click()
                    time.sleep(6)
                    capturer.capture(app, f"{step_num:02d}_{intent}_page")
                    return
            except Exception:
                continue

        try:
            links = self.page.query_selector_all("a")
            for link in links:
                href = link.get_attribute("href") or ""
                if href and re.search(r"sign.?up|login|register", href, re.IGNORECASE):
                    full_url = href if href.startswith("http") else f"https://{app.lower()}.app{href}"
                    logger.info(f"Navigating to {intent} link: {full_url}")
                    self.page.goto(full_url, timeout=90000, wait_until="domcontentloaded")
                    time.sleep(5)
                    capturer.capture(app, f"{step_num:02d}_{intent}_page")
                    return
        except Exception as e:
            logger.warning(f"No clickable {intent} links found: {e}")
        logger.warning(f"Could not locate a {intent} element for {app}. Capturing current page as fallback.")
        capturer.capture(app, f"{step_num:02d}_{intent}_fallback")