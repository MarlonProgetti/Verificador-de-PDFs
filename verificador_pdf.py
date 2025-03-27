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

# Dicionário com os CNPJ das lojas e o nome que pertence a ele.
cnpj_loja = {
    "35.689.008/0001-91": "BISCOITÊ FÁBRICA",
    "35.689.008/0002-72": "BISCOITÊ INDUSTRIA - RJ",
    "35.689.008/0003-53": "BISCOITÊ GALPÃO",
    "31.339.275/0001-88": "BISCOITÊ FRANCHISING - Antiga",
    "05.505.945/0001-89": "BISCOITÊ FRANCHISING - Atual",
    "13.830.348/0001-58": "BISCOITÊ VILLA LOBOS",
    "13.830.348/0002-39": "BISCOITÊ ALPHAVILLE",
    "21.768.856/0001-81": "BISCOITÊ MORUMBI/QSQ",
    "21.768.856/0002-62": "BISCOITÊ MORUMBI TOWN",
    "33.707.451/0001-12": "BISCOITÊ TOP CENTER",
    "35.274.006/0001-31": "BISCOITÊ MORUMBI PARK (SP MARKET)",
    "35.274.006/0002-12": "BISCOITÊ MOOCA",
    "31.131.092/0001-72": "BISCOITÊ VILA OLIMPIA",
    "31.131.092/0002-53": "BISCOITÊ JK",
    "39.267.229/0001-22": "BISCOITÊ CENTER NORTE",
    "39.267.229/0002-03": "BISCOITÊ PLAZA SUL",
    "39.267.229/0003-94": "BISCOITÊ ELDORADO",
    "39.267.229/0004-75": "BISCOITÊ TAMBORÉ",
    "39.267.229/0005-56": "BISCOITÊ SOROCABA",
    "39.267.229/0006-37": "BISCOITÊ METRÓPOLE (CIDADE JARDIM)",
    "39.267.229/0007-18": "BISCOITÊ MOOCA(Center Norte)",
    "39.267.229/0008-07": "BISCOITÊ TABOÃO",
    "39.267.229/0009-80": "BISCOITÊ TRAILER/EVENTOS",
    "39.267.229/0010-13": "BISCOITÊ PAMPLONA",
    "39.267.229/0011-02": "BISCOITÊ VILLA LOBOS(Center Norte)",
    "39.267.229/0012-85": "BISCOITÊ ALPHAVILLE(Center Norte)",
    "39.267.229/0013-66": "BISCOITÊ MORUMBI/QSQ(Center Norte)",
    "39.267.229/0014-47": "BISCOITÊ MORUMBI TOWN(Center Norte)",
    "39.267.229/0015-28": "BISCOITÊ TOP CENTER (COLINAS)",
    "39.267.229/0016-09": "BISCOITÊ BOURBON (MORUMBI PARK)",
    "39.267.229/0017-90": "BISCOITÊ VILA OLIMPIA(Center Norte)",
    "39.267.229/0018-70": "BISCOITÊ AEROPORTO DE GUARULHOS (JK)",
    "39.267.229/0019-51": "BISCOITÊ TIETÊ PLAZA",
    "39.267.229/0020-95": "BISCOITÊ CATARINA FASHION OUTLET (PRAIA MAR)",
    "39.267.229/0021-76": "BISCOITÊ NORTE SHOPPING",
    "39.267.229/0022-57": "BISCOITÊ NITEROI",
    "39.267.229/0023-38": "BISCOITÊ LEBLON",
    "39.267.229/0024-19": "BISCOITE INTERNATIONAL GRU",
    "39.267.229/0025-08": "BISCOITE NOVA AMÉRICA",
    "39.267.229/0026-80": "BISCOITE TIJUCA (RIO SUL)",
    "39.267.229/0027-61": "BISCOITÊ JARDIM SUL",
    "39.267.229/0028-42": "BISCOITÊ RIO MAR",
    "39.267.229/0029-23": "BISCOITÊ BUTANTÃ",
    "39.267.229/0030-67": "BISCOITÊ ANÁLIA FRANCO",
    "39.267.229/0031-48": "BISCOITÊ SÃO BERNARDO DO CAMPO",
    "39.267.229/0032-29": "BISCOITÊ CASA CULTURA / HIGIENOPOLIS",
    "39.267.229/0033-00": "BISCOITÊ PENHA",
    "39.267.229/0034-90": "BISCOITÊ HCOR",
    "31.505.237/0001-58": "BISCOITÊ CAMPINAS",
    "31.505.237/0002-39": "BISCOITÊ CAMPINAS GALLERIA",
    "31.505.237/0003-10": "BISCOITÊ CAMPINAS PATIO PTA",
    "46.738.045/0001-69": "BISCOITÊ CAMBUI",
    "46.204.143/0001-16": "BISCOITÊ DOM PEDRO",
    "46.204.143/0002-05": "BISCOITÊ CAMPINAS(FILIAL)",
    "46.204.143/0003-88": "BISCOITÊ CAMPINAS GALLERIA(FILIAL)",
    "46.204.143/0004-69": "BISCOITÊ CAMPINAS PATIO PTA(FILIAL)",
    "46.204.143/0005-40": "BISCOITÊ CAMBUI(FILIAL)"
}

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
    
    # Variavel que recebe a Conversão do CNPJ em nome da Loja.
    nome_loja = cnpj_loja.get(cnpj, "Loja desconhecida")

    # Remover caracteres inválidos no nome do arquivo
    novo_nome = f"NFs{numero_nota}_{nome_loja}_R${valor_total}.pdf"
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
