import numpy as np

# ── Размерности и данные ──────────────────────────────────
p, m, q = 2, 2, 2

np.random.seed(1)
A = np.random.uniform(-1, 1, (p, m))
B = np.random.uniform(-1, 1, (m, q))
E = np.random.uniform(-1, 1, (1, m))
G = np.random.uniform(-1, 1, (p, q))

print("Исходные матрицы:")
print("A =\n", A)
print("B =\n", B)
print("E =\n", E)
print("G =\n", G)

# ── Базовые операции нечёткой логики ─────────────────────
def imp(x, y):
    """Импликация Лукасевича: x ~> y = min(1, 1 - x + y)"""
    return min(1, 1 - x + y)

def equiv(x, y):
    """Эквиваленция: x ~ y = min(x, y)"""
    return min(x, y)

def conj(x, y):
    r"""Конъюнкция (t-норма Лукасевича): x /~\ y = max(0, x + y - 1)"""
    return max(0, x + y - 1)

def prod_over_k(values):
    r"""Произведение по всем k: /~\k"""
    return np.prod(values)

def union_over_k(values):
    r"""Нечёткое объединение (t-конорма): \\~/k"""
    return 1 - np.prod(1 - np.array(values))

# ── Ввод времён операций ──────────────────────────────────
operation3_time  = int(input("Введите время для x /~\\ y и x (~) y: "))
sum_time         = int(input("Введите время для суммы: "))
implication_time = int(input("Введите время для импликации: "))
product_time     = int(input("Введите время для произведения: "))
negation_time    = int(input("Введите время для разности: "))

# ── Трассировка ЯПФ для C[0,0] ───────────────────────────
L_sum = 0
L_avg = 0
r = 94  # финальный ранг

# NOTICE: в L_avg первое число — количество операций,
# второе — время типа операции, третье — ранг операции

