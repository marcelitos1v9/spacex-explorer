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

1. Clone o repositório:
```bash
git clone https://github.com/marcelitos1v9/spacex-explorer
cd spacex-explorer
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
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

## Estrutura do Projeto
```
spacex-explorer/
├── app.py                 # Arquivo principal da aplicação
├── requirements.txt       # Dependências do projeto
├── controllers/          
│   └── routes.py         # Rotas e lógica da aplicação
├── static/
│   ├── css/              # Arquivos CSS
│   ├── js/               # Arquivos JavaScript
│   └── imgs/             # Imagens e recursos
└── templates/            # Templates HTML
    ├── base.html         # Template base
    ├── index.html        # Página inicial
    ├── launches.html     # Página de lançamentos
    ├── rockets.html      # Página de foguetes
    ├── crew.html         # Página da tripulação
    ├── landpads.html     # Página de áreas de pouso
    └── custom_data.html  # Página de dados personalizados
```

## Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Agradecimentos

- [SpaceX API](https://github.com/r-spacex/SpaceX-API)
- [Bootstrap](https://getbootstrap.com)
- [Font Awesome](https://fontawesome.com)
