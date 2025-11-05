"""
Detects UI or DOM state changes between actions.
"""
from loguru import logger

class StateDetector:
    """
    Monitors page state and determines when a new UI state appears.
    """
    
    def __init__(self, page):
        self.page = page
        
    def detect_state_change(self, previous_state=None):
        """
        Placeholder: Detect DOM or visual change after each action.
        """
        logger.debug("Checking for UI state change...")
        return True