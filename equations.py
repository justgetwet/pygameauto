
def quadratic_equation(a, b, c):

    # x0, x1 = 0., 0.
    d = b**2 - 4*a*c
    if a == 0:
        if b == 0:
            return []
        x = -c / b
        return [x]
    if d == 0:
        x = -b / (2.0*a)
        return [x]
    if d < 0:
        return []
    else:
        x0 = (-b + d**0.5) / (2.0*a)
        x1 = (-b - d**0.5) / (2.0*a)

    return [x0, x1]
