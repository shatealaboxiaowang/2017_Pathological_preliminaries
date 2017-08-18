# -*- coding: utf-8 -*-
import re


def get_info_player(file_name):
    '''
    Get the player_name/player_ID
    :parameter
        file_name(str): real path of team's .txt file
    :return
        team's id and name (team = player)
    '''
    player_result_file_split = re.split('\\\\', file_name)
    player_result_file_split = player_result_file_split[-1]
    player_result_file_split = re.split('_|\.', player_result_file_split)
    player_id = player_result_file_split[0]
    player_name =player_result_file_split[1]
    return player_id, player_name


def txt_to_dict(txt_file):
    '''
    Read file，and convert the content in file to dict
    :parameter
        txt_file(type:str)
    '''
    with open(txt_file, 'rb') as f:
        content = f.read()
        content = content.decode('utf-8')
    f.close()
    # ------If content is null------
    if content.strip() == '':
        return('Null')
    # ------If content is not null------
    else:
        lines = content.split('\n')
        lines_split_all = [re.split('\t', v) for v in lines]
        lines_split = []
        for i in lines_split_all:
            if len(i) == 2:
                lines_split.append(i)
        qp_names = [v[0] for v in lines_split]
        qp_results = [v[1] for v in lines_split]
        standard_result_dict = dict(zip(qp_names, qp_results))
        return(standard_result_dict)


def comput_score(TP, FP, FN):
    '''
    Get the score of team
    :parameter
        TP(int)：True Positive，To be classified as belonging to cancer area, but classified correctly；
        FP(int)：False Positive，To be classified as belonging to cancer area, but classified incorrectly；
        FN(int)：False Negative，To be classified as belonging to non-cancer area, but classified incorrectly.
    :returns
        precision, recall, score
    '''
    # =============================================python3.5========================================
    # ------If TP and FP are zero------
    try:
        precision = round((abs(TP)) / (abs(TP) + abs(FP)), 4)
    except:
        precision = 0.0
        print('The player\'s file name would be wrong!!!')
    # ------If TP and FN are zero------
    try:
        recall = round((abs(TP)) / (abs(TP) + abs(FN)), 4)
    except:
        recall = 0.0
    # ------If precision and recall are zero------
    try:
        score = (2 * precision * recall) / (precision + recall)
        score = round(score, 2)
    except:
        score = 0.00
    return precision, recall, score

    # # ===========================================python2.7==========================================
    # # ------If TP and FP are zero------
    # if TP == 0 and FP == 0:
    #     precision = 0.0
    # else:
    #     precision = round((abs(TP)) / (abs(TP) + abs(FP)), 4)
    # # ------If TP and FN are zero------
    # if TP == 0 and FN == 0:
    #     recall = 0.0
    # else:
    #     recall = round((abs(TP)) / (abs(TP) + abs(FN)), 4)
    # # ------If precision and recall are zero------
    # if precision == 0 and recall == 0:
    #     score = 0.00
    # else:
    #     score = (2 * precision * recall) / (precision + recall)
    #     score = round(score, 2)
    # return precision, recall, score


def check_result(standard_result, player_reault):
    '''
     Check the player\'s answer according to standard results
     :parameter
        standard_result(dict): real path of standard result
        player_result(dict): real path of player result
     :returns
        TP、FP、FN
    '''
    num_TP = 0
    num_FP = 0
    num_FN = 0
    for i in player_reault:
        if i in standard_result:
            if player_reault[i] == standard_result[i] and player_reault[i] == 'P':
                num_TP = num_TP + 1
            elif standard_result[i] == 'N' and player_reault[i] == 'P':
                num_FP = num_FP + 1
            elif player_reault[i] == 'N' and standard_result[i] == 'P':
                num_FN = num_FN + 1
    return num_TP, num_FP, num_FN


def save_info(all_team_info, save_path):
    '''
    Saving all information of all teams
    :parameter
        all_team_info(list): information of all teams
        save_path(str): saving path
    '''
    for i in all_team_info:
        with open(save_path, 'a') as f:
            f.write('\n%-10s %-10s %-10.2f'%(i[0], i[1], i[2]))
        f.close()