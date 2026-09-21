def matrix_maker():
    row = int(input("number of rows?"))
    col = int(input("number of columns?"))
    matrix = []
    for nr in range(row):
        x = []
        for nc in range(0, col, 1):
            num = input(f"input row {nr+1}, col {nc+1}?")
            num = int(num)
            x.append(num)
        matrix.append(x)

    print(matrix)
    return(matrix)

def plus_minus_matrix(matrix_a, matrix_b, symbol="+"):
    if not (len(matrix_a) == len(matrix_b) and len(matrix_a[0]) == len(matrix_b[0])):
        return None
    
    matrix_sum = []
    for x in range(len(matrix_a)):
        placeholder = []
        for y in range(0, len(matrix_a[0]), 1):
            if symbol == "-":
                placeholder.append(int(matrix_a[x][y]) - int(matrix_b[x][y]))
            placeholder.append(int(matrix_a[x][y]) + int(matrix_b[x][y]))
        matrix_sum.append(placeholder)
    return matrix_sum
    
def scalar_multiplication_matrix(matrix_a = 0, matrix_b = 0, scalar = 2):
    matrix_a_scalar = []
    for x in range(len(matrix_a)):
        placeholder = []
        for y in range(0, len(matrix_a[0]), 1):
            placeholder.append(scalar *int(matrix_a[x][y]))
        matrix_a_scalar.append(placeholder)
    matrix_b_scalar = []
    for x in range(len(matrix_b)):
        placeholder = []
        for y in range(0, len(matrix_b[0]), 1):
            placeholder.append(scalar *int(matrix_b[x][y]))
        matrix_b_scalar.append(placeholder)
    return(matrix_a_scalar, matrix_b_scalar)

def matrix_multily_matrix(matrix_a, matrix_b):
    rowa = len(matrix_a)
    cola = len(matrix_a[0])
    rowb = len(matrix_b)
    colb = len(matrix_b[0])
    if cola != rowb:
        return None
    
    total_matrix = []
    for x in range(rowa):
        total_matrix.append([])
        for y in range(colb):
            sum = 0
            for i in range(cola):
                sum += (matrix_a[x][i]) * (matrix_b[i][y])
            total_matrix[-1].append(sum)

    return(total_matrix)

def row_sum(matrix_a, matrix_b=[]):
    len_row_a = len(matrix_a)
    len_col_a = len(matrix_a[0])
    sum = 0
    for i in range(len_row_a):
        for j in range(len_col_a):
            sum += matrix_a[i][j]
        
        print(f"sum of row {i} is {sum}")
        sum = 0

def col_sum(matrix_a, matrix_b=[]):
    len_row_a = len(matrix_a)
    len_col_a = len(matrix_a[0])
    sum = 0
    for i in range(len_row_a):
        for j in range(len_col_a):
            sum += matrix_a[j][i]
        
        print(f"sum of col {i} is {sum}")
        sum = 0

def diagonal_sum(matrix_a, matrix_b=[]):
    len_row_a = len(matrix_a)
    len_col_a = len(matrix_a[0])
    sum = 0
    if len_row_a != len_col_a:
        print("unmathable")
        return None
    for i in range(len_row_a):
        sum += matrix_a[i][i]
        
    print(f"sum of col {i} is {sum}")
    sum = 0
    
if __name__ == "__main__":
    # matrix_a = matrix_maker()
    # matrix_b = matrix_maker()
    # matrix_sub = plus_minus_matrix(matrix_a, matrix_b, "-")
    # matrix_add = plus_minus_matrix(matrix_a, matrix_b)
    # matrix_a_scalar, matrix_b_scalar = scalar_multiplication_matrix(matrix_a, matrix_b, 3)
    # print(matrix_multily_matrix(matrix_a, matrix_b))
    # row_sum(matrix_a)
    # col_sum(matrix_a)
    # diagonal_sum(matrix_a)
    pass