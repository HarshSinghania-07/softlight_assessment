"""
Captures screenshots and metadata for each UI state.
"""
import os, json
from datetime import datetime
from loguru import logger

class StateCapturer:
    """
    Handles screenshot capture and metadata logging for each workflow step
    """
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        os.makedirs(dataset_path, exist_ok=True)
        self.metadata = []
        
    def capture(self, page, step_name: str, description: str):
        """
        Takes a screenshot and records metadata
        """
        page.wait_for_timeout(1500)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.dataset_path, f"{step_name}_{timestamp}.png")
        
        logger.info(f"Capturing screenshot for step : {step_name}")
        page.screenshot(path=file_path)
        entry = {
            "step": step_name,
            "description": description,
            "timestamp": timestamp,
            "file_path": file_path
        }
        self.metadata.append(entry)
        
    def save_metadata(self):
        """
        Save all metadata to JSON file
        """
        meta_file = os.path.join(self.dataset_path, "metadata.json")
        with open(meta_file, "w") as f:
            json.dump(self.metadata, f, indent=1)
        logger.info(f"Metadata saved at {meta_file}")