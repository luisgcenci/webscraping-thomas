from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import json
import xlwt
from xlwt import Workbook

PATH = "./chromedriver.exe"

def launchBrowser():
    driver = webdriver.Chrome(PATH)
    driver.get("http://playfasa.com/points.asp")
    return driver

def createTeam(team_name, team_city, team_state, team_age, team_class, team_points, tourn_sanction, teams_db):
    teams_db[team_name] = {
        'team_name': team_name, 
        'team_city': team_city, 
        'team_state': team_state, 
        'team_age': team_age, 
        'team_class':team_class, 
        'team_points': team_points, 
        'tournaments': 
        {
            'FASA': 
            { 
                'tournaments': {}, 
                'games': {},
                'upcoming_tournaments': {}
            }, 
            'USSSA': 
            { 
                'tournaments': {}, 
                'games': {},
                'upcoming_tournaments': {}
            }, 
            'USFA': 
            { 
                'tournaments': {}, 
                'games': {},
                'upcoming_tournaments': {}
            }
        }
    }

def getScoreAndResult(team_name, team_1, team_1_score, team_2, team_2_score):
    
    team_1_result = ""
    team_2_result = ""

    if team_1_score == None or team_2_score == None or team_1_score == team_2_score:
        team_1_result = "T"
        team_2_result = "T"
    
    elif team_1_score > team_2_score:
        team_1_result = "W"
        team_2_result = "L"
    
    elif team_1_score < team_2_score:
        team_1_result = "L"
        team_2_result = "W"
    
    return (team_1_result, team_2_result)

def createGames(game_id, game_date, team_age, team_name, 
    bracket_division, tournament_name, tournament_city, tournament_state, 
    tourn_sanction, team_1, team_2, team_1_score, team_2_score, teams_db):
    
    (team_1_result, team_2_result) = getScoreAndResult(team_name, team_1, team_1_score, team_2, team_2_score)
    team_age_1 = ""
    team_age_2 = ""

    if team_name == team_1:
        team_age_1 = team_age
    else:
        team_age_2 = team_age

    if game_id == 400:
        print (teams_db)
    game_1 = {
        "game_id" : str(game_id) + team_1_result, "game_date":game_date, "team_age": team_age_1, 
        "team_name": team_1, "score": team_1_score, "tournament_santion": "FASA", 
        "bracket_divison": bracket_division, "tournament_name": tournament_name,
        "tournament_location": tournament_city + "," + tournament_state,
    }

    game_2 = {
        "game_id" : str(game_id) + team_2_result, "game_date":game_date, "team_age": team_age_2, 
        "team_name": team_2, "score": team_2_score, "tournament_santion": "FASA", 
        "bracket_divison": bracket_division, "tournament_name": tournament_name,
        "tournament_location": tournament_city + "," + tournament_state,
    }

    teams_db[team_name]['tournaments'][tourn_sanction]['games'][str(game_id) + team_1_result] = game_1
    teams_db[team_name]['tournaments'][tourn_sanction]['games'][str(game_id) + team_2_result] = game_2
    

def getTournamentsAndGamesPage(tournaments_link, team_name, team_age, tourn_sanction, game_id, teams_db):

    tournaments_link.click()
    
    tournaments_body = driver.find_elements_by_tag_name("tbody").pop(7)
    all_trs = tournaments_body.find_elements_by_tag_name("tr")

    tournament_name = ""
    tournament_city = ""
    tournament_state = ""
    tournament_date = ""
    bracket_division = ""
    tournament_placement = ""
    upcomingTournaments = False
    

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
                        "t_id": "", 't_start_date': t_start_date, 
                        "t_sanction": tourn_sanction, "t_name": t_name, "t_location" : t_city + ',' + t_state
                    }
                    teams_db[team_name]['tournaments'][tourn_sanction]['upcoming_tournaments'][t_name] = upcoming_tournament

                    continue

            else:
                upcomingTournaments = True
                continue
        try:
            #its a game tr
            if tr.find_element_by_tag_name("td").text == "":
                
                game_date = tr.find_element_by_tag_name("th").text.strip()
                tds = tr.find_elements_by_tag_name("td")
                
                team_1 = tds.pop(1).text.strip()
                team_1_score = tds.pop(1).text.strip()
                team_1_score = int(team_1_score) if len(team_1_score) != 0 else None

                team_2 = tds.pop(2).text.strip()
                team_2_score = tds.pop(2).text.strip()
                team_2_score = int(team_2_score) if len(team_2_score) != 0 else None
                                
                createGames(game_id, game_date, team_age, team_name, 
                bracket_division, tournament_name, tournament_city, tournament_state, 
                tourn_sanction, team_1, team_2, team_1_score, team_2_score, teams_db)
                game_id += 1
                # print("GAME INFO:" + game_id + team_1 + team_1_score + "VS" + team_2 + team_2_score)          

            else:    
                tournament_info = tr.find_elements_by_class_name("style10")
                tournament_info2 = tr.find_elements_by_tag_name("td")
                if len(tournament_info) != 0:
                    tournament_name = tournament_info.pop(0).text.strip()
                    tournament_city = tournament_info.pop(0).text.strip()
                    tournament_state = tournament_info.pop(0).text.strip()
                    tournament_date = tournament_info.pop(0).text.strip()
                    tournament_placement = tournament_info2.pop(6).text.strip()
                    tournament = {
                        't_id': "", 't_start_date': tournament_date, "t_sanction": tourn_sanction,
                        't_placement': tournament_placement, 't_name': tournament_name, 't_location': tournament_city + ',' + tournament_state,
                    }
                    teams_db[team_name]['tournaments'][tourn_sanction]['tournaments'][tournament_name] = tournament

                    # print("TOURNAMENT INFO: " + tournament_name + tournament_city + tournament_state + tournament_or_game_start_date)
                else:
                    bracket_division = tr.find_element_by_css_selector("td > a").get_attribute('href')
        except Exception as e:
            # print(e.traceback.format_exc())
            pass

    #upcoming tournaments
        
    driver.execute_script("window.history.go(-1)")
    return game_id

def getTeamInfo(teams_db):

    select = Select(driver.find_element_by_name('STATE'))
    select.select_by_value('LA')
    search_btn = driver.find_element_by_xpath("//input[@type='submit' and @value='Search']")

    time.sleep(1)

    teams = driver.find_elements_by_class_name("tmpaid")
    teams_length = len(teams)
    count = 0
    game_id = 1
    print(teams_length)

    for i in range(teams_length):
        print(count)
        print(game_id)
        select = Select(driver.find_element_by_name('STATE'))
        select.select_by_value('LA')

        time.sleep(1)
        
        search_btn = driver.find_element_by_xpath("//input[@type='submit' and @value='Search']")
        # search_team = driver.find_element_by_css_selector("table > tbody > tr > td > input")
        # search_team.send_keys("007 Brignac 10U")
        # search_btn.click()

        time.sleep(1)
        
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
        game_id = getTournamentsAndGamesPage(tournaments_link, team_name, team_age, tourn_sanction, game_id, teams_db)
        count+=1

driver = launchBrowser()

teams_db = {}
getTeamInfo(teams_db)

driver.quit()

with open('fasa_data.json', 'w') as fd:
    json.dump(teams_db, fd)

fd.close()