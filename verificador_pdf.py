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
    "Espaço para colocar", "Os CNPJs"
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
