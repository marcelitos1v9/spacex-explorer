from flask import render_template, request, redirect, url_for
import urllib
import json
from datetime import datetime
import requests

jogadores = []
gamelist = [{"Titulo": "CS-GO",
         "Ano": 2017,
          "Categoria": "FPS-Online"
         }, {
             
         }]

# Listas globais para armazenar os dados
custom_list = []
custom_dict = []

def init_app(app):
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
        year = datetime.now().year
        response = requests.get(f'https://api.spacexdata.com/v5/launches/{launch_id}')
        launch = response.json()
        return render_template('launch_detail.html', year=year, launch=launch)

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

    @app.route('/custom-data', methods=['GET', 'POST'])
    def custom_data_page():
        year = datetime.now().year
        message = None
        
        if request.method == 'POST':
            if 'list_item' in request.form:
                # Adiciona item à lista
                item = request.form.get('list_item')
                if item:
                    custom_list.append(item)
                    message = {'type': 'success', 'text': 'Item adicionado à lista com sucesso!'}
            
            elif 'json_data' in request.form:
                try:
                    # Adiciona dicionário
                    json_data = request.form.get('json_data')
                    data_dict = json.loads(json_data)
                    custom_dict.append(data_dict)
                    message = {'type': 'success', 'text': 'Dicionário adicionado com sucesso!'}
                except json.JSONDecodeError:
                    message = {'type': 'danger', 'text': 'Erro: JSON inválido'}
                except Exception as e:
                    message = {'type': 'danger', 'text': f'Erro: {str(e)}'}
        
        return render_template('custom_data.html', 
                             year=year, 
                             custom_list=custom_list,
                             custom_dict=custom_dict,
                             message=message)

    @app.route('/custom-data/clear/<data_type>', methods=['POST'])
    def clear_custom_data(data_type):
        if data_type == 'list':
            custom_list.clear()
        elif data_type == 'dict':
            custom_dict.clear()
        return redirect(url_for('custom_data_page'))

    @app.route('/custom-data/remove/<data_type>/<int:index>')
    def remove_item(data_type, index):
        try:
            if data_type == 'list':
                custom_list.pop(index)
            elif data_type == 'dict':
                custom_dict.pop(index)
        except IndexError:
            pass
        return redirect(url_for('custom_data_page'))
