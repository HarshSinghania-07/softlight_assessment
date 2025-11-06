import os, time, json
from loguru import logger
from PIL import Image, ImageDraw, ImageFont

class StateCapturer:
    def __init__(self, page, workflow_folder):
        self.page = page
        self.workflow_folder = workflow_folder

    def capture(self, app: str, name: str):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        view_path = os.path.join(self.workflow_folder, f"{name}_view.png")
        full_path = os.path.join(self.workflow_folder, f"{name}_full.png")

        self.page.screenshot(path=view_path, full_page=False)
        self._overlay_url(view_path)
        logger.info(f"Captured viewport screenshot: {view_path}")

        self.page.screenshot(path=full_path, full_page=True)
        self._overlay_url(full_path)
        logger.info(f"Captured full-page screenshot: {full_path}")

    def _overlay_url(self, file_path: str):
        """Add a fake URL bar on top of each screenshot."""
        current_url = self.page.url
        img = Image.open(file_path)
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        draw.rectangle([(0, 0), (img.width, 40)], fill=(240, 240, 240))
        draw.text((10, 10), f"URL: {current_url}", fill=(0, 0, 0), font=font)
        img.save(file_path)

    def save_metadata(self, app: str, workflow: str):
        meta = {
            "app": app,
            "workflow": workflow,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "final_url": self.page.url,
        }
        meta_path = os.path.join(self.workflow_folder, "metadata.json")
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
        logger.info(f"Metadata saved at {meta_path}")
