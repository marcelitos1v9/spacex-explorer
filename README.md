# SpaceX Explorer

## Sobre o Projeto

O SpaceX Explorer é uma aplicação web desenvolvida em Flask que permite aos usuários explorar dados sobre a SpaceX, incluindo lançamentos, foguetes, tripulações e áreas de pouso. A aplicação consome a API pública da SpaceX para fornecer informações atualizadas e detalhadas sobre as atividades da empresa espacial.

## Funcionalidades

### Página Inicial
- Visão geral da SpaceX com linha do tempo histórica
- Design moderno com animações e efeitos visuais
- Background animado com efeito de estrelas

### Lançamentos
- Lista completa de lançamentos passados
- Filtros por status (sucesso/falha)
- Sistema de busca por nome
- Paginação (9 itens por página)
- Detalhes completos de cada lançamento

### Foguetes
- Catálogo de foguetes da SpaceX
- Especificações técnicas detalhadas
- Galeria de imagens
- Métricas de desempenho

### Tripulação
- Perfis dos astronautas
- Filtros por status
- Sistema de busca por nome
- Paginação integrada
- Informações detalhadas de cada membro

### Áreas de Pouso (Landpads)
- Listagem de todas as áreas de pouso
- Filtros por status operacional
- Sistema de busca
- Paginação
- Detalhes de cada local

### Dados Personalizados
- Adição de itens em lista
- Suporte para dados em formato JSON
- Gerenciamento de dados (adicionar/remover)
- Feedback visual de operações

## Tecnologias Utilizadas

### Backend
- Python 3.x
- Flask (Framework Web)
- Requests (Consumo de API)
- JSON (Manipulação de dados)

### Frontend
- HTML5
- CSS3 com animações personalizadas
- JavaScript
- Bootstrap 5.3.3
- Font Awesome 5.15.4 (ícones)

### APIs e Serviços
- SpaceX API v4/v5
- CDN para recursos externos

## Recursos Visuais
- Design responsivo
- Navbar com efeitos de transição
- Tema escuro com gradientes
- Animações suaves
- Ícones interativos
- Footer com múltiplas seções

## Como Executar

### Opção 1: Ambiente Virtual Python

1. Clone o repositório:
```bash
git clone https://github.com/marcelitos1v9/spacex-explorer
cd spacex-explorer
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# Para Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Para Windows (Command Prompt - CMD):
venv\Scripts\activate.bat

# Para Linux/Mac:
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
python app.py
```

5. Acesse a aplicação em seu navegador:
```
http://localhost:5000
```

6. Para desativar o ambiente virtual quando terminar:
```bash
deactivate
```

**Nota**: Se estiver usando Windows e encontrar problemas de permissão no PowerShell, execute o seguinte comando como administrador:
```powershell
Set-ExecutionPolicy RemoteSigned
```

### Opção 2: Docker Compose

1. Clone o repositório:
```bash
git clone https://github.com/marcelitos1v9/spacex-explorer
cd spacex-explorer
```

2. Certifique-se de que o Docker e o Docker Compose estão instalados no seu sistema.

3. Execute a aplicação com Docker Compose:
```bash
docker-compose up --build
```

4. Acesse a aplicação em seu navegador:
```
http://localhost:5000
```

5. Para parar a aplicação, pressione `Ctrl+C` no terminal ou execute em outro terminal:
```bash
docker-compose down
```

## Estrutura do Projeto
```