from flask import render_template, request, redirect, url_for
import urllib
import json
from datetime import datetime
import requests
from models.custom_data import db, CustomList, CustomDict, CustomData

jogadores = []
gamelist = [{"Titulo": "CS-GO",
         "Ano": 2017,
          "Categoria": "FPS-Online"
         }, {
             
         }]

# Listas globais para armazenar os dados
custom_list = []
custom_dict = []

def get_valid_image_url(url):
    """
    Verifica se a URL da imagem é válida e retorna uma URL padrão caso não seja.
    """
    if not url:
        return url_for('static', filename='images/placeholder.jpg')
    
    # Verifica se a URL começa com http ou https
    if not url.startswith(('http://', 'https://')):
        return f"https://{url}"
    
    return url

def init_app(app):
    # Configuração do SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///custom_data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        year = datetime.now().year
        response = requests.get('https://api.spacexdata.com/v4/history')
        history_data = response.json()
        return render_template('index.html', year=year, history=history_data)

    @app.route('/launches')
    def launches():
        year = datetime.now().year
        page = request.args.get('page', 1, type=int)
        items_per_page = 9
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        
        # Busca todos os lançamentos
        response = requests.get('https://api.spacexdata.com/v5/launches')
        all_launches = response.json()
        
        # Remove lançamentos pendentes e ordena por data
        filtered_launches = [launch for launch in all_launches if launch['upcoming'] == False]
        filtered_launches.sort(key=lambda x: x['date_unix'], reverse=True)
        
        # Aplica filtros adicionais
        if search:
            filtered_launches = [
                launch for launch in filtered_launches 
                if search.lower() in launch['name'].lower()
            ]
        if status:
            if status == 'success':
                filtered_launches = [launch for launch in filtered_launches if launch['success'] == True]
            elif status == 'failed':
                filtered_launches = [launch for launch in filtered_launches if launch['success'] == False]
        
        # Paginação
        total_launches = len(filtered_launches)
        total_pages = (total_launches + items_per_page - 1) // items_per_page
        
        # Ajusta a página atual se estiver fora do intervalo
        if page > total_pages:
            page = total_pages
        if page < 1:
            page = 1
            
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_launches = filtered_launches[start_idx:end_idx]
        
        # Verifica e corrige URLs de imagens para cada lançamento
        for launch in current_launches:
            if 'links' in launch and 'patch' in launch['links']:
                if 'small' in launch['links']['patch']:
                    launch['links']['patch']['small'] = get_valid_image_url(launch['links']['patch']['small'])
                if 'large' in launch['links']['patch']:
                    launch['links']['patch']['large'] = get_valid_image_url(launch['links']['patch']['large'])
        
        return render_template(
            'launches.html',
            year=year,
            launches=current_launches,
            page=page,
            total_pages=total_pages,
            search=search,
            status=status
        )

    @app.route('/rockets')
    def rockets():
        year = datetime.now().year
        response = requests.get('https://api.spacexdata.com/v4/rockets')
        rockets_data = response.json()
        return render_template('rockets.html', year=year, rockets=rockets_data)

    @app.route('/crew')
    def crew():
        year = datetime.now().year
        page = request.args.get('page', 1, type=int)
        items_per_page = 9
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        
        # Busca todos os membros da tripulação
        response = requests.get('https://api.spacexdata.com/v4/crew')
        all_crew = response.json()
        
        # Aplica filtros
        filtered_crew = all_crew
        if search:
            filtered_crew = [
                member for member in filtered_crew 
                if search.lower() in member['name'].lower()
            ]
        if status:
            filtered_crew = [
                member for member in filtered_crew 
                if member['status'].lower() == status.lower()
            ]
        
        # Ordenar por nome
        filtered_crew.sort(key=lambda x: x['name'])
        
        # Paginação
        total_crew = len(filtered_crew)
        total_pages = (total_crew + items_per_page - 1) // items_per_page
        
        # Ajusta a página atual se estiver fora do intervalo
        if page > total_pages:
            page = total_pages
        if page < 1:
            page = 1
            
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_crew = filtered_crew[start_idx:end_idx]
        
        return render_template(
            'crew.html',
            year=year,
            crew=current_crew,
            page=page,
            total_pages=total_pages,
            search=search,
            status=status
        )

    @app.route('/api-docs')
    def api_docs():
        year = datetime.now().year
        return render_template('api_docs.html', year=year)

    @app.route('/launch/<launch_id>')
    def launch_detail(launch_id):
        try:
            response = requests.get(f"https://api.spacexdata.com/v4/launches/{launch_id}")
            
            if response.status_code == 200:
                try:
                    launch = response.json()
                    
                    # Corrige URLs de imagens
                    if 'links' in launch and 'patch' in launch['links']:
                        if 'small' in launch['links']['patch']:
                            launch['links']['patch']['small'] = get_valid_image_url(launch['links']['patch']['small'])
                        if 'large' in launch['links']['patch']:
                            launch['links']['patch']['large'] = get_valid_image_url(launch['links']['patch']['large'])
                    
                    # Corrige URLs de imagens de fotos do lançamento
                    if 'links' in launch and 'flickr' in launch['links']:
                        if 'original' in launch['links']['flickr']:
                            launch['links']['flickr']['original'] = [
                                get_valid_image_url(img) for img in launch['links']['flickr']['original']
                            ]
                    
                    return render_template("launch_detail.html", launch=launch)
                except requests.exceptions.JSONDecodeError:
                    return render_template("error.html", message="Erro ao processar dados do lançamento. Resposta inválida da API.")
            else:
                return render_template("error.html", message=f"Erro ao buscar dados do lançamento. Código de status: {response.status_code}")
        
        except Exception as e:
            return render_template("error.html", message=f"Ocorreu um erro: {str(e)}")

    @app.route('/rocket/<rocket_id>')
    def rocket_detail(rocket_id):
        year = datetime.now().year
        response = requests.get(f'https://api.spacexdata.com/v4/rockets/{rocket_id}')
        rocket = response.json()
        return render_template('rocket_detail.html', year=year, rocket=rocket)

    @app.route('/landpads')
    def landpads():
        year = datetime.now().year
        page = request.args.get('page', 1, type=int)
        items_per_page = 9
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        
        # Busca todos os landpads
        response = requests.get('https://api.spacexdata.com/v4/landpads')
        all_landpads = response.json()
        
        # Aplica filtros
        filtered_landpads = all_landpads
        if search:
            filtered_landpads = [
                pad for pad in filtered_landpads 
                if search.lower() in pad['name'].lower() or search.lower() in pad['full_name'].lower()
            ]
        if status:
            filtered_landpads = [
                pad for pad in filtered_landpads 
                if pad['status'].lower() == status.lower()
            ]
        
        # Ordenar por nome
        filtered_landpads.sort(key=lambda x: x['name'])
        
        # Paginação
        total_landpads = len(filtered_landpads)
        total_pages = (total_landpads + items_per_page - 1) // items_per_page
        
        if page > total_pages:
            page = total_pages
        if page < 1:
            page = 1
            
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_landpads = filtered_landpads[start_idx:end_idx]
        
        return render_template(
            'landpads.html',
            year=year,
            landpads=current_landpads,
            page=page,
            total_pages=total_pages,
            search=search,
            status=status
        )

    @app.route('/custom-data')
    def custom_data_page():
        page = request.args.get('page', 1, type=int)
        per_page = 10  # itens por página
        
        # Busca dados com paginação
        pagination = CustomData.query.order_by(CustomData.data_criacao.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Estatísticas
        total_registros = CustomData.query.count()
        ultima_atualizacao = CustomData.query.order_by(CustomData.data_atualizacao.desc()).first()
        total_categorias = db.session.query(CustomData.tipo.distinct()).count()
        
        return render_template('custom_data.html',
                             dados=pagination.items,
                             page=page,
                             total_pages=pagination.pages,
                             has_next=pagination.has_next,
                             has_prev=pagination.has_prev,
                             total_registros=total_registros,
                             ultima_atualizacao=ultima_atualizacao.data_atualizacao if ultima_atualizacao else None,
                             total_categorias=total_categorias)

    @app.route('/custom-data/novo', methods=['GET', 'POST'])
    def novo_dado():
        if request.method == 'POST':
            novo = CustomData(
                titulo=request.form['titulo'],
                descricao=request.form['descricao'],
                tipo=request.form['tipo']
            )
            db.session.add(novo)
            db.session.commit()
            return redirect(url_for('custom_data_page'))
        return render_template('custom_data_form.html')

    @app.route('/custom-data/editar/<int:id>', methods=['GET', 'POST'])
    def editar_dado(id):
        dado = CustomData.query.get_or_404(id)
        if request.method == 'POST':
            dado.titulo = request.form['titulo']
            dado.descricao = request.form['descricao']
            dado.tipo = request.form['tipo']
            db.session.commit()
            return redirect(url_for('custom_data_page'))
        return render_template('custom_data_form.html', dado=dado)

    @app.route('/custom-data/deletar/<int:id>')
    def deletar_dado(id):
        dado = CustomData.query.get_or_404(id)
        db.session.delete(dado)
        db.session.commit()
        return redirect(url_for('custom_data_page'))
