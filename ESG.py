import json
import os
import matplotlib.pyplot as plt
from mpmath import mp, mpf, log

# 設定 mpmath 的精度
mp.dps = 100  # 設置精度為 100 位

# 載入 JSON 檔案
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

# 計算指定的表達式
def calculate_upperbdd(p_values, m_values):
    results = {}

    for m in m_values:
        results[m] = []
        for p in p_values:
            p = mpf(p)  # 將 p 轉換為高精度數值
            data = load_json(p)
            if data is None:
                continue
            try:
                # 取得 f_m(p) 和 alpha_m(p)
                f_m = data[f'f{m}']
                alpha_m = data[f'alpha_{m}']

                # 計算 [log(f_m(p)) + 3/2 log(1 + 2 * alpha_m(p))] / 3^m
                numerator = log(f_m) + (3 / 2) * log(1 + 2 * alpha_m)
                denominator = 3**m
                result = numerator / denominator

                results[m].append((float(p), float(result)))  # 儲存結果，p 和結果轉為普通浮點數
            except KeyError:
                print(f"Key not found for m={m}, p={p}")
                continue

    return results

def calculate_lowerbdd(p_values, m_values):
    results = {}

    for m in m_values:
        results[m] = []
        for p in p_values:
            p = mpf(p)  # 將 p 轉換為高精度數值
            data = load_json(p)
            if data is None:
                continue
            try:
                # 取得 f_m(p) 和 alpha_m(p)
                f_m = data[f'f{m}']
                gamma_m = data[f'gamma_{m}']

                # 計算 [log(f_m(p)) + 3/2 log(1 + 2 * alpha_m(p))] / 3^m
                numerator = log(f_m) + (3 / 2) * log(1 + 2 * gamma_m)
                denominator = 3**m
                result = numerator / denominator

                results[m].append((float(p), float(result)))  # 儲存結果，p 和結果轉為普通浮點數
            except KeyError:
                print(f"Key not found for m={m}, p={p}")
                continue

    return results


# 繪製圖形
def plot_results(results):
    plt.figure(figsize=(10, 8))

    for m, values in results.items():
        if not values:
            continue
        p_values, y_values = zip(*values)  # 解壓縮 p 和結果
        plt.plot(p_values, y_values, label=f'm={m}')

    plt.xlabel('p')
    plt.ylabel('[log(f_m(p)) + 3/2 log(1 + 2 * alpha_m(p))] / 3^m')
    plt.title('Expression vs p for different m')
    plt.legend()
    plt.grid(True)
    plt.show()

# 設定 p 和 m 的值
p_values = [mpf(1)/10, mpf(1)/2, mpf(7)/10, mpf(9)/10]  # p 值列表
m_values = [2, 3, 4, 5]  # m 值列表

# 計算表達式
results = calculate_upperbdd(p_values, m_values)

print("upperbdd")
print(results)

results = calculate_lowerbdd(p_values, m_values)

print("lowerbdd")
print(results)