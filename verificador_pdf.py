import os
import shutil
import pytesseract
from pdf2image import convert_from_path
import re
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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
    "35.689.008/0001-91": "FÁBRICA",
    "35.689.008/0002-72": "INDUSTRIA - RJ",
    "35.689.008/0003-53": "GALPÃO",
    "31.339.275/0001-88": "FRANCHISING - Antiga",
    "05.505.945/0001-89": "FRANCHISING - Atual",
    "13.830.348/0001-58": "VILLA LOBOS",
    "13.830.348/0002-39": "ALPHAVILLE",
    "21.768.856/0001-81": "MORUMBI/QSQ",
    "21.768.856/0002-62": "MORUMBI TOWN",
    "33.707.451/0001-12": "TOP CENTER",
    "35.274.006/0001-31": "MORUMBI PARK (SP MARKET)",
    "35.274.006/0002-12": "MOOCA",
    "31.131.092/0001-72": "VILA OLIMPIA",
    "31.131.092/0002-53": "JK",
    "39.267.229/0001-22": "CENTER NORTE",
    "39.267.229/0002-03": "PLAZA SUL",
    "39.267.229/0003-94": "ELDORADO",
    "39.267.229/0004-75": "TAMBORÉ",
    "39.267.229/0005-56": "SOROCABA",
    "39.267.229/0006-37": "METRÓPOLE (CIDADE JARDIM)",
    "39.267.229/0007-18": "MOOCA(Center Norte)",
    "39.267.229/0008-07": "TABOÃO",
    "39.267.229/0009-80": "TRAILER/EVENTOS",
    "39.267.229/0010-13": "PAMPLONA",
    "39.267.229/0011-02": "VILLA LOBOS(Center Norte)",
    "39.267.229/0012-85": "ALPHAVILLE(Center Norte)",
    "39.267.229/0013-66": "MORUMBI/QSQ(Center Norte)",
    "39.267.229/0014-47": "MORUMBI TOWN(Center Norte)",
    "39.267.229/0015-28": "TOP CENTER (COLINAS)",
    "39.267.229/0016-09": "BOURBON (MORUMBI PARK)",
    "39.267.229/0017-90": "VILA OLIMPIA(Center Norte)",
    "39.267.229/0018-70": "AEROPORTO DE GUARULHOS (JK)",
    "39.267.229/0019-51": "TIETÊ PLAZA",
    "39.267.229/0020-95": "CATARINA FASHION OUTLET (PRAIA MAR)",
    "39.267.229/0021-76": "NORTE SHOPPING",
    "39.267.229/0022-57": "NITEROI",
    "39.267.229/0023-38": "LEBLON",
    "39.267.229/0024-19": "INTERNATIONAL GRU",
    "39.267.229/0025-08": "NOVA AMÉRICA",
    "39.267.229/0026-80": "TIJUCA (RIO SUL)",
    "39.267.229/0027-61": "JARDIM SUL",
    "39.267.229/0028-42": "RIO MAR",
    "39.267.229/0029-23": "BUTANTÃ",
    "39.267.229/0030-67": "ANÁLIA FRANCO",
    "39.267.229/0031-48": "SÃO BERNARDO DO CAMPO",
    "39.267.229/0032-29": "CASA CULTURA / HIGIENOPOLIS",
    "39.267.229/0033-00": "PENHA",
    "39.267.229/0034-90": "HCOR",
    "31.505.237/0001-58": "CAMPINAS",
    "31.505.237/0002-39": "CAMPINAS GALLERIA",
    "31.505.237/0003-10": "CAMPINAS PATIO PTA",
    "46.738.045/0001-69": "CAMBUI",
    "46.204.143/0001-16": "DOM PEDRO",
    "46.204.143/0002-05": "CAMPINAS(FILIAL)",
    "46.204.143/0003-88": "CAMPINAS GALLERIA(FILIAL)",
    "46.204.143/0004-69": "CAMPINAS PATIO PTA(FILIAL)",
    "46.204.143/0005-40": "CAMBUI(FILIAL)"
}

# Função que converte a imagem em texto e extrai as informações e coloca na variável texto_extraido
def orc_pdf(pdf_path):
    try:
        imagens = convert_from_path(pdf_path, poppler_path=poppler_path)

        texto_extraido = ""

        for i, imagem in enumerate(imagens):
            texto = pytesseract.image_to_string(imagem)
            texto_extraido += texto

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
    sem_espaco = re.sub(r'\s+', '', texto) # Correção de Bug dos Espaços no CNPJ
    cnpjs = re.findall(r'CPF/CNPJ:\s*([\d/.-]+)', sem_espaco)
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

    if not os.path.exists(pasta_organizada):
        print(f"A pasta de destino não existe: {pasta_organizada}")
        return

    try:
        shutil.move(pdf_path, novo_caminho)
    except Exception as e:
        print(f"Erro ao mover o arquivo {pdf_path} para {novo_caminho}: {e}")

# Função para processar os arquivos PDFs e atualizar a barra de progresso
def processar_pdfs(progress):
    arquivos = os.listdir(pasta_desorganizada)
    arquivos_pdf = [arquivo for arquivo in arquivos if arquivo.lower().endswith('.pdf')]

    if not arquivos_pdf:
        messagebox.showinfo("Processamento Concluído!","Não há arquivos .pdf na pasta Desorganizada.")
        root.quit()
        return
    
    total_files = len(arquivos_pdf)
    progress["maximum"] = 100  # Define o valor máximo da barra de progresso

    # Processando os arquivos um por um
    for i, arquivo_pdf in enumerate(arquivos_pdf):
        pdf_path = os.path.join(pasta_desorganizada, arquivo_pdf)

        if os.path.exists(pdf_path):
            orc_pdf(pdf_path)
        
        # Atualiza a barra de progresso a cada arquivo processado
        progress["value"] = (i + 1) * 100 / total_files
        progress.update()

    # Exibe uma mensagem quando o processamento estiver completo
    messagebox.showinfo("Processamento concluído", "Todos os PDFs foram processados.")
    root.quit()

# Função para iniciar o processamento
def iniciar_processamento():
    processar_pdfs(progress)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Verificador de PDFs")
root.geometry("400x200")  # Tamanho da janela

title2 = Label(root, text="VERIFICANDO OS PDFS")
title2.grid(column=0, row=0)
title2.pack(pady=(40,5))

# Criando a barra de progresso
progress = ttk.Progressbar(root, length=300, mode="determinate")
progress.pack(pady=(0,20))

# Botão para iniciar o processamento
btn_iniciar = tk.Button(root, text="Iniciar Processamento", command=iniciar_processamento)
btn_iniciar.pack(pady=(10, 20))

# Rodando a interface gráfica
root.mainloop()
