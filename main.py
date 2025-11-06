import time
from loguru import logger
from src.browser_manager import BrowserManager
from src.workflow_executor import WorkflowExecutor
from src.llm_manager import LLMManager


def enrich_plan(plan):
    """Add fallback logic to make LLM output executable."""
    app = plan.get("app", "Unknown")
    workflow = plan.get("workflow", "").lower()
    steps = plan.get("steps", [])

    base_urls = {
        "Linear": "https://linear.app",
        "Notion": "https://www.notion.so"
    }

    app_url = base_urls.get(app, "https://www.google.com")

    enriched_steps = [{"action": "OPEN", "url": app_url, "name": "homepage"}]
    if not steps:
        if any(k in workflow for k in ["sign up", "signup", "create account", "get started", "register"]):
            enriched_steps.append({"action": "OPEN", "url": f"{app_url}/signup", "name": "signup"})
        elif "login" in workflow or "sign in" in workflow:
            enriched_steps.append({"action": "OPEN", "url": f"{app_url}/login", "name": "login"})
        elif "pricing" in workflow:
            enriched_steps.append({"action": "OPEN", "url": f"{app_url}/pricing", "name": "pricing"})
        elif "feature" in workflow:
            enriched_steps.append({"action": "OPEN", "url": f"{app_url}/features", "name": "features"})
        else:
            enriched_steps.append({"action": "CAPTURE", "name": "homepage_view"})
    else:
        enriched_steps.extend(steps)

    logger.info(f"Resolved workflow for {app}: {enriched_steps}")
    return {"app": app, "workflow": workflow, "steps": enriched_steps}


def main():
    logger.info("=== Starting UI State Capture System ===")
    user_query = input("Enter your query: ")

    llm = LLMManager()
    plan = llm.generate_workflow_plan(user_query)
    plan = enrich_plan(plan)
    logger.info(f"Generated Plan: {plan}")
    browser_mgr = BrowserManager()
    page = browser_mgr.launch_browser()
    executor = WorkflowExecutor(page)
    executor.run_dynamic_workflow(plan)
    browser_mgr.close_browser()
    logger.info("=== Workflow completed successfully ===")


if __name__ == "__main__":
    main()