import os
import jieba
import jieba.posseg as pseg
import csv
import json
jieba.set_dictionary('dict_tw.txt')
jieba.load_userdict('my.dict.txt')

savePath = {
    'weight_max': 'result_data/weight_max/',
    'weight_average': 'result_data/weight_average/'
}

Bpath = {
    'path1': '0_experiment_data/B/1/',
    'path10': '0_experiment_data/B/10/'
}

# max score
picture = {'a': 0, 'g': 0, 'h': 0, 'l': 0, 'm': 0, 'n': 0,
           'o': 0, 'q': 0, 's': 0, 'w': 0, 'x': 0, 'z': 0}
picture_n = {'a': 0, 'g': 0, 'h': 0, 'l': 0, 'm': 0, 'n': 0,
             'o': 0, 'q': 0, 's': 0, 'w': 0, 'x': 0, 'z': 0}
all = {'a': 0, 'g': 0, 'h': 0, 'l': 0, 'm': 0, 'n': 0,
       'o': 0, 'q': 0, 's': 0, 'w': 0, 'x': 0, 'z': 0}
all_n = {'a': 0, 'g': 0, 'h': 0, 'l': 0, 'm': 0, 'n': 0,
         'o': 0, 'q': 0, 's': 0, 'w': 0, 'x': 0, 'z': 0}

# average score
a_picture = {'a': 0, 'g': 0, 'h': 0, 'l': 0, 'm': 0, 'n': 0,
             'o': 0, 'q': 0, 's': 0, 'w': 0, 'x': 0, 'z': 0}
a_picture_n = {'a': 0, 'g': 0, 'h': 0, 'l': 0, 'm': 0, 'n': 0,
               'o': 0, 'q': 0, 's': 0, 'w': 0, 'x': 0, 'z': 0}
a_all = {'a': 0, 'g': 0, 'h': 0, 'l': 0, 'm': 0, 'n': 0,
         'o': 0, 'q': 0, 's': 0, 'w': 0, 'x': 0, 'z': 0}
a_all_n = {'a': 0, 'g': 0, 'h': 0, 'l': 0, 'm': 0, 'n': 0,
           'o': 0, 'q': 0, 's': 0, 'w': 0, 'x': 0, 'z': 0}


def adj_i():
    with open('0_experiment_data/adj_dict.csv', newline='') as dcsv:
        adj_dict = csv.reader(dcsv)
        score = {}
        for adj in adj_dict:
            try:
                score[adj[0]] = adj[1]
            except IndexError:
                continue
        return score


def adj_b():
    with open('0_experiment_data/my_adj/b.csv', newline='') as bcsv:
        adj_dict = csv.reader(bcsv)
        score = {}
        for adj in adj_dict:
            try:
                score[adj[0]] = adj[1]
            except IndexError:
                continue
        return score


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
    for f in os.listdir(Bpath['path1']):
        with open(Bpath['path1']+str(f), 'r') as fr:
            lines = fr.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip('\n')
            for line in range(2, len(lines)):
                flag = True
                cflag = False
                b = {}
                for i in range(len(lines[line])):
                    if lines[line][i] == 'c':
                        cflag = True
                    if lines[line][i] in all:
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
                        scoreP(temp, words)
                    if cflag is False:
                        scoreA(temp, words)


def scoreA(name, jieba):
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
        temp_a += 0.29  # average score

    if temp_m > 0:
        all[name] += temp_m
    elif temp_m < 0:
        all_n[name] += abs(temp_m)

    if temp_a > 0:
        a_all[name] += temp_a
    elif temp_a < 0:
        a_all_n[name] += abs(temp_a)


def picture_score():
    for f in os.listdir(Bpath['path10']):
        with open(Bpath['path10']+str(f), 'r') as fr:
            lines = fr.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip('\n')
            for line in range(2, len(lines)):
                flag = True
                b = {}
                for i in range(len(lines[line])):
                    if lines[line][i] in picture:
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
                    scoreP(temp, words)


def scoreP(name, jieba):
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
        temp_a += 0.29  # average score

    if temp_m > 0:
        picture[name] += temp_m
    elif temp_m < 0:
        picture_n[name] += abs(temp_m)

    if temp_a > 0:
        a_picture[name] += temp_a
    elif temp_a < 0:
        a_picture_n[name] += abs(temp_a)


