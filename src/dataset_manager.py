"""
dataset_manager.py
Manages dataset folder structure and organization.
"""
import os
from loguru import logger

class DatasetManager:
    """
    Creates and maintains dataset folders for screenshots and metadata.
    """
    def __init__(self, base_dir="datasets"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def create_app_folder(self, app_name: str):
        app_path = os.path.join(self.base_dir, app_name)
        os.makedirs(app_path, exist_ok=True)
        logger.debug(f"Created dataset folder for {app_name}")
        return app_path
