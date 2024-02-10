import re

# 根据第三列的值，将数据拆分为7个文件
for i in range(1, 8):
    with open(f'txt{i}.txt', 'w') as out:
        pass  # 创建空的目标文件

with open('diamond.out', 'r') as f:
    data = f.readlines()

for line in data:
    cols = line.split()
    if len(cols) >= 3:
        score = float(cols[2])
        if score >= 60 and score < 65:
            with open('pident1.txt', 'a') as out1:
                out1.write(line)
        elif score >= 65 and score < 70:
            with open('pident2.txt', 'a') as out2:
                out2.write(line)
        elif score >= 70 and score < 75:
            with open('pident3.txt', 'a') as out3:
                out3.write(line)
        elif score >= 75 and score < 80:
            with open('pident4.txt', 'a') as out4:
                out4.write(line)
        elif score >= 80 and score < 85:
            with open('pident5.txt', 'a') as out5:
                out5.write(line)
        elif score >= 85 and score < 90:
            with open('pident6.txt', 'a') as out6:
                out6.write(line)
        elif score >= 90:
            with open('pident7.txt', 'a') as out7:
                out7.write(line)

for i in range(1, 8):
    with open(f'pident{i}.txt', 'r') as f:
        data = f.readlines()
    with open(f'id{i}.txt', 'w') as out:
        for line in data:
            cols = line.split()
            if len(cols) > 0:
                out.write(cols[0] + '\n')
