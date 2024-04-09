import multiprocessing
from multiprocessing import Queue, Array, Value
from multiprocessing import Process


import time



#в процессах блокировщик нужно явно перdдавать, чтобы использовать его
def add_value(locker, data: Array, start, end: Value, result: Value):
    with locker:
        sum = 0
        # result.value = 0
        for i in range(start, end):
            sum = sum + data[i]
        result.value = sum


def fill_array(arr: Array):
		for i in range(len(arr)):
				arr[i] = 1


if __name__ == '__main__':

    lock = multiprocessing.Lock()

    N = int(5000000)
    arr = Array('d', N)					# массив из N элементов типа double ('d'), размещается в общей для процессов памяти

    print('Array initializing...')
    fill_array(arr)

    S1 = Value('d', 0.0)				# объект размещённый в общей памяти, хранит значение типа double
    S2 = Value('d', 0.0)
    S3 = Value('d', 0.0)  # объект размещённый в общей памяти, хранит значение типа double



    print('Calculating...')
    t0 = time.time()


    proc1 = Process(target = add_value, args=(lock, arr, 0, N//4, S1))
    proc2 = Process(target=add_value, args=(lock, arr, N//4, N // 2, S2))
    proc3 = Process(target=add_value, args=(lock, arr, N // 2, N, S3))
    proc1.start()
    proc2.start()
    proc3.start()

    proc1.join()
    proc2.join()
    proc3.join()


    print(f'Fineshed in {(time.time()-t0)} seconds')
    S = S1.value + S2.value + S3.value

    print(f'sum = {S}')

