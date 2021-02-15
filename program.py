from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import xlwt
from xlwt import Workbook

PATH = "./chromedriver.exe"

def launchBrowser():
    driver = webdriver.Chrome(PATH)
    driver.get("http://playfasa.com/points.asp")
    return driver

def getScoreAndResult(team_name, team_1, team_1_score, team_2, team_2_score):

    if team_1_score == None or team_2_score == None:
        score = None
        result = "T"
    elif (team_name == team_1):
        score = team_1_score
        if score > team_2_score:
            result = "W"
        elif score == team_2_score:
            result = "T"
        else:
            result = "L"
    else:
        score = team_2_score
        if score > team_1_score:
            result = "W"
        elif score == team_1_score:
            result = "T"
        else:
            result = "L"
    
    return (score, result)

def createTeam(team_name, team_city, team_state, team_age, team_class, team_points, tourn_sanction, teams_db):
    teams_db[team_name] = {'team_name': team_name, 'team_city': team_city, 'team_state': team_state, 'team_age': team_age, 'team_class':team_class, 'team_points': team_points, 'games' : {}, 'tournaments': {}, 'upcoming_tournaments': {}}

def createGame(game_id, tournament_or_game_start_date, team_age, team_name, score, result, bracket_division, 
    tournament_name, tournament_city, tournament_state, teams_db):
    game = {
        "game_id" : game_id, "game_date":tournament_or_game_start_date, "team_age": team_age, 
        "team_name": team_name, "score": score, "result": result, "tournament_santion": "FASA", 
        "bracket_divison": bracket_division, "tournament_name": tournament_name, 
        "tournament_location": tournament_city + "," + tournament_state,
    }
    
    teams_db[team_name]['games'][game_id] = game

def getTournamentsAndGamesPage(tournaments_link, team_name, team_age, tourn_sanction, teams_db):

    tournaments_link.click()
    
    tournaments_body = driver.find_elements_by_tag_name("tbody").pop(7)
    all_trs = tournaments_body.find_elements_by_tag_name("tr")

    tournament_name = ""
    tournament_city = ""
    tournament_state = ""
    tournament_or_game_start_date = ""
    bracket_division = ""
    tournament_placement = ""
    tournament_id = 0
    upcomingTournaments = False
    upcoming_tournament_id = 0

    for tr in all_trs:
        if tr.text == "Up Coming Tournaments" or upcomingTournaments:

            if upcomingTournaments:
                tds = tr.find_elements_by_tag_name("td")
                if len(tds) > 0:
                    t_name = tds.pop(0).text.strip()
                    t_city = tds.pop(0).text.strip()
                    t_state = tds.pop(0).text.strip()
                    t_start_date = tds.pop(0).text.strip()

                    upcoming_tournament = {
                        "t_id": upcoming_tournament_id, 't_start_date': t_start_date, 
                        "t_sanction": tourn_sanction, "t_name": t_name, "t_location" : t_city + ',' + t_state
                    }
                    teams_db[team_name]['upcoming_tournaments'][t_name] = upcoming_tournament

                    upcoming_tournament_id += 1
                    continue

            else:
                upcomingTournaments = True
                continue
        try:
            #its a game tr
            if tr.find_element_by_tag_name("td").text == "":
                game_id = tr.find_element_by_tag_name("th").text
                tds = tr.find_elements_by_tag_name("td")
                
                team_1 = tds.pop(1).text.strip()
                team_1_score = tds.pop(1).text.strip()
                team_1_score = int(team_1_score) if len(team_1_score) != 0 else None

                team_2 = tds.pop(2).text.strip()
                team_2_score = tds.pop(2).text.strip()
                team_2_score = int(team_2_score) if len(team_2_score) != 0 else None
                
                (score, result) = getScoreAndResult(team_name, team_1, team_1_score, team_2, team_2_score)
                
                createGame(game_id, tournament_or_game_start_date, team_age, team_name, score, result, bracket_division, 
                tournament_name, tournament_city, tournament_state, teams_db)

                # print("GAME INFO:" + game_id + team_1 + team_1_score + "VS" + team_2 + team_2_score)          

            else:    
                tournament_info = tr.find_elements_by_class_name("style10")
                tournament_info2 = tr.find_elements_by_tag_name("td")
                if len(tournament_info) != 0:
                    tournament_name = tournament_info.pop(0).text.strip()
                    tournament_city = tournament_info.pop(0).text.strip()
                    tournament_state = tournament_info.pop(0).text.strip()
                    tournament_or_game_start_date = tournament_info.pop(0).text.strip()
                    tournament_placement = tournament_info2.pop(6).text.strip()
                    tournament = {
                        't_id': tournament_id, 't_start_date': tournament_or_game_start_date, "t_sanction": tourn_sanction,
                        't_placement': tournament_placement, 't_name': tournament_name, 't_location': tournament_city + ',' + tournament_state,
                    }
                    teams_db[team_name]['tournaments'][tourn_sanction + ":" + tournament_name] = tournament
                    tournament_id += 1

                    # print("TOURNAMENT INFO: " + tournament_name + tournament_city + tournament_state + tournament_or_game_start_date)
                else:
                    bracket_division = tr.find_element_by_css_selector("td > a").get_attribute('href')
        except Exception:
            pass

    #upcoming tournaments
        
    driver.execute_script("window.history.go(-1)")
    return 0

