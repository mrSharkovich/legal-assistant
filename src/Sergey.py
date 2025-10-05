import PyPDF2
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
import pdfplumber
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import os

# Убедитесь, что путь к Tesseract указан правильно
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Compukter\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def text_pages(pdf_path):
    """
    Извлекает текст из PDF файла и возвращает массив строк

    Args:
        pdf_path (str): Путь к PDF файлу

    Returns:
        list: Массив строк, где каждый элемент - строка из PDF
    """

    def text_extraction(element):
        line_text = element.get_text()
        line_formats = []
        for text_line in element:
            if isinstance(text_line, LTTextContainer):
                for character in text_line:
                    if isinstance(character, LTChar):
                        line_formats.append(character.fontname)
                        line_formats.append(character.size)
        format_per_line = list(set(line_formats))
        return (line_text, format_per_line)

    def extract_table(pdf_path, page_num, table_num):
        pdf = pdfplumber.open(pdf_path)
        table_page = pdf.pages[page_num]
        table = table_page.extract_tables()[table_num]
        return table

    def table_converter(table):
        table_string = ''
        for row_num in range(len(table)):
            row = table[row_num]
            cleaned_row = [
                item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for
                item
                in row]
            table_string += ('|' + '|'.join(cleaned_row) + '|' + '\n')
        table_string = table_string[:-1]
        return table_string

    def crop_image(element, pageObj):
        [image_left, image_top, image_right, image_bottom] = [element.x0, element.y0, element.x1, element.y1]
        pageObj.mediabox.lower_left = (image_left, image_bottom)
        pageObj.mediabox.upper_right = (image_right, image_top)
        cropped_pdf_writer = PyPDF2.PdfWriter()
        cropped_pdf_writer.add_page(pageObj)
        with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
            cropped_pdf_writer.write(cropped_pdf_file)

    def convert_to_images(input_file):
        images = convert_from_path(input_file)
        image = images[0]
        output_file = 'PDF_image.png'
        image.save(output_file, 'PNG')

    def image_to_text(image_path):
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text

    # Основная логика функции
    pages_array = []

    try:
        # Создаем объекты для работы с PDF
        pdfFileObj = open(pdf_path, 'rb')
        pdfReaded = PyPDF2.PdfReader(pdfFileObj)

        # Извлекаем страницы из PDF
        for pagenum, page in enumerate(extract_pages(pdf_path)):
            pageObj = pdfReaded.pages[pagenum]
            page_lines=[]
            page_text = []
            line_format = []
            text_from_images = []
            text_from_tables = []
            page_content = []
            table_num = 0
            first_element = True
            table_extraction_flag = False

            pdf = pdfplumber.open(pdf_path)
            page_tables = pdf.pages[pagenum]
            tables = page_tables.find_tables()

            # Находим все элементы
            page_elements = [(element.y1, element) for element in page._objs]
            page_elements.sort(key=lambda a: a[0], reverse=True)

            # Обрабатываем элементы страницы
            for i, component in enumerate(page_elements):
                pos = component[0]
                element = component[1]

                # Обработка текстовых элементов
                if isinstance(element, LTTextContainer):
                    if table_extraction_flag == False:
                        (line_text, format_per_line) = text_extraction(element)
                        page_text.append(line_text)
                        line_format.append(format_per_line)
                        page_content.append(line_text)

                        # Добавляем строки текста в общий массив
                        lines = line_text.strip().split('\n')
                        for line in lines:
                            if line.strip():  # Добавляем только непустые строки
                                page_lines.append(line.strip())
                    else:
                        pass

                # Обработка изображений
                if isinstance(element, LTFigure):
                    crop_image(element, pageObj)
                    convert_to_images('cropped_image.pdf')
                    image_text = image_to_text('PDF_image.png')
                    text_from_images.append(image_text)
                    page_content.append(image_text)
                    page_text.append('image')
                    line_format.append('image')

                    # Добавляем текст из изображения
                    lines = image_text.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            page_lines.append(line.strip())

                # Обработка таблиц
                if isinstance(element, LTRect):
                    if first_element == True and (table_num + 1) <= len(tables):
                        lower_side = page.bbox[3] - tables[table_num].bbox[3]
                        upper_side = element.y1
                        table = extract_table(pdf_path, pagenum, table_num)
                        table_string = table_converter(table)
                        text_from_tables.append(table_string)
                        page_content.append(table_string)
                        table_extraction_flag = True
                        first_element = False
                        page_text.append('table')
                        line_format.append('table')

                        # Добавляем данные таблицы
                        lines = table_string.strip().split('\n')
                        for line in lines:
                            if line.strip():
                                page_lines.append(line.strip())

                    if element.y0 >= lower_side and element.y1 <= upper_side:
                        pass
                    elif not isinstance(page_elements[i + 1][1], LTRect):
                        table_extraction_flag = False
                        first_element = True
                        table_num += 1
            pages_array.append(page_lines)
        # Закрываем файл
        pdfFileObj.close()

        # Удаляем временные файлы, если они были созданы
        if os.path.exists('cropped_image.pdf'):
            os.remove('cropped_image.pdf')
        if os.path.exists('PDF_image.png'):
            os.remove('PDF_image.png')

    except Exception as e:
        print(f"Ошибка при обработке PDF: {e}")

    return pages_array

# Пример использования функции:
pdf_path = 'C:/Users/Compukter/Desktop/Образец.pdf'
pag_array = text_pages(pdf_path)
for page_num, page_lines in enumerate(pag_array):
    print(f"=== Страница {page_num+1} ===")
    for line in page_lines:
        print(line)
    print()
# print(pag_array)
