from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
from utils import selectors_sinan



def iniciar_e_logar(url: str, usuario: str, senha: str) -> webdriver.Chrome:
    """Configura o WebDriver, abre a URL, faz o login e navega até o formulário."""
    logging.info("Configurando o WebDriver do Chrome.")
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    # chrome_options.add_argument('--headless') # Descomente para rodar sem interface gráfica

    service = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=service, options=chrome_options)
    
    wait = WebDriverWait(navegador, 20) # Aumentar o tempo de espera para mais robustez

    logging.info(f"Acessando a URL: {url}")
    navegador.get(url)

    logging.info("Preenchendo credenciais e realizando login.")
    wait.until(EC.element_to_be_clickable(selectors_sinan.USER_INPUT)).send_keys(usuario)
    wait.until(EC.element_to_be_clickable(selectors_sinan.PASS_INPUT)).send_keys(senha)
    wait.until(EC.element_to_be_clickable(selectors_sinan.LOGIN_BUTTON)).click()

    logging.info("Navegando pelos menus até o formulário de notificação.")
    wait.until(EC.element_to_be_clickable(selectors_sinan.MENU_VIOLENCIA)).click()
    wait.until(EC.element_to_be_clickable(selectors_sinan.SUBMENU_NOTIFICACAO_INDIVIDUAL)).click()
    wait.until(EC.element_to_be_clickable(selectors_sinan.CONTINUAR_BUTTON)).click()
    
    logging.info("Login e navegação inicial concluídos com sucesso.")
    return navegador
