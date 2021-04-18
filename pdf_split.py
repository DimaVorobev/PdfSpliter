from pdf2image import convert_from_path
import PIL
import PyPDF2
from PyPDF2 import PdfFileMerger
import os 
import argparse

PIL.Image.MAX_IMAGE_PIXELS=933120000

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='filename in currnt directory or global path to file')
parser.add_argument('n',  type=int, help='number of pages')
parser.add_argument('--out', type=str, help='output directory')
args = parser.parse_args()

filename = args.filename
n_pages = args.n

image = convert_from_path(filename)[0]
width, height = image.getbbox()[2:4]
page_height = height // n_pages
pages = []
merger = PdfFileMerger()

for i in range(n_pages):
    page = image.crop((0, i*page_height, width, (i+1)*page_height))
    page.save(f'page{i}.pdf', format = 'pdf')
    merger.append(open(f'page{i}.pdf', 'rb'))

out = args.out
if out == None:
    out = 'splitted.pdf'
with open(out, 'wb') as fout:
    merger.write(fout)

if os.name == 'posix':
    cmd_to_del = 'rm'
else:
    cmd_to_del = 'del'

for i in range(n_pages):
    os.system(f'{cmd_to_del} page{i}.pdf') 
