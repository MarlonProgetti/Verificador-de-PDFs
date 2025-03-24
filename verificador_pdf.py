import os

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

  
