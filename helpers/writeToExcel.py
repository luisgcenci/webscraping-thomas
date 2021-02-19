import json
import xlwt
from xlwt import Workbook

data = {}
# usssa_data = {}

with open('n_fasa_usfa_usssa_data.json', 'r') as fasa_and_usfa:
    data = json.load(fasa_and_usfa)

# with open('usssa_data.json', 'r') as usssa:
#     usssa_data = json.load(usssa)

# def write_games(tournaments, row, db):
    
#     column = 0
#     for sanction in tournaments:
        
#         all_games = tournaments[sanction]['games']
#         for g in all_games:
#             g = all_games[g]
            
#             for info in g:
#                 if column == 7:
#                     column +=3
#                 db.write(row, column, g[info])
#                 column += 1

#             column = 0
#             row += 1

#     return (row)


# def write_tournaments(team_name, team_age, tournaments, row, tournament_id, db):

#     column = 0
#     for sanction in tournaments:
        
#         all_tournaments = tournaments[sanction]['tournaments']
#         for t in all_tournaments:
            
#             t = all_tournaments[t]
#             t['t_id'] = tournament_id
#             tournament_id += 1
            
#             for info in t:
#                 if column == 2:
#                     db.write(row, column, team_age)
#                     column += 1
#                     db.write(row, column, team_name)
#                     column += 2
#                 elif column == 6:
#                     column += 1
#                 elif column == 8:
#                     column += 2
#                 db.write(row, column, t[info])
#                 column += 1

#             column = 0
#             row += 1

#     return (row, tournament_id)

# def write_up_tournaments(team_name, team_age, up_tournaments, row, tournament_id, db):
    
#     column = 0
#     for sanction in up_tournaments:
        
#         tournaments = up_tournaments[sanction]['upcoming_tournaments']
#         for t in tournaments:
            
#             t = tournaments[t]
#             t['t_id'] = tournament_id
#             tournament_id += 1
            
#             for info in t:
                
#                 if column == 2:
#                     db.write(row, column, team_age)
#                     column += 1
#                     db.write(row, column, team_name)
#                     column += 2
#                 elif column == 6:
#                     column += 4
#                 db.write(row, column, t[info])
#                 column += 1

#             column = 0
#             row += 1

#     return (row, tournament_id)

# def write_to_excel_spreadsheet1(teams_db):
    
#     wb = Workbook()
#     db = wb.add_sheet('DB Sheet 1')

#     #headers
#     db.write(0, 0, 'Game ID')
#     db.write(0, 1, 'Tournament Start Date / Game Date')
#     db.write(0, 2, 'Team Age')
#     db.write(0, 3, 'Team Name')
#     db.write(0, 4, 'Score')
#     db.write(0, 5, 'Tournament Sanction')
#     db.write(0, 6, 'Bracket Division')
#     db.write(0, 7, 'Tournament Placement')
#     db.write(0, 8, 'Notes')
#     db.write(0, 9, 'Coach Name')
#     db.write(0, 10, 'Tournament Name')
#     db.write(0, 11, 'Tournament City, State')
#     db.write(0, 12, 'Tournament Director')
#     db.write(0, 13, 'Season')

#     #games
#     row = 1
#     column = 0  
#     tournament_id = 1607

#     for team in teams_db:


#         tournaments = teams_db[team]['tournaments']
#         up_tournaments = teams_db[team]['tournaments']
#         team_name = teams_db[team]['team_name']
#         team_age = teams_db[team]['team_age']

#         (row) = write_games(tournaments, row, db)
#         (row, tournament_id) = write_up_tournaments(team_name, team_age, up_tournaments, row, tournament_id, db)
#         (row, tournament_id) = write_tournaments(team_name, team_age, tournaments, row, tournament_id, db)
        
    
#     wb.save('spreadsheet-part2.xls')

