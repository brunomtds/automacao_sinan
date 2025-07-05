from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

# Importa as funções auxiliares e os seletores
from sinan import data_handler
from utils import selectors_sinan
from sinan import form_filler

def selecionar_opcao(wait: WebDriverWait, seletor: tuple, texto_visivel: str):
    """
    Função auxiliar para selecionar uma opção em um dropdown (Select).
    Replicada aqui para evitar dependência circular com form_filler,
    ou pode ser movida para um módulo 'common_ui_actions.py' se houver muitas.
    """
    try:
        select_element = Select(wait.until(EC.element_to_be_clickable(seletor)))
        select_element.select_by_visible_text(texto_visivel)
    except NoSuchElementException:
        logging.error(f"Opção '{texto_visivel}' não encontrada no seletor {seletor}")
        raise
    except TimeoutException:
        logging.error(f"Timeout: Não foi possível encontrar o seletor {seletor} no tempo estimado")
        raise

def preencher_sinais_clinicos(wait: WebDriverWait, linha: dict):
    """
    Preenche os campos de sinais clínicos comuns na tela de investigação.
    """
    # Mapeia os nomes das colunas da planilha para os valores esperados no SINAN
    sintomas_map = {
        selectors_sinan.FEBRE_SELECT: data_handler.converter_sim_nao(linha.get('Febre')),
        selectors_sinan.MIALGIA_SELECT: data_handler.converter_sim_nao(linha.get('Mialgia')),
        selectors_sinan.CEFALEIA_SELECT: data_handler.converter_sim_nao(linha.get('Cefaleia')),
        selectors_sinan.EXANTEMA_SELECT: data_handler.converter_sim_nao(linha.get('Exantema')),
        selectors_sinan.VOMITO_SELECT: data_handler.converter_sim_nao(linha.get('Vômito')),
        selectors_sinan.NAUSEA_SELECT: data_handler.converter_sim_nao(linha.get('Náusea')),
        selectors_sinan.DOR_COSTAS_SELECT: data_handler.converter_sim_nao(linha.get('Dor nas Costas')),
        selectors_sinan.CONJUNTIVITE_SELECT: data_handler.converter_sim_nao(linha.get('Conjuntivite')),
        selectors_sinan.ARTRITE_SELECT: data_handler.converter_sim_nao(linha.get('Artrite')),
        selectors_sinan.ARTRALGIA_SELECT: data_handler.converter_sim_nao(linha.get('Artralgia intensa')),
        selectors_sinan.PETEQUIAS_SELECT: data_handler.converter_sim_nao(linha.get('Petéquias')),
        selectors_sinan.RETROORBITAL_SELECT: data_handler.converter_sim_nao(linha.get('Dor retroorbital')),
        selectors_sinan.LACO_POSITIVA_SELECT: data_handler.converter_sim_nao(linha.get('Prova do laço positiva')),
        selectors_sinan.LEUCOPENIA_SELECT: data_handler.converter_sim_nao(linha.get('Leucopenia')),
    }

    for seletor, valor in sintomas_map.items():
        tentativas = 0
        max_tentativas = 2
        sucesso = False
        while tentativas < max_tentativas and not sucesso:

            try:
                selecionar_opcao(wait, seletor, valor)
                sucesso = True
            except Exception as e:
                tentativas += 1
        
        if not sucesso:
            selecionar_opcao(wait, seletor, '2 - Não')

    logging.info("Sinais clínicos comuns preenchidos.")

