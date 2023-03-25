import lib as lib

url = "https://www.thebluealliance.com/api/v3/team/frc"

if __name__ == "__main__":
	team_number = input("enter team number: ")
	info = lib.get_info(url + team_number)
	print(info)
	events = lib.get_team_status_avg(team_number, 2023)
	print(events)