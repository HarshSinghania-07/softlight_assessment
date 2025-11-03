"""
Handles browser initialization and teardown using Playwright.
"""

from playwright.sync_api import sync_playwright
from loguru import logger

class BrowserManager:
    """
    Responsible for launching and managing Playwright browser sessions.
    """
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
    
    def launch_browser(self):
        """
        Launch the Playwright browser and open a new page context.
        """
        
        logger.info("Launching Playwright browser...")
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        logger.info("Browser launcged successfully.")
        return self.page
    
    def close_browser(self):
        """
        Close the browser and cleanup.
        """
        
        if self.browser:
            logger.info("Closing browser...")
            self.browser.close()