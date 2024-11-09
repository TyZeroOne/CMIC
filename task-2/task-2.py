import random
import sympy

# Разложение чисел в цепную дробь
def continued_fraction(numerator, denominator):
    result = []
    P = [0, 1]
    Q = [1, 0]
    i = 2
    while denominator != 0:
        integer_part = numerator // denominator
        result.append(integer_part)
        P.append(result[i - 2] * P[i - 1] + P[i - 2])
        Q.append(result[i - 2] * Q[i - 1] + Q[i - 2])
        remainder = numerator % denominator
        numerator, denominator = denominator, remainder
        i += 1
    return result, P, Q
def normal_Euclid(a, b):
    while a !=0 and b != 0:
        if a > b:
            a = a % b
        else: 
            b = b % a
    return a + b
# Решение диофантовых уравнений ax - by = c
def linear_diofant(a, b, c):
    nod = normal_Euclid(a, b)
    if c % nod != 0:
        return (0, 0)
    else: 
        res, P, Q = continued_fraction(a, b)
        x = pow(-1, len(res) - 2) * c / nod * Q[-2] + b
        y = pow(-1, len(res) - 2) * c / nod * P[-2] + a
        return (int(x), int(y))
# Решение линейных сравнений ax = b (mod m)
def compare(a, b, m):
    nod = normal_Euclid(a, m)
    if b % nod != 0:
        return 0
    else: 
        res, P, Q = continued_fraction(a, m)
        x = pow(-1, len(res) - 2) * b / nod * Q[-2]
        return int(x % m)
# Вычисление обратного элемента в кольце вычетов Zm
def reverse(a, m):
    return compare(a, 1, m)
# Вычисление символа Якоби
def jacobi_symbol(a, n):
    if n <= 0 or n % 2 == 0:
        return 0
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a 
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0
def factorization_number(num):
    n = num
    i = 2
    result = []

    while i * i <= n:
        while n % i == 0:
            result.append(i)
            n //= i
        i += 1

    if n > 1:
        result.append(n)

    return result
# Вычисление символа Лежандра
def legendre_symbol(first, second):
    a = first
    factors = factorization_number(second)
    if len(factors) == 1:
        p = second
    else:
        return None
    numerators = []
    result = 1
    if a < 0:
        numerators.append(-1)
        a = abs(a)
    a %= p
    arr = factorization_number(a)
    count_dict = {}
    for num in arr:
        if num in count_dict:
            count_dict[num] += 1
        else:
            count_dict[num] = 1
    for key, count in count_dict.items():
        if count % 2 == 1:
            numerators.append(key)
    for elem in numerators:
        if elem == -1:
            result *= int(pow(-1, (p - 1) // 2))
            continue

        if elem == 2:
            result *= int(pow(-1, (p * p - 1) // 8))
        else:
            result *= legendre_symbol(p, elem) * int(pow(-1, ((p - 1) // 2) * ((elem - 1) // 2)))

    return result
# Вероятностный алгоритм извлечения квадратного корня в поле Zp с арифметикой только этого поля.
def sq(a, p):
    if not sympy.isprime(p):
        return None
    if legendre_symbol(a, p) != 1:
        return None
    a = a % p
    q = p - 1
    m = 0
    while q % 2 == 0:
        q //= 2
        m += 1
    while True:
        b = random.randint(0, p - 1)
        if legendre_symbol(b, p) == -1:
            break
    buff = [a]
    k_buff = []
    while int(pow(buff[-1], q, p)) != 1:
        for k in range(p):
            if int(pow(buff[-1], int(pow(2, k, p)) * q, p)) == 1:
                k_buff.append(k)
                buff.append(buff[-1] * int(pow(b, int(pow(2, m - k_buff[-1], p)), p)) % p)
                break
    k_buff.append(0)
    buff.append(buff[-1] * int(pow(b, int(pow(2, m - k_buff[-1], p)), p)) % p)
    r = int(pow(buff[-1], (q + 1) // 2, p))
    for i in range(len(k_buff) - 1, -1, -1):
        l = reverse(int(pow(b, int(pow(2, m - k_buff[i] - 1, p)), p)), p)
        r = (r * l) % p
    return r
def test_function_choice(choice):
    if choice == 1:
        numerator = int(input("Введите числитель для разложения в цепную дробь: "))
        denominator = int(input("Введите знаменатель: "))
        result = continued_fraction(numerator, denominator)
        print(f"Результат разложения: {result}")
    elif choice == 2:
        a = int(input("Введите a: "))
        b = int(input("Введите b: "))
        c = int(input("Введите c: "))
        result = linear_diofant(a, b, c)
        if result == (0, 0):
            print("Числа не подходят, уравнение не разрешимо.")
        else:
            print(f"Решение уравнения: x = {result[0]}, y = {result[1]}")
    elif choice == 3:
        a = int(input("Введите a: "))
        b = int(input("Введите b: "))
        m = int(input("Введите m: "))
        result = compare(a, b, m)
        if result == 0:
            print("Уравнение не разрешимо.")
        else:
            print(f"Решение сравнения: x = {result}")
    elif choice == 4:
        a = int(input("Введите a: "))
        m = int(input("Введите m: "))
        result = reverse(a, m)
        if result is None:
            print("Уравнение не разрешимо.")
        else:
            print(f"Обратный элемент: {result}")
    elif choice == 5:
        a = int(input("Введите a: "))
        n = int(input("Введите n: "))
        result = jacobi_symbol(a, n)
        print(f"Символ Якоби: {result}")
    elif choice == 6:
        first = int(input("Введите первое число: "))
        second = int(input("Введите второе число (простое): "))
        result = legendre_symbol(first, second)
        if result is None:
            print(f"Второе число должно быть простым")
        else:
            print(f"Символ Лежандра: {result}")
    elif choice == 7:
        a = int(input("Введите a: "))
        p = int(input("Введите p (простое): "))
        result = sq(a, p)
        if result is None:
            print("Числа не подходят.")
        else:
            print(f"Квадратный корень: {result}")

def main():
    print("Выберите функцию для тестирования:")
    print("1. Разложение чисел в цепную дробь")
    print("2. Решение диофантовых уравнений ax - by = c")
    print("3. Решение линейных сравнений ax = b (mod m)")
    print("4. Вычисление обратного элемента в кольце вычетов Z_m")
    print("5. Вычисление символа Якоби")
    print("6. Вычисление символа Лежандра")
    print("7. Вероятностный алгоритм извлечения квадратного корня в поле Z_p")

    choice = int(input("Введите номер функции (1-7): "))
    
    if 1 <= choice <= 7:
        test_function_choice(choice)
    else:
        print("Неверный выбор. Пожалуйста, введите число от 1 до 7.")

if __name__ == "__main__":
    main()


# def legendre_symbol(a, p):
#     if not sympy.isprime(p):
#         return None
#     if a < 0:
#         a = -a
#         result = legendre_symbol(a, p) * (-1 if p % 4 == 3 else 1)
#         return result
#     a %= p
#     if a == 0:
#         return 0
#     if a == 1:
#         return 1
#     if a == 2:
#         if p % 8 == 1 or p % 8 == 7:
#             return 1
#         else:
#             return -1
#     if a % 2 == 0:
#         return legendre_symbol(2, p) * legendre_symbol(a // 2, p)
#     if a % 2 != 0:
#         return legendre_symbol(p, a) * (-1 if (p % 4 == 3 and a % 4 == 3) else 1)