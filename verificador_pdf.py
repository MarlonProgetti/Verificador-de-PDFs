import os
import shutil
import pytesseract
from pdf2image import convert_from_path
import re

# Caminho da pasta principal do projeto
pasta_principal = "C:/VerificadorDePDF"

# Caminho das Subpastas
pasta_desorganizada = os.path.join(pasta_principal, "Desorganizada")
pasta_organizada = r"C:\VerificadorDePDF\Organizada"  # Corrigido para usar string bruta

# Verifica se as pastas existem e cria, se necessário
if not os.path.exists(pasta_principal):
    os.makedirs(pasta_principal)
    print(f"Criei a pasta principal: {pasta_principal}")

if not os.path.exists(pasta_desorganizada):
    os.makedirs(pasta_desorganizada)
    print(f"Criei a pasta de Desorganizada: {pasta_desorganizada}")

if not os.path.exists(pasta_organizada):
    os.makedirs(pasta_organizada)
    print(f"Criei a pasta de Organizada: {pasta_organizada}")

# Mostrando o caminho onde se encontra o tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Mostrando o caminho onde se encontra o poppler
poppler_path = r"C:\poppler\Release-24.08.0-0\poppler-24.08.0\Library\bin"

# Função que converte a imagem em texto e extrai as informações e coloca na variável texto_extraido
def orc_pdf(pdf_path):
    try:
        imagens = convert_from_path(pdf_path, poppler_path=poppler_path)

        texto_extraido = ""

        for i, imagem in enumerate(imagens):
            texto = pytesseract.image_to_string(imagem)
            texto_extraido += texto
            print(f"Texto extraído da página {i + 1}:")
            print(texto)

        # Variáveis que vão armazenar as informações solicitadas
        nota_fiscal = buscar_nota_fiscal(texto_extraido)
        cnpj = buscar_cnpj(texto_extraido)
        valor_total = buscar_valor_total(texto_extraido)

        # Agora renomeia o arquivo usando as informações extraídas
        renomear_arquivo(pdf_path, nota_fiscal, cnpj, valor_total)

    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo {pdf_path}: {e}")

# Função para buscar a Nota fiscal depois de uma frase
def buscar_nota_fiscal(texto):
    match = re.search(r'PREFEITURA DO MUNICIPIO DE SAO PAULO\s*(\d{8})', texto)
    if match:
        return match.group(1)
    return "Nota Fiscal não encontrada"

# Função para buscar o CNPJ após localizar uma palavra
def buscar_cnpj(texto):
    cnpjs = re.findall(r'CPF/CNPJ:\s*([\d/.-]+)', texto)
    if len(cnpjs) >= 2:
        return cnpjs[1]  # Retorna o segundo CNPJ
    return "CNPJ não encontrado"

# Função para buscar o Valor após uma palavra
def buscar_valor_total(texto):
    match = re.search(r'VALOR TOTAL RECEBIDO =\s*R\$\s*([\d,\.]+)', texto)
    if match:
        return match.group(1)
    return "Valor não encontrado"

# Função que renomeia o arquivo PDF
def renomear_arquivo(pdf_path, numero_nota, cnpj, valor_total):
    # Remover caracteres inválidos no nome do arquivo
    novo_nome = f"NF_{numero_nota}_CNPJ_{cnpj}_VALOR_{valor_total}.pdf"
    caracteres_invalidos = r'\/:*?"<>|'
    for char in caracteres_invalidos:
        novo_nome = novo_nome.replace(char, '_')

    # Garante que o nome do novo arquivo não ultrapasse o limite de caracteres do sistema de arquivos
    if len(novo_nome) > 255:
        novo_nome = novo_nome[:255]  # Trunca o nome do arquivo se for muito longo

    novo_caminho = os.path.join(pasta_organizada, novo_nome)

    # Verifica se o caminho de destino está correto
    print(f"Renomeando para o caminho: {novo_caminho}")

    # Verifica se a pasta de destino existe
    if not os.path.exists(pasta_organizada):
        print(f"A pasta de destino não existe: {pasta_organizada}")
        return

    # Renomeando o arquivo
    try:
        shutil.move(pdf_path, novo_caminho)
        print(f"Arquivo renomeado e movido para: {novo_caminho}")
    except Exception as e:
        print(f"Erro ao mover o arquivo {pdf_path} para {novo_caminho}: {e}")

# Função que filtra arquivos .PDF
def processar_pdfs():
    arquivos = os.listdir(pasta_desorganizada)

    arquivos_pdf = [arquivo for arquivo in arquivos if arquivo.lower().endswith('.pdf')]

    if not arquivos_pdf:
        print("Não há arquivos PDF na pasta Desorganizada.")
        return
    
    # Processando os arquivos um por um.
    for arquivo_pdf in arquivos_pdf:
        pdf_path = os.path.join(pasta_desorganizada, arquivo_pdf)

        if os.path.exists(pdf_path):
            print(f"\nProcessando o arquivo: {pdf_path}")
            orc_pdf(pdf_path)
        else:
            print(f"O arquivo {pdf_path} não foi encontrado!")

# Inicia o processamento dos PDFs
processar_pdfs()
