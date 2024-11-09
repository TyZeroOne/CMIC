import random
# Тест Ферма
def fermat_primality_test(n, k=5):
    if n <= 1:
        return False
    if n == 2:
        return True
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True
# Тест Миллера-Рабина
def miller_rabin(n, k):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

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
# Тест Соловея-Штрассена
def solovay_strassen_test(n, k=5):
    if n <= 2:
        return n == 2
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 1)
        jacobi = jacobi_symbol(a, n)
        mod_exp = pow(a, (n - 1) // 2, n)

        if jacobi == 0 or mod_exp != (jacobi % n):
            return False
    return True

def primality_test_interface():
    print("Выберите тест на простоту числа:")
    print("1. Тест Ферма")
    print("2. Тест Миллера-Рабина")
    print("3. Тест Соловея-Штрассена")
    
    choice = int(input("Введите номер теста: "))

    n = int(input("Введите число, которое нужно проверить на простоту: "))
    k = int(input("Введите количество итераций: "))

    if choice == 1:
        result = fermat_primality_test(n, k)
        if result:
            print(f"Результат: число {n}, вероятно, простое.")
        else:
            print(f"Результат: число {n} составное.")
    
    elif choice == 2:
        result = miller_rabin(n, k)
        if result:
            print(f"Результат: число {n}, вероятно, простое.")
        else:
            print(f"Результат: число {n} составное.")
    
    elif choice == 3:
        result = solovay_strassen_test(n, k)
        if result:
            print(f"Результат: число {n}, вероятно, простое.")
        else:
            print(f"Результат: число {n} составное.")
    
    else:
        print("Неверный выбор.")

primality_test_interface()
