from PIL import Image as PILImage
import cv2
import numpy as np
import pytesseract

class MICRReader:
    def __init__(self, tessdata_dir):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.tessdata_dir_config = f'--tessdata-dir "{tessdata_dir}"'

    def read_micr_code(self, file_path):
        print(f"Loading image from: {file_path}")
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Image at {file_path} could not be loaded.")
        print(f"Image loaded successfully with shape: {image.shape}")

        cropped_image = self._crop_micr_area(image)
        micr_code = self._extract_micr_code(cropped_image)
        micr_code = self._replace_invalid_characters(micr_code)
        pil_image = PILImage.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        return micr_code, pil_image

    def _crop_micr_area(self, image):
        height, width, _ = image.shape
        mm_to_pixels = height / 76.0  # Assuming the check height is 76 mm
        micr_height = int(12.70 * mm_to_pixels)  # 12.70 mm to pixels
        micr_region = image[height - micr_height:height, 0:width]
        print(f"Cropped MICR area with shape: {micr_region.shape}")
        return micr_region

    def _extract_micr_code(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Gray image created for OCR")
        micr_code = pytesseract.image_to_string(gray_image, config=f'--psm 7 -c tessedit_char_whitelist=0123456789ABCD -l e13b {self.tessdata_dir_config}')
        print(f"Extracted MICR code: {micr_code.strip()}")
        return micr_code.strip()

    def _replace_invalid_characters(self, micr_code):
        return micr_code.replace('A', '0').replace('B', '0').replace('C', '0').replace('D', '0')
