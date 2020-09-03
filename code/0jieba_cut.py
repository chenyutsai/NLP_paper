import jieba
import jieba.posseg as pseg
import csv
jieba.set_dictionary('dict_tw.txt')

with open('50noID.txt', 'r') as fr:
    with open('aiaiaiai', 'w') as fw:
        d = {}
        lines = fr.readlines()
        for i in range(len(lines)):
            print(i)
            words = jieba.posseg.cut(lines[i])
            for w, z in words:
                # print(w+': '+z)
                if z == 'a' or z == 'i':
                    if w not in d:
                        d[w] = z
                        fw.write(w+': '+z+'\n')
        # print(d)
# t = "我要和天一樣高"
# words = jieba.posseg.cut(t)
# for w, z in words:
#     print(w)
#     print(z)
# with open('antusd/dict.csv', newline='') as c:

#     # 讀取 CSV 檔案內容
#     rows = csv.reader(c)
#     an = []
#     dd = []
#     # 以迴圈輸出每一列
#     for row in rows:
#         print(row)
#         an.append(row[0])
#     print(an)
#     for j in an:
#         words = jieba.posseg.cut(j)
#         for word, flag in words:
#             # fw.write(f'{word}={flag} ')
#             if flag == 'a' or flag == 'i':
#                 # fw.write(word+'\n')
#                 dd.append(word)
#         # fw.write(",")
#         # count += 1
#     s_d = set(dd)
#     print(s_d)
# with open('antusd/dict_a.csv', 'w', newline='') as csvfile:
#     # 建立 CSV 檔寫入器
#     writer = csv.writer(csvfile)

#     for test in s_d:
#         writer.writerow([test])


# with open('50noID.txt', 'r') as fp:
#     all_lines = fp.readlines()

# title = []

# for i in all_lines:
#     title.append(i.strip("\n"))

# with open('antusd/a_ii.txt', 'w') as fw:

#     dd = []
#     count = 0
#     for j in range(0, 100, 1):
#         # fw.write(title[j])
#         count += 1
#         words = jieba.posseg.cut(title[j])
#         # print(words)
#         # fw.write(words)
#         for word, flag in words:
#             # fw.write(f'{word}={flag} ')
#             if flag == 'a' or flag == 'i':
#                 # fw.write(word+'\n')
#                 dd.append([word, flag])
#         print(count)
#         # fw.write(",")
#         # count += 1
#     # s_d = set(dd)
#     # for i in s_d:
#     #     fw.write(i+"\n")
#     print(dd)
