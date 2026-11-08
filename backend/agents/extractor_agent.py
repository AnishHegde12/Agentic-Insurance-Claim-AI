import base64

from ..services.state import State
import pytesseract
from PIL import Image
import json
from langchain_core.document_loaders import TextLoader, PyPDFLoader
def extract_text_from_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text= file.read()
    return text.strip()

def extract_text_from_pdf(file_path):
    loader= PyPDFLoader(file_path)
    document= loader.load()
    text=" ".join([page.page_content for page in document])
    return text.strip()

def extract_text_from_image(file_path):
    image= Image.open(file_path)
    text= pytesseract.image_to_string(image)
    with open(file_path, "rb") as file:
        image_data= base64.b64encode(file.read()).decode("utf-8")
    
    return {"text": text.strip(), "image_base64": image_data}

def extract_text_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data= json.load(file)
    text= json.dumps(data)
    return text.strip()

def extract_text_from_file(state:State):
    text=''
    image=''
    file_paths=state['file_path_list']
    for file_path in file_paths:
        if file_path.endswith('.txt'):
            text+= extract_text_from_text_file(file_path)
        elif file_path.endswith('.pdf'):
            text+=extract_text_from_pdf(file_path)
        elif file_path.endswith('.png'):
            data=extract_text_from_image(file_path)
            text+=data['text']
            image+=data['image_base64']
        else:
            text+=extract_text_from_json(file_path)
    text=text.strip()
    return {'extracted_data':text, 'image_base64':image}