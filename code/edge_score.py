import os
import jieba
import jieba.posseg as pseg
import csv
import json
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)
jieba.set_dictionary('dict_tw.txt')
jieba.load_userdict('my.dict.txt')
brand = {'a': 'apple', 'g': 'google', 'h': 'htc', 'l': 'lg', 'm': 'mi', 'n': 'nokia',
         'o': 'oppo', 'q': 'other', 's': 'samsung', 'w': 'huawei', 'x': 'sony', 'z': 'asus'}
w_bd = {'wa': 'apple', 'wg': 'google', 'wh': 'htc', 'wl': 'lg', 'wm': 'mi', 'wn': 'nokia',
        'wo': 'oppo', 'wq': 'other', 'ws': 'samsung', 'ww': 'huawei', 'wx': 'sony', 'wz': 'asus'}

savePath = {
    'weight_max': 'result_data/weight_max/',
    'weight_average': 'result_data/weight_average/'
}

Bpath = {
    'path2': '0_experiment_data/B/2/',
    'path20': '0_experiment_data/B/20/'
}

a = pd.DataFrame(np.random.random([12, 12]), index=brand, columns=brand)
a_n = pd.DataFrame(np.random.random([12, 12]), index=brand, columns=brand)
pict = pd.DataFrame(np.random.random([12, 12]), index=brand, columns=brand)
pict_n = pd.DataFrame(np.random.random([12, 12]),
                      index=brand, columns=brand)

aa = pd.DataFrame(np.random.random([12, 12]), index=brand, columns=brand)
aa_n = pd.DataFrame(np.random.random([12, 12]), index=brand, columns=brand)
apict = pd.DataFrame(np.random.random([12, 12]), index=brand, columns=brand)
apict_n = pd.DataFrame(np.random.random([12, 12]),
                       index=brand, columns=brand)


for c in a.columns:
    for i in a.index:
        a[c][i] = 0
        a_n[c][i] = 0
        pict[c][i] = 0
        pict_n[c][i] = 0
        aa[c][i] = 0
        aa_n[c][i] = 0
        apict[c][i] = 0
        apict_n[c][i] = 0


def adj_n():
    with open('0_experiment_data/my_adj/n.csv', newline='') as ncsv:
        adj_dict = csv.reader(ncsv)
        score = {}
        for adj in adj_dict:
            try:
                score[adj[0]] = adj[1]
            except IndexError:
                continue
        return score


def adj_p():
    with open('0_experiment_data/my_adj/p.csv', newline='') as pcsv:
        adj_dict = csv.reader(pcsv)
        score = {}
        for adj in adj_dict:
            try:
                score[adj[0]] = adj[1]
            except IndexError:
                continue
        return score


def all_score():
    for f in os.listdir(Bpath['path2']):
        with open(Bpath['path2']+str(f), 'r') as fr:
            name = []
            lines = fr.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip('\n')
            for l in lines[0]:
                if l in brand:
                    name.append(l)
            for line in range(2, len(lines)):
                flag = True
                cflag = False
                b = {}
                for i in range(len(lines[line])):
                    if lines[line][i] == 'c':
                        cflag = True
                    if lines[line][i] in brand:
                        temp = lines[line][i]
                        if lines[line][i] not in b:
                            b[lines[line][i]] = 0
                        else:
                            b[lines[line][i]] += 1
                    if len(b) > 1:
                        flag = False
                        break
                if flag:
                    words = jieba.posseg.cut(lines[line])
                    if cflag is True:
                        scoreP(temp, words, name)
                    if cflag is False:
                        scoreA(temp, words, name)


def scoreA(b, jieba, name):
    n = adj_n()
    p = adj_p()

    neg = ['沒有', '沒', '不是', '不會', '不', '非', '無']
    flag_neg = 1

    count = 0
    temp_m = 0
    temp_a = 0
    for w, z in jieba:
        if w in n:
            try:
                if flag_neg == -1:
                    temp_m -= float(n[w])
                else:
                    temp_m += float(n[w])
                flag_neg = 1
                count += 1
            except KeyError:
                continue
        elif w in p:
            try:
                if flag_neg == -1:
                    temp_m -= float(p[w])
                else:
                    temp_m += float(p[w])
                flag_neg = 1
                count += 1
            except KeyError:
                continue
        else:
            flag_neg = 1

        if w in neg:
            flag_neg = -1

    temp_a = temp_m
    if count == 0:
        temp_m += 0.9  # max score
        temp_a += 0.29

    if temp_m > 0:
        for j in name:
            if j != b:
                a[b][j] += round(temp_m, 2)
    elif temp_m < 0:
        for j in name:
            if j != b:
                a_n[b][j] += abs(round(temp_m, 2))

    if temp_a > 0:
        for j in name:
            if j != b:
                aa[b][j] += round(temp_a, 2)
    elif temp_a < 0:
        for j in name:
            if j != b:
                aa_n[b][j] += abs(round(temp_a, 2))