def compute_score():
    # weight_max
    with open(savePath['weight_max']+'mW_a.json', 'w') as mfa:
        json.dump(all, mfa)
    with open(savePath['weight_max']+'mW_p.json', 'w') as mfp:
        json.dump(picture, mfp)
    with open(savePath['weight_max']+'mW_a_n.json', 'w') as mfan:
        json.dump(all_n, mfan)
    with open(savePath['weight_max']+'mW_p_n.json', 'w') as mfpn:
        json.dump(picture_n, mfpn)
    # weight_average
    with open(savePath['weight_average']+'aW_a.json', 'w') as afa:
        json.dump(a_all, afa)
    with open(savePath['weight_average']+'aW_p.json', 'w') as afp:
        json.dump(a_picture, afp)
    with open(savePath['weight_average']+'aW_a_n.json', 'w') as afan:
        json.dump(a_all_n, afan)
    with open(savePath['weight_average']+'aW_p_n.json', 'w') as afpn:
        json.dump(a_picture_n, afpn)


def weight_max_score():
    # weight_max load
    with open(savePath['weight_max']+'mW_a.json', 'r') as mfa:
        load_mfa = json.load(mfa)
    with open(savePath['weight_max']+'mW_p.json', 'r') as mfp:
        load_mfp = json.load(mfp)
    with open(savePath['weight_max']+'mW_a_n.json', 'r') as mfan:
        load_mfan = json.load(mfan)
    with open(savePath['weight_max']+'mW_p_n.json', 'r') as mfpn:
        load_mfpn = json.load(mfpn)
    # weight_max div
    with open(savePath['weight_max']+'mdiv_vertex_A.json', 'w') as mdva:
        vertexA = {}
        for i in load_mfa:
            try:
                vertexA[i] = round(load_mfa[i] / load_mfan[i], 2)
            except ZeroDivisionError:
                vertexA[i] = round(load_mfa[i] / 1, 2)
        json.dump(vertexA, mdva)
    with open(savePath['weight_max']+'mdiv_vertex_P.json', 'w') as mdvp:
        vertexP = {}
        for j in load_mfp:
            try:
                vertexP[j] = round(load_mfp[j] / load_mfpn[j], 2)
            except ZeroDivisionError:
                vertexP[j] = round(load_mfp[j] / 1, 2)
        json.dump(vertexP, mdvp)
    # weight_max sub
    with open(savePath['weight_max']+'msub_vertex_A.json', 'w') as msva:
        vertexA = {}
        for i in load_mfa:
            vertexA[i] = round((load_mfa[i] - load_mfan[i]), 2)
        json.dump(vertexA, msva)
    with open(savePath['weight_max']+'msub_vertex_P.json', 'w') as msvp:
        vertexP = {}
        for j in load_mfp:
            vertexP[j] = round((load_mfp[j] - load_mfpn[j]), 2)
        json.dump(vertexP, msvp)


def weight_average_score():
   # weight_average load
    with open(savePath['weight_average']+'aW_a.json', 'r') as afa:
        load_afa = json.load(afa)
    with open(savePath['weight_average']+'aW_p.json', 'r') as afp:
        load_afp = json.load(afp)
    with open(savePath['weight_average']+'aW_a_n.json', 'r') as afan:
        load_afan = json.load(afan)
    with open(savePath['weight_average']+'aW_p_n.json', 'r') as afpn:
        load_afpn = json.load(afpn)
    # weight_average div
    with open(savePath['weight_average']+'adiv_vertex_A.json', 'w') as adva:
        vertexA = {}
        for i in load_afa:
            try:
                vertexA[i] = round(load_afa[i] / load_afan[i], 2)
            except ZeroDivisionError:
                vertexA[i] = round(load_afa[i] / 1, 2)
        json.dump(vertexA, adva)
    with open(savePath['weight_average']+'adiv_vertex_P.json', 'w') as advp:
        vertexP = {}
        for j in load_afp:
            try:
                vertexP[j] = round(load_afp[j] / load_afpn[j], 2)
            except ZeroDivisionError:
                vertexP[j] = round(load_afp[j] / 1, 2)
        json.dump(vertexP, advp)
    # weight_average sub
    with open(savePath['weight_average']+'asub_vertex_A.json', 'w') as asva:
        vertexA = {}
        for i in load_afa:
            vertexA[i] = round((load_afa[i] - load_afan[i]), 2)
        json.dump(vertexA, asva)
    with open(savePath['weight_average']+'asub_vertex_P.json', 'w') as asvp:
        vertexP = {}
        for j in load_afp:
            vertexP[j] = round((load_afp[j] - load_afpn[j]), 2)
        json.dump(vertexP, asvp)


def testcase():
    pass


if __name__ == "__main__":
    # testcase()
    all_score()

    picture_score()

    compute_score()
    weight_max_score()
    weight_average_score()

    pass
