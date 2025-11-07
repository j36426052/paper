import json
import os
import matplotlib.pyplot as plt
from mpmath import mp, mpf

# 設定 mpmath 的精度
mp.dps = 100  # 設置精度為 100 位

def load_json(p):
    filename = f"data/{p}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            # 將 JSON 中的字串數值轉換為高精度數值
            for key in data:
                data[key] = mpf(data[key])
            return data
    else:
        print(f"File {filename} not found.")
        return None

def plot_new_graph(p_values):
    plt.figure(figsize=(10, 8))

    for n in range(1, 6):  # n 從 1 到 5
        y_values = []
        for p in p_values:
            p = mpf(p) / 100  # 將 p 除以 100 並轉為高精度數值
            data = load_json(p)
            if data is None:
                continue
            try:
                # 計算 Z_n(p)
                Z_n = data[f'f{n}'] + 3 * data[f'g{n}'] + 3 * data[f'h{n}'] + data[f't{n}']
            except KeyError:
                print(f"Key not found for n={n}, p={p}")
                continue

            y_values.append(float(Z_n))  # 將高精度數值轉換為普通浮點數供繪圖使用

        # 將 x 軸的 p 值也轉換成普通浮點數
        plt.plot([float(p / 100) for p in p_values], y_values, label=f'n={n}')

    plt.xlabel('p')
    plt.ylabel('Z_n(p)')
    plt.title('Z_n(p) vs p')
    plt.legend()
    plt.grid(True)

    # 設置 x 軸範圍為 0 到 1
    plt.xlim(0, 1)

    plt.tight_layout()
    plt.savefig("Z_n(p).png")  # 儲存圖形
    plt.show()

# 生成 p 值範圍
p_values = range(1, 100)

# 繪製新的圖形
plot_new_graph(p_values)
