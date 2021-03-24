import json,time

def fix_part1(data_to_fix):
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
    
    return data_to_fix


def fix_part2(teams):
    
    print(len(teams))
    count = 0

    try:
        for team in list(teams):
            for t in list(teams[team]['tournaments']):
                for g in list(teams[team]['tournaments'][t]['games']):
                    game = teams[team]['tournaments'][t]['games'][g]
                    
                    for o_team in list(teams):
                        for o_t in list(teams[o_team]['tournaments']):
                            for o_g in list(teams[o_team]['tournaments'][o_t]['games']):
                                game_poss_dupl = teams[o_team]['tournaments'][o_t]['games'][o_g]
                                                        
                                if (game['game_date'] == game_poss_dupl['game_date'] and 
                                    game['team_age'] == game_poss_dupl['team_age'] and
                                    game['team_name'] == game_poss_dupl['team_name'] and
                                    game['score'] == game_poss_dupl['score'] and
                                    game['tournament_santion'] == game_poss_dupl['tournament_santion'] and
                                    game['bracket_divison'] == game_poss_dupl['bracket_divison'] and
                                    game['tournament_name'] == game_poss_dupl['tournament_name'] and
                                    game['tournament_location'] == game_poss_dupl['tournament_location'] and
                                    game['game_id'] != game_poss_dupl['game_id']):

                                    count += 1
                                    print(teams[o_team]['tournaments'][o_t]['games'][o_g])
                                    del teams[o_team]['tournaments'][o_t]['games'][o_g]
    except Exception as e:
        pass

    
    print("{} duplicated rows deleted.".format(count))
    return teams

remove_keys = []
data_to_fix = {}
with open ('./data_out/fasa_usfa_usssa_data.json') as data:
    data_to_fix = json.load(data)

data.close()

data_to_fix = fix_part1(data_to_fix)

data_fixed = fix_part2(data_to_fix)

with open('./data_out/fixed_fasa_usfa_usssa_data.json', 'w') as file:
    json.dump(data_fixed, file)

file.close()
