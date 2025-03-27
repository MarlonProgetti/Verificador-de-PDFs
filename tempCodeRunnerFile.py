import os
import shutil
import pytesseract
from pdf2image import convert_from_path

#Caminho da pasta principal do projeto
pasta_principal = "C:/VerificadorDePDF"

#Caminho das Subpastas
pasta_desorganizada = os.path.join(pasta_principal, "Desorganizada")
pasta_organizada = os.path.join(pasta_principal, "Organizada")

#Cria uma pasta principal se ela não existir
if not os.path.exists(pasta_principal):
  os.makedirs(pasta_principal)

#Cria as subpastas se não existirem
if not os.path.exists(pasta_desorganizada):
  os.makedirs(pasta_desorganizada)

if not os.path.exists(pasta_organizada):
  os.makedirs(pasta_organizada)

# Mostrando o caminho onde se encontra o tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Mostrando o caminho onde se encontra o poppler
poppler_path = r"C:\poppler\Release-24.08.0-0\poppler-24.08.0\Library\bin"

# Função que converte a imagem em texto e extrai as informações e coloca na variavel texto_extraido
def orc_pdf(pdf_path):
  try:
    imagens = convert_from_path(pdf_path, poppler_path=poppler_path)

    texto_extraido = ""

    for i, imagem in enumerate(imagens):
      texto = pytesseract.image_to_string(imagem)
      texto_extraido += texto
      print(f"Texto extraído da página {i + 1}:")
      print(texto)
    return texto_extraido

  except Exception as e:
    print(f"Ocorreu um erro: {e}")

#Função que filtra arquivos .PDF
def processar_pdfs():
  arquivos = os.listdir(pasta_desorganizada)

  arquivos_pdf = [arquivo for arquivo in arquivos if arquivo.lower().endswith('.pdf')]

  if not arquivos_pdf:
     return "Não há arquivos PDF na pasta Desorganizada."
  
  # Processando os arquivos um por um.
  for arquivo_pdf in arquivos_pdf:
    pdf_path = os.path.join(pasta_desorganizada, arquivo_pdf)

    if os.path.exists(pdf_path):
      print(f"\nProcessando o arquivo: {pdf_path}")
      orc_pdf(pdf_path)
    else:
      print(f"O arquivo {pdf_path} não foi encontrado!")

processar_pdfs()
