import random
import math
from math import gcd

def pollard_rho(n, epsilon):
    T = int(math.sqrt(2 * math.sqrt(math.log(n) / epsilon)) + 1)
    f = lambda x: (x * x + 1) % n

    while True:
        x0 = random.randint(1, n - 1)
        x_values = [x0]

        for i in range(T):
            x_next = f(x_values[-1])
            x_values.append(x_next)

            for k in range(i + 1):
                dk = gcd(x_values[i + 1] - x_values[k], n)
                if 1 < dk < n:
                    return dk  
                elif dk == n:
                    break
print()
    