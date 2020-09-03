import csv


def adj_score():
    antusd = {}
    new = []
    flag = False
    with open('antusd/antusd.csv', newline='') as acsv:
        rs = csv.reader(acsv)
        for r in rs:
            antusd[r[0]] = r[1]
    with open('aatest/uppercase/nia.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if flag:
                try:
                    new.append([n, round(s/count, 8)])
                except ZeroDivisionError:
                    new.append([n, round(0, 8)])
            flag = True
            n = row[0]
            s = 0
            count = 0
            for r in range(len(row[0])-1, len(row[0])//2 - 1, -1):
                # print(row[0])
                for k in antusd:
                    if row[0][r] in k:
                        count += 1
                        s += float(antusd[k])
                        continue
        new.append([n, round(s/count, 8)])
        # print(new)
    with open('0_experiment_data/uppercase/my_score.csv', 'w', newline='') as fw:
        # 建立 CSV 檔寫入器
        writer = csv.writer(fw)
        for i in new:
            writer.writerow(i)


def not_in_antusd():
    antusd = []
    n = []
    with open('antusd/antusd.csv', newline='') as acsv:
        rs = csv.reader(acsv)
        for r in rs:
            antusd.append(r[0])
        # print(antusd)
    with open('aatest/uppercase/adjadj.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if row[0] not in antusd:
                n.append(row)
    with open('aatest/uppercase/nia.csv', 'w', newline='') as fw:
        # 建立 CSV 檔寫入器
        writer = csv.writer(fw)
        for i in n:
            writer.writerow(i)


def adj():
    adj = []
    counti = 0
    countadj = 0
    with open('/Users/tsaichenyu/Desktop/Lab/0_experiment_data/nia.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)

        # 以迴圈輸出每一列
        for row in rows:
            if len(row[0]) == 1:
                continue
            elif len(row[0]) < 4 and row[1] == 'i':
                continue
            else:
                adj.append(row)
                print(row)
                if row[1] == 'i':
                    counti += 1
                if row[1] == 'a':
                    countadj += 1
    print(counti)
    print(countadj)

    # with open('aatest/uppercase/adjadj.csv', 'w', newline='') as fw:
    #     # 建立 CSV 檔寫入器
    #     writer = csv.writer(fw)
    #     for i in adj:
    #         writer.writerow(i)


if __name__ == "__main__":
    # adj_score()
    # not_in_antusd()
    adj()
    pass
