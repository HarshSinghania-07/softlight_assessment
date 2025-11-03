"""
Loads workflow configuration from YAML files.
"""
from pathlib import Path
import yaml
from loguru import logger
class ConfigLoader:
    """
    Loads and parses workflow definitions from YAML
    """
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
    
    def load_config(self):
        """
        Reads YAML configuration and returns parsed data.
        """
        
        logger.info(f"Loading workflow configuration from {self.config_path}...")
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)
        logger.info("Configuration loaded successfully.")
        return config