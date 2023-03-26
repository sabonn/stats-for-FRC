import requests
import json

TBA_Auth_Key = "aiQP5YMSkLerl0ibDSmM77GSDr3tVc9fZr9LIw7fL8AknFM1XuMZRgFtlEMttcBf"
header = {
    'accept': 'application/json',
    'X-TBA-Auth-Key': TBA_Auth_Key,
    'User-Agent': 'scouting app'
}

def on_load(event_key):
    json_data = {
        'teams': [],
    }

    teams = get_info(f'https://www.thebluealliance.com/api/v3/event/{event_key}/teams/keys')
    for team in teams:
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

    with open('data.json', 'w') as data:
        json.dump(json_data,data)

def update_db(event_key):
    data = get_info(f'https://www.thebluealliance.com/api/v3/event/{event_key}/matches')

    search_in_tele = ['tele_T', 'tele_M', 'tele_B', 'tele_Dock']
    search_in_auto = ['auto_T', 'auto_M', 'auto_B', 'auto_Dock']
    search = ['T', 'M', 'B']

    current_data = get_db()

    for game in data:
        current_data = search_data('blue', search_in_auto, search, current_data, game)
        current_data = search_data('red', search_in_auto, search,current_data, game)
        current_data = search_data('blue', search_in_tele, search,current_data, game)
        current_data = search_data('red', search_in_tele, search,current_data, game)


    with open('data.json', 'w') as json_data:
        json.dump(current_data, json_data)

def get_db():
    current_data = {'Error': 'no data from file'}
    with open('data.json', 'r') as data:
        current_data = json.load(data)
    return current_data

def get_db_team(team_key):
    current_data = {}
    with open('data.json', 'r') as data:
        current_data = json.load(data)

    for i, elem in enumerate(current_data['teams']):
        if elem['key'] == team_key:
            return i

    return -1

def get_info(url):
    info = requests.get(url, headers=header)
    json = info.json()
    try:
        json['Error']
        return {'Error': 'didnt get data'}
    except:
        return json

def search_data(team, search_in_data, search, current_data, data):
    cone_count = 0
    cube_count = 0

    for i in range(3):
        cone_count = data['score_breakdown'][team]['autoCommunity'][search[i]].count('Cone')
        cube_count = data['score_breakdown'][team]['autoCommunity'][search[i]].count('Cube')
        for j in range(3):
            current_data['teams'][get_db_team(data['alliances'][team]['team_keys'][j])][search_in_data[j]] += cube_count + cone_count

            if data['score_breakdown'][team][f'autoChargeStationRobot{j+1}'] == 'Docked':
                current_data['teams'][get_db_team(data['alliances'][team]['team_keys'][j])]['auto_Dock'] += 1
            if data['score_breakdown'][team][f'endGameChargeStationRobot{j+1}'] == 'Docked':
                current_data['teams'][get_db_team(data['alliances'][team]['team_keys'][j])]['tele_Dock'] += 1

    return current_data


