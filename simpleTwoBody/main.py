import pygame
from simulation import update
from simulation import update2
import math

FPS = 50
SIZE = 20
qsize = 20
gsize = qsize/5
duration = 20

pygame.init()

screen_width = 900
screen_height = screen_width
my_font = pygame.font.SysFont('Arial', 30)
my_font2 = pygame.font.SysFont('Arial', 10)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()

earth = [
    0,
    1,
    5.972E+27,
    -math.pi/4,
    1E+5,
    0]

earth2 = [
    -384.4E+6/5,
    -384.4E+6/5,
    5.972E+27]
initvel = 1.022E+5/3
moon = [
    -384.4E+6/5,
    0,
    7.34767309E+25,
    math.pi/2,
    0,
    0]

entities = [[],[]]
entities[0] = earth
entities[1] = earth2
step = 1E-3
384.4E+6
factor = screen_width/2/384.4E+6
_line = [(screen_width/2+moon[0]*factor,screen_height/2+moon[1]*factor)]
running = True
pause = False
focus = 0
while running:

    # event stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            _line = [((screen_width/2+moon[0]*factor,screen_height/2+moon[1]*factor))]
            x, y = pygame.mouse.get_pos()
            entities[focus][0]=(x-screen_width/2)/factor + screen_width/2
            entities[focus][1]=(y-screen_height/2)/factor + screen_height/2
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_p]:
                if pause:
                    pause = False
                else:
                    pause = True
            if pygame.key.get_pressed()[pygame.K_1]:
                if focus != len(entities)-1:
                    focus += 1
                else:
                    focus = 0
            
        
    screen.fill((255,255,255))
    if not pause:
        for _ in range(int(1/step/FPS)*100):
            entities, moon = update2(entities,moon,step)
    x_t = my_font.render("X: "+str(round(moon[0]))+" m", False, (0, 0, 0))
    screen.blit(x_t, (0,0)) 
    y_t = my_font.render("Y: "+str(round(moon[1]))+" m", False, (0, 0, 0))
    screen.blit(y_t, (0,40)) 
    s_t = my_font.render("Velocity: "+str(round(moon[4]))+" m/s", False, (0, 0, 0))
    screen.blit(s_t, (0,80)) 
    _line.append((screen_width/2+moon[0]*factor,screen_height/2+moon[1]*factor))

    num = 0
    for i in entities:
        if focus == num:
            color = "black"
        else:
            color = "green"
        pygame.draw.circle(screen, color, (screen_width/2+i[0]*factor,screen_height/2+i[1]*factor),20)
        
        
        num += 1
    pygame.draw.circle(screen,"grey",(screen_width/2+factor*moon[0],screen_height/2+factor*moon[1]),10)
    pygame.draw.lines(screen,"blue",False,_line,2)
    pygame.display.flip()
    #i+=1

    clock.tick(FPS)
pygame.quit()
