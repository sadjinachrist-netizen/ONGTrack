from PyPDF2 import PdfReader
from pathlib import Path

paths = [
    Path('cahier_de_charges_projetMIDA.pdf'),
    Path('cahier_d\\analyse_projetMIDA.pdf')
]

for path in paths:
    print('\n===', path, '===')
    reader = PdfReader(path)
    print('pages', len(reader.pages))
    for i, page in enumerate(reader.pages[:5]):
        t = page.extract_text() or ''
        print(f'--- page {i+1} ---')
        print(t[:1200])
    print('--- preview end ---')