def compute_C11(A, B, E, G):
    global L_sum, L_avg

    # first layer
    impl_ab  = imp(A[0,0], B[0,0])   # rank 2
    impl_ba  = imp(B[0,0], A[0,0])   # rank 2
    impl_ab_ = imp(A[0,1], B[1,0])   # rank 2
    impl_ba_ = imp(B[1,0], A[0,1])   # rank 2

    L_sum += 4 * implication_time
    L_avg += (4 * implication_time * 2) / r

    # second layer
    impl_4   = impl_ab * 4            # rank 3
    E_11_2   = E[0,0] * 2            # rank 2
    impl_4_  = impl_ab_ * 4           # rank 3
    E_12_2   = E[0,1] * 2            # rank 2

    L_sum += 4 * product_time
    L_avg += (2 * product_time * 2 + 2 * product_time * 3) / r

    # third layer
    impl_4_2   = impl_4 - 2           # rank 4
    E_11_2_1   = E_11_2 - 1          # rank 3
    impl_4_2_  = impl_4_ - 2          # rank 4
    E_12_2_1   = E_12_2 - 1          # rank 3

    L_sum += 4 * negation_time
    L_avg += (2 * negation_time * 4 + 2 * negation_time * 3) / r

    # fourth layer
    temp1        = E[0,0] * impl_4_2       # rank 5
    impl_ab_E_11 = E_11_2_1 * impl_ab     # rank 5
    temp2        = E[0,1] * impl_4_2_      # rank 5
    impl_ab_E_11_= E_12_2_1 * impl_ab_    # rank 5

    L_sum += 4 * product_time
    L_avg += (4 * product_time * 5) / r

    # fifth layer
    temp1_1  = temp1 + 1               # rank 6
    part1_1  = impl_ab_E_11 * E[0,0]  # rank 6
    temp2_1  = temp2 + 1               # rank 6
    part1_2  = impl_ab_E_11_ * E[0,1] # rank 6

    L_sum += 2 * product_time + 2 * sum_time
    L_avg += (2 * product_time * 6 + 2 * sum_time * 6) / r

    # sixth layer
    temp  = impl_ba * temp1_1          # rank 8
    temp_ = impl_ba_ * temp2_1         # rank 8
    E11   = 1 - E[0,0]                # rank 2
    E12   = 1 - E[0,1]                # rank 2

    L_sum += 2 * product_time + 2 * negation_time
    L_avg += (2 * product_time * 8 + 2 * negation_time * 2) / r

    # seventh layer
    part2_1 = temp * E11               # rank 10
    part2_2 = temp_ * E12              # rank 10
    d1      = conj(A[0,0], B[0,0])    # rank 2
    d2      = conj(A[0,1], B[1,0])    # rank 2

    L_sum += 2 * product_time + 2 * operation3_time
    L_avg += (2 * product_time * 10 + 2 * operation3_time * 2) / r

    # eighth layer
    f111 = part2_1 + part1_1           # rank 16
    f112 = part2_2 + part1_2           # rank 16
    d1_1 = 1 - d1                      # rank 3
    d2_1 = 1 - d2                      # rank 3

    L_sum += 2 * negation_time + 2 * sum_time
    L_avg += (2 * negation_time * 3 + 2 * sum_time * 16) / r

    # ninth layer
    f_prod = f111 * f112               # rank 32
    Pk     = d1_1 * d2_1              # rank 6

    L_sum += 2 * product_time
    L_avg += (product_time * 32 + product_time * 6) / r

    # tenth layer
    G1   = 1 - G[0,0]                 # rank 2
    G_3  = G[0,0] * 3                 # rank 2
    d11  = 1 - Pk                     # rank 7

    L_sum += 2 * negation_time + product_time
    L_avg += (negation_time * 2 + product_time * 2 + negation_time * 7) / r

    # eleventh layer
    d11_3 = d11 * 3                   # rank 8
    df    = conj(d11, f_prod)         # rank 39
    G_32  = G_3 - 2                   # rank 3

    L_sum += product_time + operation3_time + negation_time
    L_avg += (product_time * 8 + operation3_time * 39 + negation_time * 3) / r

    # twelfth layer
    GG_32 = G_32 * G[0,0]            # rank 4
    df4   = df * 4                    # rank 40

    L_sum += 2 * product_time
    L_avg += (product_time * 4 + product_time * 40) / r

    # thirteenth layer
    part_c_1 = GG_32 * f_prod        # rank 36
    dd4      = df4 - d11_3           # rank 48

    L_sum += product_time + negation_time
    L_avg += (product_time * 36 + negation_time * 48) / r

    # fourteenth layer
    dd4g = dd4 * G[0,0]              # rank 49

    L_sum += product_time
    L_avg += (product_time * 49) / r

    # fifteenth layer
    ddd4g = dd4g + d11               # rank 56

    L_sum += sum_time
    L_avg += (sum_time * 56) / r

    # sixteenth layer
    part_c_2 = ddd4g * G1            # rank 58

    L_sum += product_time
    L_avg += (product_time * 58) / r

    # seventeenth layer
    C_11 = part_c_2 + part_c_1       # rank 94

    L_sum += sum_time
    L_avg += (sum_time * 94) / r

    return C_11


C_11 = compute_C11(A, B, E, G)
print(f"\nC_11    = {C_11}")
print(f"L_sum   = {L_sum}")
print(f"L_avg   = {L_avg}")
print(f"D       = {L_sum / L_avg}")

# ── Полное вычисление матрицы C ───────────────────────────
def compute_f_ijk(a, b, e):
    """f_ijk через импликации Лукасевича"""
    imp_ab = imp(a, b)
    imp_ba = imp(b, a)
    term1  = imp_ab * (2*e - 1) * e
    term2  = imp_ba * (1 + (4*imp_ab - 2) * e) * (1 - e)
    return term1 + term2

def compute_C_ij(i, j, A, B, E, G):
    """Вычисление одного элемента C[i,j]"""
    f_list, d_list = [], []

    for k in range(m):
        a, b, e = A[i, k], B[k, j], E[0, k]
        d_list.append(conj(a, b))
        f_list.append(compute_f_ijk(a, b, e))

    prod_f = prod_over_k(f_list)
    d_ij   = union_over_k(d_list)
    comb   = conj(prod_f, d_ij)
    g      = G[i, j]

    termA = prod_f * (3*g - 2) * g
    termB = (1 - g) * (d_ij + (4*comb - 3*d_ij) * g)
    return termA + termB


C = np.zeros((p, q))
for i in range(p):
    for j in range(q):
        C[i, j] = compute_C_ij(i, j, A, B, E, G)

print("\nРезультирующая матрица C:")
print(C)