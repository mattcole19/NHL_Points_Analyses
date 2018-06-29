from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import csv

'''Creates and returns array of all dates that regular season games were played 
in year-month-day format '''
def get_dates():
    oct = month_day_creator('201710', ['29', '30', '31'])
    oct.remove('20171001')
    nov = month_day_creator('201711', ['29', '30'])
    dec = month_day_creator('201712', ['29', '30', '31'])
    jan = month_day_creator('201801', ['29', '30', '31'])
    jan.remove('20180126')
    jan.remove('20180127')
    jan.remove('20180128')
    jan.remove('20180129')
    feb = month_day_creator('201802', [])
    mar = month_day_creator('201803', ['29', '30', '31'])
    apr = ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408']
    #dates = oct + nov + dec + jan + feb + mar + apr
    dates = ['20171010']
    return dates

'''Creates list of days for each month in year-month day format.  For example: Oct. 9, 2017 is '20171009'
 parameters:
    year_month - string of numerical value for respective month and year.  For example: Dec 2017 is '201712 
    end_days - days of month after the 28th. For example: October has 31 days so it would be ['29','30','31']'''
def month_day_creator(year_month, end_days):
    month_days = []
    days =['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                     '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28']
    for day in days:
        month_days.append(year_month + day)
    for day in end_days:
        month_days.append(year_month + day)
    return month_days

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

'''From the boxcore link title, this function determines the matchup and returns both teams as their abbreviation
parameters:
    soup'''
def get_teams(soup):
    abbreviations = {
    'Ducks':'ANA','Bruins':'BOS','Buffalo':'BUF','Flames':'CLG','Hurricanes':'CAR','Blackhawks':'CHI','Avalance':'COL','Blue Jackets':'CBJ','Stars':'DAL','Red Wings':'DET','Oilers':'EDM',
    'Panthers':'FLA','Kings':'LAK','Wild':'MIN','Canadiens':'MTL','Predators':'NSH','Devils':'NJD','Islanders':'NYI','Rangers':'NYR','Senators':'OTT','Flyers':'PHI','Coyotes':'ARI',
    'Penguins':'PIT','Blues':'STL','Sharks':'SJS','Lightning':'TBL','Toronto':'TOR','Canucks':'VAN','Golden Knights':'VGK','Capitals':'WSH','Jets':'WNP'
    }
    website_title = soup.find('title').text
    title_separated = website_title.split(' vs. ')
    home = title_separated[0]
    another_separation = title_separated[1].split(' - ')
    away = another_separation[0]
    #switches name to appropriate abbreviation
    home_team = abbreviations[home]
    away_team = abbreviations[away]
    return home_team, away_team

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

'''Calculates appropriate amount of points a team earned throughout the season
parameters:
    data = data set'''
def calc_points(data):
    for row in data:
        if row[0] != 'TEAM':
            points = 2*row[2] + 1*row[4]
            row[5] = points
    return data
'''Creates csv file from data
parameters:
    data = data set'''
def create_csv(data):
    with open('nhl_data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)


'''Main function'''
def main():
    start_time =time.time()
    dates = get_dates()
    print('GATHERING GAME IDS')
    ids = gather_ids(dates)
    #arrays that will be created
    data = []
    '''header = team name, games played, wins, losses, overtime losses, points, goals for, 
    goals against, shots for, shots against, hits for, hits against'''
    header = ['TEAM', 'GP', 'W', 'L', 'OTL', 'POINTS', 'GF', 'GA', 'SF', 'SA', 'HF', 'HA']
    data.append(header)
    print("PLEASE WAIT WHILE STATS ARE GATHERED")
    print('-----------------------------------------------------------------------')
    teams = []
    invalid_ids = []
    ids.sort()
    for id in ids:
        #sets link to team stats page
        link = 'http://www.espn.com/nhl/matchup/_/gameId/' + id
        url = requests.get(link).text
        soup = BeautifulSoup(url, 'html.parser')
        website_title = soup.find('title').text
        if 'vs' not in website_title:
            invalid_ids.append(id)
            continue
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

    complete_data = calc_points(data)
    df = pd.DataFrame.from_records(complete_data)
    create_csv(complete_data)
    print(df)
    print('-----------------------------------------------------------------------')
    print("Games missing:", invalid_ids)
    print('PROGRAM COMPLETE')
    print('My program took', time.time() - start_time,'seconds to run')


if __name__ == '__main__':
    main()