def preencher_doencas_pre_existentes(wait: WebDriverWait, linha: dict):
    """
    Preenche os campos de doenças pré-existentes, se aplicável.
    """
    
    doenc_preex = data_handler.converter_sim_nao(linha.get('Doenças pré-existentes'))

    if doenc_preex == '1 - Sim':
        doencas_map = {
            selectors_sinan.DIABETES_SELECT: data_handler.converter_sim_nao(linha.get('Diabetes')),
            selectors_sinan.RENAL_CRONICA_SELECT: data_handler.converter_sim_nao(linha.get('Doença renal crônica')),
            selectors_sinan.HEMATOLOGICAS_SELECT: data_handler.converter_sim_nao(linha.get('Doenças hematológicas')),
            selectors_sinan.HEPATOPATIAS_SELECT: data_handler.converter_sim_nao(linha.get('Hepatopatias')),
            selectors_sinan.HIPERTENSAO_SELECT: data_handler.converter_sim_nao(linha.get('Hipertensão arterial')),
            selectors_sinan.ACIDA_PEPTICA_SELECT: data_handler.converter_sim_nao(linha.get('Doença ácida-péptica')),
            selectors_sinan.AUTO_IMUNES_SELECT: data_handler.converter_sim_nao(linha.get('Doenças auto-imunes')),
        }
        for seletor, valor in doencas_map.items():
            try:
                selecionar_opcao(wait, seletor, valor)
            except Exception as e:
                logging.warning(f"Não foi possível preencher doença pré-existente para o seletor {seletor}. Erro: {e}")
    else:

        doencas_map_nao = [
            selectors_sinan.DIABETES_SELECT, selectors_sinan.RENAL_CRONICA_SELECT, selectors_sinan.HEMATOLOGICAS_SELECT,
            selectors_sinan.HEPATOPATIAS_SELECT, selectors_sinan.HIPERTENSAO_SELECT, selectors_sinan.ACIDA_PEPTICA_SELECT,
            selectors_sinan.AUTO_IMUNES_SELECT
        ]
        for seletor in doencas_map_nao:
            try:
                selecionar_opcao(wait, seletor, "2 - Não")
            except Exception as e:
                logging.warning(f"Não foi possível preencher 'Não' para doença pré-existente no seletor {seletor}. Erro: {e}")

def preencher_sinais_de_alarme(wait: WebDriverWait, linha: dict):
    """
    Preenche os campos de sinais de alarme, se a classificação indicar.
    """
    
    classif_sinais_alarme = data_handler.converter_sim_nao(linha.get('Sinais de Alerta'))
    resultado = linha.get('RESULTADO', '').capitalize()

    if classif_sinais_alarme == '1 - Sim' and resultado == 'Positivo':
        dt_alarme = data_handler.format_date(linha.get('Início dos Sintomas')) # Ou uma coluna específica para data de alarme

        sinais_alarme_map = {
            selectors_sinan.HIPOTENSAO_SELECT: data_handler.converter_sim_nao(linha.get('Hipotensão postural e/ou lipotimia')),
            selectors_sinan.PLAQUETAS_SELECT: data_handler.converter_sim_nao(linha.get('Queda abrupta das plaquetas')),
            selectors_sinan.VOMITOS_PERSISTENTES_SELECT: data_handler.converter_sim_nao(linha.get('Vômitos persistentes')),
            selectors_sinan.DOR_ABDOMINAL_SELECT: data_handler.converter_sim_nao(linha.get('Dor abdominal intensa')),
            selectors_sinan.LETARGIA_SELECT: data_handler.converter_sim_nao(linha.get('Letargia ou irritabilidade')),
            selectors_sinan.SANGRAMENTO_SELECT: data_handler.converter_sim_nao(linha.get('Sangramento de mucosa/outras hemorragias')),
            selectors_sinan.HEMATOCRITO_SELECT: data_handler.converter_sim_nao(linha.get('Aumento progressivo de hematócrito')),
            selectors_sinan.HEPATOMEGALIA_SELECT: data_handler.converter_sim_nao(linha.get('Hepatomegalia >= 2cm')),
            selectors_sinan.ACUMULO_LIQUIDOS_SELECT: data_handler.converter_sim_nao(linha.get('Acúmulo de líquidos')),
        }

        for seletor, valor in sinais_alarme_map.items():
            try:
                selecionar_opcao(wait, seletor, valor)
            except Exception as e:
                logging.warning(f"Não foi possível preencher sinal de alarme para o seletor {seletor}. Erro: {e}")
        
        # Preencher data de início dos sintomas de alarme
        form_filler.preencher_data(wait, selectors_sinan.DATA_ALARME_INPUT, dt_alarme)
    else:
        pass

