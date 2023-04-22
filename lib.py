import requests
import json

TBA_Auth_Key = "aiQP5YMSkLerl0ibDSmM77GSDr3tVc9fZr9LIw7fL8AknFM1XuMZRgFtlEMttcBf"#auth key for the blue alliance data base
header = {#header format for the get requests
    'accept': 'application/json',
    'X-TBA-Auth-Key': TBA_Auth_Key,
    'User-Agent': 'scouting app'
}

def on_load(event_key):#updating and creating the database
    game_history = {#storing match key's
        'games': [
            'something',

        ],
    }

    json_data = {#general data
        'teams': [],
    }

    teams = get_info(f'https://www.thebluealliance.com/api/v3/event/{event_key}/teams/keys')
    try:#checking if we have connection with the TBA database
        teams['Error']
        print('** Data Faild **')
        return
    except:
        print('** Data Granted **')
    for team in teams:#updating the teams in the database(going to update this for loop soon)
        json_data['teams'].append({
            'key': team,
            'auto_T': 0,
            'auto_M': 0,
            'auto_B': 0,
            'auto_Dock': 0,
            'tele_T': 0,
            'tele_M': 0,
            'tele_B': 0,
            'tele_Dock': 0,
            })

    update_game_data(json_data)
    update_game_history(game_history)

def update_db(event_key):
    data = get_info(f'https://www.thebluealliance.com/api/v3/event/{event_key}/matches')
    try:
        data['Error']
        print('** Data Faild **')
        pass
    except:
        print('** Data Granted**')
    search_in_tele = ['tele_T', 'tele_M', 'tele_B', 'tele_Dock']
    search_in_auto = ['auto_T', 'auto_M', 'auto_B', 'auto_Dock']
    search = ['T', 'M', 'B']

    game_history = get_game_history()
    current_data = get_db()

    try:
        game_history['Error']
        print('** History Faild **')
        return
    except:
        print('** History Granted **')

    for game in data:
        if game['key'] in game_history['games']:#the history list is not working
            continue
        else:
            game_history['games'].append(game['key'])
        current_data = search_data('blue', search_in_auto, search, current_data, game, 'autoCommunity')
        current_data = search_data('red', search_in_auto, search,current_data, game, 'autoCommunity')
        current_data = search_data('blue', search_in_tele, search,current_data, game, 'teleopCommunity')
        current_data = search_data('red', search_in_tele, search,current_data, game, 'teleopCommunity')
    try:
        update_game_history(game_history)
        update_game_data(current_data)
        print('** Update Data Granted **')
    except:
        print('** Update Data Faild **')


def update_game_history(game_history):
    with open('game.json', 'w') as game_data:
        json.dump(game_history, game_data)

def update_game_data(game_data):
    with open('data.json', 'w') as json_data:
        json.dump(game_data, json_data)

def get_db():
    current_data = {'Error': 'no data from file'}
    with open('data.json', 'r') as data:
        current_data = json.load(data)
    return current_data

def get_game_history():
    current_game_history = {'Error': 'no data from file'}
    with open('game.json', 'r') as data:
        current_game_history = json.load(data)
    return current_game_history

def get_db_team(team_key):#getting the index of a team in the data base
    current_data = get_db()
    
    for i, elem in enumerate(current_data['teams']):
        if elem['key'] == team_key:
            return i

    return -1

def get_info(url):#function for get requests from the database
    info = requests.get(url, headers=header)
    json = info.json()
    try:
        json['Error']
        return {'Error': 'didnt get data'}
    except:
        return json

def search_data(team, search_in_data, search, current_data, data, community): #getting data on a match and the teams in the match
    cone_count = 0
    cube_count = 0

    for i in range(3):
        cone_count = data['score_breakdown'][team][community][search[i]].count('Cone')
        cube_count = data['score_breakdown'][team][community][search[i]].count('Cube')
        for j in range(3):
            current_data['teams'][get_db_team(data['alliances'][team]['team_keys'][j])][search_in_data[j]] += cube_count + cone_count

        if data['score_breakdown'][team][f'autoChargeStationRobot{i+1}'] == 'Docked':
            current_data['teams'][get_db_team(data['alliances'][team]['team_keys'][i])]['auto_Dock'] += 1
        if data['score_breakdown'][team][f'endGameChargeStationRobot{i+1}'] == 'Docked':
            current_data['teams'][get_db_team(data['alliances'][team]['team_keys'][i])]['tele_Dock'] += 1
    return current_data
