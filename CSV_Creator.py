from bs4 import BeautifulSoup
import requests
import numpy as np

'''Creates and returns array of all dates that regular season games were played 
in year-month-day format '''
def get_dates():
    dates = []
    dates.append('20171004')
    return dates


'''Creates and returns array of all game IDS from the regular season
parameters:
    days - every day regular season NHL games are played'''
def gather_ids(days):
    game_ids = []
    for day in days:
        link = "http://www.espn.com/nhl/scoreboard?date=" + day
        url = requests.get(link).text
        soup = BeautifulSoup(url, 'html.parser')
        for game in soup.find_all('a'):
            if 'boxscore' in game.get('href'):
                boxscore_link = game.get('href')
                link_separated = boxscore_link.split('=')
                game_id = link_separated[1]
                if game_id not in game_ids:
                    game_ids.append(game_id)
    return game_ids

'''From the boxcore link title, this function determines the matchup and returns both teams
parameters:
    soup'''
def get_teams(soup):
    website_title = soup.find('title').text
    title_separated = website_title.split(' vs. ')
    home = title_separated[0]
    another_separation = title_separated[1].split(' - ')
    away = another_separation[0]
    return home, away

'''Finds and returns score of game
parameters:
    soup'''
def get_score(soup):
    score = []
    for goals in soup.find_all('div', class_='Gamestrip__Score'):
        score.append(goals.text)
    home_goals = score[0]
    away_goals = score[1]
    return home_goals, away_goals

def main():
    dates = get_dates()
    ids = gather_ids(dates)
    #arrays that will be created
    data = []
    header = ['TEAM', 'GP', 'W', 'L', 'OTL', 'POINTS', 'GF/GP', 'GA/GP']
    data.append(header)
    print("PLEASE WAIT WHILE STATS ARE GATHERED")
    print('-------------------------------------')
    teams = []
    for id in ids:
        print(id)
        #sets link to team stats page
        link = 'http://www.espn.com/nhl/matchup/_/gameId/' + id
        url = requests.get(link).text
        soup = BeautifulSoup(url, 'html.parser')
        print(link)
        home_team, away_team = get_teams(soup)
        if home_team not in teams:
            teams.append(home_team)
        if away_team not in teams:
            teams.append(away_team)
        home_goals, away_goals = get_score(soup)



if __name__ == '__main__':
    main()