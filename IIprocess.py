__author__ = "Самаев Антон ИВТ-21"

import multiprocessing
import random
import time

# процессы не имеют общей памяти
# они могут взаимодействовать друг с другом [неявно] используя средства ОС
# зато, в отличии от потоков в Python, они могут выполнятся ||

#в процессах блокировщик нужно явно передавать, чтобы использовать его
def add_value(locker, array, index):
    with locker:
        num = random.randint(0, 20)
        vtime = time.ctime() #текущее время
        array[index] = num
        print(f"array[{index}] = {num}, sleep = {vtime}")
        time.sleep(1)


#Это надо для того, чтобы наш модуль можно было безопасно подключать в другие модули и при этом не создавались новые процессы без нашего ведома
if __name__ == '__main__':

    #mutex
    lock = multiprocessing.Lock()

    #массив из 10 элементов типа int ("i"), размещается в общей для процессов памяти
    arr = multiprocessing.Array("i", range(10))

    #список процессов, используется в дальнейшем для join()
    process = []

    for i in range(10):
        pr = multiprocessing.Process(target=add_value, args=(lock, arr, i, ))
        process.append(pr)
        pr.start()

    #ожидание завершения работы всех процессов
    for i in process:
        i.join()


    print(list(arr))