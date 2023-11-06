import sys
import os

BASE_DIR = os.path.dirname(__file__)
# sys.path.append(BASE_DIR + '/../DocumentUnderstanding/DocXLayout')
sys.path.append(BASE_DIR + '/../Applications/DocXLayout')

import numpy as np
from pipelines.general_text_reading import GeneralTextReading
from pipelines.table_parsing import TableParsing
from pipelines.document_structurization import DocumentStructurization
from utilities.visualization import *



def document_structurization(image):

    # configure
    configs = dict()
    
    layout_analysis_configs = dict()
    layout_analysis_configs['from_modelscope_flag'] = False
    layout_analysis_configs['model_path'] = '/home/DocXLayout_231012.pth'  # note that: currently the layout analysis model is NOT from modelscope
    configs['layout_analysis_configs'] = layout_analysis_configs
    
    text_detection_configs = dict()
    text_detection_configs['from_modelscope_flag'] = False # set to true if you want OCR - Text detection
    text_detection_configs['model_path'] = 'damo/cv_resnet18_ocr-detection-line-level_damo'
    configs['text_detection_configs'] = text_detection_configs

    text_recognition_configs = dict()
    text_recognition_configs['from_modelscope_flag'] = False  # set to true if you want OCR - Text recog
    text_recognition_configs['model_path'] = 'damo/cv_convnextTiny_ocr-recognition-document_damo'  # alternatives: 'damo/cv_convnextTiny_ocr-recognition-scene_damo', 'damo/cv_convnextTiny_ocr-recognition-general_damo', 'damo/cv_convnextTiny_ocr-recognition-handwritten_damo' 
    configs['text_recognition_configs'] = text_recognition_configs

    # initialize
    document_structurizer = DocumentStructurization(configs)

    # run
    final_result = document_structurizer(image)

    if True:
        print (final_result)

    # visualize
    output_image = document_structurization_visualization(final_result, image)

    # release
    document_structurizer.release()

    return final_result, output_image
    
    # import cv2
    # op_image = cv2.imread("/Users/manigandan.p@avalara.com/myprojects/ocr-translation-playground/AdvancedLiterateMachinery/Applications/DocXChain/bang_2_op_2.jpg")
    
    # return {"some": "other"},  op_image