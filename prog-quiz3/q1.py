def mean(x, axis=0):
    n, m = len(x), len(x[0])
    avg0 = [0] * m  
    avg1 = [0] * n  
    for i in range(n):
        for j in range(m):
            avg0[j] += x[i][j] / n
            avg1[i] += x[i][j] / m
    if axis == 0:
        return avg0
    elif axis == 1:
        return avg1

'''
x=[[1,2],[3,4], [5,6]]
s1 = mean(x, axis=0)
s2 = [3, 4]
s = 0
for i in range(len(s2)):
  s += abs(s1[i]-s2[i])
if s < 0.01:
  print("PASS")
else:
  print("FAIL")
'''
