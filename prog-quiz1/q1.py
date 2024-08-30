def list_rotate(l, N):
    n = N%len(l)
    return l[n:] + l[:n]
