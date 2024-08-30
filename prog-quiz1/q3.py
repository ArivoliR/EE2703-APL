import io
def countfruits(msg):
    dict = {}
    sfp = io.StringIO(msg)
    for line in sfp.readlines():
        if len(line.split())==2:
            fruit = line.split()[0]
            if fruit in dict:
                dict[fruit]+=int(line.split()[1])
            else:
                dict[fruit]=int(line.split()[1])
    return dict
            

