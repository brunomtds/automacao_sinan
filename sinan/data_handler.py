import pandas as pd
import re
import math
from datetime import date

def carregar_e_preparar_dados(caminho_arquivo: str) -> pd.DataFrame:
    """Lê o arquivo Excel e aplica as transformações iniciais nos dados."""
    df = pd.read_excel(caminho_arquivo)
    
    # Colunas de data a serem convertidas
    date_columns = ['Data da notificação', 'Início dos Sintomas', 'Data da Coleta do Exame', 'Data Nascimento']
    for col in date_columns:
        if col in df.columns:
            df[col] = df[col].apply(parse_date)

    # Aplica formatações e conversões em outras colunas
    df['Telefone'] = df['Telefone'].apply(formatar_telefone)
    df['Doenças pré-existentes'] = df['Doenças pré-existentes'].apply(converter_sim_nao)
    # Adicione outras conversões globais aqui se necessário

    return df

def parse_date(date_str):
    """Converte uma string para um objeto datetime, tratando valores nulos."""
    if pd.isna(date_str) or date_str in ['', '0', 0]:
        return None
    try:
        return pd.to_datetime(date_str)
    except (ValueError, TypeError):
        return None

def format_date(date_value):
    """Formata um objeto datetime para string 'dd/mm/YYYY', tratando nulos."""
    if pd.isnull(date_value):
        return ''
    try:
        return date_value.strftime('%d/%m/%Y')
    except AttributeError:
        return str(date_value)

def vazio_para_zero(var):
    """Converte valores vazios, nulos ou NaN para 0."""
    if isinstance(var, (float, int)) and math.isnan(var):
        return 0
    elif var is None or var == "" or pd.isna(var):
        return 0
    else:
        return var

def converter_sim_nao(valor):
    """Converte valores como 'sim', 's', 'TRUE' para '1 - Sim' e outros para '2 - Não'."""
    if pd.isna(valor):
        return "2 - Não"
    
    valor_str = str(valor).strip().lower()
    if valor_str in ['sim', 's', 'true', '1', '1.0']:
        return "1 - Sim"
    else:
        return "2 - Não"

def formatar_telefone(numero):
    """Formata um número de telefone para o padrão brasileiro, tratando variações."""
    if pd.isna(numero):
        return ""
        
    numero = re.sub(r'\D', '', str(numero))
    
    if len(numero) < 8:
        return ""
    if len(numero) > 11:
        numero = numero[:11]
    
    if len(numero) == 11:
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    elif len(numero) == 10:
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    elif len(numero) == 9:
        return f"(11) {numero[:5]}-{numero[5:]}"
    elif len(numero) == 8:
        return f"(11) {numero[:4]}-{numero[4:]}"
    else:
        return numero
