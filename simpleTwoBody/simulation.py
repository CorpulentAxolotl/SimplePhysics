import math

def main():
        earth = [1,1,1]
        earth[0] = 0
        earth[1] = 1
        earth[2] = 5.972E+27
        moon = [1,1,1,1,1,1]
        initvel = 1.022E+3
        moon[0] = -384.4E+6
        moon[1] = 0
        moon[2] = math.pi/2
        moon[3] = initvel
        moon[4] = 7.34767309E+25
        moon[5] = 0
        entities = [[]]
        entities[0] = earth
        time = 36; #seconds
        step = 1E-5
        for _ in range(int(time/step)):
            moon = update(entities,moon,step)
        print()
        print("pos-x: %g km, pos-y: %g km" % (moon[0]/1000, moon[1]/1000))
        print("dvel: %g m/s, Distance: %g km" % ((moon[3]-initvel),moon[5]/1000))
        print("Pricision: %f, Time: %f seconds" % (step,time))
        print()

def update(ent, obj, step):
        posx = obj[0]
        posy = obj[1]
        m1 = obj[2]
        _dir = obj[3]
        vel = obj[4]
        dist = obj[5]
        #move
        newvelx = vel*math.cos(_dir)
        newvely = vel*math.sin(_dir)

        for i in range(len(ent)):
            xd = ent[i][0]-posx
            yd = ent[i][1]-posy
            m2 = ent[i][2]
            d = math.sqrt(xd*xd+yd*yd)
            a = 6.67430E-11*m2/d/d
            newvelx += a*step*xd/d
            newvely += a*step*yd/d
            if newvelx == 0:
                newvelx = step*step
        if newvelx > 0:
            newdir = math.atan(newvely/newvelx)
        else:
            newdir = math.atan(newvely/newvelx) + math.pi
        
        dx = step*vel*math.cos(_dir)
        dy = step*vel*math.sin(_dir)
        dist += (dx*dx+dy*dy)**(1/2)
        posx += dx
        posy += dy
        vel = (newvelx*newvelx+newvely*newvely)**(1/2)
        _dir = newdir
        out = [1,1,1,1,1,1]
        out[0] = posx
        out[1] = posy
        out[2] = m1
        out[3] = _dir
        out[4] = vel
        out[5] = dist
        return out
def update2(ent, obj, step):
    ent.append(obj)
    for i in range(len(ent)):
        for a in range(6):
            if a >= len(ent[i]):
                ent[i].append(0)
    new_ent = ent
    for i in range(len(ent)):
        #0: x
        #1: y
        #2: mass
        #3: direction
        #4: velocity
        #5: distance traveled
        posx = ent[i][0]
        posy = ent[i][1]
        newvelx = ent[i][4]*math.cos(ent[i][3])
        newvely = ent[i][4]*math.sin(ent[i][3])
        for a in range(len(ent)):
            if a == i:
                continue
            xd = ent[a][0]-posx
            yd = ent[a][1]-posy
            m2 = ent[a][2]
            d = math.sqrt(xd*xd+yd*yd)
            a = 6.67430E-11*m2/d/d
            newvelx += a*step*xd/d
            newvely += a*step*yd/d
            if newvelx == 0:
                newvelx = step*step
        if newvelx > 0:
            newdir = math.atan(newvely/newvelx)
        else:
            newdir = math.atan(newvely/newvelx) + math.pi
        
        dx = step*ent[i][4]*math.cos(ent[i][3])
        dy = step*ent[i][4]*math.sin(ent[i][3])
        new_ent[i][5] += (dx*dx+dy*dy)**(1/2)
        new_ent[i][0] += dx
        new_ent[i][1] += dy
        new_ent[i][4] = (newvelx*newvelx+newvely*newvely)**(1/2)
        new_ent[i][3] = newdir
    return new_ent[:-1], new_ent[-1]

