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

def plot_single_graph(p_values, y_axis):
    plt.figure(figsize=(10, 7))
    for n in range(1, 6):
        y_values = []
        for p in p_values:
            p = mpf(p) / 100  # 將 p 除以 100 並轉為高精度數值
            data = load_json(p)
            if data is None:
                continue
            try:
                if y_axis == "(1-p)/p * alpha(n) * beta(n)":
                    y = ((1 - p) / p) * data[f'alpha_{n}'] * data[f'beta_{n}']
                elif y_axis == "(1-p)/p * beta(n) * gamma(n)":
                    y = ((1 - p) / p) * data[f'beta_{n}'] * data[f'gamma_{n}']
                elif y_axis == "epsilon(n)":
                    y = data[f'epsilon_{n}']
                else:  # epsilon_prime(n)
                    y = data[f'epsilon_prime_{n}']
            except KeyError:
                print(f"Key not found for n={n}, p={p}")
                continue

            y_values.append(float(y))  # 將高精度數值轉換為普通浮點數供繪圖使用

        # 將 x 軸的 p 值也轉換成普通浮點數
        plt.plot([float(p / 100) for p in p_values], y_values, label=f'n={n}')

    plt.xlabel('p')
    plt.ylabel(y_axis)
    plt.title(f'{y_axis} vs p')
    plt.legend()
    plt.grid(True)

    # 設置 x 軸範圍為 0 到 1，y 軸範圍根據具體情況調整
    plt.xlim(0, 1)
    if y_axis != "epsilon(n)" and y_axis != "epsilon_prime(n)":
        plt.ylim(0, 1)  # 根據需要調整 y 軸範圍

    # 儲存圖形
    filename = y_axis.replace("/", "_").replace("*", "_").replace("(", "").replace(")", "").replace(" ", "_") + ".png"
    plt.savefig(filename)
    print(f"Saved plot as {filename}")
    plt.show()

def plot_graphs(p_values):
    # 定義每張圖的 y 軸標籤
    y_axes = [
        "(1-p)/p * alpha(n) * beta(n)",
        "(1-p)/p * beta(n) * gamma(n)",
        "epsilon(n)",
        "epsilon_prime(n)"
    ]
    # 為每個 y 軸標籤繪製單獨的圖形
    for y_axis in y_axes:
        plot_single_graph(p_values, y_axis)

# 生成 p 值範圍
p_values = range(1, 100)

# 繪製圖形
plot_graphs(p_values)
