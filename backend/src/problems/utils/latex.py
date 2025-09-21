def matrix_to_latex(matrix):
    latex = r"\begin{bmatrix}"
    for i,row in enumerate(matrix):
        rows = [str(x) for x in row]
        latex += " & ".join(rows)
        if i < len(matrix) - 1:
            latex+= r"\\"
    latex += r"\end{bmatrix}"
    return latex
 