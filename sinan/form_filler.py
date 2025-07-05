from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from datetime import datetime, timedelta
import time

# Importa as funções de tratamento de dados e o módulo de seletores
from . import data_handler
from utils import selectors_sinan, symptoms

# --- FUNÇÕES AUXILIARES DE INTERAÇÃO ---

def preencher_campo(wait: WebDriverWait, seletor: tuple, valor: str, tab: bool = False):
    """Preenche um campo de texto de forma segura, limpando-o primeiro."""
    try:
        campo = wait.until(EC.element_to_be_clickable(seletor))
        campo.clear()
        campo.send_keys(valor)
        if tab:
            campo.send_keys(Keys.TAB)
    except TimeoutException:
        logging.error(f"Timeout: Não foi possível encontrar o elemento {seletor}")
        raise

def preencher_data(wait: WebDriverWait, seletor: tuple, valor: str, tab: bool = False):
    """Preenche um campo de data, que muitas vezes requer tratamento especial."""
    try:
        campo = wait.until(EC.element_to_be_clickable(seletor))
        campo.send_keys(Keys.HOME)  # Move o cursor para o início para evitar erros de máscara
        campo.send_keys(valor)
        if tab:
            campo.send_keys(Keys.TAB)
    except TimeoutException:
        logging.error(f"Timeout: Não foi possível encontrar o campo de data {seletor}")
        raise

def selecionar_opcao(wait: WebDriverWait, seletor: tuple, texto_visivel: str):
    """Seleciona uma opção de um menu dropdown (Select) pelo texto visível."""
    try:
        select_element = Select(wait.until(EC.element_to_be_clickable(seletor)))
        select_element.select_by_visible_text(texto_visivel)
    except NoSuchElementException:
        logging.error(f"Opção '{texto_visivel}' não encontrada no seletor {seletor}")
        raise
    except TimeoutException:
        logging.error(f"Timeout: Não foi possível encontrar o seletor {seletor}")
        raise

# --- FUNÇÕES DE PREENCHIMENTO DE SEÇÕES ---

def preencher_dados_iniciais(wait: WebDriverWait, linha: dict): #Funcionando ok
    """Preenche a primeira parte do formulário de notificação."""
    logging.info("Preenchendo dados da notificação inicial.")
    
    preencher_campo(wait, selectors_sinan.NUM_SINAN_INPUT, str(linha.get('Sinan', '')))
    num_sinan = str(linha.get('Sinan', ''))
    
    agravo_input = wait.until(EC.element_to_be_clickable(selectors_sinan.AGRAVO_INPUT))
    agravo_input.send_keys('A90 - DENGUE', Keys.ENTER)
    
    wait.until(EC.element_to_be_clickable(selectors_sinan.DATA_NOTIF_INPUT))
    time.sleep(2)
    

    dt_notif = data_handler.format_date(linha.get('Data da notificação'))
    preencher_data(wait, selectors_sinan.DATA_NOTIF_INPUT, dt_notif, tab=True)

    cnes = str(int(linha.get('CNES Notificadora', 0))).zfill(7)
    preencher_campo(wait, selectors_sinan.CNES_INPUT, cnes, tab=True)
    time.sleep(1)
    cnes_label = wait.until(EC.element_to_be_clickable(selectors_sinan.CNES_NOME_LABEL)).get_attribute("value")
    tentativas = 0
    while cnes_label == '' and tentativas < 3:
        preencher_campo(wait, selectors_sinan.CNES_INPUT, cnes, tab=True)
        time.sleep(2)
        cnes_label = wait.until(EC.element_to_be_clickable(selectors_sinan.CNES_NOME_LABEL)).get_attribute("value")
        tentativas += 1

    wait.until(lambda d: d.find_element(*selectors_sinan.CNES_NOME_LABEL).get_attribute("value").strip() != "")

    dt_sintomas = data_handler.format_date(linha.get('Início dos Sintomas'))
    preencher_data(wait, selectors_sinan.DATA_SINTOMAS_INPUT, dt_sintomas, tab=True)

