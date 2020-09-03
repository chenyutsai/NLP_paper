import numpy as np
import pandas as pd
import csv
import json

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)

title = ['apple', 'google', 'htc', 'lg', 'mi', 'nokia',
         'oppo', 'other', 'samsung', 'huawei', 'sony', 'asus']


def v_PageRank(data, value, v_pRank):
    df = pd.read_csv(
        'result_data/'+data+'.csv', index_col='Unnamed: 0')

    with open('result_data/'+value+'.json', 'r') as va:
        vex = json.load(va)
        v = []
        for p in vex:
            v.append(vex[p])

    dfT = df.T
    nmp = dfT.values
    print(nmp)
    # 設置確定隨機跳轉機率的 alpha、網頁結點數
    alpha = 0.85
    N = 12

    # # 初始化隨機跳轉機率的矩陣
    jump = np.full([2, 1], [[alpha], [1-alpha]], dtype=float)

    # # vertex矩陣建構
    vertex = np.full([N, N], 0, dtype=float)
    row, col = np.diag_indices_from(vertex)
    vertex[row, col] = np.array(v)

    # # 鄰接矩陣的構建
    adj = np.full([N, N], nmp, dtype=float)

    # # 對鄰接矩陣進行歸一化
    row_sums = adj.sum(axis=1)  # 對每一行求和
    row_sums[row_sums == 0] = 0.1  # 防止由於分母出現 0 而導致的 Nan
    adj = adj / row_sums[:, np.newaxis]  # 除以每行之和的歸一化

    # 初始的 PageRank 值，通常是設置所有值為 1.0
    pr = np.full([1, N], 1, dtype=float)

    # with open('result_data/'+v_pRank+'.csv', 'w', newline='') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerow(['apple', 'google', 'htc', 'lg', 'mi', 'nokia',
    #                      'oppo', 'other', 'samsung', 'huawei', 'sony', 'asus'])

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

    # 加上 vexter 的權重
        pr = pr.transpose()
        pr = np.dot(vertex, pr)
        pr = pr.transpose()
        pr = pr/pr.sum()
        list = pr.tolist()
    print(list)

    # with open('result_data/'+v_pRank+'.csv', 'a', newline='') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerow(list[0])


if __name__ == "__main__":

    # # weight_no
    v_PageRank('weight_no/nW_sub', 'weight_no/nsub_vertex_A',
               'weight_no/pRank/vrank_nW_sub')
    # v_PageRank('weight_no/nW_sub_p', 'weight_no/nsub_vertex_P',
    #            'weight_no/pRank/vrank_nW_sub_p')
    # v_PageRank('weight_no/nW_div', 'weight_no/ndiv_vertex_A',
    #            'weight_no/pRank/vrank_nW_div')
    # v_PageRank('weight_no/nW_div_p', 'weight_no/ndiv_vertex_A',
    #            'weight_no/pRank/vrank_nW_div_p')

    # # weight words
    # v_PageRank('weight_words/wW_sub', 'weight_words/wsub_vertex_A',
    #            'weight_words/pRank/vrank_wW_sub')
    # v_PageRank('weight_words/wW_sub_p', 'weight_words/wsub_vertex_P',
    #            'weight_words/pRank/vrank_wW_sub_p')
    # v_PageRank('weight_words/wW_div', 'weight_words/wdiv_vertex_A',
    #            'weight_words/pRank/vrank_wW_div')
    # v_PageRank('weight_words/wW_div_p', 'weight_words/wdiv_vertex_P',
    #            'weight_words/pRank/vrank_wW_div_p')

    # # weight max
    # v_PageRank('weight_max/mW_sub', 'weight_max/msub_vertex_A',
    #            'weight_max/pRank/vrank_mW_sub')
    # v_PageRank('weight_max/mW_sub_p', 'weight_max/msub_vertex_P',
    #            'weight_max/pRank/vrank_mW_sub_p')
    # v_PageRank('weight_max/mW_div', 'weight_max/mdiv_vertex_A',
    #            'weight_max/pRank/vrank_mW_div')
    # v_PageRank('weight_max/mW_div_p', 'weight_max/mdiv_vertex_P',
    #            'weight_max/pRank/vrank_mW_div_p')

    # # weight average
    # v_PageRank('weight_average/aW_sub', 'weight_average/asub_vertex_A',
    #            'weight_average/pRank/vrank_aW_sub')
    # v_PageRank('weight_average/aW_sub_p', 'weight_average/asub_vertex_P',
    #            'weight_average/pRank/vrank_aW_sub_p')
    # v_PageRank('weight_average/aW_div', 'weight_average/adiv_vertex_A',
    #            'weight_average/pRank/vrank_aW_div')
    # v_PageRank('weight_average/aW_div_p', 'weight_average/adiv_vertex_P',
    #            'weight_average/pRank/vrank_aW_div_p')

    # special
    # v_PageRank('weight_max/mW_div', 'weight_max/msub_vertex_A',
    #            'special/svrank_mW_sub')
    # v_PageRank('weight_max/mW_div_p', 'weight_max/msub_vertex_P',
    #            'special/svrank_mW_sub_p')
    # v_PageRank('weight_no/nW_div', 'weight_no/nsub_vertex_A',
    #    'special/snvrank_nW_sub')
    # v_PageRank('weight_no/nW_div_p', 'weight_no/nsub_vertex_P',
    #    'special/snvrank_nW_sub_p')

    print("Finish")