def write_to_excel_spreadsheet2(fasa_and_usfa_data):
    
    wb = Workbook()
    db = wb.add_sheet('DB Sheet 2')

    #headers
    db.write(0, 0, 'Team #ID')
    db.write(0, 1, 'Team Name')
    db.write(0, 2, 'Team Age')

    #fasa
    db.write(0, 3, 'Class')
    db.write(0, 4, 'Record W-L-T')
    db.write(0, 5, '#Tournaments Played')
    db.write(0, 6, 'Tournaments Registered')

    #usssa
    db.write(0, 7, 'Class')
    db.write(0, 8, 'Record W-L-T')
    db.write(0, 9, '#Tournaments Played')
    db.write(0, 10, 'Tournaments Registered')

    #usfa
    db.write(0, 11, 'Class')
    db.write(0, 12, 'Record W-L-T')
    db.write(0, 13, '#Tournaments Played')
    db.write(0, 14, '#Future Tournaments Registered')

    #main headers
    db.write(0, 15, 'Coach Name')
    db.write(0, 16, 'Team City')
    db.write(0, 17, 'Team State')
    db.write(0, 18, 'Distance From Gator')
    db.write(0, 19, 'Roster Link')
    db.write(0, 20, 'Notes')

    #games
    row = 1
    column = 0  
    team_id = 1

    for team in data:
            
        up_tournaments = data[team]['tournaments']
        up_tournaments = data[team]['tournaments']
        team_name = data[team]['team_name']
        team_age = data[team]['team_age']
        team_city = data[team]['team_city']
        team_state = data[team]['team_state']
        
        #FASA
        fasa_games = data[team]['tournaments']['FASA']['games']
        fasa_w = 0
        fasa_l = 0
        fasa_t = 0
        fasa_record_w_l_t = ""
        fasa_class = data[team]['team_class']

        for g in fasa_games:
            if 'W' in fasa_games[g]['game_id']:
                fasa_w += 1
            elif 'L' in fasa_games[g]['game_id']:
                fasa_l += 1
            elif 'T' in fasa_games[g]['game_id']:
                fasa_t += 1

        fasa_tournaments_played = len(data[team]['tournaments']['FASA']['tournaments'])
        fasa_tournaments_registered = len(data[team]['tournaments']['FASA']['upcoming_tournaments'])

        #USSSA
        usssa_games = data[team]['tournaments']['USSSA']['games']
        usssa_w = 0
        usssa_l = 0
        usssa_t = 0
        usssa_record_w_l_t = ""
        for g in usssa_games:
            if 'W' in usssa_games[g]['game_id']:
                usssa_w += 1
            elif 'L' in usssa_games[g]['game_id']:
                usssa_l += 1
            elif 'T' in usssa_games[g]['game_id']:
                usssa_t += 1

        usssa_tournaments_played = len(data[team]['tournaments']['USSSA']['tournaments'])
        usssa_tournaments_registered = len(data[team]['tournaments']['USSSA']['upcoming_tournaments'])

        if 'usssa_class' in data[team].keys():
            usssa_class = data[team]['usssa_class']
        else:
            usssa_class = ""
        
        #USFA
        usfa_games = data[team]['tournaments']['USFA']['games']
        usfa_w = 0
        usfa_l = 0
        usfa_t = 0
        usfa_record_w_l_t = ""
        for g in usfa_games:
            if 'W' in usfa_games[g]['game_id']:
                usfa_w += 1
            elif 'L' in usfa_games[g]['game_id']:
                usfa_l += 1
            elif 'T' in usfa_games[g]['game_id']:
                usfa_t += 1

        usfa_tournaments_played = len(data[team]['tournaments']['USFA']['tournaments'])
        usfa_tournaments_registered = len(data[team]['tournaments']['USFA']['upcoming_tournaments'])

        #start writting to spreadsheet
        db.write(row, 0, team_id)
        db.write(row, 1, team_name)
        db.write(row, 2, team_age)

        #fasa
        db.write(row, 3, fasa_class)
        db.write(row, 4, '{}W-{}L-{}T'.format(fasa_w, fasa_l, fasa_t))
        db.write(row, 5, fasa_tournaments_played)
        db.write(row, 6, fasa_tournaments_registered)

        #usssa
        db.write(row, 7, usssa_class)
        db.write(row, 8, '{}W-{}L-{}T'.format(usssa_w, usssa_l, usssa_t))
        db.write(row, 9, usssa_tournaments_played)
        db.write(row, 10, usssa_tournaments_registered)

        #usfa
        db.write(row, 11, "")
        db.write(row, 12, '{}W-{}L-{}T'.format(usfa_w, usfa_l, usfa_t))
        db.write(row, 13, usfa_tournaments_played)
        db.write(row, 14, usfa_tournaments_registered)


        db.write(row, 15, 'Coach Name')
        db.write(row, 16, team_city)
        db.write(row, 17, team_state)
        db.write(row, 18, '')
        db.write(row, 19, '')
        db.write(row, 20, '')

        team_id += 1
        row += 1
            
    
    wb.save('spreadsheet2.xls')

write_to_excel_spreadsheet2(data)