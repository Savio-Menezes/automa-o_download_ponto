
# Automação de Download de Relatórios - Tangerino

Este projeto automatiza o processo de download de relatórios de batida de ponto do sistema Tangerino, utilizando **Selenium** para automação de navegação no navegador **Microsoft Edge**. O script preenche automaticamente o formulário de consulta, gera o relatório e faz o download dos arquivos, movendo-os para o diretório desejado.

## Tecnologias Utilizadas
- **Python**: Linguagem de programação para o desenvolvimento do script.
- **Selenium**: Ferramenta para automação de navegadores.
- **Microsoft Edge WebDriver**: Controla o navegador Edge para automação das ações.
- **python-dotenv**: Gerenciamento de variáveis de ambiente para armazenamento seguro de credenciais.
- **Paramiko** (opcional): Para integração com o servidor SFTP da TOTVS Cloud, facilitando o upload automático dos arquivos baixados.
- **Shutil**: Biblioteca Python para manipulação de arquivos, como mover e renomear.

## Configuração do Ambiente

### 1. Clonando o Repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
2. Criar Ambiente Virtual
Recomenda-se o uso de um ambiente virtual para instalar as dependências do projeto:

bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
3. Instalar Dependências
Execute o comando abaixo para instalar as bibliotecas necessárias:

bash
pip install -r requirements.txt