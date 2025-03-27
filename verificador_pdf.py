import os
import shutil
import pytesseract
from pdf2image import convert_from_path
import re

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

# Variaveis que vão amarzenar as informações solicitadas
    nota_fiscal = buscar_nota_fiscal(texto_extraido)
    cnpj = buscar_cnpj(texto_extraido)
    valor_total = buscar_valor_total(texto_extraido)

    return texto_extraido

  except Exception as e:
    print(f"Ocorreu um erro: {e}")

# Função para buscar a Nota fiscal Depois de uma frase.
def buscar_nota_fiscal(texto):
    match = re.search(r'PREFEITURA DO MUNICIPIO DE SAO PAULO\s*(\d{8})', texto)
    if match:
        return match.group(1)
    return "Nota Fiscal não encontrada."

#Função para buscar o CNPJ após localizar uma palavra.
def buscar_cnpj(texto):
  match = re.search(r'CPF/CNPJ:\s*([\d/.-]+)', texto)
  if match:
    return match.group(1)
  return "CNPJ não encontrado"

# Função para buscar o Valor após uma palavra.
def buscar_valor_total(texto):
  match = re.search(r'VALOR TOTAL RECEBIDO =\s*R\$\s*([\d,\.]+)', texto)
  if match:
    return match.group(1)
  return "Valor não encontrado"

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
