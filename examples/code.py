from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

#
# Индивидуальное задание 1 (часть 1)
#

# %display latex
# from IPython.display import display, Markdown

fio = 'Фамилия И.О.' #отредактировать тут

import random
import hashlib
seed = int(hashlib.blake2b(bytes(fio, 'utf-8')).hexdigest(), 16)
random.seed(seed)
q = random.choice([4, 7, 8, 8, 8, 9, 11, 13, 17, 19])
#F.<z> = GF(q)

# display(Markdown(f"""В качестве поля используется ${latex(F)}$,
#                 а в качестве неприводимого многочлена (если q не простое) - ${latex(F.polynomial())}$
#                 """))

# генерация матрицы G
# rand_nonzero = lambda: F.multiplicative_generator()^randint(0, q-1)
# A = matrix([[1,0,0,rand_nonzero()], [0,1,0,rand_nonzero()], [0,0,1,rand_nonzero()]])
# B = matrix([rand_nonzero() for i in range(4)])
# D1 = [1,1,1,1]; D2=D1; D3=D1; 
# D4 = [F.multiplicative_generator()^randint(1, q-2) for i in range(4)]
# G = random_matrix(F, 4, algorithm="unimodular") * block_matrix([
#     [A * diagonal_matrix(F, D1), A*diagonal_matrix(D2)],
#     [B * diagonal_matrix(D3), B*diagonal_matrix(D4)],
# ]) * diagonal_matrix([rand_nonzero() for i in range(8)])
# G.permute_columns(Permutations(8).random_element())

# display(G)
#G

# при выполнении задания можно использовать SageMath
# например, элементарные преобразования строк реализуются
# A = identity_matrix(5)
# display(A)
# A.add_multiple_of_row(1,0,4) #добавляет к первой строке нулевую, умноженную на 4
# display(A)





#
# Индивидуальное задание 1 (часть 2)
#

# !wget https://mmcs.sfedu.ru/images/stories/main_img.jpg
im = Image.open("main_img.jpg")
im.convert("RGB")
print(im.size)
im

arr = np.array(im)
arr[0, 0]  #значения яркости цветов в позиции (0,0)

# редактирование картинки
import random

for i in range(50, 150):
    for j in range(150, 350):
        arr[i,j][0] = random.randint(0,255) #красный цвет
        arr[i,j][2] = 0 #синий цвет

plt.figure(figsize=(10, 6), dpi=80)
plt.imshow(arr)
plt.show()

# редактирование картинки
import random

for i in range(50, 150):
    for j in range(150, 350):
        arr[i,j][0] = random.randint(0,255) #красный цвет
        arr[i,j][2] = 0 #синий цвет

plt.figure(figsize=(10, 6), dpi=80)
plt.imshow(arr)
plt.show()

#доступ к последним битам:
print("было: ", arr[0, 0] % 2)
#замена последнего бита для красного цвета на 1
arr[0, 0][0] += -(arr[0, 0][0] % 2) + 1
print("стало: ", arr[0, 0] % 2)

#сохранение изображения
im2 = Image.fromarray(arr)
im2.save("out.png")
