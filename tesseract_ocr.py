import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pytesseract
from PIL import Image

custom_config = r"--oem 3 --psm 12 -c tessedit_char_whitelist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '"
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


PERFORM_THRESHOLDING = True


def threshold_ocr(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if PERFORM_THRESHOLDING:
        _, img = cv2.threshold(cv2.cvtColor(
            img, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_not(img)
        text = pytesseract.image_to_string(
            img, lang='eng', config=custom_config)
        # text = text.replace('\n', ',')
        return text

def raw_ocr(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='eng', config=custom_config)
    return text