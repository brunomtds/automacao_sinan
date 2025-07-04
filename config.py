import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# Obtém as credenciais e outras configurações do ambiente
SINAN_USER = os.getenv("SINAN_USER")
SINAN_PASSWORD = os.getenv("SINAN_PASSWORD")

# Validação para garantir que as credenciais foram definidas
if not SINAN_USER or not SINAN_PASSWORD:
    raise ValueError("As credenciais SINAN_USER e SINAN_PASSWORD devem ser definidas no arquivo .env")

# Constantes da aplicação
URL_SINAN_LOGIN = "https://sinan.saude.gov.br/sinan/login/login.jsf"
CHROME_DRIVER_MANAGER = True # Use True para instalar automaticamente, ou forneça o caminho do seu driver
