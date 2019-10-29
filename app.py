import random
import os

def get_one_set():
    """
    Draw parameters defining a parenthesis object (a*xi + b*xib) with
    xib = 1 - xi. a and b are non-zero integers while xi is a boolean 
    indicating the presence of x.

    Example
    -------
    (2, -1, 1) defines (2*x - 1).

    Outputs
    -------
    params : tuple,
        (a, b, xi)
    """
    n = 10
    set_n = list(range(-n, n + 1))
    set_n.remove(0)

    return (
        random.sample(set_n, 1)[0],
        random.sample(set_n, 1)[0],
        random.randint(0, 1)
    )

def get_multi_set(n_set_max):
    """
    Concatenate up to `n_set_max` (a*xi + b*xib) set and returns a list of tuples.
    """
    if n_set_max < 2:
        raise ValueError('`n_set_max` must be at least 2.')
    n = random.randint(2, n_set_max)
    return [get_one_set() for i in range(n)]

def fmt_one_set(in_set):
    """
    Using an (a, b, xi) tuple, returns the coresponding string
    to form (a*xi + b*xib)
    """
    return (
        "("
        f"{in_set[0]}"
        f"{'x' if in_set[2] else ''}"
        f"{'+' if in_set[1] > 0 else ''}"
        f"{in_set[1]}"
        f"{'x' if (1 - in_set[2]) else ''}"
        ")"
    )

def fmt_multi_set(mult_set):
    """
    Format each element from a list of sets and concatenate them.
    """
    str_mult_set = ""
    for in_set in mult_set:
        str_mult_set += fmt_one_set(in_set)
    return str_mult_set



def get_latex_start():
    """
    """
    return (
        "\\documentclass[a4paper]{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage[T1]{fontenc}\n"

        "\\begin{document}\n"

        "\\begin{itemize}\n"
    )

def end_latex_doc(doc):
    """
    Appends the closing Latex syntax to the input doc
    represented by a single string.
    """
    return (
        doc
        + "\n\\end{itemize}"
        + "\n\\end{document}"
    )

def add_latex_math(doc, expr):
    """
    Appends the math expression `expr` to the latex document `doc`,
    including the late math delimiters.
    """
    return (
        doc 
        + f"\\item ${expr}$\n"
    )


if __name__ == '__main__':
    doc = get_latex_start()
    
    for i in range(10):
        doc = add_latex_math(doc, fmt_multi_set(get_multi_set(2)))
    
    doc = end_latex_doc(doc)

    with open('doc.tex', 'w') as f:
        f.write(doc)
    
    os.system("pdflatex doc.tex")
    