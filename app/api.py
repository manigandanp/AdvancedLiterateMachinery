from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from enum import Enum
import asyncio
import logging
import sys
import os
from .utils import secure_save, remove_file, file_streamer, image2pdf
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = os.path.dirname(__file__)
# sys.path.append(BASE_DIR + '/../DocumentUnderstanding/DocXLayout')
sys.path.append(os.path.abspath(BASE_DIR + '/../Applications/DocXChain'))

print(":" * 30)
print(sys.path)
print(":" * 30)

from .document_structurization import document_structurization
from modules.file_loading import load_document

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)
app = FastAPI(docs_url="/swagger")

executor = ThreadPoolExecutor() # Reverting back to thread pool

async def async_layout_parse(image):
    loop = asyncio.get_event_loop()
    result, output_image = await loop.run_in_executor(executor, document_structurization, image)
    return result, output_image


@app.get("/health")
async def health():
    return "OK"


@app.post("/parse_layout/")
async def extract_api(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    filepath = secure_save(file)
    logger.info(
        "[parse_layout] filename: %s",
        file.filename
    )   
    image = load_document(filepath)
    result, _  = await async_layout_parse(image)
    background_tasks.add_task(remove_file, filepath)
    return JSONResponse(result)

@app.post("/parse_layout/debug", responses={200: {"content": {"application/pdf": {}}}})
async def extract_debug_api(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    filepath = secure_save(file)
    logger.info(
        "[parse_layout/debug] filename: %s",
        file.filename
    )
    
    image = load_document(filepath)
    _, output_image  = await async_layout_parse(image)
    background_tasks.add_task(remove_file, filepath)
    debug_pdf_path = image2pdf(output_image)
    headers = {
        "Content-Disposition": f"attachment; filename={debug_pdf_path}",
        'media_type': "application/pdf"
    }
    return StreamingResponse(file_streamer(debug_pdf_path), headers=headers)
    