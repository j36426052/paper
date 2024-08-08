import json
import os
import numpy as np
import matplotlib.pyplot as plt

def load_json(p):
    filename = f"data/{p}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    else:
        print(f"File {filename} not found.")
        return None

def plot_graphs(p_values):
    plt.figure(figsize=(20, 15))

    for i, y_axis in enumerate([
        "(1-p)/p * alpha(n) * beta(n)",
        "(1-p)/p * beta(n) * gamma(n)",
        "epsilon(n)",
        "epsilon_prime(n)"
    ], 1):
        plt.subplot(2, 2, i)
        for n in range(1, 6):
            y_values = []
            for p in p_values:
                p = p / 100  # 將 p 除以 100
                data = load_json(p)
                if data is None:
                    continue
                if y_axis == "(1-p)/p * alpha(n) * beta(n)":
                    y = ((1 - p) / p) * data[f'alpha_{n}'] * data[f'beta_{n}']
                elif y_axis == "(1-p)/p * beta(n) * gamma(n)":
                    y = ((1 - p) / p) * data[f'beta_{n}'] * data[f'gamma_{n}']
                elif y_axis == "epsilon(n)":
                    y = data[f'epsilon_{n}']
                else:  # epsilon_prime(n)
                    y = data[f'epsilon_prime_{n}']

                y_values.append(y)
            plt.plot([p / 100 for p in p_values], y_values, label=f'n={n}')  # 調整 x 軸

        plt.xlabel('p')
        plt.ylabel(y_axis)
        plt.title(f'{y_axis} vs p')
        plt.legend()
        plt.grid(True)

        # 設置 x 軸範圍為 0 到 1，y 軸範圍為 0 到 1（除了 epsilon(n)）
        plt.xlim(0, 1)
        if y_axis != "epsilon(n)" and y_axis != "epsilon_prime(n)":
            plt.ylim(0, 0.18)
        

    plt.tight_layout()
    plt.savefig(f"{y_axis}.png")
    plt.show()

# 生成 p 值範圍
p_values = range(1, 100)

# 繪製圖形
plot_graphs(p_values)
