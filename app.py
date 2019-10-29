import random
import os

def draw_one_parenthesis():
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

def fmt_parenthesis(par):
    """
    Using an (a, b, xi) tuple, returns the coresponding string
    to form (a*xi + b*xib)
    """
    return (
        "("
        f"{par[0]}"
        f"{'x' if par[2] else ''}"
        f"{'+' if par[1] > 0 else ''}"
        f"{par[1]}"
        f"{'x' if (1 - par[2]) else ''}"
        ")"
    )

def get_latex_start():
    """
    """
    return (
        "\\documentclass[a4paper]{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage[T1]{fontenc}\n"

        "\\begin{document}\n"
    )

def end_latex_doc(doc):
    """
    Appends the closing Latex syntax to the input doc
    represented by a single string.
    """
    return (
        doc
        + "\n\\end{document}"
    )

def add_latex_math(doc, expr):
    """
    Appends the math expression `expr` to the latex document `doc`,
    including the late math delimiters.
    """
    return (
        doc 
        + f"\\[{expr}\\]\n"
    )


if __name__ == '__main__':
    doc = get_latex_start()
    
    doc = add_latex_math(doc, fmt_parenthesis(draw_one_parenthesis()))
    doc = add_latex_math(doc, fmt_parenthesis(draw_one_parenthesis()))
    doc = add_latex_math(doc, fmt_parenthesis(draw_one_parenthesis()))

    doc = end_latex_doc(doc)

    with open('doc.tex', 'w') as f:
        f.write(doc)
    
    os.system("pdflatex doc.tex")
    