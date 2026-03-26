from django.template.loader import render_to_string
import os

def generate_pdf_from_html(html_string):
    """
    MOCK: Returns dummy PDF bytes for local testing.
    """
    return b"%PDF-1.4 mock data"

def generate_pdf_from_template(template_name, context):
    """
    MOCK: Returns dummy PDF bytes for local testing.
    """
    return b"%PDF-1.4 mock data from template"
