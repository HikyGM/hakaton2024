from random import randint, choice, randrange, choices, sample


def addition(max_sum=99, complexity=2):
    values = []
    for _ in range(complexity):
        values.append(randint(0, max_sum))
    problem = f'{"+".join([str(i) for i in values])}'
    solution = sum(values)
    return problem, solution


def subtraction(max_minuend=99, max_diff=99, complexity=2):
    values = []
    solution = randint(0, max_minuend)
    values.append(solution)
    for _ in range(complexity - 1):
        current_value = randint(max(0, (solution - max_diff)), solution)
        solution -= current_value
        values.append(current_value)
    problem = f'{"-".join([str(i) for i in values])}'
    return problem, solution


def multiplication(max_multi=12, complexity=2):
    values = []
    solution = randint(0, max_multi)
    values.append(solution)
    for _ in range(complexity - 1):
        current_value = randint(0, max_multi)
        solution *= current_value
        values.append(current_value)
    problem = f'{"\cdot".join([str(i) for i in values])}'
    return problem, solution


def division(max_a=25, max_b=25, complexity=2):
    values = []
    a = randint(1, max_a)
    solution = a
    for _ in range(complexity - 1):
        current_value = randint(1, max_b)
        a *= current_value
        values.append(current_value)
    problem = f'{a}\div{"\div".join([str(i) for i in values])}'
    return problem, solution


def complex_quadratic(max_range=10):
    d = -1
    while d < 0:
        a = randrange(1, max_range)
        b = randrange(1, max_range)
        c = randrange(1, max_range)
        d = (b ** 2 - 4 * a * c)
    eq = ''
    if a == 1:
        eq += 'x^2 + '
    else:
        eq += str(a) + 'x^2 + '
    if b == 1:
        eq += 'x + '
    else:
        eq += str(b) + 'x + '
    eq += str(c) + ' = 0'
    problem = f'Найдите корни данного квадратного уравнения\n\n${eq}$'

    s_root1 = round((-b + (d) ** 0.5) / (2 * a), 2)
    s_root2 = round((-b - (d) ** 0.5) / (2 * a), 2)
    if s_root1 - int(s_root1) == 0:
        s_root1 = int(s_root1)
    if s_root2 - int(s_root2) == 0:
        s_root2 = int(s_root2)
    solution = ';'.join([str(s_root1), str(s_root2)])
    return problem, solution


def system_of_equations(range_x=10, range_y=10, coeff_mult_range=10):
    x = randint(-range_x, range_x)
    y = randint(-range_y, range_y)
    c1 = [1, 0, x]
    c2 = [0, 1, y]

    def randNonZero():
        return choice(
            [i for i in range(-coeff_mult_range, coeff_mult_range) if i != 0])

    c1_mult = randNonZero()
    c2_mult = randNonZero()
    new_c1 = [c1[i] + c1_mult * c2[i] for i in range(len(c1))]
    new_c2 = [c2[i] + c2_mult * c1[i] for i in range(len(c2))]
    c1_mult = randNonZero()
    c2_mult = randNonZero()
    new_c1 = [new_c1[i] + c1_mult * c1[i] for i in range(len(c1))]
    new_c2 = [new_c2[i] + c2_mult * c2[i] for i in range(len(c2))]

    def coeffToFuncString(coeffs):
        x_sign = '-' if coeffs[0] < 0 else ''
        x_coeff = str(abs(coeffs[0])) if abs(coeffs[0]) != 1 else ''
        x_str = f'{x_sign}{x_coeff}x' if coeffs[0] != 0 else ''
        op = ' - ' if coeffs[1] < 0 else (' + ' if x_str != '' else '')
        y_coeff = abs(coeffs[1]) if abs(coeffs[1]) != 1 else ''
        y_str = f'{y_coeff}y' if coeffs[1] != 0 else (
            '' if x_str != '' else '0')
        return f'{x_str}{op}{y_str} = {coeffs[2]}'

    problem = f"Дано ${coeffToFuncString(new_c1)}$ и ${coeffToFuncString(new_c2)}$, найдите $x$ и $y$."
    solution = ';'.join([str(x), str(y)])
    return problem, solution


