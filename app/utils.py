import os
import shutil
import uuid
from werkzeug.utils import secure_filename
from PIL import Image

def get_file_path(filename):
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{secure_filename(filename)}"
    directory = "/tmp/layout_parser"
    mkdirs(directory)
    return os.path.join(directory, filename)

# def save_file(file):
#     filepath = get_file_path(file.filename)
#     file.save(filepath)
#     return filepath

def remove_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        
def mkdirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def secure_save(file):
    filepath = get_file_path(file.filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return filepath
  
def file_streamer(file_path):
    with open(file_path, "rb") as f:
        yield from f
    remove_file(file_path)

def image2pdf(cv_image):
  pil_image = Image.fromarray(cv_image)
  pdf_path = get_file_path('debug.pdf')
  pil_image.save(pdf_path, "PDF", resolution=100.0)
  return pdf_path