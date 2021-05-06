import json
import xlwt
import time
from xlwt import Workbook

def write_games(fasa_coaches, tournaments, row, db, team_name, team_age, team_coach, teams_db):
    
    for sanction in tournaments:
        
        all_games = tournaments[sanction]['games']
        for g in all_games:

            g = all_games[g]

            if team_name != g['team_name']:
                team_coach = ""
                for t in teams_db:
                    if g['team_name'] == teams_db[t]['team_name']:
                        team_coach = teams_db[t]['team_coach']
                        break;                  

            if sanction == 'FASA':
                team_coach = ""
                for t in fasa_coaches:
                    if g['team_name'] == t:
                        team_coach = fasa_coaches[t]
                        break;                  

            db.write(row, 0, g['game_id'])
            db.write(row, 1, g['game_date'])
            db.write(row, 2, team_age)
            db.write(row, 3, g['team_name'])
            db.write(row, 4, g['score'])
            db.write(row, 5, g['tournament_santion'])
            db.write(row, 6, xlwt.Formula('HYPERLINK("{}","{}")'.format(g['bracket_divison'],team_age)))
            db.write(row, 7, "")
            db.write(row, 8, "")
            db.write(row, 9, team_coach)
            db.write(row, 10, g['tournament_name'])
            db.write(row, 11, g['tournament_location'])
            db.write(row, 12, "")
            db.write(row, 13, 2021)

            row += 1

    return (row)


def write_tournaments(fasa_coaches, team_name, team_age, tournaments, row, tournament_id, team_coach, db, teams_db):

    for sanction in tournaments:
        
        all_tournaments = tournaments[sanction]['tournaments']
        for t in all_tournaments:
            
            t = all_tournaments[t]
            t['t_id'] = tournament_id
            tournament_id += 1

            if sanction == 'FASA':
                    team_coach = ""
                    for tm in fasa_coaches:
                        if team_name == tm:
                            team_coach = fasa_coaches[tm]
                            break;

            db.write(row, 0, t['t_id'])
            db.write(row, 1, t['t_start_date'])
            db.write(row, 2, team_age)
            db.write(row, 3, team_name)
            db.write(row, 4, "")
            db.write(row, 5, t['t_sanction'])
            db.write(row, 6, "")
            db.write(row, 7, t['t_placement'])
            db.write(row, 8, "")
            db.write(row, 9, team_coach)
            db.write(row, 10, t['t_name'])
            db.write(row, 11, t['t_location'])
            db.write(row, 12, t['t_director'])
            db.write(row, 13, 2021)

            row += 1

    return (row, tournament_id, team_coach)

def write_up_tournaments(fasa_coaches, team_name, team_age, up_tournaments, row, tournament_id, team_coach, db, teams_db):
    
    column = 0
    for sanction in up_tournaments:
        
        tournaments = up_tournaments[sanction]['upcoming_tournaments']
        for t in tournaments:
            
            t = tournaments[t]
            t['t_id'] = tournament_id
            tournament_id += 1

            if sanction == 'FASA':
                    team_coach = ""
                    for tm in fasa_coaches:
                        if team_name == tm:
                            team_coach = fasa_coaches[tm]
                            break;
    
            db.write(row, 0, t['t_id'])
            db.write(row, 1, t['t_start_date'])
            db.write(row, 2, team_age)
            db.write(row, 3, team_name)
            db.write(row, 4, "")
            db.write(row, 5, t['t_sanction'])
            db.write(row, 6, "")
            db.write(row, 7, "")
            db.write(row, 8, "")
            db.write(row, 9, team_coach)
            db.write(row, 10, t['t_name'])
            db.write(row, 11, t['t_location'])
            db.write(row, 12, t['t_director'])
            db.write(row, 13, 2021)

            row += 1

    return (row, tournament_id, team_coach)

def write_to_excel_spreadsheet(teams_db, fasa_coaches):
    
    wb = Workbook()
    db = wb.add_sheet('DB Sheet 1')

    #headers
    db.write(0, 0, 'Game ID')
    db.write(0, 1, 'Tournament Start Date / Game Date')
    db.write(0, 2, 'Team Age')
    db.write(0, 3, 'Team Name')
    db.write(0, 4, 'Score')
    db.write(0, 5, 'Tournament Sanction')
    db.write(0, 6, 'Bracket Division')
    db.write(0, 7, 'Tournament Placement')
    db.write(0, 8, 'Notes')
    db.write(0, 9, 'Coach Name')
    db.write(0, 10, 'Tournament Name')
    db.write(0, 11, 'Tournament City, State')
    db.write(0, 12, 'Tournament Director')
    db.write(0, 13, 'Season')

    row = 1
    column = 0  
    tournament_id = 2000

    for team in teams_db:

        tournaments = teams_db[team]['tournaments']
        up_tournaments = teams_db[team]['tournaments']
        team_name = teams_db[team]['team_name']
        team_age = teams_db[team]['team_age']
        team_coach = teams_db[team]['team_coach']

        (row) = write_games(fasa_coaches, tournaments, row, db, team_name, team_age, team_coach, teams_db)
        (row, tournament_id, team_coach) = write_up_tournaments(fasa_coaches, team_name, team_age, up_tournaments, row, tournament_id, team_coach, db, teams_db)
        (row, tournament_id, team_coach) = write_tournaments(fasa_coaches, team_name, team_age, tournaments, row, tournament_id, team_coach, db, teams_db)

        teams_db[team]['team_coach'] = team_coach
        
    print("saving spreadsheet1...");

    wb.save('./data_out/spreadsheet1.xls')

    print("spreadsheet1 saved!")

data = {}

with open('./data_out/fixed_fasa_usfa_usssa_data.json', 'r') as file:
    data = json.load(file)

fasa_coaches = {}

file.close()

with open('./data_given/fasa_coaches.json', 'r') as file2:
    fasa_coaches = json.load(file2)

write_to_excel_spreadsheet(data, fasa_coaches)

file2.close()

with open('./data_out/fixed2_fasa_usfa_usssa_data.json', 'w') as file3:
    json.dump(data, file3)

file3.close()