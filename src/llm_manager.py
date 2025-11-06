import os, sys, json, re, contextlib
from llama_cpp import Llama
from loguru import logger

# Silence model spam
os.environ.update({
    "LLAMA_LOG_LEVEL": "ERROR",
    "LLAMA_DISABLE_LOGS": "1",
})

@contextlib.contextmanager
def suppress_stdout_stderr():
    with open(os.devnull, "w") as devnull:
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = devnull, devnull
        try:
            yield
        finally:
            sys.stdout, sys.stderr = old_out, old_err


class LLMManager:
    def __init__(self, model_path: str = "models/llama-2-7b-chat.Q4_K_M.gguf"):
        logger.info("Loading Llama 2 model...")
        with suppress_stdout_stderr():
            self.llm = Llama(model_path=model_path, n_ctx=2048, n_threads=6)
        logger.info("Llama model loaded successfully.")

    def generate_workflow_plan(self, query: str):
        """Ask LLM for intent and map it to the correct web page for Linear or Notion."""
        base_urls = {
            "notion": "https://www.notion.so",
            "linear": "https://linear.app"
        }

        prompt = f"""
You are an intelligent navigation planner for web automation.

Supported apps:
- Notion → https://www.notion.so
- Linear → https://linear.app

Given the user request, identify:
1. Which app the user refers to.
2. The *intent* (like pricing, login, features, templates, dashboard).
3. Return valid JSON ONLY, strictly in this format:

{{
  "app": "<Linear or Notion>",
  "workflow": "<short readable description>",
  "steps": [
    {{"action": "OPEN", "url": "<constructed URL based on intent>"}},
    {{"action": "WAIT", "seconds": 3}},
    {{"action": "CAPTURE", "name": "<meaningful page name>"}}
  ]
}}

Examples:
- "Show me the pricing for Notion" → url = "https://www.notion.so/pricing"
- "Open Linear login page" → url = "https://linear.app/login"
- "View features of Linear" → url = "https://linear.app/features"

Request: "{query}"
"""

        output = self.llm(prompt, max_tokens=512)
        raw_text = output["choices"][0]["text"].strip()
        logger.debug(f"Raw LLM output: {raw_text}")

        plan = self._parse_json_safely(raw_text)
        if plan:
            logger.info(f"Parsed plan successfully for {plan.get('app')}")
            return plan

        logger.warning("Invalid JSON, applying keyword-based fallback.")
        return self._keyword_fallback(query, base_urls)

    def _parse_json_safely(self, text: str):
        try:
            match = re.search(r"\{.*\}", text, re.S)
            if match:
                return json.loads(match.group(0))
        except Exception as e:
            logger.debug(f"JSON parsing failed: {e}")
        return None

    def _keyword_fallback(self, query: str, base_urls: dict):
        """Simple fallback when model JSON fails — detects app + intent manually."""
        q = query.lower()
        app = "notion" if "notion" in q else "linear" if "linear" in q else "notion"
        base_url = base_urls[app]

        if "pricing" in q:
            url = f"{base_url}/pricing"
            page_name = "pricing_page"
        elif "login" in q:
            url = f"{base_url}/login"
            page_name = "login_page"
        elif "features" in q:
            url = f"{base_url}/features"
            page_name = "features_page"
        elif "templates" in q:
            url = f"{base_url}/templates"
            page_name = "templates_page"
        else:
            url = base_url
            page_name = "homepage"

        return {
            "app": app.capitalize(),
            "workflow": query[:50],
            "steps": [
                {"action": "OPEN", "url": url},
                {"action": "WAIT", "seconds": 3},
                {"action": "CAPTURE", "name": page_name},
            ],
        }
