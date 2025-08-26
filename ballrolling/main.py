import pygame
from simulation import T as generateTime
from simulation import nextT as genNext
from simulation import nextN as genNorm
import math
#environmental variables
FPS = 50
SIZE = 20
qsize = 20
gsize = qsize/5
duration = 20

dx=0.00001

def f(x):
    return math.sin(x)
def derf(x):
    return (f(x+dx)-f(x))/dx
pygame.init()
my_font = pygame.font.SysFont('Arial', 30)
screen_width = 900
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption('Ball Rolling')
running = True
fpoints = [(screen_width/2,screen_width*4/5-f(0)*qsize)]
f2points = []
for i in range(int(screen_width/2/qsize*gsize)):
    fpoints.append((screen_width/2 + (i/gsize)*qsize, screen_width*4/5 - round(f(i/gsize),4)*qsize))
    fpoints.insert(0,(screen_width/2 - (i/gsize)*qsize, screen_width*4/5 - round(f(-i/gsize),4)*qsize))
    if derf(i/gsize) > 0:
        f2points.append((screen_width/2 + (i/gsize)*qsize+SIZE/(1+1/derf(i/gsize)**2)**(1/2), screen_width*4/5 - round(f(i/gsize),4)*qsize+SIZE/derf(i/gsize)/(1+1/derf(i/gsize)**2)**(1/2)))
    elif derf(i/gsize) <= 0:
        f2points.append((screen_width/2 + (i/gsize)*qsize-SIZE/(1+1/derf(i/gsize)**2)**(1/2), screen_width*4/5 - round(f(i/gsize),4)*qsize-SIZE/derf(i/gsize)/(1+1/derf(i/gsize)**2)**(1/2)))
    if derf(-i/gsize) > 0:
        f2points.insert(0,(screen_width/2 - (i/gsize)*qsize+SIZE/(1+1/derf(-i/gsize)**2)**(1/2), screen_width*4/5 - round(f(-i/gsize),4)*qsize+SIZE/derf(-i/gsize)/(1+1/derf(-i/gsize)**2)**(1/2)))
    if derf(-i/gsize) <= 0:
        f2points.insert(0,(screen_width/2 - (i/gsize)*qsize-SIZE/(1+1/derf(-i/gsize)**2)**(1/2), screen_width*4/5 - round(f(-i/gsize),4)*qsize-SIZE/derf(-i/gsize)/(1+1/derf(-i/gsize)**2)**(1/2)))

frames = generateTime(4,-9.8,20,duration,FPS,f)
#i=0
v=-40
g=-9.8
p=-2
μ=0.2
m=10 #kg
Max = 0
cycle = []
positive = v >= 0
while running:

    # event stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            p = (x-screen_width/2)/qsize
        
    screen.fill((255,255,255))
    pygame.draw.lines(screen,(200,200,255),False,fpoints,5)
    pygame.draw.lines(screen,"black",False,f2points)
    pygame.draw.circle(screen, "blue", (screen_width/2+p*qsize,screen_width*4/5-f(p)*qsize),SIZE)
    vel_text = my_font.render("Velocity: "+str(round(v,3))+" m/s", False, (0, 0, 0))
    pos_text = my_font.render("Position: "+str(round(p,3))+" m", False, (0, 0, 0))
    μ_text = my_font.render("Friction Coefficient: "+str(μ), False, (0, 0, 0))
    screen.blit(vel_text, (0,0)) 
    screen.blit(pos_text, (0,40))
    screen.blit(μ_text, (0,80))
    pygame.draw.lines(screen,"red",False,[(screen_width/2+p*qsize,screen_width*4/5-f(p)*qsize),(screen_width/2+p*qsize+v,screen_width*4/5-f(p)*qsize-derf(p)*v)],3)
    pygame.draw.lines(screen,"green",False,[(screen_width/2+p*qsize,screen_width*4/5-f(p)*qsize),(screen_width/2+p*qsize,screen_width*4/5-f(p)*qsize-g*5)],3)
    nm = genNorm(p,v,g,FPS,f)
    #pygame.draw.lines(screen,"blue",False,[(screen_width/2+p*qsize,screen_width*4/5-f(p)*qsize),(screen_width/2+p*qsize-nm,screen_width*4/5-f(p)*qsize-nm/derf(p))],3)
    pygame.draw.lines(screen,"yellow",False,[(screen_width/2+p*qsize,screen_width*4/5-f(p)*qsize),(screen_width/2+p*qsize-nm,screen_width*4/5-f(p)*qsize+derf(p)*nm)],3)
    
    p, v = genNext(p,v,g,FPS,f,μ)
    if positive and v < 0:
        Max = max(cycle)
        cycle = []
        positive = False
    elif not positive and v >= 0:
        Max = max(cycle)
        cycle = []
        positive = True
    cycle.append(abs(v))
    max_text = my_font.render("Maximum Velocity: " + str(round(Max,3)) + " m/s", False, (0, 0, 0))
    screen.blit(max_text, (0,120))

    
    
    #pygame.draw.circle(screen, "blue", 
                       #(screen_width/2 + (frames[int(i%(FPS*duration))])*qsize,screen_width*4/5-f(frames[int(i%(FPS*duration))])*qsize), SIZE)
    pygame.display.flip()
    #i+=1
    clock.tick(FPS)
pygame.quit()
