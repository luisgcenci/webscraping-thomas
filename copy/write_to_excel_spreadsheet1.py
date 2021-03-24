import json
import xlwt
from xlwt import Workbook

data = {}

with open('fasa_usfa_usssa_data.json', 'r') as file:
    data = json.load(file)

def write_games(tournaments, row, db, team_age, usssa_class):
    
    column = 0
    for sanction in tournaments:
        
        all_games = tournaments[sanction]['games']
        for g in all_games:
            g = all_games[g]
            
            for info in g:
                if column == 6:
                    if g['tournament_santion'] == 'FASA':
                        db.write(row,column,xlwt.Formula('HYPERLINK("{}","{}")'.format(g[info], team_age)))
                    elif g['tournament_santion'] == 'USSSA':
                        usssa_class = usssa_class.replace('Fast-Pitch Girls', '')
                        db.write(row,column,xlwt.Formula('HYPERLINK("{}","{}")'.format(g[info], usssa_class)))
                    column += 3
                    continue
                db.write(row, column, g[info])
                column += 1
                continue
            column = 0
            row += 1

    return (row)


def write_tournaments(team_name, team_age, tournaments, row, tournament_id, team_coach, db):

    column = 0
    for sanction in tournaments:
        
        all_tournaments = tournaments[sanction]['tournaments']
        for t in all_tournaments:
            
            t = all_tournaments[t]
            t['t_id'] = tournament_id
            tournament_id += 1
            
            for info in t:
                if column == 2:
                    db.write(row, column, team_age)
                    column += 1
                    db.write(row, column, team_name)
                    column += 2
                elif column == 6:
                    column += 1
                elif column == 8:
                    column += 1
                    db.write(row, column, t[info])
                    column += 1
                db.write(row, column, t[info])
                column += 1

            column = 0
            row += 1

    return (row, tournament_id)

def write_up_tournaments(team_name, team_age, up_tournaments, row, tournament_id, team_coach, db):
    
    column = 0
    for sanction in up_tournaments:
        
        tournaments = up_tournaments[sanction]['upcoming_tournaments']
        for t in tournaments:
            
            t = tournaments[t]
            t['t_id'] = tournament_id
            tournament_id += 1
            
            for info in t:
                
                if column == 2:
                    db.write(row, column, team_age)
                    column += 1
                    db.write(row, column, team_name)
                    column += 2
                elif column == 6:
                    column += 3
                    db.write(row, column, t[info])
                    column += 1
                db.write(row, column, t[info])
                column += 1

            column = 0
            row += 1

    return (row, tournament_id)

def write_to_excel_spreadsheet(teams_db):
    
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

    #games
    row = 1
    column = 0  
    tournament_id = 1607

    for team in teams_db:

        tournaments = teams_db[team]['tournaments']
        up_tournaments = teams_db[team]['tournaments']
        team_name = teams_db[team]['team_name']
        team_age = teams_db[team]['team_age']
        team_coach = teams_db[team]['team_coach']
        usssa_class = ""

        if 'usssa_class' in data[team].keys():
            usssa_class = data[team]['usssa_class']
        else:
            usssa_class = ""

        (row) = write_games(tournaments, row, db, team_age, team_coach, usssa_class)
        (row, tournament_id) = write_up_tournaments(team_name, team_age, up_tournaments, row, tournament_id, team_coach, db)
        (row, tournament_id) = write_tournaments(team_name, team_age, tournaments, row, tournament_id, team_coach, db)
        
    
    wb.save('./data_out/spreadsheet1.xls')

write_to_excel_spreadsheet(data)