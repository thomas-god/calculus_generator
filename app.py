import random
import os
import sqlite3
from gen_db import init_db, insert_parenthesis

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

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    cur_set = (
        random.sample(set_n, 1)[0],
        random.sample(set_n, 1)[0],
        random.randint(0, 1)
    )

    idx = insert_parenthesis(c, *cur_set)

    conn.commit()
    conn.close()
    return cur_set, idx

def get_multi_set():
    """
    Concatenate 2 (a*xi + b*xib) set2 and returns a list of tuples.
    """
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    random.seed(1234)
    flag = True
    while flag:
        parenthesis = [get_one_set() for i in range(2)]
        idx_1, idx_2 = parenthesis[0][1], parenthesis[1][1]
        try:
            c.execute("INSERT INTO exercices VALUES (?, ?)", (idx_1, idx_2))
        except sqlite3.IntegrityError:
            print("Trying to insert a record that already exists.")
            conn.rollback()
        else:
            print("New record successfully into exercices table.")
            conn.commit()
            flag = False
    
    conn.close()
    return [parenthesis[0][0], parenthesis[1][0]]

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
    init_db()
    
    doc = get_latex_start()
    
    for i in range(10):
        doc = add_latex_math(doc, fmt_multi_set(get_multi_set()))
    
    doc = end_latex_doc(doc)

    with open('doc.tex', 'w') as f:
        f.write(doc)
    
    os.system("pdflatex doc.tex")
