import os
import json
from mpmath import mp

# 設定 mpmath 的精度
mp.dps = 100  # 設定小數精度為 100 位

def main(n, p, use_old):
    global data  # 在主函數中聲明 data 為全局變數

    def check_oldfile(p):
        filename = f"data/{p}.json"
        if not os.path.isfile(filename):
            with open(filename, 'w') as json_file:
                json.dump({}, json_file)
            return False
        return True

    def load_old_parameter(p):
        filename = f"data/{p}.json"
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data

    def f(k):
        if 'f'+str(k) in data:
            return mp.mpf(data['f'+str(k)])
        fp, gp, hp, tp = f(k-1), g(k-1), h(k-1), t(k-1)
        result = fp**3 + 6*(gp)*(fp**2) + 3*(hp)*(fp**2) + 9*(gp**2)*(fp) + 6*(fp)*(hp)*(gp) + 2*(gp**3)
        data['f'+str(k)] = str(result)
        return result

    def g(k):
        if 'g'+str(k) in data:
            return mp.mpf(data['g'+str(k)])
        fp, gp, hp, tp = f(k-1), g(k-1), h(k-1), t(k-1)
        result = (fp**2)*(gp) + 4*(fp)*(gp**2) + 2*(fp**2)*(hp) + (tp)*(fp**2) + 2*(fp)*(gp)*(hp) + 6*(fp)*(gp)*(hp) + \
                 3*(gp**3) + 2*(fp)*(gp)*(tp) + 2*(fp)*(hp**2) + 2*(gp**2)*(hp) + 2*(gp**2)*(hp)
        data['g'+str(k)] = str(result)
        return result

    def h(k):
        if 'h'+str(k) in data:
            return mp.mpf(data['h'+str(k)])
        fp, gp, hp, tp = f(k-1), g(k-1), h(k-1), t(k-1)
        result = (fp)*(gp**2) + 4*(fp)*(gp)*(hp) + 2*(gp**3) + 2*(fp)*(gp)*(tp) + (gp**2)*(hp) + 6*(gp**2)*(hp) + \
                 3*(fp)*(hp**2) + 2*(gp**2)*(tp) + 2*(gp)*(hp**2) + 2*(fp)*(hp)*(tp) + 2*(gp)*(hp**2)
        data['h'+str(k)] = str(result)
        return result

    def t(k):
        if 't'+str(k) in data:
            return mp.mpf(data['t'+str(k)])
        fp, gp, hp, tp = f(k-1), g(k-1), h(k-1), t(k-1)
        result = (gp**3) + 6*(gp**2)*(hp) + 3*(gp**2)*(tp) + 9*(gp)*(hp**2) + 6*(gp)*(hp)*(tp) + 2*(hp**3)
        data['t'+str(k)] = str(result)
        return result

    def alpha(k):
        if 'alpha_'+str(k) in data:
            return mp.mpf(data['alpha_'+str(k)])
        fp, gp, hp, tp = f(k), g(k), h(k), t(k)
        try:
            result = gp / fp
        except ZeroDivisionError:
            result = mp.mpf('9999')
        data['alpha_'+str(k)] = str(result)
        return result

    def beta(k):
        if 'beta_'+str(k) in data:
            return mp.mpf(data['beta_'+str(k)])
        fp, gp, hp, tp = f(k), g(k), h(k), t(k)
        try:
            result = hp / gp
        except ZeroDivisionError:
            result = mp.mpf('9999')
        data['beta_'+str(k)] = str(result)
        return result

    def gamma(k):
        if 'gamma_'+str(k) in data:
            return mp.mpf(data['gamma_'+str(k)])
        fp, gp, hp, tp = f(k), g(k), h(k), t(k)
        try:
            result = tp / hp
        except ZeroDivisionError:
            result = mp.mpf('9999')
        data['gamma_'+str(k)] = str(result)
        return result

    def epsilon(k, p):
        if 'epsilon_'+str(k) in data:
            return mp.mpf(data['epsilon_'+str(k)])
        qp = p / (1-p)
        result = qp * (alpha(k) - beta(k))
        data['epsilon_'+str(k)] = str(result)
        return result

    def epsilon_prime(k, p):
        if 'epsilon_prime_'+str(k) in data:
            return mp.mpf(data['epsilon_prime_'+str(k)])
        qp = p / (1-p)
        result = qp * (beta(k) - gamma(k))
        data['epsilon_prime_'+str(k)] = str(result)
        return result

    # Main logic
    status = check_oldfile(p)

    if status and use_old:
        data = load_old_parameter(p)
    else:
        data = {}

    f1 = p**9 + 3 * p**8 * (1-p)
    g1 = 2 * p**8 * (1-p) + 2 * p**7 * (1-p)**2
    h1 = 3 * p**7 * (1 - p)**2
    t1 = 2 * p**6 * (1 - p)**3

    data['f1'] = str(f1)
    data['g1'] = str(g1)
    data['h1'] = str(h1)
    data['t1'] = str(t1)

    for i in range(1, n + 1):
        print(f"epsilon_{i}", epsilon(i, p))
        print(f"epsilon_prime_{i}", epsilon_prime(i, p))
        print("=========")

    filename = f"data/{p}.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
for i in range(1, 100):
    main(5, mp.mpf(i) / 100, False)
