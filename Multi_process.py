import multiprocessing
import time

# Hàm xét điều kiện so sánh
def cmp(a, b):
    return a < b

# Hàm merge để kết hợp 2 mảng con lại thành 1 mảng đã sắp xếp
def merge(left, right):
    sorted_arr = []     # List lưu lại kết quả
    i, j = 0, 0         # Tạo giá trị cho index i của left, j của right
    while i < len(left) and j < len(right):
        if cmp(left[i], right[j]):      # Thêm các phần tử theo thứ tự
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1
    sorted_arr.extend(left[i:]) # Thêm phần còn lại của left nếu còn
    sorted_arr.extend(right[j:])# Thêm phần còn lại của right nếu còn

    return sorted_arr

# Hàm merge sort truyền thống
def merge_sort(arr):
    if len(arr) <= 1:   # Điểm trả về trong đệ quy
        return arr
    # Khởi tạo các giá trị cần
    mid = len(arr) // 2 
    left = arr[:mid]
    right = arr[mid:]

    left_sorted = merge_sort(left)  # Sắp xếp phần bên trái
    right_sorted = merge_sort(right)# Sắp xếp phần bên phải

    return merge(left_sorted, right_sorted)

# Hàm merge sort trong xử lý song song
def parallel_merge_sort(arr):
    if len(arr) <= 1:   # Điểm trả về nếu như mảng quá bé
        return arr

    num_processes = multiprocessing.cpu_count() # Số lượng cpu trong máy (trong máy của em là 16)
    child_size = len(arr) // num_processes      # Kích thước của các mảng con

    if child_size == 0:    # Tránh trường hợp mảng quá bé
        child_size = 1

    with multiprocessing.Pool(processes=num_processes) as pool: # Tạo các pool để chạy song song
        childs = [arr[i:i+child_size] for i in range(0, len(arr), child_size)]  # Chia mảng con thành các phần vô các cpu khác nhau
        sorted_childs = pool.map(merge_sort, childs)    # Đưa mảng con vào từng cpu để giải quyết bằng merge sort truyền thống
        # Kết hợp các mảng con đã được sắp xếp cho tới khi chỉ còn 1 mảng duy nhất
        while len(sorted_childs) > 1:
            ans = []     # Lưu các mảng con được sắp xếp
            for i in range(0, len(sorted_childs), 2):   # Xét từng cặp mảng con
                if i+1 < len(sorted_childs):
                    merged = merge(sorted_childs[i], sorted_childs[i+1])    # Merge lại
                else:
                    merged = sorted_childs[i]       # Nếu không có đôi có cặp thì thêm vào luôn
                ans.append(merged)
            sorted_childs = ans

        return sorted_childs[0]

#Bắt đầu chương trình
# Thêm vào để đảm bảo rằng chương trình sẽ chạy trực tiếp
if __name__ == '__main__':
    test_size = 100000 # Điều chỉnh số lượng trong 1 test case
    test_num = 10    # Điều chỉnh số lượng bộ test

    test_case = []  # Lưu các bộ test
    with open('test_case.txt', mode='r') as file:
        for i in range(test_num):
            # Lấy dữ liệu từng test case
            trash_line = file.readline()        # Bỏ dòng đánh dấu
            data = file.readline()              # Đọc dữ liệu               
            data = data.split(' ')[:-1]         # Tách dữ liệu thành list
            data = [int(var) for var in data]   # Chuyển kiểu dữ liệu thành số nguyên
            test_case.append(data)              # Thêm vào test case

    for i, test in enumerate(test_case):        # Thử với từng bộ test case
        # Đo thời gian bằng thuật toán gốc
        start_time = time.time()                # Đếm thời gian chạy của từng bộ test
        sort_arr = merge_sort(test)    # Lấy kết quả lưu vào sort_arr
        end_time = time.time()

        execution_time = end_time - start_time  # Tính toán thời gian chạy cho từng test case
        print("Time to run test case {}: {} seconds by non-parallel.".format(i, execution_time))
        # Đo thời gian chạy bằng thuật toán song song
        start_time = time.time()                # Đếm thời gian chạy của từng bộ test
        sort_arr = parallel_merge_sort(test)    # Lấy kết quả lưu vào sort_arr
        end_time = time.time()

        execution_time = end_time - start_time  # Tính toán thời gian chạy cho từng test case
        print("Time to run test case {}: {} seconds by parallel.".format(i, execution_time))