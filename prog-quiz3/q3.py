def dedup(l):
    s,t = set(), []
    for i in l:
        if i not in s:
            t.append(i)
            s.add(i)
    return t


'''
if (r == e):
  print("PASS")
else:
  print("FAIL")
'''
