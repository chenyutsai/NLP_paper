import numpy as np
import pandas as pd
import csv

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)

title = ['apple', 'google', 'htc', 'lg', 'mi', 'nokia',
         'oppo', 'other', 'samsung', 'huawei', 'sony', 'asus']
score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
score_p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
w_score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
w_score_p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def PageRank(data, pRank):
    df = pd.read_csv(
        'result_data/'+data+'.csv', index_col='Unnamed: 0')

    dfT = df.T
    nmp = dfT.values
    # print(nmp)
    # 設置確定隨機跳轉機率的 alpha、網頁結點數
    alpha = 0.85
    N = 12

    # # 初始化隨機跳轉機率的矩陣
    jump = np.full([2, 1], [[alpha], [1-alpha]], dtype=float)
    # # 鄰接矩陣的構建
    adj = np.full([N, N], nmp, dtype=float)

    # # 對鄰接矩陣進行歸一化
    row_sums = adj.sum(axis=1)
    # # 對每一行求和
    row_sums[row_sums == 0] = 0.1
    # # 防止由於分母出現 0 而導致的 Nan
    adj = adj / row_sums[:, np.newaxis]
    # # 除以每行之和的歸一化
    # # 初始的 PageRank 值，通常是設置所有值為 1.0
    pr = np.full([1, N], 1, dtype=float)

    with open('result_data/'+pRank+'.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['apple', 'google', 'htc', 'lg', 'mi', 'nokia',
                         'oppo', 'other', 'samsung', 'huawei', 'sony', 'asus'])

    # PageRank 算法本身是採樣疊代方式進行的，當最終的取值趨於穩定後結束。
    for i in range(0, 100):
        # 進行點乘，計算Σ(PR(pj)/L(pj))
        pr = np.dot(pr, adj)
    # 轉置保存Σ(PR(pj)/L(pj)) 結果的矩陣，並增加長度為 N 的列向量，其中每個元素的值為 1/N，便於下一步的點乘。
        pr_jump = np.full([N, 2], [[0, 1/N]])
        pr_jump[:, :-1] = pr.transpose()
    # 進行點乘，計算α(Σ(PR(pj)/L(pj))) + (1-α)/N)
        pr = np.dot(pr_jump, jump)
    # 歸一化 PageRank 得分
        pr = pr.transpose()
        pr = pr / pr.sum()
        # print("round", i + 1, pr)
        # print(type(pr[0]))
        list = pr.tolist()
    # print(list[0])

    with open('result_data/'+pRank+'.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(list[0])


if __name__ == "__main__":

    # weight_no
    PageRank('weight_no/nW_sub', 'weight_no/pRank/rank_nW_sub')
    PageRank('weight_no/nW_sub_p', 'weight_no/pRank/rank_nW_sub_p')
    PageRank('weight_no/nW_div', 'weight_no/pRank/rank_nW_div')
    PageRank('weight_no/nW_div_p', 'weight_no/pRank/rank_nW_div_p')

    # weight words
    PageRank('weight_words/wW_sub', 'weight_words/pRank/rank_wW_sub')
    PageRank('weight_words/wW_sub_p', 'weight_words/pRank/rank_wW_sub_p')
    PageRank('weight_words/wW_div', 'weight_words/pRank/rank_wW_div')
    PageRank('weight_words/wW_div_p', 'weight_words/pRank/rank_wW_div_p')

    # weight max
    PageRank('weight_max/mW_sub', 'weight_max/pRank/rank_mW_sub')
    PageRank('weight_max/mW_sub_p', 'weight_max/pRank/rank_mW_sub_p')
    PageRank('weight_max/mW_div', 'weight_max/pRank/rank_mW_div')
    PageRank('weight_max/mW_div_p', 'weight_max/pRank/rank_mW_div_p')

    # weight average
    PageRank('weight_average/aW_sub', 'weight_average/pRank/rank_aW_sub')
    PageRank('weight_average/aW_sub_p', 'weight_average/pRank/rank_aW_sub_p')
    PageRank('weight_average/aW_div', 'weight_average/pRank/rank_aW_div')
    PageRank('weight_average/aW_div_p', 'weight_average/pRank/rank_aW_div_p')

    print("Finish")
    pass
