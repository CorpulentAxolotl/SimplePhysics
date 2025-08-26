"""
this project calculates the ultimate velocity of a ball that roles on a curve
no friction
no air resistance
the 2d path of the center of mass of the ball can be modeled using f(x)
ball starts at x=s
ball starts with initial velocity v0
two types of options: `time (seconds)`, or x value (might be impossible, in which case will throw an error)
"""
from riemannsum import main as integral #a, b, f(x)
def X():
    v0 = 2 #m/s
    g = 9.8 #m/s^2
    def f(x):
        return 2**(-x)
    s = -2
    n = 6
    def derf(x):
        h=0.00001
        return (f(x+h)-f(x))/h
    def vel(x):
        return g/((1+1/(derf(x)**2))**(1/2))
    v1=integral(s,n,vel)
    print(f"ultimate velocity: {v0+v1}")
def T(v,g,p,t,FPS,f): #initial velocity, gravity, starting x, time(seconds)
    h = 0.00001
    def derf(x):
        return (f(x+h)-f(x))/h
    frames = []
    for _t in range(int(t/h)):
        prevp = p
        p+=v*h/(1+derf(p)**2)**(1/2)
        d = derf(prevp)
        v+=g*h*d**3/abs(d)/(1+d**2)**(1/2)
        if _t%(1/h/FPS)==0:
            frames.append(p)
    print(f"position: {p}, velocity: {v}")
    return frames
T(0,-10, -2, 20, 50, lambda x: x*x)
def nextT(p,v,g,FPS,f,μ):
    h=0.00001
    def derf(x):
        return (f(x+h)-f(x))/h
    
    for _t in range(int(1/h/FPS)):
        prevp=p
        p+=v*h/(1+derf(p)**2)**(1/2)
        d = derf(prevp)
        v+=g*h*d**3/abs(d)/(1+d**2)**(1/2)
        N=g*h*d/(1+d**2)**(1/2)
        v*=(1-abs(N*μ/v))
    return p, v
def nextN(p,v,g,FPS,f):
    h=0.00001
    def derf(x):
        return (f(x+h)-f(x))/h
    for _t in range(int(1/h/FPS)):
        prevp=p
        p+=v*h/(1+derf(p)**2)**(1/2)
        d = derf(prevp)
        v+=g*h*d/(1+d**2)**(1/2)
    return v


    
