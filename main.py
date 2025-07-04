import config
from sinan import browser_manager, data_handler, form_filler
from tkinter import Tk, filedialog
import logging

# Configuração do logging para salvar os resultados em um arquivo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automacao_sinan.log", mode='w'),
        logging.StreamHandler()
    ]
)

def selecionar_arquivo():
    """Abre uma janela para o usuário selecionar o arquivo Excel."""
    Tk().withdraw()  # Esconde a janela principal do Tkinter
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo Excel com os dados",
        filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
    )
    if not arquivo:
        logging.warning("Nenhum arquivo selecionado. Encerrando o programa.")
        return None
    return arquivo

def main():
    """Função principal que orquestra a automação."""
    logging.info("Iniciando a automação de preenchimento do SINAN.")

    # 1. Selecionar o arquivo de dados
    caminho_arquivo = selecionar_arquivo()
    if not caminho_arquivo:
        return

    # 2. Iniciar o navegador e realizar o login
    try:
        navegador = browser_manager.iniciar_e_logar(
            url=config.URL_SINAN_LOGIN,
            usuario=config.SINAN_USER,
            senha=config.SINAN_PASSWORD
        )
    except Exception as e:
        logging.error(f"Falha crítica ao iniciar o navegador ou fazer login: {e}")
        return

    # 3. Carregar e preparar os dados da planilha
    try:
        df_notificacoes = data_handler.carregar_e_preparar_dados(caminho_arquivo)
        logging.info(f"{len(df_notificacoes)} notificações carregadas para processamento.")
    except Exception as e:
        logging.error(f"Erro ao ler ou processar o arquivo Excel: {e}")
        navegador.quit()
        return

    # 4. Iterar sobre cada notificação e preencher o formulário
    for index, linha in df_notificacoes.iterrows():
        num_sinan = linha.get('Sinan', 'N/A')
        logging.info(f"--- Iniciando processamento da notificação SINAN: {num_sinan} ---")
        try:
            form_filler.preencher_notificacao_completa(navegador, linha)
            logging.info(f">>> Notificação {num_sinan} processada com SUCESSO. <<<")
        except Exception as e:
            logging.error(f"XXX Falha ao processar a notificação {num_sinan}. Erro: {e} XXX")
            # Opcional: decidir se deve parar ou continuar para a próxima
            # break # Descomente para parar no primeiro erro
    
    logging.info("--- Processamento de todas as notificações concluído. ---")
    input("Pressione Enter para fechar o navegador e encerrar o programa...")
    navegador.quit()

if __name__ == "__main__":
    main()
