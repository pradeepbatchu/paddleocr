from paddleocr import PaddleOCR,draw_ocr
from flask import Flask, abort, request
import os
from werkzeug.utils import secure_filename
ocr = PaddleOCR(use_angle_cls=True, lang='en')

UPLOAD_FOLDER = '/upload/'


def imagetotext():
    file = request.files['image']
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    image = os.path.join(UPLOAD_FOLDER, filename)
    print(image)
    result = ocr.ocr(image, cls=True)
    txts = [line[1][0] for line in result]
    text = {'results': txts}
    return text