def picture_score():
    for f in os.listdir(Bpath['path20']):
        with open(Bpath['path20']+str(f), 'r') as fr:
            name = []
            lines = fr.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip('\n')
            for l in lines[0]:
                if l in brand:
                    name.append(l)
            for line in range(2, len(lines)):
                flag = True
                b = {}
                for i in range(len(lines[line])):
                    if lines[line][i] in brand:
                        temp = lines[line][i]
                        if lines[line][i] not in b:
                            b[lines[line][i]] = 0
                        else:
                            b[lines[line][i]] += 1
                    if len(b) > 1:
                        flag = False
                        break
                if flag:
                    words = jieba.posseg.cut(lines[line])
                    scoreP(temp, words, name)


def scoreP(b, jieba, name):
    n = adj_n()
    p = adj_p()

    neg = ['沒有', '沒', '不是', '不會', '不', '非', '無']
    flag_neg = 1

    count = 0
    temp_m = 0
    temp_a = 0
    for w, z in jieba:
        if w in n:
            try:
                if flag_neg == -1:
                    temp_m -= float(n[w])
                else:
                    temp_m += float(n[w])
                flag_neg = 1
                count += 1
            except KeyError:
                flag_neg = 1
                continue
        elif w in p:
            try:
                if flag_neg == -1:
                    temp_m -= float(p[w])
                else:
                    temp_m += float(p[w])
                flag_neg = 1
                count += 1
            except KeyError:
                flag_neg = 1
                continue
        else:
            flag_neg = 1

        if w in neg:
            flag_neg = -1
    temp_a = temp_m
    if count == 0:
        temp_m += 0.9  # max score
        temp_a += 0.29

    if temp_m > 0:
        for j in name:
            if j != b:
                pict[b][j] += round(temp_m, 2)
    elif temp_m < 0:
        for j in name:
            if j != b:
                pict_n[b][j] += abs(round(temp_m, 2))

    if temp_a > 0:
        for j in name:
            if j != b:
                apict[b][j] += round(temp_a, 2)
    elif temp_a < 0:
        for j in name:
            if j != b:
                apict_n[b][j] += abs(round(temp_a, 2))


def save_to_csv():
    pict.to_csv(savePath['weight_max']+'mW_p.csv',
                float_format='%.2f')
    pict_n.to_csv(savePath['weight_max']+'mW_p_n.csv',
                  float_format='%.2f')
    a.to_csv(savePath['weight_max']+'mW_a.csv',
             float_format='%.2f')
    a_n.to_csv(savePath['weight_max']+'mW_a_n.csv',
               float_format='%.2f')

    apict.to_csv(savePath['weight_average']+'aW_p.csv',
                 float_format='%.2f')
    apict_n.to_csv(savePath['weight_average']+'aW_p_n.csv',
                   float_format='%.2f')
    aa.to_csv(savePath['weight_average']+'aW_a.csv',
              float_format='%.2f')
    aa_n.to_csv(savePath['weight_average']+'aW_a_n.csv',
                float_format='%.2f')


