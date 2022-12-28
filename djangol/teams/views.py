from django.shortcuts import render
from .models import Team, Country
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
