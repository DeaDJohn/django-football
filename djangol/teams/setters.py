
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import unicodedata
from datetime import datetime

def format_date(date_string, date_format = '%Y-%m-%d'):
    date = pd.to_datetime(date_string, format=date_format)
    date_string = date.strftime(date_format)
    date = datetime.strptime(date_string, date_format)

    return date

def remove_accents(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    
def get_teams_from_web() :

    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"} 
    '''Obtener los equipos de las 5 principales ligas de futbol.'''
    comps_url = [
        'https://www.transfermarkt.es/laliga/startseite/wettbewerb/ES1',
        'https://www.transfermarkt.es/premier-league/startseite/wettbewerb/GB1',
        'https://www.transfermarkt.es/serie-a/startseite/wettbewerb/IT1',
        'https://www.transfermarkt.es/1-bundesliga/startseite/wettbewerb/L1',
        'https://www.transfermarkt.es/ligue-1/startseite/wettbewerb/FR1'
    ]


    columns_names = ["team_name", "team_image", "team_profile"]
    df_teams = pd.DataFrame(columns = columns_names)

    for comp_url in comps_url:
        response_obj = requests.get(comp_url, headers=headers)
        page_bs = BeautifulSoup(response_obj.content, 'html.parser')
        teams = page_bs.find_all("table", {"class": "items"})[0].find_all("tr", {"class": re.compile(r"odd|even")})
        for team in teams:
            team_name = team.find_all("td", {"class": "hauptlink"})[0].find("a").text.strip()
            team_image = team.find_all("td", {"class": "zentriert"})[0].find("img").get("src").replace("tiny", "head")
            team_profile = "https://www.transfermarkt.es" + team.find_all("td", {"class": "hauptlink"})[0].find("a").get("href").replace('startseite','kader') + "/plus/1"
            df_teams.loc[len(df_teams)] = [team_name, team_image, team_profile]
    df_teams = df_teams.reset_index()

    return df_teams


def get_countries_from_web(teams):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"} 
    
    '''Obtener los paises recorriendo las url de los equipos obtenidos de la tabla tab_teams de la bbdd.'''
    columns_teams = ["name", "image", "profile"]
    df_teams = pd.DataFrame(teams, columns=columns_teams)
    df_teams = df_teams.reset_index()
    print(df_teams)
    country_column_names = ["name", "image"]
    df_countries = pd.DataFrame(columns=country_column_names)
    print(df_teams)
    for index, row in df_teams.iterrows():
        print(row)
        url = row["profile"]
        response_obj = requests.get(url, headers=headers)
        page_bs = BeautifulSoup(response_obj.content, 'html.parser')
        players = page_bs.find_all("table", {"class": "items"})[0].find_all("tr", {"class": re.compile(r"odd|even")})
        
        for player in players :
            player_image_element = player.find_all("td", {"class": "zentriert"})[2].find("img")
            player_country = player_image_element.get("title")
            if not any( df_countries['name'] == player_country) :

                player_country_img = player_image_element.get("src").replace("verysmall", "head")
                df_countries.loc[len(df_countries)] = [player_country, player_country_img]
    df_countries = df_countries.reset_index()

    return df_countries

def get_players_from_web(teams, countries):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"} 
    date_format = '%d/%m/%Y'
    '''Obtener todos los jugadores de los equipos que esten almacenados en la bbdd en la tabla tab_teams.'''
    columns_teams = ["name", "image", "profile"]
    df_teams = pd.DataFrame(teams, columns=columns_teams)
    df_teams = df_teams.reset_index()

    columns_countries = ["name", "image", "profile"]
    df_countries = pd.DataFrame(countries, columns=columns_countries)
    df_countries = df_countries.reset_index()
    player_column_names = ["name", "birth", "age", "height", "pref_foot", "position", "sing_date", "end_contract", "market_value", "image", "country", 'id_team', 'id_country']
    df_players = pd.DataFrame(columns=player_column_names)


    for index, row in df_teams.iterrows():

        url = row["profile"]
        id_team = row['name']
        response_obj = requests.get(url, headers=headers)
        page_bs = BeautifulSoup(response_obj.content, 'html.parser')
        players = page_bs.find_all("table", {"class": "items"})[0].find_all("tr", {"class": re.compile(r"odd|even")})
        
        for player in players :
            player_name = player.find("td", {"class": "posrela"}).find("table").find("tr").find("td").find("img").get("title")
            
            name = remove_accents(player_name)
            print(name)
            position = player.find( "td", {"class": "posrela"}).find("table").find_all("tr")[1].find("td").text.strip()
            birth = player.find_all("td", {"class": "zentriert"})[1].text.rstrip() 
            age = birth.split("(")[1].split(")")[0]
            birth = birth.split("(")[0].rstrip() 
            print(birth)
            height = player.find_all("td", {"class": "zentriert"})[3].text
            foot = player.find_all("td", {"class": "zentriert"})[4].text
            sing_date = player.find_all("td", {"class": "zentriert"})[5].text.rstrip()
            print(sing_date)
            end_contract = player.find_all("td", {"class": "zentriert"})[7].text.rstrip()
            print(end_contract)
            market_value = player.find("td", {"class": "rechts hauptlink"}).text
            img = player.find("td", {"class": "posrela"}).find("table").find("tr").find("td").find("img").get("data-src")
            country = player.find_all("td", {"class": "zentriert"})[2].find("img").get("title")
    
            id_country = df_countries.loc[df_countries['name'] == country]['name'].values[0]
            df_players.loc[len(df_players)] = [name, birth, age, height, foot, position, sing_date, end_contract, market_value, img, country, id_team, id_country]
            
    for column in df_players :
        df_players.loc[( (df_players[column] == " ") | (df_players[column] == "-")), column] = np.nan
        # df_players['birth'] = pd.to_datetime(df_players['birth'], format='%d/%m/%Y')
        # df_players['sing_date'] = pd.to_datetime(df_players['sing_date'], format='%d/%m/%Y')
        # df_players['end_contract'] = pd.to_datetime(df_players['end_contract'], format='%d/%m/%Y')



    return df_players

