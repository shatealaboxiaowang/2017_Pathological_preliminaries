# -*- coding: utf-8 -*-
import re
import os
from fun import *
import argparse

# ------命令行输入参数------
# parser = argparse.ArgumentParser()
# parser.add_argument('--save_file')
# parser.add_argument('--player_file')
# args = parser.parse_args()
# standard_result_file = args.std_file
# save_file = args.save_file
# player_result_file = args.player_file

# ------The path of standard results------
path1 = 'D:\\Huaat_works\\2017_Pathological_preliminaries\\'
# ------The path of all results submitted by players------
path2 = 'D:\\Huaat_works\\2017_Pathological_preliminaries\\data5'
# ------The saving path------
path3 = 'D:\\Huaat_works\\2017_Pathological_preliminaries\\results\\'
# ------The yesterday file path------
path4 = 'D:\\Huaat_works\\2017_Pathological_preliminaries\\yesterday_files.txt'

# ------The file real path of standard results------
STANDARD_RESULT_FILE = path1 + 'standard_result.txt'

# ------Get yesterday's files------
with open(path4, 'r') as f:
    content = f.readlines()
f.close()
yesterday_all_day_list = []

for i in content:
    j = i.replace('\n', '')
    yesterday_all_day_list.append(j)
yesterday_all_day_files = '  '.join(yesterday_all_day_list)
print('The number of files submitted until yesterday is %d, respectively are: %s'%(len(yesterday_all_day_list), yesterday_all_day_files))
print('Today is the %dth day'%(len(yesterday_all_day_list)+1))

# ------Get current day's files------
current_all_day_file = os.listdir(path2)
current_all_day_files = '  '.join(current_all_day_file)
print('The number of files submitted until today is %d, respectively are: %s'%(len(current_all_day_file), current_all_day_files))

# ------Get new submitted file------
new_date_path = ''
new_date = ''
for i in current_all_day_file:
    if i not in yesterday_all_day_list:
        new_date = i
        new_date_path = os.path.join(path2, i)
        print('today\'s file submitted is: ' + i)
        # ------Write today\'s file submitted to history
        with open(path4, 'a') as f:
            f.write(i + '\n')
        f.close()
print('new data path is: ' + new_date_path)

# ------Get all teams today------
teams_list = os.listdir(new_date_path)

# ------Convert .txt standard result to dict form------
standard_result_dict = txt_to_dict(STANDARD_RESULT_FILE)

# ------Set the saving path and head, different file every day------
save_path = path3 + new_date + '.txt'
print('Saving path is: ' + save_path)
if not os.path.exists(save_path):
    f = open(save_path, 'w')
    f.write('%-10s %-10s %-10s'%('Team_id', 'Team_name', 'score'))
    f.close()

# ------Compute every team's score and save------
team_info_list = []
score_list = []
for i in teams_list:
    team_path = os.path.join(new_date_path, i)
    team_result_list = os.listdir(team_path)
    team_result_file = os.path.join(team_path, team_result_list[0])
    team_id, team_name = get_info_player(team_result_file)
    print(team_name + '\'s .txt file result is: ' + team_result_file)
    print('team\'s id is: %s     team\'s name is: %s'%(team_id, team_name))
    player_result_dict = txt_to_dict(team_result_file) # Get player's result in dict format
    # ------If content submitted by player is null------
    if player_result_dict == 'Null':
        score = 0.00
        print('Content submitted by ' + team_name + ' is empty')
    else:
        # ------Get the number of TP FP FN------
        num_TP, num_FP, num_FN = check_result(standard_result_dict, player_result_dict)
        print('True positive has：%d，false positive has：%d，false negative has：%d'%(num_TP, num_FP, num_FN))
        # ------Computing the player's score------
        precision, recall, score = comput_score(num_TP, num_FP, num_FN)
        print('%s\'s grade is: precision is %.2f，recall is %.2f，F1 score is %.2f'%(team_name, precision, recall, score))
    # ------one team's information------
    one_team_info_list = [team_id, team_name, score]
    team_info_list.append(one_team_info_list)
    score_list.append(score)

# ------sorting according score for all teams and add to sort_info_list------
sort_info_list = []
sort_score_list = sorted(score_list, reverse = True)
for i in sort_score_list:
    for j in team_info_list:
        if i == j[2]:
            sort_info_list.append(j)

# ------saving the information of all teams------
save_info(sort_info_list, save_path)

