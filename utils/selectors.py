# utils/selectors.py
from selenium.webdriver.common.by import By

# Módulo para centralizar todos os seletores de elementos da página.
# Usar IDs é sempre preferível a XPaths longos.
# NOTA: Os IDs aqui são exemplos baseados na estrutura comum de JSF.
# Verifique os IDs reais na página do SINAN com a ferramenta de desenvolvedor (F12).

# --- PÁGINA DE LOGIN E NAVEGAÇÃO ---
USER_INPUT = (By.ID, 'form:username') 
PASS_INPUT = (By.ID, 'form:password') 
LOGIN_BUTTON = (By.NAME, 'form:j_id21')
MENU_VIOLENCIA = (By.XPATH, '/html/body/div[2]/form/div/table/tbody/tr/td[2]/div/div[1]')
SUBMENU_NOTIFICACAO_INDIVIDUAL = (By.XPATH, '/html/body/div[2]/form/div/table/tbody/tr/td[2]/div/div[2]/div/div/div[1]')
CONTINUAR_BUTTON = (By.XPATH, '/html/body/div[3]/form/p/input[1]')

# --- FORMULÁRIO: NOTIFICAÇÃO ---
NUM_SINAN_INPUT = (By.ID, 'form:nuNotificacao')
AGRAVO_INPUT = (By.ID, 'form:richagravocomboboxField')
DATA_NOTIF_INPUT = (By.ID, 'form:dtNotificacaoInputDate')
CNES_INPUT = (By.ID, 'form:notificacao_unidadeSaude_coCnes')
CNES_NOME_LABEL = (By.ID, 'form:notificacao_unidadeSaude_estabelecimentocomboboxField')
DATA_SINTOMAS_INPUT = (By.ID, 'form:dtPrimeirosSintomasInputDate')

# --- FORMULÁRIO: PACIENTE ---
NOME_PACIENTE_INPUT = (By.ID, 'form:notificacao_nomePaciente')
DATA_NASC_INPUT = (By.ID, 'form:dtNascimentoInputDate')
IDADE_LABEL = (By.ID, 'form:notificacao_paciente_idade')
SEXO_SELECT = (By.ID, 'form:notificacao_paciente_sexo')
RACA_SELECT = (By.ID, 'form:notificacao_paciente_raca')
NOME_MAE_INPUT = (By.ID, 'form:notificacao_nome_mae')
UF_RESIDENCIA_SELECT = (By.ID, 'form:notificacao_paciente_endereco_municipio_uf_id')
MUNICIPIO_RESIDENCIA_INPUT = (By.ID, 'form:notificacao_paciente_endereco_municipio_id')
LOGRADOURO_INPUT = (By.ID, 'form:notificacao_paciente_endereco_noLogradouro')
NUMERO_INPUT = (By.ID, 'form:notificacao_paciente_endereco_numeroCasa')
CEP_INPUT = (By.ID, 'form:notificacao_paciente_endereco_cep')
TELEFONE_INPUT = (By.ID, 'form:notificacao_paciente_telefone')

# --- FORMULÁRIO: INVESTIGAÇÃO ---
DATA_INVESTIGACAO_INPUT = (By.ID, 'form:dtInvestigacaoInputDate')
CLASSIFICACAO_FINAL_SELECT = (By.ID, 'form:dengue_classificacao')
CRITERIO_CONFIRMACAO_SELECT = (By.ID, 'form:dengue_criterio')
EVOLUCAO_SELECT = (By.ID, 'form:dengue_evolucao')
DATA_ENCERRAMENTO_INPUT = (By.ID, 'form:dengue_dataEncerramentoInputDate')

# --- BOTÕES DE AÇÃO ---
SALVAR_BUTTON = (By.ID, 'form:btnSalvarInvestigacao')
VOLTAR_BUTTON = (By.NAME, 'form:j_id848')
CONFIRMAR_POPUP_BUTTON = (By.ID, 'form:btnNovaNotificacao')


# --- FORMULÁRIO: SINAIS CLÍNICOS (INVESTIGAÇÃO) ---
# Verifique os IDs/XPaths reais no SINAN
FEBRE_SELECT = (By.ID, 'form:chikungunya_sinaisFebre')
MIALGIA_SELECT = (By.ID, 'form:chikungunya_sinaisMialgia')
CEFALEIA_SELECT = (By.ID, 'form:chikungunya_sinaisCefaleia')
EXANTEMA_SELECT = (By.ID, 'form:chikungunya_sinaisExantema')
VOMITO_SELECT = (By.ID, 'form:chikungunya_sinaisVomito')
NAUSEA_SELECT = (By.ID, 'form:chikungunya_sinaisNausea')
DOR_COSTAS_SELECT = (By.ID, 'form:chikungunya_sinaisDorCostas')
CONJUNTIVITE_SELECT = (By.ID, 'form:chikungunya_sinaisConjuntivite')
ARTRITE_SELECT = (By.ID, 'form:chikungunya_sinaisArtrite')
ARTRALGIA_SELECT = (By.ID, 'form:chikungunya_sinaisArtralgia')
PETEQUIAS_SELECT = (By.ID, 'form:chikungunya_sinaisPetequias')
RETROORBITAL_SELECT = (By.ID, 'form:chikungunya_sinaisRetroorbital')
LACO_POSITIVA_SELECT = (By.ID, 'id="form:chikungunya_sinaisProvaLaco"')
LEUCOPENIA_SELECT = (By.ID, 'form:chikungunya_sinaisLeucopenia')

# --- FORMULÁRIO: DOENÇAS PRÉ-EXISTENTES (INVESTIGAÇÃO) ---
# Verifique os IDs/XPaths reais no SINAN
DIABETES_SELECT = (By.ID, 'form:chikungunya_doencasDiabete')
RENAL_CRONICA_SELECT = (By.ID, 'form:chikungunya_doencasRenal')
HEMATOLOGICAS_SELECT = (By.ID, 'form:chikungunya_doencasHematologicas')
HEPATOPATIAS_SELECT = (By.ID, 'form:chikungunya_doencasHepatopatias')
HIPERTENSAO_SELECT = (By.ID, 'form:chikungunya_doencasHipertensao')
ACIDA_PEPTICA_SELECT = (By.ID, 'form:chikungunya_doencasAcido')
AUTO_IMUNES_SELECT = (By.ID, 'form:chikungunya_doencasAutoimune')

# --- FORMULÁRIO: SINAIS DE ALARME (INVESTIGAÇÃO) ---
# Verifique os IDs/XPaths reais no SINAN
HIPOTENSAO_SELECT = (By.ID, 'form:dengue_sinais_alarme_hipotensao')
PLAQUETAS_SELECT = (By.ID, 'form:dengue_sinais_alarmequeda')
VOMITOS_PERSISTENTES_SELECT = (By.ID, 'form:dengue_sinais_alarme_vomitos')
DOR_ABDOMINAL_SELECT = (By.ID, 'form:dengue_sinais_alarme_dor')
LETARGIA_SELECT = (By.ID, 'form:dengue_sinais_alarme_letargia')
SANGRAMENTO_SELECT = (By.ID, 'form:dengue_sinais_alarme_sangramento')
HEMATOCRITO_SELECT = (By.ID, 'form:dengue_sinais_alarme_hematocrito')
HEPATOMEGALIA_SELECT = (By.ID, 'form:dengue_sinais_alarme_hepatomegalia')
ACUMULO_LIQUIDOS_SELECT = (By.ID, 'form:dengue_sinais_alarme_liquidos')
DATA_ALARME_INPUT = (By.ID, 'rich-calendar-input rich-calendar-input')