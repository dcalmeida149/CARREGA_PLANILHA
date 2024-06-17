# Projeto de Upload de Planilhas com Flask
Este projeto permite que os usuários façam upload de arquivos Excel (XLSX, XLS) ou CSV, associando-os a uma data específica. Os dados são processados e inseridos em um banco de dados PostgreSQL. A aplicação é construída utilizando Flask, SQLAlchemy e pandas.

## Estrutura do Projeto
```markdown
my_flask_app/
│
├── app.py
├── models.py
├── secrets.json
├── README.md
└── templates/
    └── index.html
```
Pré-requisitos
Python 3.x
PostgreSQL

Instalação
1. Clonar o Repositório
```sh
git clone git@github.com:dcalmeida149/CARREGA_PLANILHA.git
cd my_flask_app
```
2. Criar e Ativar um Ambiente Virtual
```sh
python3 -m venv venv
source venv/bin/activate
```
3. Instalar as Dependências
```sh
pip install flask sqlalchemy pandas psycopg2-binary openpyxl
```
4. Configurar o Banco de Dados PostgreSQL
Crie um banco de dados no PostgreSQL e atualize DATABASE_URI no secrets.json com as credenciais do seu banco.

5. Arquivo secrets.json
Crie um arquivo secrets.json com o seguinte conteúdo:

```json
{
    "SECRET_KEY": "seu_secret_key_aqui",
    "DATABASE_URI": "postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco"
}
```
6. Estrutura do Banco de Dados
Certifique-se de que o banco de dados PostgreSQL possui as tabelas necessárias. O SQLAlchemy criará automaticamente as tabelas definidas no modelo.

### Execução
1. Iniciar a Aplicação
```sh
python app.py
```
2. Acessar a Aplicação
Abra um navegador e acesse http://localhost:5000.

### Utilização
Interface de Upload
Selecione uma data utilizando o datepicker.
Escolha um arquivo Excel (XLSX, XLS) ou CSV.
Clique em "Submit" para fazer o upload.

### Exemplos de Personalização
Alterar o Diretório de Templates
Se desejar alterar o diretório onde os templates estão armazenados, você pode atualizar a linha de inicialização do Flask em app.py:

```python
app = Flask(__name__, template_folder='templates')
```
Para:

```python
app = Flask(__name__, template_folder='novo_diretorio')
```
E mova seus templates para o novo diretório.

### Adicionar Novas Rotas
Para adicionar novas rotas à aplicação, utilize o decorator @app.route no arquivo app.py:

```python
@app.route('/nova_rota')
def nova_rota():
    return "Nova Rota"
```

### Personalizar o Frontend
Edite o arquivo index.html na pasta paginas para personalizar a interface do usuário. Você pode adicionar novos elementos, modificar o CSS ou incluir novas funcionalidades em JavaScript.

Estrutura do Código
app.py
Este é o arquivo principal que define a aplicação Flask, configura o banco de dados, e contém as rotas para upload e verificação de arquivos.

models.py
Define os modelos de banco de dados utilizando SQLAlchemy.

secrets.json
Contém a configuração do segredo da aplicação e a URI do banco de dados.

index.html
O template HTML que contém o formulário de upload e a lógica para exibir mensagens de erro e sucesso.

Dependências
Flask
SQLAlchemy
pandas
psycopg2-binary
openpyxl
