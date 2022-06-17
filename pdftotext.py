from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import json
import pandas as pd
import re
import logging
import io
import os
from flask import Flask, abort, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/upload/'


def extract_text_from_pdf():
  pdf_path = request.files['pdf_path']
  filename = secure_filename(pdf_path.filename)
  pdf_path.save(os.path.join(UPLOAD_FOLDER, filename))
  pdf_path = os.path.join(UPLOAD_FOLDER, filename)
  resource_manager = PDFResourceManager()
  fake_file_handle = io.StringIO()
  converter = TextConverter(resource_manager,fake_file_handle)
  page_interpreter = PDFPageInterpreter(resource_manager, converter)
  with open(pdf_path, 'rb') as fh:
    for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
      page_interpreter.process_page(page)
    text = fake_file_handle.getvalue()

  converter.close()
  fake_file_handle.close()
  if text:
    logging.info(text)
    return text
