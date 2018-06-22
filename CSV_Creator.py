from bs4 import BeautifulSoup
import requests
import time
'''Creates and returns array of all dates that regular season games were played 
in year-month-day format '''
def get_dates():
    dates = []
    dates = ['20171004']
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

''' initializes an array for team following header format
parameters:
    team - team name'''
def initialize_array(team):
    new_array = [team, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return new_array

'''Finds and returns score of game
parameters:
    soup'''
def get_score(soup):
    score = []
    for goals in soup.find_all('div', class_='Gamestrip__Score'):
        score.append(goals.text)
    home_goals = int(score[0])
    away_goals = int(score[1])
    return home_goals, away_goals

'''Searches for row in data that corresponds to the desired team and returns the index
parameters:
    data - data being collected
    home_team - home team name
    away_team - away team name'''
def search(data, home_team, away_team):
    home_index = -1
    away_index = -1
    index = 0
    for row in data:
        if row[0] == home_team:
            home_index = index
        if row[0] == away_team:
            away_index = index
        index +=1
        if (home_index != -1) and (away_index != -1):
            return home_index, away_index

'''Searches for shots in game and returns them as home and away shots
parameters:
    soup'''
def get_shots(soup):
    shots_list= []
    for num_shots in soup.find_all('div', class_='BarLine__Stat'):
        shots_list.append(num_shots.text)
    home_shots = int(shots_list[0])
    away_shots = int(shots_list[1])
    return home_shots, away_shots

'''Searches for hits in game and returns them as home and away hits
parameters:
    soup'''
def get_hits(soup):
    hits_list= []
    for num_hits in soup.find_all('div', class_='BarLine__Stat'):
        hits_list.append(num_hits.text)
    home_hits = int(hits_list[2])
    away_hits = int(hits_list[3])
    return home_hits, away_hits

'''Main function'''
def main():
    start_time =time.time()
    dates = get_dates()
    ids = gather_ids(dates)
    #arrays that will be created
    data = []
    '''header = team name, games played, wins, losses, overtime losses, points, goals for, 
    goals against, shots for, shots against, hits for, hits against'''
    header = ['TEAM', 'GP', 'W', 'L', 'OTL', 'POINTS', 'GF', 'GA', 'SF', 'SA', 'HF', 'HA']
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
            data.append(initialize_array(home_team))
            teams.append(home_team)
        if away_team not in teams:
            data.append(initialize_array(away_team))
            teams.append(away_team)
        home_index, away_index = search(data, home_team, away_team)

        home_goals, away_goals = get_score(soup)

        #games played
        data[home_index][1] +=1
        data[away_index][1] +=1

        #wins, losses, OT losses
        game_type_title = soup.find('div', class_='ScoreCell__Time').text
        if home_goals > away_goals:
            data[home_index][2] += 1
            if game_type_title == 'Final':
                data[away_index][3] += 1
            else:
                data[away_index][4] +=1
        else:
            data[away_index][2] += 1
            if game_type_title == 'Final':
                data[home_index][3] += 1
            else:
                data[home_index][4] +=1

        #goals for
        data[home_index][6] += home_goals
        data[away_index][6] += away_goals

        #goals against
        data[home_index][7] += away_goals
        data[away_index][7] += home_goals

        #shots for, shots against
        home_shots, away_shots = get_shots(soup)
        data[home_index][8] += home_shots
        data[home_index][9] += away_shots
        data[away_index][8] += away_shots
        data[away_index][9] += home_shots

        #hits
        home_hits, away_hits = get_hits(soup)
        data[home_index][10] += home_hits
        data[home_index][11] += away_hits
        data[away_index][10] += away_hits
        data[away_index][11] += home_hits

    for row in data:
        print(row)
    print('-------------------------------------')
    print('PROGRAM COMPLETE')
    print('My program took', time.time() - start_time,'seconds to run')

if __name__ == '__main__':
    main()