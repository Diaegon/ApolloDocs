# Projeto Solar Automático

Sistema para automatização de projetos de energia solar residenciais e comerciais.  
O programa recebe os dados do cliente e gera automaticamente toda a documentação necessária, poupando tempo com preenchimentos repetitivos e cálculos simples.

## Funcionalidades previstas

- Geração automática de documentos:  
  - Memorial descritivo  (gerado com a biblioteca ReportLab)
  - Diagrama unifilar  (feito com a biblioteca PyMuPDF a partir de um template existente)
  - Diagrama de situação (se necessário)  
  - Formulário de entrada (modelo ENEL-CE)  (feito com a biblioteca PyMuPDF a partir de um template existente)
  - Procuração particular  (gerado com a biblioteca ReportLab)
  - PDF com dados para TRT/ART  (em produção)
- Criação de banco de dados de equipamentos (inversores, placas etc.)  (em produção)
- Interface para entrada de dados e gerenciamento do banco  (TKinter)
- Organização automática dos documentos em pastas por cliente  (em produção)

## Fases do projeto

1. **Memorial descritivo e definição de inputs**  
   - Entrada dos dados via arquivo JSON  
   - Suporte a múltiplos modelos de inversores e placas  

2. **Geração da documentação complementar**  
   - Diagrama unifilar  (arquivos bases com edição utilizando a biblioteca pymupdf)
   - Preenchimento automático dos formulários  (biblioteca pymupdf)
   - Geração de procuração e PDF FICHA DO CLIENTE  

3. **Banco de dados dinâmico**  (projeto do banco de dados vai correr em paralelo com o da geração de projetos)
   - Cadastro e atualização de novos modelos de equipamentos  
   - Geração automática de pastas organizadas por cliente  

4. **Desenvolvimento da interface gráfica**  
   - Interface para entrada de dados, execução do programa e edição do banco  

5. **Geração do diagrama de situação**  
   - Desenho automático da localização da residência e sistema a partir de coordenadas geográficas  

6. **Atualizações para melhoria do código**
   - Cadastrar os inversores com a quantidade de string de cada modelo para que se possa fazer uma lógica adaptativa para que o texto se modifique de acordo com o inversor.
   - Diminuir o código "equacoes.py" para que o programa adicione uma quantidade ilimitada de inversores/placas de acordo com o input, sem a limitação de 3 tipos de inversores diferentes. 

# Como Usar

> ⚠️ **Projeto em desenvolvimento**

## Pré-requisitos

- Python 3.x
- Poetry (gerenciador de dependências)

## Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositório>
   cd <nome-do-projeto>
   ```

2. **Instale o Poetry**
   
   Se ainda não tiver o Poetry instalado, siga as instruções em [python-poetry.org](https://python-poetry.org/docs/#installation)

3. **Instale as dependências do projeto**
   ```bash
   poetry install
   ```

4. **Baixe os arquivos de suporte**
   
   Faça o download da pasta `support-files` através [deste link](https://drive.google.com/drive/folders/1wS_3gRbTehiSYByUsZgDKmRfIrHZ1TSS?usp=drive_link) e coloque-a na raiz do projeto.

## Configuração dos Dados de Entrada

Os dados de entrada estão em formato JSON e devem ser preenchidos antes da execução.

### Formato dos Dados

- **Tipos de valores aceitos:**
  - `string`: para textos (nomes, endereços, etc.)
  - `integer`: para valores numéricos (potência, quantidade, etc.)
  - `null`: para campos opcionais ou vazios

### Dados Necessários

Os arquivos JSON devem conter:
- Dados pessoais do cliente
- Dados do projetista
- Informações do procurador/homologador
- Especificações dos materiais utilizados
- Padrão elétrico residencial do cliente

Edite os arquivos de entrada de acordo com as especificações do projeto a ser desenvolvido.

## Execução

### Gerar Todos os Documentos

Para gerar todos os documentos de uma só vez, execute:

```bash
poetry run python main.py
```

### Gerar Documentos Específicos

#### Memorial Descritivo e Procuração

```bash
poetry run python gerar_pdf.py
```

Este script:
- Processa os dados de entrada
- Realiza os cálculos necessários
- Gera o memorial descritivo do sistema conforme as normas vigentes
- Cria a procuração

#### Diagrama Unifilar

O diagrama unifilar utiliza templates pré-estabelecidos para 1, 2 ou 3 inversores. O programa seleciona automaticamente o template adequado baseado nos dados de entrada e utiliza a biblioteca **PyMuPDF** para renderização.

#### Formulário ENEL-CE

Aplica a mesma lógica de templates do diagrama unifilar. O programa preenche automaticamente o formulário correto da ENEL-CE com os dados do cliente de acordo com as especificações do projeto.

## Estrutura do Projeto

```
.
├── support-files/          # Arquivos de suporte (templates, etc.)
├── main.py                 # Script principal
├── gerar_pdf.py           # Geração de memorial e procuração
├── pyproject.toml         # Configuração do Poetry
└── [arquivos JSON]        # Dados de entrada
```

## Observações

- Certifique-se de que todos os campos obrigatórios nos arquivos JSON estejam preenchidos
- Os documentos gerados seguem as normas técnicas vigentes
- Os templates são específicos para projetos da área de concessão da ENEL-CE




objetivo de estrutura final

meu_projeto/
│
├── models/
│   ├── __init__.py
│   ├── sistema_instalado.py    # Schema/Model
│   ├── inversor.py
│   ├── placa.py
│   └── procurador.py
│
├── factories/
│   ├── __init__.py
│   ├── sistema_factory.py      # Factory para criar sistemas
│   └── equipamento_factory.py  # Factory para criar equipamentos
│
├── services/
│   ├── __init__.py
│   └── sistema_service.py      # Lógica de negócio complexa
│
└── main.py
 
