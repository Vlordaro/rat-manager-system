import streamlit as st
import gspread
import datetime
from google.oauth2.service_account import Credentials
from docx import Document 
from io import BytesIO
from docx2pdf import convert
import tempfile
import os
import time
import shutil
import pandas as pd
import re
import pythoncom
from docx.shared import Pt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

# Configuração das credenciais
creds_json = os.getenv('GOOGLE_CREDS_PATH')
scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(creds_json, scopes=scopes)
client = gspread.authorize(creds)

def get_greeting():
   hour = datetime.datetime.now().hour
   if 5 <= hour < 12:
       return "Bom dia"
   elif 12 <= hour < 18:
       return "Boa tarde"
   else:
       return "Boa noite"

def send_email(pdf_path, bkn):
   try:
       sender_email = os.getenv('SMTP_EMAIL')
       app_password = os.getenv('SMTP_PASSWORD')
       cc_email = os.getenv('CC_EMAIL')

       msg = MIMEMultipart()
       msg['From'] = sender_email
       msg['To'] = f"{bkn}@empresa.com.br"
       msg['Cc'] = cc_email
       msg['Subject'] = f"RAT - Manutenção {bkn}"

       greeting = get_greeting()
       body = f"""{greeting},\n\nEm anexo segue RAT de atendimento.\nFavor imprimir, assinar e entregar a RAT para o técnico."""
       msg.attach(MIMEText(body, 'plain'))

       if not os.path.exists(pdf_path):
           raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")
       
       with open(pdf_path, "rb") as f:
           pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
           pdf_attachment.add_header('Content-Disposition', 'attachment', filename="RAT.pdf")
           msg.attach(pdf_attachment)

       server = smtplib.SMTP("smtp.gmail.com", 587)
       server.set_debuglevel(1)
       server.starttls()
       server.login(sender_email, app_password)

       to_emails = msg['To'].split(', ') + [cc_email]
       server.sendmail(sender_email, to_emails, msg.as_string())
       server.quit()

       return True, "Email enviado com sucesso!"
   except Exception as e:
       print(f"Erro ao enviar email: {e}")
       return False, f"Erro ao enviar email: {str(e)}"

def criar_planilha(nome_planilha):
   try:
       spreadsheet = client.open(nome_planilha)
   except gspread.exceptions.SpreadsheetNotFound:
       spreadsheet = client.create(nome_planilha)
       spreadsheet.share(creds.service_account_email, perm_type='user', role='writer')
       sheet = spreadsheet.sheet1
       sheet.append_row(["Usuário", "Nome", "Email", "Data de Nascimento", "Senha"])
   return spreadsheet

def criar_planilha_funcionarios(nome_planilha="Funcionarios"):
   try:
       spreadsheet = client.open(nome_planilha)
   except gspread.exceptions.SpreadsheetNotFound:
       spreadsheet = client.create(nome_planilha)
       spreadsheet.share(creds.service_account_email, perm_type='user', role='writer')
       sheet = spreadsheet.sheet1
       sheet.append_row(["Codigo_Loja", "Nome_Funcionario", "Telefone"])
   return spreadsheet

try:
   planilha_usuarios = criar_planilha(os.getenv('USERS_SHEET'))
   planilha_funcionarios = criar_planilha_funcionarios()
except Exception as e:
   print(f"Erro ao criar/verificar planilhas: {e}")

def obter_funcionarios_loja(codigo_loja):
   try:
       planilha = client.open(os.getenv('EMPLOYEES_SHEET'))
       sheet = planilha.sheet1
       
       todos_dados = sheet.get_all_values()
       linhas_dados = todos_dados[1:] if len(todos_dados) > 0 else []
       
       funcionarios = []
       for linha in linhas_dados:
           if len(linha) >= 3 and linha[0] == codigo_loja:
               funcionarios.append({
                   "nome": linha[1],
                   "telefone": linha[2]
               })
       
       return funcionarios
       
   except Exception as e:
       print(f"Erro ao obter funcionários: {str(e)}")
       return []

def adicionar_funcionario(codigo_loja, nome, telefone):
   try:
       planilha = client.open(os.getenv('EMPLOYEES_SHEET'))
       sheet = planilha.sheet1
       
       dados_existentes = sheet.get_all_values()
       if not dados_existentes:
           sheet.append_row(["Codigo_Loja", "Nome_Funcionario", "Telefone"])
       
       nova_linha = [str(codigo_loja), str(nome), str(telefone)]
       sheet.append_row(nova_linha)
       return True
       
   except Exception as e:
       print(f"Erro ao adicionar funcionário: {str(e)}")
       st.error(f"Erro ao adicionar funcionário: {str(e)}")
       return False

[resto do código permanece igual, substituindo strings hardcoded por variáveis de ambiente]
