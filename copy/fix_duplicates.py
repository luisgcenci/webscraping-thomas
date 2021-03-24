import json

def fix(data_to_fix):
    count = 0
    for team in data_to_fix:
        san_t = data_to_fix[team]['tournaments']
        team_o_name = data_to_fix[team]['team_name']
        for san in san_t:
            games = san_t[san]['games']
            for g in games:
                if games[g]['team_name'] != team_o_name:
                    team_name = games[g]['team_name']
                    team_score = games[g]['score']
                    game_date = games[g]['game_date']
                    tournament_name = games[g]['tournament_name']
                    tournament_location = games[g]['tournament_location']
                    
                    for team in data_to_fix:
                        try:

                            if data_to_fix[team]['team_name'] == team_name:
                                games[g]['team_age'] = data_to_fix[team]['team_age']
                                count += 1
                        except KeyError:
                            pass 

                        else:
                            pass
    
    print(count)

remove_keys = []
data_to_fix = {}
with open ('fasa_data.json') as data:
    data_to_fix = json.load(data)

data.close()

fix(data_to_fix)

with open('./data_out/n_fasa_data.json', 'w') as file:
    json.dump(data_to_fix, file)

file.close()
