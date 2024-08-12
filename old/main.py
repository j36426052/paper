import os
import json
import math

# parameter setting
n = 5               # which SG_n
p = 0.92             # the probability to release path
use_old = False      # whether clean old parameter setting

# function
## tool
def check_oldfile(p):
    """
    Generate whether the p.json exist, if not create it.
    After that, return is it exist at first.

    Args:
        p (float): The probability to release path
    """
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

### generate


## main functin
def f(k):
    global data
    if 'f'+str(k) in data:
        return data['f'+str(k)]
    fp,gp,hp,tp = f(k-1),g(k-1),h(k-1),t(k-1)
    #result = fp**3 + 6*(gp)*(fp**2) + 3*(hp)*(fp**2) + 9*(gp**2)*(fp) + 6*(fp)*(hp)*(gp) + 2*(gp**3)
    result = (fp**3)/(1-p)**3 + 3*(fp)*(gp**2)/(p*(1-p)**2) + 3*(gp**2)*(hp)/(p**2 * (1-p)) + (hp**3)/p**3
    print("(fp**3)/(1-p)**3" ,(fp**3)/(1-p)**3)
    print('(1-p)**3',(1-p)**3)
    print("fp**3",fp**3)
    print('(1-p)**6',(1-p)**6)
    data['f'+str(k)] = result
    print('f'+str(k)+'finish')
    return result


def g(k):
    global data
    if 'g'+str(k) in data:
        return data['g'+str(k)]
    fp,gp,hp,tp = f(k-1),g(k-1),h(k-1),t(k-1)
    #result = (fp**2)*(gp) + 4*(fp)*(gp**2) + 2*(fp**2)*(hp) + (tp)*(fp**2) + 2*(fp)*(gp)*(hp) + 6*(fp)*(gp)*(hp) + \
    #3*(gp**3) + 2*(fp)*(gp)*(tp) + 2*(fp)*(hp**2) + 2*(gp**2)*(hp) + 2*(gp**2)*(hp)
    result = (fp**2)*(gp)/ (1-p)**3 + 2*(fp)*(gp)*(hp)/ (p* (1-p)**2) + (gp**3)/(p* (1-p)**2) + 2*(gp)*(hp**2)/(p**2 * (1-p)) + (gp**2)*(tp)/(p**2 * (1-p)) + (hp**2)*(tp)/p**3
    data['g'+str(k)] = result
    print('g'+str(k)+'finish')
    return result


def h(k):
    global data
    if 'h'+str(k) in data:
        return data['h'+str(k)]
    fp,gp,hp,tp = f(k-1),g(k-1),h(k-1),t(k-1)
    #result = (fp)*(gp**2) + 4*(fp)*(gp)*(hp) + 2*(gp**3) + 2*(fp)*(gp)*(tp) + (gp**2)*(hp) + 6*(gp**2)*(hp) + \
    #3*(fp)*(hp**2) + 2*(gp**2)*(tp) + 2*(gp)*(hp**2) + 2*(fp)*(hp)*(tp) + 2*(gp)*(hp**2)
    result = (fp)*(gp**2)/(1-p)**3 + (fp)*(hp**2)/(p*(1-p)**2) + 2*(gp**2)*(hp)/(p*(1-p)**2) + (hp**3)/(p**2 * (1-p)) + 2*(gp)*(hp)*(tp)/(p**2 * (1-p)) + (hp)*(tp**2)/p**3
    data['h'+str(k)] = result
    print('h'+str(k)+'finish')
    return result


def t(k):
    global data
    if 't'+str(k) in data:
        return data['t'+str(k)]
    fp,gp,hp,tp = f(k-1),g(k-1),h(k-1),t(k-1)
    #result = (gp**3) + 6*(gp**2)*(hp) + 3*(gp**2)*(tp) + 9*(gp)*(hp**2) + 6*(gp)*(hp)*(tp) + 2*(hp**3)
    result = (gp**3)/(1-p)**3 + 3*(gp)*(hp**2)/(p * (1-p)**2) + 3*(hp**2)*(tp)/(p**2 * (1-p)) + (tp**3)/p**3
    data['t'+str(k)] = result
    print('t'+str(k)+'finish')
    return result

def alpha(k):
    global data
    if 'alpha_'+str(k) in data:
        return data['alpha_'+str(k)]
    fp,gp,hp,tp = f(k),g(k),h(k),t(k)
    try:
        result = gp/fp
    except ZeroDivisionError as e:
        data['gamma_'+str(k)] = 9999
        print(e)
        return 9999
    data['alpha_'+str(k)] = result
    print('alpha_'+str(k)+'finish')
    return result

def beta(k):
    global data
    if 'beta_'+str(k) in data:
        return data['beta_'+str(k)]
    fp,gp,hp,tp = f(k),g(k),h(k),t(k)
    try:
        result = hp/gp
    except ZeroDivisionError as e:
        data['gamma_'+str(k)] = 9999
        print(e)
        return 9999
    data['beta_'+str(k)] = result
    print('beta_'+str(k)+'finish')
    return result

def gamma(k):
    global data
    if 'gamma_'+str(k) in data:
        return data['gamma_'+str(k)]
    fp,gp,hp,tp = f(k),g(k),h(k),t(k)
    try:
        result = tp/hp
    except ZeroDivisionError as e:
        data['gamma_'+str(k)] = 9999
        print(e)
        return 9999
    data['gamma_'+str(k)] = result
    print('gamma_'+str(k)+'finish')
    return result

def epsilon(k,p):
    global data
    if 'epsilon_'+str(k) in data:
        return data['epsilon_'+str(k)]
    qp = (1-p)/p
    result = qp*(beta(k) - alpha(k))
    data['epsilon_'+str(k)] = result
    print('epsilon_'+str(k)+'finish')
    return result

def epsilon_prime(k,p):
    global data
    if 'epsilon_prime_'+str(k) in data:
        return data['epsilon_prime_'+str(k)]
    qp = (1-p)/p
    result = qp*(gamma(k) - beta(k))
    data['epsilon_prime_'+str(k)] = result
    print('epsilon_prime_'+str(k)+'finish')
    return result

## logic

# 1. Check the file save parameter exist, if not, generate the json file
status = check_oldfile(p)

# 2. Initialize the dynamic programminng set (Can set parameter above that don't use old parameter)
if (status and use_old):
    data = load_old_parameter(p)
else:
    data = {}

# 3. Just run the target
# f0 = (1-p)**3
# g0 = ((1-p)**2)*p
# h0 = 0
# t0 = 0

f0 = (1-p)**3
g0 = ((1-p)**2)*p
h0 = 0
t0 = 0

data['f0'] = f0
data['g0'] = g0
data['h0'] = h0
data['t0'] = t0

for i in range(1,10):
    print(i)
    # print(f"f{i}",f(i))
    # print(f"g{i}",g(i))
    # print(f"h{i}",h(i))
    # print(f"t{i}",t(i))
    # print(f"alpha_{i}",alpha(i))
    # print(f"beta_{i}",beta(i))
    # print(f"gamma_{i}",gamma(i))
    print(f"epsilon_{i}",epsilon(i,p))
    print(f"epsilon_prime_{i}",epsilon_prime(i,p))
    print("=========")


filename = f"data/{p}.json"
with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)





