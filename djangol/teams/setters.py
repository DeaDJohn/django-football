
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import unicodedata


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

