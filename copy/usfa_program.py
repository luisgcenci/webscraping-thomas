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
    driver.get("https://baseball.sincsports.com/TTFilterEvents.aspx?tid=USFALA&tab=2&sub=1&stid=USFALA")
    return driver


def create_usfa_team(team_name, team_age, team_state, teams_db,  usfa_db):
    usfa_db[team_name] = {
    'team_name': team_name, 
    'team_city': "", 
    'team_state': team_state, 
    'team_age': team_age, 
    'team_class':"", 
    'team_points': "", 
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

def createTeam(team_name, team_age, team_state, teams_db,  usfa_db):
    
    teams_db[team_name] = {
        'team_name': team_name, 
        'team_city': "", 
        'team_state': team_state, 
        'team_age': team_age, 
        'team_class':"", 
        'team_points': "", 
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

def getTeamInfo(teams_db,  usfa_db):
    
    tournaments = driver.find_elements_by_class_name('event_top')

    tournaments_length = len(tournaments)
    print(tournaments_length)
    count = 0

    # print(tournaments_length)

    for i in range(tournaments_length):
        print(count)
        tourn = driver.find_elements_by_class_name("event_top").pop(i)
        tourn_date = tourn.find_element_by_css_selector("div > .eventdate").text.strip()
        tourn_name = tourn.find_element_by_css_selector("div > .eventname").text.strip()
        
        tourn_loc = tourn.find_element_by_css_selector("div > .r8 > div > table > tbody > tr")
        tourn_loc = tourn_loc.find_elements_by_tag_name("td").pop(1).text.strip()

        tourn_dir = tourn.find_elements_by_css_selector("div > .r8 > div > table > tbody").pop(1)
        
        try:
            tourn_dir = tourn_dir.find_elements_by_css_selector("tr > td > div").pop(1).text.strip()
        except Exception:
            tourn_dir = ""
            pass

        tourn_san = "USFA"

        tourn_button = tourn.find_element_by_class_name("eventbtn > a")
        tourn_button.click()

        team_name = ""
        team_age = ""
        tournament_id = 0

        time.sleep(1)
        
        display = driver.find_element_by_id("ctl00_ContentPlaceHolder1_DialogTeams_bdt")
        teams = display.find_elements_by_css_selector("tbody > tr > td > div > div > table > tbody > tr")
        
        for i in range(2, len(teams)):
            team = teams[i]
            team = team.find_elements_by_tag_name("td")
            team_name = team.pop(0).text.strip()
            team_age = team.pop(0).text.strip()
            team_state = team.pop(1).text.strip()

            tournament = {
                't_id': "", 't_start_date': tourn_date, "t_sanction": tourn_san,
                't_name': tourn_name, 't_location': tourn_loc, "t_director": tourn_dir
            }

            if team_name in teams_db.keys():
                pass
            else:
                createTeam(team_name, team_age, team_state, teams_db, usfa_db)
            
            if team_name in usfa_db.keys():
                pass
            else:
                create_usfa_team(team_name, team_age, team_state, teams_db, usfa_db)
            
            teams_db[team_name]['tournaments'][tourn_san]['upcoming_tournaments'][tourn_name] = tournament
            usfa_db[team_name]['tournaments'][tourn_san]['upcoming_tournaments'][tourn_name] = tournament

        
        close_buttom = display.find_element_by_id("ctl00_ContentPlaceHolder1_DialogTeams_close")
        close_buttom.click()
        
        time.sleep(1)

        count+=1


driver = launchBrowser()

teams_db = {}
usfa_db = {}

with open('./data_out/n_fasa_data.json', 'r') as fd:
    teams_db = json.load(fd)

fd.close()
getTeamInfo(teams_db,  usfa_db)

with open('./data_out/fasa_usfa_data.json', 'w') as fud:
    json.dump(teams_db, fud)

fud.close()

with open('./data_out/usfa_data.json', 'w') as ud:
    json.dump(usfa_db, ud)

ud.close()

driver.quit()