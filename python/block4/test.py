import numpy as np

rnd = np.random.rand(3, 3)
print(rnd)
# Как получить элемент из третьей строки и второго столбца двумерного массива A?
print(rnd[2, 1])
a = np.arange(5)
print(f"last element {a[-1]}")
b = np.arange(5)
print(a * b)
print(a[-2:])
print(np.multiply(a,2))
print(a*2)
a*=2
print(a)
print("{} {} {}".format(a.min(), np.min(a), np.amin(a)))
print(np.arange(0,21,2))
np.add(a,b)
print(np.sum([a,b], axis=0))
z = np.zeros(12)
print(z)
print(rnd.reshape(-1))
print(rnd.flatten())
print(rnd.ravel())
print("4x4")
print(np.random.randint(4, size=(4,4)))
print(np.random.random_sample((4,4)))

m=np.array([[0,1],[2,3]])
print("det(m)={}".format(np.linalg.det(m)))
e=np.array([[1,0],[0,1]])
print(np.dot(m,e))
# некорректное умножение матриц print(m*e)
c = np.arange(4)
d = c.reshape(2,2)
d[0] = 10
print(c)
print(d)

arr = np.array([22, 2, 4, 6, 8, 10, 12, 14, 16, 18])
print(np.where(arr>5))