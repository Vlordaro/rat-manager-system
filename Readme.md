# RAT Manager System

Sistema automatizado para gestão de RATs (Relatórios de Atendimento Técnico) com Google Sheets.

## Features
- Login e cadastro de usuários
- Geração PDF de RATs
- Integração Google Sheets
- Envio automático por email
- Gestão de funcionários por loja
- Interface Streamlit

## Requisitos
- Python 3.x
- Credenciais Google Cloud Platform
- Conta Gmail para SMTP
- Bibliotecas em `requirements.txt`

## Instalação
  git clone https://github.com/your-username/rat-manager-system.git
  cd rat-manager-system
  pip install -r requirements.txt

## Configuração
  1.Configure .env:
    GOOGLE_CREDS_PATH=
    SMTP_EMAIL=
    SMTP_PASSWORD=
    CC_EMAIL=
    USERS_SHEET=
    EMPLOYEES_SHEET=
    COSTS_SHEET=
    TEMPLATE_PATH=
    OUTPUT_PATH=
  2.Execute:
    streamlit run app.py
    
