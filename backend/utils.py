import json
import csv
import pandas as pd
import docx
from PyPDF2 import PdfReader
from pptx import Presentation
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import load_workbook

"""
In this file Factory Design Pattern is used to make this functionalities more flexible & maintainable.
Currently there are main file handlers for PDF, DOCX, TXT, PPTX, XLSX, CSV, HTML, XML, JSON. 
"""


def read_pdf(file):
    try:
        reader = PdfReader(file)
        return [page.extract_text() for page in reader.pages]
    except Exception as e:
        print(f"Error reading Pdf file: {e}")
        return


def read_docx(file):
    try:
        doc = docx.Document(file)
        return [para.text for para in doc.paragraphs]
    except Exception as e:
        print(f"Error reading Docx file: {e}")
        return


def read_txt(file):
    try:
        return file.read().splitlines()
    except Exception as e:
        print(f"Error reading Txt file: {e}")
        return


def read_pptx(file):
    try:
        pres = Presentation(file)
        return [slide.notes_slide.text for slide in pres.slides if slide.notes_slide]
    except Exception as e:
        print(f"Error reading pptx file: {e}")
        return


def read_xlsx(file):
    try:
        reader = pd.read_excel(file)
        return [" ".join(row) for row in reader]
    except Exception as e:
        print(f"Error reading Xlsx file: {e}")
        return


def read_csv(file):
    try:
        reader = csv.reader(file)
        return [" ".join(row) for row in reader]
    except Exception as e:
        print(f"Error reading Csv file: {e}")
        return


def read_html(file):
    try:
        soup = BeautifulSoup(file, "html.parser")
        return soup.get_text()
    except Exception as e:
        print(f"Error reading Html file: {e}")
        return


def read_xml(file):
    try:
        tree = etree.parse(file)
        return etree.tostring(tree.getroot(), pretty_print=True)
    except Exception as e:
        print(f"Error reading Xml file: {e}")
        return


def read_json(file):
    try:
        return json.load(file)
    except Exception as e:
        print(f"Error reading Json file: {e}")
        return
