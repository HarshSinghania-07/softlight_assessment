from loguru import logger

class TaskInterpreter:
    """
    Converts natural-language task requests into executable workflow steps.
    """
    def __init__(self):
        self.app_keywords = {
            "linear": "Linear",
            "notion": "Notion"
        }

    def interpret(self, user_query: str):
        logger.info(f"Interpreting task: {user_query}")
        app_name = None
        for key, val in self.app_keywords.items():
            if key in user_query.lower():
                app_name = val
                break

        if not app_name:
            raise ValueError("Could not infer app from query.")
        if "create a project" in user_query.lower():
            steps = ["open_homepage", "click_login", "click_product", "capture_landing_page"]
            workflow_name = "dynamic_create_project"
        elif "filter" in user_query.lower():
            steps = ["open_homepage", "click_pricing", "capture_pricing_modal"]
            workflow_name = "dynamic_filter_database"
        else:
            steps = ["open_homepage", "capture_landing_page"]
            workflow_name = "generic_capture"

        workflow = {"name": workflow_name, "steps": steps}
        logger.info(f"Generated workflow dynamically: {workflow}")

        return app_name, workflow
