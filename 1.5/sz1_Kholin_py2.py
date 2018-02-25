#!/bin/bash
# -*- coding: utf-8 -*-

import numpy as np

print '1.Создать \"шахматную доску\" на numpy'
n = 5
m = 5
a = np.array([[(x + y + 1) % 2 for x in range(m)] for y in range(n)])
print a

print "2.Создать случайный вектор и занулить три самых больших по модулю значения"
n = 5
a = np.random.rand(n)
print a
b = abs(a)
for i in range(3):
    j = np.argmax(b)
    a[j] = 0
    b[j] = 0
    print j
print a

print "3.Диагональная матрица с квадратами натуральных чисел"
n = 5
a = np.diag([x * x for x in range(1, n + 1)])
print a

print "4.Змейка"
n = 5
m = 5
a = np.array([[x * n + y + 1 for x in range(m)] for y in range(n)])
print a

print "5.Евклидово расстояние между вектором и всеми строчками матрицы"
n = 5
m = 5
a = np.array([[x * n + y + 1 for x in range(m)] for y in range(n)])
b = np.array(range(1, m + 1))
print a
print b
c = a - b
c = c * c
d = np.sum(c, axis=1)
print np.sqrt(d)

print "6.Косинусное расстояние между вектором и всеми строчками матрицы. Косинусное расстояние для векторов"
n = 5
m = 5
a = np.array([[x * n + y + 1 for x in range(m)] for y in range(n)])
b = np.array(range(1, m + 1))
print a
print b
d1 = np.sqrt(np.sum(a * a, axis=1))
d2 = np.sqrt(np.sum(b * b))
c = (np.sum(a * b, axis=1) / (d1 * d2))
print c
