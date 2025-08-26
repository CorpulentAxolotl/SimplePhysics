def main(a,b,f):
    p = [a,b]
    r = p[1]-p[0]
    w = 0.000001
    _sum=0
    for i in range(int(r/w)):
        _sum+=f(p[0]+i*w)*w
    _sum = round(_sum,3)
    return(_sum)
