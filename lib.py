import requests

TBA_Auth_Key = "aiQP5YMSkLerl0ibDSmM77GSDr3tVc9fZr9LIw7fL8AknFM1XuMZRgFtlEMttcBf"
header = {
	'accept': 'application/json',
	'X-TBA-Auth-Key': TBA_Auth_Key,
	'User-Agent': 'scouting app'
}

def get_info(url):
	info = requests.get(url, headers=header)
	json = info.json()
	try:
		json['Error']
		return {'Error': 'didnt get data'} 
	except:
		return json

def get_team_status_avg(team_number, year):
	events = requests.get(f'https://www.thebluealliance.com/api/v3/team/frc{team_number}/events/{year}/keys', headers = header)
	events_json = events.json()
	try:
		events_json['Error']
		return {'Error': 'faild to get data from api'}
	except:
		print("got data")

	avg_data = []
	for event in events_json:
		avg_data.append(get_team_status_event(team_number, event))

	return avg_data


def get_team_status_event(team_number, event_key):
	req = requests.get(f'https://www.thebluealliance.com/api/v3/team/frc{team_number}/event/{event_key}/matches', headers=header)
	matches = req.json()
	try:
		matches['Error']
		return {'Error': 'faild to get data from api'}
	except:
		print("got data")

	important_matches = []
	for match in matches:
		if f'frc{team_number}' in match['alliances']['blue']['team_keys'] or f'frc{team_number}' in match['alliances']['red']['team_keys']:
			important_matches.append(match)

	data = {
		'avg_T': 0,
		'avg_M': 0,
		'avg_B': 0,
		'avg_auto_T': 0,
		'avg_auto_M': 0,
		'avg-auto_B': 0,
		'avg_Dock': 0,
		'avg_auto_Dock': 0,
	}