def factorial(max_input=10):
    problem = randint(0, max_input)
    n = problem
    solution = 1
    while problem != 1 and n > 0:
        solution *= n
        n -= 1
    return f'{problem}!', solution


def cube_root(min_no=1, max_no=1000):
    b = randint(min_no, max_no)
    solution = b ** (1 / 3)
    problem = rf"\sqrt[3]{{{b}}}"
    return problem, round(solution, 2)


def square_root(min_no=1, max_no=1000):
    b = randint(min_no, max_no)
    solution = b ** (1 / 2)
    problem = rf"\sqrt[2]{{{b}}}"
    return problem, round(solution, 2)


def square(max_square_num=20):
    a = randint(1, max_square_num)
    solution = a ** 2
    problem = f'{a}^2'
    return problem, solution


def divide_fractions(max_val=10):
    a = randint(1, max_val)
    b = randint(1, max_val)

    while (a == b):
        b = randint(1, max_val)

    c = randint(1, max_val)
    d = randint(1, max_val)
    while (c == d):
        d = randint(1, max_val)

    def calculate_gcd(x, y):
        while (y):
            x, y = y, x % y
        return x

    tmp_n = a * d
    tmp_d = b * c

    gcd = calculate_gcd(tmp_n, tmp_d)
    sol_numerator = tmp_n // gcd
    sol_denominator = tmp_d // gcd

    return rf'\frac{{{a}}}{{{b}}}\div\frac{{{c}}}{{{d}}}', sol_numerator / sol_denominator


def fraction_multiplication(max_val=10):
    a = randint(1, max_val)
    b = randint(1, max_val)
    c = randint(1, max_val)
    d = randint(1, max_val)

    while (a == b):
        b = randint(1, max_val)

    while (c == d):
        d = randint(1, max_val)

    def calculate_gcd(x, y):
        while (y):
            x, y = y, x % y
        return x

    tmp_n = a * c
    tmp_d = b * d

    gcd = calculate_gcd(tmp_n, tmp_d)

    problem = rf"\frac{{{a}}}{{{b}}}\cdot\frac{{{c}}}{{{d}}}"
    if (tmp_d == 1 or tmp_d == gcd):
        solution = tmp_n / gcd
    else:
        solution = tmp_n // gcd / tmp_d // gcd
    return problem, solution


def simplify_square_root(max_variable=100):
    x = randint(1, max_variable)
    factors = {}
    f = 2
    while x != 1:
        if x % f == 0:
            if f not in factors:
                factors[f] = 0
            factors[f] += 1
            x /= f
        else:
            f += 1
    a = b = 1
    for i in factors.keys():
        if factors[i] & 1 == 0:
            a *= i ** (factors[i] // 2)
        else:
            a *= i ** ((factors[i] - 1) // 2)
            b *= i
    if a == 1 or b == 1:
        return simplify_square_root(max_variable)
    else:
        return rf'{a}\sqrt{{{b}}}', a * b ** 0.5


def basic_algebra(max_variable=10):
    a = randint(1, max_variable)
    b = randint(1, max_variable)
    c = randint(b, max_variable)

    # calculate gcd
    def calculate_gcd(x, y):
        while (y):
            x, y = y, x % y
        return x

    i = calculate_gcd((c - b), a)
    x = ((c - b) // i) / (a // i)

    if (c - b == 0):
        x = 0
    elif a == 1 or a == i:
        x = c - b

    problem = f"{a}x + {b} = {c}"
    solution = round(x, 2)
    return problem, solution

def log(max_base=3, max_val=8):
    a = randint(1, max_val)
    b = randint(2, max_base)
    c = pow(b, a)

    problem = f'log_{{{b}}}({c})'
    solution = a
    return problem, solution