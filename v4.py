import matplotlib.pyplot as plt
import numpy as np
import math

# Исходные параметры
d = 0.5
b = [i / 100 for i in range(1, 50)]
N = 10**4

# Аналитический способ
M = [b[i] / (d - b[i]) for i in range(len(b))]

# Решение системы
K = [10, 100, 1000]
for i in range(3):
    right = [0 for j in range(K[i] - 1)] + [1]
    population = []  #Массив состоящий из значения популяции на каждом шаге
    for j in range(len(b)): #Цикл по всем значения b
        matrix, counter = [], 0 #Счетчик коэфициентов
        for k in range(K[i]): #Цикл по строкам матрицы
            s = [0 for q in range(K[i] + 1)]#Формирование строки
            if k == 0: #Для первой строки
                s[0], s[1] = -b[j], d
            else:
                s[0 + counter], s[1 + counter], s[2 + counter] = b[j], round(-b[j] - d, 2), d
                counter += 1
            matrix.append(s[0:len(s) - 1])
        for q in range(len(matrix[-1])):
            matrix[-1][q] = 1 #Для каждого столбца меняем элементы последней строчки на 1
        pi = np.linalg.solve(matrix, right) #Решаем СЛАУ
        population.append(sum([pi[m] * m for m in range(len(pi))])) #Добавляем полученное среднее число особей в популяцию

    name = 'Решение СЛАУ при K = ' + str(K[i])
    plt.figure(1)
    plt.semilogy(b, population)

    plt.figure()
    plt.semilogy(b, population, '.-')
    plt.grid()
    plt.title(name)
    plt.xlabel('Вероятность рождения')
    plt.ylabel('Среднее число популяции')

# Имитационное моделирование
y = []
for i in range(len(b)): #Цикл по значения вероятности смерти
    population, counter = [], 0  # Число популяции
    probabilities = np.random.uniform(0, 1, N) #Массив случайных чисел
    interval = [d, d + b[i], 1]  #Интервалы в которые мы попадаем
    for j in range(N):
        if counter == 0: #Если число популяуии = 0 проверяем только вероятность рождения
            if interval[0] < probabilities[j] <= interval[1]: #Если текущая вероятность меньше или равна вероятности рождения и больше вероятности гибели
                counter += 1 #увеличиваем популяцию на 1
            population.append(counter)
        else:
            if probabilities[j] <= interval[0]:# Если вероятность меньше или равна вероятности смерти
                counter -= 1 # Уменьшаем число популяции
            elif interval[0] < probabilities[j] <= interval[1]:
                counter += 1
            population.append(counter)
    y.append(sum(population) / N)
    if b[i] == 0.4:
        plt.figure()
        plt.plot([i for i in range(100)], population[0:100], '.-')
        print((sum(population[0:100])))
        plt.grid()
        name = 'Случайный процесс при b = ' + str(b[i])
        plt.title(name)
        plt.xlabel('Номер шага')
        plt.ylabel('Число особей')

# Графики
plt.figure()
plt.semilogy(b, M)
plt.grid()
plt.legend(['Вероятность гибели 0.5'])
plt.title('Аналитическое решение')
plt.xlabel('Вероятность рождения')
plt.ylabel('Среднее число популяции')

plt.figure()
plt.semilogy(b, y, '.-')
plt.plot(b, y)
plt.grid()
plt.title('Имитационное моделирование')
plt.xlabel('Вероятность рождения')
plt.ylabel('Среднее число популяции')

plt.figure(1)
plt.semilogy(b, M, b, y)
plt.grid()
plt.title('Все виды анализа системы')
plt.xlabel('Вероятность рождения')
plt.ylabel('Среднее число популяции')
plt.legend(['Решение СЛАУ при К = 10', 'Решение СЛАУ при К = 100', 'Решение СЛАУ при К = 1000', 'Аналитическое решение', 'Имитационное моделирование'])
plt.show()