def preencher_dados_paciente(wait: WebDriverWait, linha: dict):
    """Preenche a seção de dados do paciente e seu endereço."""
    logging.info("Preenchendo dados do paciente e endereço.")
    time.sleep(2)
    preencher_campo(wait, selectors_sinan.NOME_PACIENTE_INPUT, str(linha.get('Nome', '')))
    
    dt_nasc = data_handler.format_date(linha.get('Data Nascimento'))
    preencher_data(wait, selectors_sinan.DATA_NASC_INPUT, dt_nasc, tab=True)
    wait.until(lambda d: d.find_element(*selectors_sinan.IDADE_LABEL).get_attribute("value").strip() != "")

    selecionar_opcao(wait, selectors_sinan.SEXO_SELECT, str(linha.get('Sexo', '')).capitalize())
    selecionar_opcao(wait, selectors_sinan.RACA_SELECT, "9 - Ignorado")
    
    nome_mae = str(linha.get('Nome da Mãe', 'Não Informado'))
    if not nome_mae or nome_mae in ['0', 'nan']:
        nome_mae = 'Não Informado'
    preencher_campo(wait, selectors_sinan.NOME_MAE_INPUT, nome_mae)

    selecionar_opcao(wait, selectors_sinan.UF_RESIDENCIA_SELECT, "SP")
    time.sleep(2)
    wait.until(EC.element_to_be_clickable(selectors_sinan.MUNICIPIO_RESIDENCIA_INPUT)).send_keys('352590', Keys.TAB)
    time.sleep(1)
    preencher_campo(wait, selectors_sinan.LOGRADOURO_INPUT, str(linha.get('Endereço', '')))
    preencher_campo(wait, selectors_sinan.NUMERO_INPUT, str(int(linha.get('Número', 1))))
    preencher_campo(wait, selectors_sinan.CEP_INPUT, str(linha.get('CEP', '')))
    preencher_campo(wait, selectors_sinan.TELEFONE_INPUT, str(linha.get('Telefone', '')))

def salvar_e_avancar(wait: WebDriverWait, linha: dict):
    """Clica para salvar a notificação e confirma a operação para avançar."""
    logging.info("Salvando notificação inicial e avançando para investigação.")
    wait.until(EC.element_to_be_clickable(selectors_sinan.BTN_OK_NOTIF)).click()
    num_sinan = str(linha.get('Sinan', ''))

    try:
        confirm_button = wait.until(EC.element_to_be_clickable(selectors_sinan.BTN_CONF_NOTIF))
        confirm_button.click()
    except TimeoutException:
        logging.warning("Pop-up de confirmação não encontrado. Verificando alertas.")
        try:
            alert = wait.until(EC.alert_is_present())
            logging.warning(f"Alerta encontrado: {alert.text}")
            alert.accept()
        except TimeoutException:
            logging.error("Nenhum pop-up de confirmação ou alerta encontrado.")
            raise Exception("Fluxo de salvamento da notificação interrompido.")
        
    try:
        elemento_center = wait.until(EC.presence_of_element_located((selectors_sinan.POPUP_DUPLICIDADE)))
        texto_center = elemento_center.text

        if "Notificação Cadastrada com Sucesso!" in texto_center:
            confirm_button = wait.until(EC.element_to_be_clickable(selectors_sinan.BTN_CONF_NOTIF))
            confirm_button.click()
            time.sleep(2)
        else:
            wait.until(EC.element_to_be_clickable((selectors_sinan.BTN_CONF_DUPLICIDADE))).click()
            time.sleep(2.5)
            wait.until(EC.element_to_be_clickable((selectors_sinan.BTN_CONF_NOTIF))).click()
    

        print(f"Notificação {num_sinan} enviada")

    except Exception as e:
        print(f"Erro ao processar a notificação {num_sinan}: {str(e)}")

