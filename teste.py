import pytesseract
from pdf2image import convert_from_path

poppler_path = r"C:\poppler\Release-24.08.0-0\poppler-24.08.0\Library\bin"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pdf = r"c:\VerificadorDePDF\Desorganizada\NFs01133303_Loja desconhecida_R$2.996,80.pdf"

paginas = convert_from_path(pdf, 300, poppler_path=poppler_path)

for i, pagina in enumerate(paginas):
  texto = pytesseract.image_to_string(pagina)
  print(f"Texto da página {i+1};\n{texto}\n")
  print("\n" + "-"*50 +"\n")