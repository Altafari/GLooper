def feed_range(start, end, step):
    tol = 1.0e-7
    delta = end - start
    sign = copysign(1, delta)
    step = copysign(step,  delta)
    x = start
    res = []
    while (x * sign - end * sign) < -tol:
        res.append(x)
        x += step
    return res