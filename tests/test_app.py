import os
import io
import tempfile
import pytest
from app import app
from flask import Flask

PDF_SAMPLE_CONTENT = b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 100 700 Td (Hello, PDF!) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000117 00000 n \n0000000211 00000 n \ntrailer\n<< /Root 1 0 R /Size 5 >>\nstartxref\n276\n%%EOF'


def get_real_pdf_path():
    # Retorna o caminho do PDF real fornecido pelo usuário
    return os.path.join(os.path.dirname(__file__), 'teste.pdf')

def test_extract_text_success():
    tester = app.test_client()
    pdf_path = get_real_pdf_path()
    with open(pdf_path, 'rb') as f:
        data = {'file': (io.BytesIO(f.read()), 'teste.pdf')}
        response = tester.post('/extract-text', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert 'text' in response.json
    assert response.json['text'].strip() != ''

def test_extract_text_no_file():
    tester = app.test_client()
    response = tester.post('/extract-text', content_type='multipart/form-data', data={})
    assert response.status_code == 400
    assert 'error' in response.json

def test_extract_text_invalid_file_type():
    tester = app.test_client()
    data = {'file': (io.BytesIO(b'not a pdf'), 'sample.txt')}
    response = tester.post('/extract-text', content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert 'error' in response.json
