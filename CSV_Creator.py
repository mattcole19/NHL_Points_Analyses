from bs4 import BeautifulSoup
import requests
import numpy as np

'''creates and returns array of all dates that regular season games were played 
in year-month-day format '''
def get_dates():
    dates = []
    dates.append('20171004')
    return dates


'''creates and returns array of all game IDS from the regular season
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
paramters:
    '''
def get_teams():
    return


def main():
    dates = get_dates()
    ids = gather_ids(dates)
    #arrays that will be created
    header = ['TEAM', 'GP', 'W', 'L', 'OTL', 'POINTS', 'GF/GP', 'GA/GP']
    print("PLEASE WAIT WHILE STATS ARE GATHERED")
    print('-------------------------------------')
    teams = []
    for id in ids:
        print(id)
        get_teams()

if __name__ == '__main__':
    main()