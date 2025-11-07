import re

# 假設的用戶輸入
input_str = input("input the erase edge: \n")

term1 = '[dash pattern=on 1pt off 2pt, very thick, blue]'
term2 = '[very thick,black]'

lines = [
    '\\draw (3,{3*sqrt(3)}) -- (5,{3*sqrt(3)});',
    '\\draw (7,{3*sqrt(3)}) -- (9,{3*sqrt(3)});',
    '\\draw (9,{3*sqrt(3)}) -- (8,{2*sqrt(3)});',
    '\\draw (7,{sqrt(3)}) -- (6,0);',
    '\\draw (6,0) -- (5,{sqrt(3)});',
    '\\draw (4,{2*sqrt(3)}) -- (3,{3*sqrt(3)});'
]

# 處理每一行
for i, line in enumerate(lines):
    if str(i+1) in input_str.split():
        lines[i] = line.replace('\\draw', f'\\draw{term1}')
    else:
        lines[i] = line.replace('\\draw', f'\\draw{term2}')

# 將結果寫入文件
with open('trangle.txt', 'w') as f:
    f.write('\n'.join(lines))

# print("File 'trangle.txt' has been created with the modified lines.")
# print("\nContents of trangle.txt:")
# with open('/mnt/data/trangle.txt', 'r') as f:
#     print(f.read())