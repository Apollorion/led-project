#!/usr/bin/env python
# Display a runtext with double-buffering.
import os
import time
import sys
import requests
import random

def run():
    teams_url = "https://statsapi.web.nhl.com/api/v1/teams"
    nhl_teams = requests.get(teams_url).json()["teams"]
    while True:
        random.shuffle(nhl_teams)
        for team in nhl_teams:
            display_nhl_standings(team)


def display_nhl_standings(team):
    url = f"https://statsapi.web.nhl.com/api/v1/teams/{team['id']}/stats"
    r = requests.get(url).json()

    team_name = team["name"]
    team_venue = team["venue"]["name"]
    team_location = team["locationName"]
    first_year_of_play = team["firstYearOfPlay"]
    division_name = team["division"]["name"]
    conference_name = team["conference"]["name"]
    abbreviation = team["abbreviation"]
    in_the_league = r["stats"][1]["splits"][0]["stat"]["wins"]
    main_stats = r["stats"][0]["splits"][0]["stat"]

    win_loss_ot = f"{main_stats['wins']}-{main_stats['losses']}-{main_stats['ot']}"
    points = main_stats["pts"]
    games_played = main_stats["gamesPlayed"]
    gols_per_game = main_stats["goalsPerGame"]
    goals_against_per_game = main_stats["goalsAgainstPerGame"]
    faceoffs_taken = round(main_stats["faceOffsTaken"])
    faceoffs_win_pct = main_stats["faceOffWinPercentage"]
    save_pct = main_stats["savePctg"]

    team_intro = f"The {team_name} ({win_loss_ot}) are currently {in_the_league} in the league."
    display_text(team_intro)
    team_facts = f"{team_name} | {abbreviation} | {win_loss_ot} | {team_location} | {conference_name} Conference | {division_name} Division | {team_venue} | Since {first_year_of_play}"
    display_text(team_facts, 120)
    team_stats = f"{team_name} | {abbreviation} | {win_loss_ot} | Pts: {points} | GP: {games_played} | GPG: {gols_per_game} | GAPG: {goals_against_per_game} | FOT: {faceoffs_taken} | FOW%: {faceoffs_win_pct}% | Save%: {save_pct}%"
    display_text(team_stats, 120)

def display_text(my_text, seconds=60):
    if "LOCAL" not in os.environ:
        from matrix import display_text as dt
        dt(my_text, seconds=seconds)
    else:
        print(f"Displaying text: \"{my_text}\" for {seconds} seconds")
        time.sleep(5)

try:
    print("Press CTRL-C to stop")
    run()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)