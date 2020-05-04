def _floats_equal(first, second):
    eps = 0.000001
    return abs(first - second) < eps
