import requests
import pandas

TBA_Auth_Key = "aiQP5YMSkLerl0ibDSmM77GSDr3tVc9fZr9LIw7fL8AknFM1XuMZRgFtlEMttcBf"
url = "https://www.thebluealliance.com/api/v3/team/frc4661"
header = {
	'accept': 'application/json',
	'X-TBA-Auth-Key': TBA_Auth_Key,
	'User-Agent': 'scouting app'
}

if __name__ == "__main__":
	info = requests.get(url, headers=header)
	print(info.json())
