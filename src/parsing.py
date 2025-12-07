import PyPDF2
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
import pdfplumber
from PIL import Image
from pdf2image import convert_from_path
import easyocr
import os
import re


def clean_cid_text(text):
    """
    Function to clean text from regular strings
    """
    if not text:
        return text
    text = re.sub(r'\(cid:\d+\)', '', text)
    text = re.sub(r'\x00', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def check_pdf_type(pdf_path):
    """
    Function to check pdf type with PyPDF2
    text pdf or scanned pdf
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        page = reader.pages[0]
        text = page.extract_text()
        if text and text.strip():
            return "text_pdf"
        else:
            return "scanned_pdf"


def extract_text_with_easyocr(pdf_path):
    """
    Function to extract text with easyocr
    """
    pages_array = []
    try:
        reader = easyocr.Reader(['ru', 'en'])
        images = convert_from_path(pdf_path, dpi=300)
        for i, image in enumerate(images):
            page_lines = []
            # Сохраняем временное изображение
            temp_image_path = f'temp_page_{i}.png'
            image.save(temp_image_path, 'PNG')
            # Распознаем текст с EasyOCR
            results = reader.readtext(temp_image_path)
            # Извлекаем текст из результатов
            text_parts = []
            for (bbox, text, confidence) in results:
                if confidence > 0.3:  # Фильтр по уверенности распознавания
                    text_parts.append(text)
            full_text = ' '.join(text_parts)
            full_text = clean_cid_text(full_text)
            if full_text.strip():
                # Разбиваем на строки и очищаем
                lines = full_text.split('\n')
                for line in lines:
                    cleaned_line = line.strip()
                    if cleaned_line:
                        page_lines.append(cleaned_line)
            if page_lines:
                combined_text = ' '.join(page_lines)
                pages_array.append([combined_text])
            else:
                pages_array.append([])
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
        return pages_array
    except Exception as e:
        for i in range(10):  # Очищаем возможные временные файлы
            temp_path = f'temp_page_{i}.png'
            if os.path.exists(temp_path):
                os.remove(temp_path)
        return []


def text_former(pdf_path):
    pages_array = []
    try:
        pdfFileObj = open(pdf_path, 'rb')
        pdfReaded = PyPDF2.PdfReader(pdf_path)
        for pagenum, page in enumerate(extract_pages(pdf_path)):
            pageObj = pdfReaded.pages[pagenum]
            page_lines = []
            table_num = 0
            first_element = True
            table_extraction_flag = False
            lower_side = 0
            upper_side = 0
            pdf = pdfplumber.open(pdf_path)
            page_tables = pdf.pages[pagenum]
            tables = page_tables.find_tables()
            page_elements = [(element.y1, element) for element in page._objs]
            page_elements.sort(key=lambda a: a[0], reverse=True)
            for i, component in enumerate(page_elements):
                element = component[1]
                if isinstance(element, LTTextContainer):
                    if table_extraction_flag == False:
                        line_text = element.get_text()
                        line_text = clean_cid_text(line_text)
                        lines = line_text.strip().split('\n')
                        for line in lines:
                            cleaned_line = clean_cid_text(line.strip())
                            if cleaned_line:
                                page_lines.append(cleaned_line)
                elif isinstance(element, LTFigure):
                    try:
                        # Используем EasyOCR для изображений
                        [image_left, image_top, image_right, image_bottom] = [element.x0, element.y0, element.x1, element.y1]
                        pageObj.mediabox.lower_left = (image_left, image_bottom)
                        pageObj.mediabox.upper_right = (image_right, image_top)
                        cropped_pdf_writer = PyPDF2.PdfWriter()
                        cropped_pdf_writer.add_page(pageObj)
                        with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
                            cropped_pdf_writer.write(cropped_pdf_file)
                        # Конвертируем в изображение и используем EasyOCR
                        images = convert_from_path('cropped_image.pdf')
                        if images:
                            image = images[0]
                            image.save('PDF_image.png', 'PNG')

                            reader = easyocr.Reader(['ru', 'en'])
                            results = reader.readtext('PDF_image.png')

                            image_text_parts = []
                            for (bbox, text, confidence) in results:
                                if confidence > 0.3:
                                    image_text_parts.append(text)

                            image_text = ' '.join(image_text_parts)
                            image_text = clean_cid_text(image_text)

                            lines = image_text.strip().split('\n')
                            for line in lines:
                                cleaned_line = clean_cid_text(line.strip())
                                if cleaned_line:
                                    page_lines.append(cleaned_line)
                    except:
                        pass
                elif isinstance(element, LTRect):
                    if first_element == True and (table_num + 1) <= len(tables):
                        lower_side = page.bbox[3] - tables[table_num].bbox[3]
                        upper_side = element.y1
                        table = page_tables.extract_tables()[table_num]
                        table_string = ''
                        for row in table:
                            cleaned_row = [
                                clean_cid_text(item.replace('\n',
                                                            ' ') if item is not None and '\n' in item else 'None' if item is None else item)
                                for item in row
                            ]
                            table_string += ('|' + '|'.join(cleaned_row) + '|' + '\n')
                        table_string = table_string[:-1]
                        lines = table_string.strip().split('\n')
                        for line in lines:
                            cleaned_line = clean_cid_text(line.strip())
                            if cleaned_line:
                                page_lines.append(cleaned_line)
                        table_extraction_flag = True
                        first_element = False
            if page_lines:
                combined_text = ' '.join(page_lines)
                pages_array.append([combined_text])
            else:
                pages_array.append([])
        pdfFileObj.close()
        pdf.close()
        temp_files = ['cropped_image.pdf', 'PDF_image.png']
        for temp_file in temp_files: # Очистка временных файлов
            if os.path.exists(temp_file):
                os.remove(temp_file)
    except:
        pass
    return pages_array


def simple_text_former(pdf_path):
    pages_array = []
    try:
        for page_layout in enumerate(extract_pages(pdf_path)):
            page_lines = []
            for element in page_layout[1]:
                if isinstance(element, LTTextContainer):
                    text = element.get_text().strip()
                    text = clean_cid_text(text)
                    if text:
                        lines = text.split('\n')
                        for line in lines:
                            cleaned_line = line.strip()
                            if cleaned_line:
                                page_lines.append(cleaned_line)
            if page_lines:
                combined_text = ' '.join(page_lines)
                pages_array.append([combined_text])
            else:
                pages_array.append([])
    except:
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    text = clean_cid_text(text)
                    if text:
                        pages_array.append([text.strip()])
                    else:
                        pages_array.append([])
        except:
            pages_array = []
    return pages_array

def text_extract(pdf_path):
    try:
        pdf_type = check_pdf_type(pdf_path)
        if pdf_type == "scanned_pdf":
            result = extract_text_with_easyocr(pdf_path)
            if result and any(len(page) > 0 for page in result):
                return result
        else:
            try:
                result = text_former(pdf_path)
                if result and any(len(page) > 0 for page in result):
                    return result
            except:
                pass
            result = simple_text_former(pdf_path)
            if result and any(len(page) > 0 for page in result):
                return result
        result = extract_text_with_easyocr(pdf_path)
        if result and any(len(page) > 0 for page in result):
            return result
        return ["Ошибка при обработке файла"] # Если дошли сюда - все методы не сработали
    except Exception as e: # Любая ошибка на верхнем уровне
        return ["Ошибка при обработке файла"]