def getTeamInfo(teams_db):
    teams = driver.find_elements_by_class_name("tmpaid")
    teams_length = len(teams)
    count = 0
    print(teams_length)

    for i in range(teams_length):
        # if count == 5:
        #     break
        team = driver.find_elements_by_class_name("tmpaid").pop(i)
        team_name = team.find_element_by_tag_name("a").text.strip()
        tournaments_link = team.find_element_by_tag_name("a")
        tds = team.find_elements_by_tag_name("td")
        team_city = tds.pop(1).text.strip()
        team_state = tds.pop(1).text.strip()
        team_age = tds.pop(1).text.strip()
        team_class = tds.pop(1).text.strip()
        team_points = tds.pop(1).text.strip()
        tourn_sanction = "FASA"

        createTeam(team_name, team_city, team_state, team_age, team_class, team_points, tourn_sanction, teams_db)
        getTournamentsAndGamesPage(tournaments_link, team_name, team_age, tourn_sanction, teams_db)
        count+=1

def writeGames(games, row, db):

    column = 0
    for game in games:
        
        game = games[game]
        for info in game:
            if column == 8:
                column +=3
            db.write(row, column, game[info])
            column += 1

        column = 0
        row += 1

    return (row)


def writeTournaments(team_name, team_age, tournaments, row, db):

    column = 0
    for t in tournaments:
        
        t = tournaments[t]

        for info in t:
            if column == 2:
                db.write(row, column, team_age)
                column += 1
                db.write(row, column, team_name)
                column += 3
            elif column == 7:
                column += 1
            elif column == 9:
                column += 2
            db.write(row, column, t[info])
            column += 1

        column = 0
        row += 1

    return (row)

def WriteUpTournaments(team_name, team_age, up_tournaments, row, db):
    
    column = 0
    for t in up_tournaments:
        
        t = up_tournaments[t]

        for info in t:
            if column == 2:
                db.write(row, column, team_age)
                column += 1
                db.write(row, column, team_name)
                column += 3
            elif column == 7:
                column += 4
            db.write(row, column, t[info])
            column += 1

        column = 0
        row += 1

    return (row)

def writeToExcel(teams_db):
    
    wb = Workbook()
    db = wb.add_sheet('DB Sheet 1')

    #headers
    db.write(0, 0, 'Game ID')
    db.write(0, 1, 'Tournament Start Date / Game Date')
    db.write(0, 2, 'Team Age')
    db.write(0, 3, 'Team Name')
    db.write(0, 4, 'Score')
    db.write(0, 5, 'Result')
    db.write(0, 6, 'Tournament Sanction')
    db.write(0, 7, 'Bracket Division')
    db.write(0, 8, 'Tournament Placement')
    db.write(0, 9, 'Notes')
    db.write(0, 10, 'Coach Name')
    db.write(0, 11, 'Tournament Name')
    db.write(0, 12, 'Tournament City, State')
    db.write(0, 13, 'Tournament Director')
    db.write(0, 14, 'Season')

    #games
    row = 1
    column = 0

    for team in teams_db:

        games = teams_db[team]['games']
        tournaments = teams_db[team]['tournaments']
        up_tournaments = teams_db[team]['upcoming_tournaments']
        team_name = teams_db[team]['team_name']
        team_age = teams_db[team]['team_age']

        (row) = writeGames(games, row, db)
        (row) = writeTournaments(team_name, team_age, tournaments, row, db)
        (row) = WriteUpTournaments(team_name, team_age, up_tournaments, row, db)
    
    
    wb.save('xlwt db.xls')

driver = launchBrowser()

teams_db = {}
games_played = []
tournaments_played = {}
getTeamInfo(teams_db)

driver.quit()

writeToExcel(teams_db)