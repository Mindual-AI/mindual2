import os
from PIL import Image

class PageImageAgent:
    def __init__(self, root_image_dir: str):
        """
        root_image_dir 예: 'project/db/pdf_pages'
        """
        self.root = root_image_dir

    def get_page_image(self, manual_name: str, page_num: int):
        """
        해당 매뉴얼의 특정 페이지 이미지 파일을 불러옴.
        있으면 이미지 반환하고, 없으면 None 반환.
        """
        manual_dir = os.path.join(self.root, manual_name)
        image_path = os.path.join(manual_dir, f"page_{page_num}.png")

        if os.path.exists(image_path):
            try:
                img = Image.open(image_path).convert("RGB")
                return {
                    "manual": manual_name,
                    "page": page_num,
                    "has_image": True,
                    "image": img
                }
            except Exception as e:
                print("[ERROR] 이미지 로딩 실패:", e)

        return {
            "manual": manual_name,
            "page": page_num,
            "has_image": False,
            "image": None
        }