def preencher_investigacao(wait: WebDriverWait, linha: dict):
    """Preenche todos os campos da tela de investigação."""
    logging.info("Preenchendo dados da investigação.")
    
    dt_invest = data_handler.format_date(linha.get('Data da notificação'))
    preencher_data(wait, selectors_sinan.DATA_INVESTIGACAO_INPUT, dt_invest, tab=True)

    symptoms.preencher_sinais_clinicos(wait, linha)

    symptoms.preencher_doencas_pre_existentes(wait, linha)

    resultado = linha.get('RESULTADO', '')
    if resultado == 'Negativo':
        selecionar_opcao(wait, selectors_sinan.CLASSIFICACAO_FINAL_SELECT, '5 - Descartado')
    elif resultado == 'Positivo':
        if data_handler.converter_sim_nao(linha.get('Sinais de Alerta')) == '1 - Sim':
            selecionar_opcao(wait, selectors_sinan.CLASSIFICACAO_FINAL_SELECT, '11 - Dengue com sinais de alarme')
        else:
            selecionar_opcao(wait, selectors_sinan.CLASSIFICACAO_FINAL_SELECT, '10 - Dengue')
    
    criterio = linha.get('Critério', '')
    if criterio == 'Laboratório':
        selecionar_opcao(wait, selectors_sinan.CRITERIO_CONFIRMACAO_SELECT, '1 - Laboratório')
    elif criterio == 'Clínico-Epidemiológico':
        selecionar_opcao(wait, selectors_sinan.CRITERIO_CONFIRMACAO_SELECT, '2 - Clínico-Epidemiológico')

    if resultado != 'Aguardando Resultado':
        selecionar_opcao(wait, selectors_sinan.EVOLUCAO_SELECT, '1 - Cura')
        
        dt_notif_obj = linha.get('Data da notificação')
        if dt_notif_obj and (datetime.now().date() - dt_notif_obj.date()).days > 60:
            dt_encerramento = (dt_notif_obj + timedelta(days=59)).strftime('%d/%m/%Y')
        else:
            dt_encerramento = datetime.now().strftime('%d/%m/%Y')
        
        preencher_data(wait, selectors_sinan.DATA_ENCERRAMENTO_INPUT, dt_encerramento)

    symptoms.preencher_sinais_de_alarme(wait, linha)

def salvar_investigacao(wait: WebDriverWait):
    """Clica para salvar a investigação e confirma."""
    logging.info("Salvando investigação.")
    wait.until(EC.element_to_be_clickable(selectors_sinan.BTN_SALVAR_INVEST)).click()
    
    try:
        confirm_button = wait.until(EC.element_to_be_clickable(selectors_sinan.CONFIRMAR_POPUP_BUTTON))
        confirm_button.click()
    except TimeoutException:
        logging.error("Não foi possível confirmar o salvamento da investigação.")
        raise

# --- FUNÇÃO PRINCIPAL ORQUESTRADORA ---

def preencher_notificacao_completa(navegador: WebDriver, linha: dict):
    """Orquestra o preenchimento completo de uma notificação, da criação à investigação."""
    wait = WebDriverWait(navegador, 20)

    # Etapa 1: Preencher a primeira página (Notificação)
    preencher_dados_iniciais(wait, linha)
    preencher_dados_paciente(wait, linha)
    
    # Etapa 2: Salvar e ir para a segunda página (Investigação)
    salvar_e_avancar(wait)
    
    # Etapa 3: Preencher a segunda página
    preencher_investigacao(wait, linha)
    
    # Etapa 4: Salvar a investigação
    salvar_investigacao(wait)

    # Etapa 5: Voltar para a tela de seleção para a próxima notificação
    logging.info("Retornando à tela inicial para a próxima notificação.")
    wait.until(EC.element_to_be_clickable(selectors_sinan.VOLTAR_BUTTON)).click()
