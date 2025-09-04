elapsed = (25) / 1000

YVelo = -50
XVelo = -70

if YVelo > 0:
    Ydist = (YVelo * elapsed) + ((0.5 * (-280)) * (elapsed * elapsed))
else:
    Ydist = (YVelo * elapsed) + ((0.5 * (280)) * (elapsed * elapsed))

if YVelo > 0:
    Xdist = (XVelo * elapsed) + ((0.5 * (-225)) * (elapsed * elapsed))
else:
    Xdist = (XVelo * elapsed) + ((0.5 * (225)) * (elapsed * elapsed))

print(Ydist)
print(Xdist)

Ydist = (YVelo * elapsed) 
Xdist = (XVelo * elapsed)

print(Ydist)
print(Xdist)