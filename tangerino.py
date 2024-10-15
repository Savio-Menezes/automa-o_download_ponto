import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import shutil
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configure as variáveis de ambiente
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
edge_driver_path = os.getenv("EDGE_DRIVER_PATH")
download_dir = os.getenv("DOWNLOAD_DIR")

# Verifique se as variáveis de ambiente foram carregadas corretamente
if not all([username, password, edge_driver_path, download_dir]):
    raise EnvironmentError("Por favor, verifique se todas as variáveis de ambiente estão definidas no arquivo .env")

# Configure as opções do Edge para definir o diretório de download automático
options = webdriver.EdgeOptions()
prefs = {"download.default_directory": download_dir, "download.prompt_for_download": False}
options.add_experimental_option("prefs", prefs)

# Inicialize o driver com o Service e as opções
service = EdgeService(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=options)

try:
    # Acesse o site de login
    driver.get("https://app.tangerino.com.br")
    time.sleep(5)

    # Aguarde até que o campo de usuário esteja presente e visível
    username_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "id4"))
    )
    
    # Preencha o campo de usuário
    username_input.send_keys(username)
    time.sleep(5)

    # Aguarde até que o campo de senha esteja presente e visível
    password_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "id8"))
    )

    # Preencha o campo de senha e pressione Enter
    password_input.send_keys(password, Keys.RETURN)
    time.sleep(5)

    # Aguarde até que a primeira modal apareça
    modal1 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="bgInterna"]/div[2]'))
    )

    # Aguarde 3 segundos antes de atualizar a página
    time.sleep(3)

    # Atualize a página
    driver.refresh()
    time.sleep(5)

    # Tente acessar o menu "Ponto"
    aplicacoes_menu = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='itensMenu']/nav[1]/ul/li[5]/div/a"))
    )
    aplicacoes_menu.click()

    # Aguarde o dropdown aparecer
    time.sleep(3)  # Dê algum tempo para o dropdown se expandir, ajuste se necessário

    # Aguarde até que o menu de "relatórios" esteja visível
    envio_relatorio_menu = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/aside/div/nav[1]/ul/li[5]/div/ul/li[3]/a'))
    )
    envio_relatorio_menu.click()
    time.sleep(5)

    # Tela de Exportar
    export_ponto_menu = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/aside/div/nav[1]/ul/li[5]/div/ul/li[3]/ul/li[1]/a'))
    )   
    export_ponto_menu.click()
    time.sleep(5)

    # Obter a data atual e a data 3 dias atrás
    today = datetime.today().strftime('%d/%m/%Y')
    three_days_ago = (datetime.today() - timedelta(days=3)).strftime('%d/%m/%Y')

    # Acessar o formulário onde o campo de data de entrada está localizado
    form = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/main/div/div/div[2]/span/form'))
    )
    
    # Localizar o fieldset dentro do form
    fieldset = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/main/div/div/div[2]/span/form/fieldset'))
    )

    # Localizar a div dentro do fieldset
    div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="idc1"]'))
    )

    # Agora, localizar e interagir com o campo de data de entrada dentro dessa div
    data_inicial_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div/div/div[2]/span/form/fieldset/div[14]/input'))  # Xpath do campo de data de entrada dentro da div
    )
    data_inicial_input.click()
    data_inicial_input.clear()  # Limpar o campo antes de preencher
    data_inicial_input.send_keys(three_days_ago)  # Inserir a data de 3 dias atrás

    time.sleep(3)

    divfinal = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="idc2"]'))
    )

    # Agora, localizar e interagir com o campo de data de saída dentro dessa div 
    data_final_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div/div/div[2]/span/form/fieldset/div[15]/input'))  # Xpath do campo de data de entrada dentro da div
    )
    data_final_input.click()
    data_final_input.clear()  # Limpar o campo antes de preencher
    data_final_input.send_keys(today)  # Inserir a data atual

    # Gerar relatório
    gerar_relatorio = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div/div/div[2]/span/form/fieldset/div[20]/input[1]"))
    )

    # Rolar a página até o botão estar visível
    driver.execute_script("arguments[0].scrollIntoView(true);", gerar_relatorio)
    time.sleep(1)  # Dar um pequeno tempo para o scroll ser realizado

    # Agora, tentar clicar no botão
    gerar_relatorio.click()

    # Monitorar o diretório de download para verificar se o arquivo foi baixado
    time.sleep(10)  # Aguarde um tempo para que o download inicie

    # Loop para verificar o download
    file_name = ""
    while not file_name:
        for file in os.listdir(download_dir):
            if file.endswith(".crdownload") or file.endswith(".tmp"):  # Arquivo em progresso
                continue
            else:
                file_name = file
                break
        time.sleep(2)  # Aguarde um tempo antes de verificar novamente

    # Renomear e substituir o arquivo baixado
    original_file = os.path.join(download_dir, file_name)
    new_file = os.path.join(download_dir, "Importacao_de_ponto.txt")  
    
    # Substituir o arquivo existente, se ele existir
    if os.path.exists(new_file):
        os.remove(new_file)  # Remover o arquivo antigo, se existir

    shutil.move(original_file, new_file)  # Mover o arquivo para o novo nome
    print(f"Relatório baixado e renomeado para {new_file}")

except Exception as e:
    print(f"Erro: {e}")
finally:
    driver.quit()
