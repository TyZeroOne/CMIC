# Обычный алгоритм Евклида
def normal_Euclid(a, b):
    while a !=0 and b != 0:
        if a > b:
            a = a % b
        else: 
            b = b % a
    return a + b
# Расширенный алгоритм Евклида
def extended_Euclid(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return a, x, y
# Бинарный алгоритм Евклида
def binary_Euclid(a, b):
    if a == 0:
        return b
    elif b == 0 or a == b:
        return a
    elif a == 1 or b == 1:
        return 1
    elif a % 2 == 0 and b % 2 == 0:
        return 2 * binary_Euclid(a / 2, b / 2)
    elif a % 2 == 0 and b % 2 != 0:
        return binary_Euclid(a / 2, b)
    elif a % 2 != 0 and b % 2 == 0:
        return binary_Euclid(a, b / 2)
    elif a % 2 != 0 and b % 2 != 0:
        if b > a:
            return binary_Euclid((b - a) / 2, a)
        else:
            return binary_Euclid((a - b) / 2, b)
# Поиск обратного элемента
def mod_inverse(z, m):
    gcd, x, _ = extended_Euclid(z, m)
    return inv_elem(x, m)
def inv_elem(x, m):
    if x < 0:
        x = x + m
    return x % m
inv_elem(-5, 4)
# Китайская теорема об остатках
def chinese_theorem(a, m):
    M = 1
    for num in m:
        M *= num
    M_j = []
    for i in range(len(m)):
        M_j.append(M / m[i])
    z = []
    for i in range(len(M_j)):
        z.append((mod_inverse(M_j[i], m[i]) * a[i]) % m[i])
    x = 0
    for i in range(len(z)):
        x += M_j[i] * z[i]
    return x % M
# Алгоритм Гарнера
def Garner_algorithm(a, m):
    c = [0] * len(m)
    for i in range(1, len(m)):
        c[i] = 1
        for j in range(i):
            u = mod_inverse(m[j], m[i])
            c[i] = (u * c[i]) % m[i]
    u = a[0]
    x = u
    for i in range(1, len(m)):
        u = (a[i] - x) * c[i]
        if u < 0:
            u += m[i]
        u %= m[i]
        m_j = 1
        for j in range(i):
            m_j *= m[j]
        x += u * m_j
    return x
# Метод Гаусса
def gauss_jordan_modul(matrix, mod):
    n = len(matrix)
    m = len(matrix[0]) - 1  
    row_idx = 0  
    for col_idx in range(m):
        # Найдем строку с ненулевым ведущим элементом
        pivot_row = None
        for i in range(row_idx, n):
            if matrix[i][col_idx] != 0:
                pivot_row = i
                break
        if pivot_row is None:
            continue
        # Меняем строки местами, если нужно
        if pivot_row != row_idx:
            matrix[row_idx], matrix[pivot_row] = matrix[pivot_row], matrix[row_idx]
        # Приведение ведущего элемента к единице
        inv = mod_inverse(matrix[row_idx][col_idx], mod)
        for k in range(m + 1):
            matrix[row_idx][k] = (matrix[row_idx][k] * inv) % mod
        # Обнуление всех элементов в текущем столбце, кроме ведущего
        for i in range(n):
            if i != row_idx and matrix[i][col_idx] != 0:
                factor = matrix[i][col_idx]
                for k in range(m + 1):
                    matrix[i][k] = (matrix[i][k] - factor * matrix[row_idx][k]) % mod
        # Удаление нулевых строк
        matrix = [row for row in matrix if any(row[:-1])]
        # Увеличиваем индекс строки для следующей итерации
        row_idx += 1
        # Обновляем количество строк n, так как могли удалить нулевые строки
        n = len(matrix)
    return matrix
# Приведение матрицы к виду для поля
def reverse_matrix(matrix, m):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = inv_elem(matrix[i][j], m)
    return matrix

def algorithm_interface():
    def input_numbers():
        a = int(input("Введите первое число: "))
        b = int(input("Введите второе число: "))
        return a, b

    def input_chinese_theorem():
        a = list(map(int, input("Введите список коэффициентов a через пробел: ").split()))
        m = list(map(int, input("Введите список модулей m через пробел: ").split()))
        return a, m

    def input_matrix():
        rows = int(input("Введите количество строк матрицы: "))
        cols = int(input("Введите количество столбцов матрицы (включая правую часть): "))
        matrix = []
        for i in range(rows):
            row = list(map(int, input(f"Введите строку {i + 1} через пробел: ").split()))
            matrix.append(row)
        mod = int(input("Введите модуль для расчетов: "))
        return matrix, mod

    def explain_extended_Euclid(a, b, gcd, x, y):
        explanation = f"Расширенный алгоритм Евклида для чисел {a} и {b}:\nНОД({a}, {b}) = {gcd}\n"
        explanation += f"Линейное разложение: {gcd} = {x} * {a} + {y} * {b}\n"
        return explanation

    def explain_gauss(matrix, mod):
        print("Решение системы методом Гаусса:")
        num_vars = len(matrix[0]) - 1  
        num_rows = len(matrix)
        for row in matrix:
            print(" + ".join(f"{el}*x{i + 1}" for i, el in enumerate(row[:-1])) + f" = {row[-1]}")
        partial_solution = {}
        for i in range(num_rows, num_vars):
            value = int(input(f"Введите значение для частной переменной x{i + 1}: "))
            partial_solution[f'x{i + 1}'] = value
        complete_solution = [0] * num_vars
        for row in reversed(matrix):
            lead_idx = None
            for i in range(len(row) - 1):
                if row[i] != 0:
                    lead_idx = i
                    break
            if lead_idx is None:
                continue
            result = row[-1]  
            for i in range(lead_idx + 1, len(row) - 1):
                if f'x{i + 1}' in partial_solution:
                    result -= row[i] * partial_solution[f'x{i + 1}']
                else:
                    result -= row[i] * complete_solution[i]
            if mod != 0:
                result = (result % mod + mod) % mod
            if row[lead_idx] != 0:
                complete_solution[lead_idx] = result // row[lead_idx] if mod == 0 else (result * mod_inverse(row[lead_idx], mod)) % mod
        for i in range(num_rows, num_vars):
            complete_solution[i] = partial_solution[f'x{i + 1}']
        print("Частное решение:")
        for i in range(num_vars):
            print(f"x{i + 1} = {complete_solution[i]}")

    while True:
        print("\nВыберите алгоритм:")
        print("1. Обычный алгоритм Евклида")
        print("2. Расширенный алгоритм Евклида")
        print("3. Бинарный алгоритм Евклида")
        print("4. Метод Гаусса")
        print("5. Алгоритм Гарнера")
        print("6. Китайская теорема об остатках")
        print("7. Выход")

        choice = int(input("Ваш выбор: "))

        if choice == 1:
            a, b = input_numbers()
            result = normal_Euclid(a, b)
            print(f"НОД({a}, {b}) = {result}")

        elif choice == 2:
            a, b = input_numbers()
            gcd, x, y = extended_Euclid(a, b)
            explanation = explain_extended_Euclid(a, b, gcd, x, y)
            print(explanation)

        elif choice == 3:
            a, b = input_numbers()
            result = binary_Euclid(a, b)
            print(f"НОД({a}, {b}) с помощью бинарного алгоритма = {result}")

        elif choice == 4:
            matrix, mod = input_matrix()
            matrix = reverse_matrix(matrix, mod)
            result_matrix = gauss_jordan_modul(matrix, mod)
            explain_gauss(result_matrix, mod)

        elif choice == 5:
            a, m = input_chinese_theorem()
            result = Garner_algorithm(a, m)
            print(f"Решение системы по алгоритму Гарнера: x = {result}")

        elif choice == 6:
            a, m = input_chinese_theorem()
            result = chinese_theorem(a, m)
            print(f"Решение системы по Китайской теореме об остатках: x = {result}")

        elif choice == 7:
            print("Выход.")
            break

        else:
            print("Некорректный выбор, попробуйте снова.")
algorithm_interface()
  
# print(normal_Euclid(33, 5))
# print(extended_Euclid(33, 5)[0])
# print(binary_Euclid(33, 5))
# # Пример запуска интерфейса
# 
# mod = 7 
# matrix = [
#     [2, 3, 4, 5],  # 2x + 3y + 4z = 5
#     [1, 1, 1, 6],  # x + y + z = 6
#     [3, 4, 5, 7],  # 3x + 4y + 5z = 7
# ]
# matrix2 = [[1, 0, 5, 3, 2], [2, 5, 0, 4, 1], [0, 2, 3, 2, 3]]
# result = gauss_jordan_modulo(matrix2, mod)
