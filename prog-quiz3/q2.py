import io
def csv_countfruits(msg):
    sfp = io.StringIO(msg)
    sfp.readline()
    dict = {}
    for line in sfp.readlines():
        fruit = line.split(',')[0]
        if fruit in dict:
            dict[fruit]+=int(line.split(',')[1])
        else:
            dict[fruit]=int(line.split(',')[1])
    return dict

'''
msg = """Fruit,Number
Apple,3
Orange,5
Banana,4
Apple,7
Apple,2
Banana,3
"""
X = csv_countfruits(msg)
Exp = {'Apple': 12, 'Banana': 7, 'Orange': 5}
for i in Exp.keys():
  if Exp[i] != X[i]:
    print("FAIL")
print("PASS")
'''
