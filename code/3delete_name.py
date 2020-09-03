# coding=UTF-8
# Open file
fp = open('article/fliter/iwant_push_t.txt', "r")

# 變數 lines 會儲存 filename.txt 的內容
lines = fp.readlines()

# close file
fp.close()

# print content
for i in range(len(lines)):
    lines[i] = lines[i].strip('\n')
    # print(lines[i])

name_push = []
user = ""
push = ""


for i in lines:
    name_push.append(i.split(": "))

fw = open('article/fliter/iwant_push_F.txt', "w")

for i in range(1, len(name_push)):
    print(i)
    if name_push[i-1][0] != name_push[i][0]:
        fw.write(name_push[i-1][1].lstrip()+"\n")
    elif name_push[i-1][0] == name_push[i][0]:
        fw.write(name_push[i-1][1].lstrip())
fw.write(name_push[i][1].lstrip())
fw.close()