def div_score():
    dfp = pd.read_csv(
        savePath['weight_max']+'mW_p.csv', index_col='Unnamed: 0')
    dfpn = pd.read_csv(
        savePath['weight_max']+'mW_p_n.csv', index_col='Unnamed: 0')
    dfa = pd.read_csv(
        savePath['weight_max']+'mW_a.csv', index_col='Unnamed: 0')
    dfan = pd.read_csv(
        savePath['weight_max']+'mW_a_n.csv', index_col='Unnamed: 0')
    result = pd.DataFrame(np.random.random(
        [12, 12]), index=w_bd, columns=brand)
    result_p = pd.DataFrame(np.random.random(
        [12, 12]), index=w_bd, columns=brand)
    for i in dfa.index:
        for c in dfa.columns:
            result[c][i] = 0
            result_p[c][i] = 0
            if dfan[c][i] == 0:
                dfan[c][i] = 1
            if dfpn[c][i] == 0:
                dfpn[c][i] = 1
            result[c][i] = abs(round(dfa[c][i]/dfan[c][i], 2))
            result_p[c][i] = abs(round(dfp[c][i]/dfpn[c][i], 2))
    result.to_csv(savePath['weight_max']+'mW_div.csv')
    result_p.to_csv(savePath['weight_max']+'mW_div_p.csv')

    # weight_average
    adfp = pd.read_csv(
        savePath['weight_average']+'aW_p.csv', index_col='Unnamed: 0')
    adfpn = pd.read_csv(
        savePath['weight_average']+'aW_p_n.csv', index_col='Unnamed: 0')
    adfa = pd.read_csv(
        savePath['weight_average']+'aW_a.csv', index_col='Unnamed: 0')
    adfan = pd.read_csv(
        savePath['weight_average']+'aW_a_n.csv', index_col='Unnamed: 0')
    result = pd.DataFrame(np.random.random(
        [12, 12]), index=w_bd, columns=brand)
    result_p = pd.DataFrame(np.random.random(
        [12, 12]), index=w_bd, columns=brand)
    for i in adfa.index:
        for c in adfa.columns:
            result[c][i] = 0
            result_p[c][i] = 0
            if adfan[c][i] == 0:
                adfan[c][i] = 1
            if adfpn[c][i] == 0:
                adfpn[c][i] = 1
            result[c][i] = abs(round(adfa[c][i]/adfan[c][i], 2))
            result_p[c][i] = abs(round(adfp[c][i]/adfpn[c][i], 2))
    result.to_csv(savePath['weight_average']+'aW_div.csv')
    result_p.to_csv(savePath['weight_average']+'aW_div_p.csv')


def sub_score():
    dfp = pd.read_csv(
        savePath['weight_max']+'mW_p.csv', index_col='Unnamed: 0')
    dfpn = pd.read_csv(
        savePath['weight_max']+'mW_p_n.csv', index_col='Unnamed: 0')
    dfa = pd.read_csv(
        savePath['weight_max']+'mW_a.csv', index_col='Unnamed: 0')
    dfan = pd.read_csv(
        savePath['weight_max']+'mW_a_n.csv', index_col='Unnamed: 0')
    result = pd.DataFrame(np.random.random(
        [12, 12]), index=w_bd, columns=brand)
    result_p = pd.DataFrame(np.random.random(
        [12, 12]), index=w_bd, columns=brand)
    for i in dfa.index:
        for c in dfa.columns:
            result[c][i] = 0
            result_p[c][i] = 0
            result[c][i] = round(dfa[c][i]-dfan[c][i], 2)
            result_p[c][i] = round(dfp[c][i]-dfpn[c][i], 2)
    result.to_csv(savePath['weight_max']+'mW_sub.csv')
    result_p.to_csv(savePath['weight_max']+'mW_sub_p.csv')

    # weight_average
    adfp = pd.read_csv(
        savePath['weight_average']+'aW_p.csv', index_col='Unnamed: 0')
    adfpn = pd.read_csv(
        savePath['weight_average']+'aW_p_n.csv', index_col='Unnamed: 0')
    adfa = pd.read_csv(
        savePath['weight_average']+'aW_a.csv', index_col='Unnamed: 0')
    adfan = pd.read_csv(
        savePath['weight_average']+'aW_a_n.csv', index_col='Unnamed: 0')
    result = pd.DataFrame(np.random.random(
        [12, 12]), index=w_bd, columns=brand)
    result_p = pd.DataFrame(np.random.random(
        [12, 12]), index=w_bd, columns=brand)
    for i in adfa.index:
        for c in adfa.columns:
            result[c][i] = 0
            result_p[c][i] = 0
            result[c][i] = round(adfa[c][i]-adfan[c][i], 2)
            result_p[c][i] = round(adfp[c][i]-adfpn[c][i], 2)
    result.to_csv(savePath['weight_average']+'aW_sub.csv')
    result_p.to_csv(savePath['weight_average']+'aW_sub_p.csv')


if __name__ == "__main__":

    # compute score
    picture_score()
    all_score()

    # save result

    a.index = a_n.index = pict.index = pict_n.index = w_bd
    aa.index = aa_n.index = apict.index = apict_n.index = w_bd
    save_to_csv()
    div_score()
    sub_score()

    print("Finish")

    pass
