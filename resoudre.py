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

    string.replace("1x", "x")

    return string


def get_eq_deg1():
    """
    Return the correctly formatted string for a degree 1 equation in x.
    """
    params = get_params(4, 1, 10)
    string = fmt_deg1(*params[0:2])
    string += " = "
    string += fmt_deg1(*params[2:])
    return string


if __name__ == "__main__":
    print(get_eq_deg1())
