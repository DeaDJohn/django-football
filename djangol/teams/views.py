from django.shortcuts import render
import math
from datetime import datetime
from .models import Team, Country, Player
from . import setters

# Create your views here.
def index(request):
    """La pagina de inicio para Learning Log"""
    return render(request, 'teams/index.html')


def update_teams(request):
    # Aquí puedes colocar la lógica de tu función
    teams = setters.get_teams_from_web()
    
    instancias = []
    for index, team in teams.iterrows():
        instancias.append(Team(name=team['team_name'], image=team['team_image']))
    print (instancias)
    Team.objects.bulk_create(instancias)
    num_instancias = Team.objects.count()
    print(num_instancias)
    context = { 'new_teams': num_instancias}
    return render(request, 'teams/update_teams.html', context)


def update_countries(request):
    # Aquí puedes colocar la lógica de tu función
    teams = Team.objects.all().values()

    countries = setters.get_countries_from_web(teams)
    print(countries)
    instancias = []
    for index, country in countries.iterrows():
    
        instancias.append(Country(name=country['name'],  image=country['image']))
    print (instancias)
    Country.objects.bulk_create(instancias)
    num_instancias = Country.objects.count()
    print(num_instancias)
    context = { 'new_countries': num_instancias}
    return render(request, 'teams/update_countries.html', context)

def update_players(request):
    # Aquí puedes colocar la lógica de tu función
    teams = Team.objects.all().values()
    countries = Country.objects.all().values()

    players = setters.get_players_from_web(teams, countries)

    instancias = []
    jugadores_creados = 0
    jugadores_existentes = 0
    for index, player in players.iterrows():
        print('birth')
        print(player['birth'])
        try:
            birth = datetime.strptime(player['birth'], '%d/%m/%Y')
            birth = birth.strftime('%Y-%m-%d')
        except:
            # Aquí puedes poner código para manejar el caso en el que la conversión falle
            # Por ejemplo, asignar un valor por defecto a la variable `sing_date`
            birth = None
        print(birth)
        print('sing_date')
        print(player['sing_date'])
        try:
            sing_date = datetime.strptime(player['sing_date'], '%d/%m/%Y')
            sing_date = sing_date.strftime('%Y-%m-%d')
        except:
            # Aquí puedes poner código para manejar el caso en el que la conversión falle
            # Por ejemplo, asignar un valor por defecto a la variable `sing_date`
            sing_date = None
        print(sing_date)
        print('end_contract')
        print(player['end_contract'])
        try:
            end_contract = datetime.strptime(player['end_contract'], '%d/%m/%Y')
            end_contract = end_contract.strftime('%Y-%m-%d')
        except:
            # Aquí puedes poner código para manejar el caso en el que la conversión falle
            # Por ejemplo, asignar un valor por defecto a la variable `sing_date`
            end_contract = None

        print(end_contract)
        print( Team.objects.filter(name=player['id_team']).first() )
        print( player['id_country'])
        print("=====")
        player, created = Player.objects.get_or_create(
            team=Team.objects.filter(name=player['id_team']).first(),
            country=Country.objects.filter(name=player['id_country']).first(),
            name=player['name'],
            defaults={
                'position': player['position'],
                'age': player['age'],
                'birth': birth,
                'height': player['height'],
                'foot': player['pref_foot'],
                'sing_date': sing_date,
                'end_contract': end_contract,
                'market_value': player['market_value'],
                'image': player['image']
            }
        )

        if created:
            jugadores_creados = jugadores_creados + 1
        else:
            jugadores_existentes = jugadores_existentes + 1


    num_instancias = Player.objects.count()
    print(num_instancias)
    context = { 'new_players': jugadores_creados, 'exist_players': jugadores_existentes}
    return render(request, 'teams/update_players.html', context)