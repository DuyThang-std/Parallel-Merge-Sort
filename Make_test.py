import numpy as np

test_size = 100000 # Điều chỉnh số lượng trong 1 test case
test_num = 10    # Điều chỉnh số lượng bộ test
with open('test_case.txt', mode='w') as file:       # Tạo file để lưu bộ test
    for i in range(test_num):                       # Tạo từng bộ test 
        file.write('test case {}: \n'.format(i))    # Đánh dấu thứ tự các bộ test

        for i in range(test_size):
            variable = np.random.randint(low=0, high=test_size) # Random giá trị cho bộ test
            file.write(str(variable) + ' ')

        file.write('\n')
file.close