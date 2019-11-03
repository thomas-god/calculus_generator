import random


def get_params(n, n_zeros, int_max):
    """
    """
    params = [random.randint(-int_max, int_max) for i in range(n - n_zeros)] + [
        0
    ] * n_zeros
    random.shuffle(params)
    return params


def fmt_deg1(a, b):
    """
    ax + b
    """
    if a == 0 and b == 0:
        string = "0"
    elif a != 0 and b > 0:
        string = f"{a}x + {b}"
    elif a != 0 and b < 0:
        string = f"{a}x  {b}"
    elif a == 0:
        string = f"{b}"
    elif b == 0:
        string = f"{a}x"

    string = string.replace("1x", "x")
    string = string.replace("-1x", "-x")

    return string


def fmt_deg2(a, b, c):
    """
    ax² + bx + c
    """
    if a == 0:
        string = fmt_deg1(b, c)
    elif (b > 0) or (b == 0 and c > 0):
        string = f"{a}x^2 + " + fmt_deg1(b, c)
    elif (b < 0) or (b == 0 and c < 0):
        string = f"{a}x^2" + fmt_deg1(b, c)
    else:
        string = "0"

    string = string.replace("1x^2", "x^2")
    string = string.replace("-1x^2", "-x^2")

    return string


def get_eq_deg1():
    """
    Return the correctly formatted string for a degree 1 equation in x.
    ax + b = cx + d
    """
    params = get_params(4, 1, 10)
    string = fmt_deg1(*params[0:2])
    string += " = "
    string += fmt_deg1(*params[2:])
    return string


def get_eq_deg2():
    """
    Return the correctly formatted string for a degree 2 equation in x.
    ax² + bx + c = dx² + ex + f
    """
    params = get_params(6, 2, 10)
    while params[0] == 0 and params[3] == 0:
        params = get_params(6, 2, 10)
    string = fmt_deg2(*params[0:3])
    string += " = "
    string += fmt_deg2(*params[3:])
    return string


if __name__ == "__main__":
    print(get_eq_deg2())
