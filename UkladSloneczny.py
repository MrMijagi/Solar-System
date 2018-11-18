#!/usr/bin/env python

import pygame,sys, math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pygame import *
from sys import exit
from math import *

width = 1366
height = 768
clock = pygame.time.Clock()

translateX = 0.0
translateY = 0.0
translateZ = 0.0

cameraX = 0.0
cameraY = 10.0
cameraZ = 0.0

mouseAngle = [0,0]

angleX = 0.0
angleY = 0.0
angleZ = 0.0

currentPlanet = 0
eyeX = 0.0
eyeZ = 0.0
eyeY = 0.0

scaleWsp = 1.0
matrixScale = [scaleWsp,0,0,0,0,scaleWsp,0,0,0,0,scaleWsp,0,0,0,0,1]
matrixTranslate = [1,0,0,0,0,1,0,0,0,0,1,0,translateX,translateY, translateZ,1]
matrixRotate = [cos(radians(angleY))*cos(radians(angleZ)), (-sin(radians(angleY))*-sin(radians(angleX))*cos(radians(angleZ)))+(cos(radians(angleX))*sin(radians(angleZ))), (cos(radians(angleX))*-sin(radians(angleY))*cos(radians(angleZ)))+(sin(radians(angleX))*sin(radians(angleZ))),0,cos(radians(angleY))*-sin(radians(angleZ)),(-sin(radians(angleY))*-sin(radians(angleX))*-sin(radians(angleZ)))+(cos(radians(angleX))*cos(radians(angleZ))), (cos(radians(angleX))*-sin(radians(angleY))*-sin(radians(angleZ)))+(sin(radians(angleX))*cos(radians(angleZ))), 0, sin(radians(angleY)), -sin(radians(angleX))*cos(radians(angleY)), cos(radians(angleX))*cos(radians(angleY)), 0, 0, 0, 0, 1]
squaresAmount = 90

stateOrbity = True
stateLights = False

slonce = [0.0, 2.32, 0.0, 0.05,0.0,0.0, (1,1,0)]
merkury = [5.0,0.1, 1.0, 0.11,0.0,0.0]
wenus = [6.0, 0.2, 0.5,0.48,0.0,0.0]
ziemia = [7.0, 0.2, 0.25, 0.04,0.0,0.0]
mars = [8.0, 0.1, 0.125, 0.048,0.0,0.0]
jowisz = [11.0, 1.0, 0.05, 0.01,0.0,0.0]
saturn = [13.0, 0.8, 0.0025,0.02,0.0,0.0]
uran = [15.0, 0.6, 0.0012,0.034,0.0,0.0]
neptun = [17.0, 0.4, 0.0006, 0.032,0.0,0.0]
planety = [slonce, merkury, wenus, ziemia, mars, jowisz, saturn, uran, neptun] #Wiem, ze Slonce nie jest planeta :P
images = ['sunmap.jpg', 'mercurymap.jpg', 'venusmap.jpg', 'earthmap1k.jpg', 'mars_1k_color.jpg', 'jupitermap.jpg', 'saturnmap.jpg', 'uranusmap.jpg', 'neptunemap.jpg']
textures = range(len(images))

def InitGL(Width, Height):
    global cameraX, cameraY, cameraZ, translateX, translateY, translateZ, squaresAmount, stateLights
    
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_TEXTURE_2D)
    
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glFrontFace(GL_CW)
    
    glLightfv(GL_LIGHT0, GL_DIFFUSE,(1,1,1,0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,(1,1,1,0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,(1,0,0,0))
    glLightfv(GL_LIGHT0, GL_POSITION,(0,1,0,1))
    glEnable(GL_LIGHT0)
    if stateLights:
        glEnable(GL_LIGHTING)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 400.0)
    gluLookAt(cameraX, cameraY, cameraZ, 0,0,0, 0,1,0)
    
    glNewList(1,GL_COMPILE)
    glBegin(GL_LINES)
    for i in range(180):
        glNormal3f(sin(radians(i*2)), 0,cos(radians(i*2)))
        glVertex3f(sin(radians(i*2)), 0,cos(radians(i*2)))
        glNormal3f(sin(radians((i+1)*2)), 0,cos(radians((i+1)*2)))
        glVertex3f(sin(radians((i+1)*2)), 0,cos(radians((i+1)*2)))
    glEnd()
    glEndList()
    
    glNewList(2,GL_COMPILE)
    glBegin(GL_QUADS)
    for j in range(squaresAmount):
        for i in range(squaresAmount):
            glNormal3f(sin(radians(i * (360 / squaresAmount))) * sin(radians(j * (180 / squaresAmount))),
                       cos(radians(j * (180 / squaresAmount))),
                       cos(radians(i * (360 / squaresAmount))) * sin(radians(j * (180 / squaresAmount))))
            glTexCoord2f(float((squaresAmount - i)) / float(squaresAmount),
                         float((squaresAmount - j)) / float(squaresAmount))
            glVertex3f(sin(radians(i * (360 / squaresAmount))) * sin(radians(j * (180 / squaresAmount))),
                       cos(radians(j * (180 / squaresAmount))),
                       cos(radians(i * (360 / squaresAmount))) * sin(radians(j * (180 / squaresAmount))))
            glNormal3f(
                sin(radians((i + 1) * (360 / squaresAmount))) * sin(radians(j * (180 / squaresAmount))),
                cos(radians(j * (180 / squaresAmount))),
                cos(radians((i + 1) * (360 / squaresAmount))) * sin(radians(j * (180 / squaresAmount))))
            glTexCoord2f(float((squaresAmount - (i + 1))) / float(squaresAmount),
                         float((squaresAmount - j)) / float(squaresAmount))
            glVertex3f(
                sin(radians((i + 1) * (360 / squaresAmount))) * sin(radians(j * (180 / squaresAmount))),
                cos(radians(j * (180 / squaresAmount))),
                cos(radians((i + 1) * (360 / squaresAmount))) * sin(radians(j * (180 / squaresAmount))))
            glNormal3f(
                sin(radians((i + 1) * (360 / squaresAmount))) * sin(radians((j + 1) * (180 / squaresAmount))),
                cos(radians((j + 1) * (180 / squaresAmount))),
                cos(radians((i + 1) * (360 / squaresAmount))) * sin(radians((j + 1) * (180 / squaresAmount))))
            glTexCoord2f(float((squaresAmount - (i + 1))) / float(squaresAmount),
                         float((squaresAmount - (j + 1))) / float(squaresAmount))
            glVertex3f(
                sin(radians((i + 1) * (360 / squaresAmount))) * sin(radians((j + 1) * (180 / squaresAmount))),
                cos(radians((j + 1) * (180 / squaresAmount))),
                cos(radians((i + 1) * (360 / squaresAmount))) * sin(radians((j + 1) * (180 / squaresAmount))))
            glNormal3f(
                sin(radians(i * (360 / squaresAmount))) * sin(radians((j + 1) * (180 / squaresAmount))),
                cos(radians((j + 1) * (180 / squaresAmount))),
                cos(radians(i * (360 / squaresAmount))) * sin(radians((j + 1) * (180 / squaresAmount))))
            glTexCoord2f(float((squaresAmount - i)) / float(squaresAmount),
                         float((squaresAmount - (j + 1))) / float(squaresAmount))
            glVertex3f(
                sin(radians(i * (360 / squaresAmount))) * sin(radians((j + 1) * (180 / squaresAmount))),
                cos(radians((j + 1) * (180 / squaresAmount))),
                cos(radians(i * (360 / squaresAmount))) * sin(radians((j + 1) * (180 / squaresAmount))))

    glEnd()
    glEndList()
    
    glMatrixMode(GL_MODELVIEW)

def LoadTextures():
    global textures, images
    
    tekstury = []
    
    textures = glGenTextures(len(images))
    for tekstura in range(len(images)):
        tekstury.append([[],[],[]])
        tekstury[tekstura][0] = pygame.image.load(images[tekstura])
        tekstury[tekstura][1] = tekstury[tekstura][0].get_width()
        tekstury[tekstura][2] = tekstury[tekstura][0].get_height()
        tekstury[tekstura][0] = pygame.image.tostring(tekstury[tekstura][0], 'RGBA', True)
        
        glBindTexture(GL_TEXTURE_2D, textures[tekstura])
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri( GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 4, tekstury[tekstura][1], tekstury[tekstura][2], GL_RGBA, GL_UNSIGNED_BYTE, tekstury[tekstura][0])


def Scene(Width, Height):
    global cameraX, cameraY, cameraZ, translateX, translateY, translateZ, planety, eyeX, eyeZ, eyeY
    
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 400.0)
    gluLookAt(cameraX, cameraY, cameraZ, eyeX,eyeY,eyeZ, 0,1,0)
    
    glMatrixMode(GL_MODELVIEW)
    
def Draw():
    global matrixScale, scaleWsp, matrixTranslate, matrixRotate, angleX, angleY, angleZ, planety, translateX, translateY, translateZ, stateOrbity
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    
    #glColor3f(0,0,1)
    if stateOrbity:
        for i in range(len(planety)):
            scaleWsp = planety[i][0]
            matrixScale = [scaleWsp,0,0,0,0,scaleWsp,0,0,0,0,scaleWsp,0,0,0,0,1]
            glMultMatrixf(matrixScale)
            glCallList(1)
            glLoadIdentity()
    
    #glColor3f(1,0,0)
    for i in range(len(planety)):
        glBindTexture(GL_TEXTURE_2D, textures[i])
        scaleWsp = planety[i][1]
        translateY = 0.0
        translateX = (planety[i][0])*sin(radians(planety[i][4]))
        translateZ = (planety[i][0])*cos(radians(planety[i][4]))
        angleY = planety[i][5]
        matrixScale = [scaleWsp,0,0,0,0,scaleWsp,0,0,0,0,scaleWsp,0,0,0,0,1]
        matrixTranslate = [1,0,0,0,0,1,0,0,0,0,1,0,translateX,translateY, translateZ,1]
        matrixRotate = [cos(radians(angleY))*cos(radians(angleZ)), (-sin(radians(angleY))*-sin(radians(angleX))*cos(radians(angleZ)))+(cos(radians(angleX))*sin(radians(angleZ))), (cos(radians(angleX))*-sin(radians(angleY))*cos(radians(angleZ)))+(sin(radians(angleX))*sin(radians(angleZ))),0,cos(radians(angleY))*-sin(radians(angleZ)),(-sin(radians(angleY))*-sin(radians(angleX))*-sin(radians(angleZ)))+(cos(radians(angleX))*cos(radians(angleZ))), (cos(radians(angleX))*-sin(radians(angleY))*-sin(radians(angleZ)))+(sin(radians(angleX))*cos(radians(angleZ))), 0, sin(radians(angleY)), -sin(radians(angleX))*cos(radians(angleY)), cos(radians(angleX))*cos(radians(angleY)), 0, 0, 0, 0, 1]
        glMultMatrixf(matrixTranslate)
        glMultMatrixf(matrixScale)
        glMultMatrixf(matrixRotate)
        glCallList(2)
        glLoadIdentity()
        
        planety[i][4] += planety[i][2]
        planety[i][5] += planety[i][3]
    
    pygame.display.flip()

def Keys():
    global cameraX, cameraY, cameraZ, currentPlanet, planety, eyeX, eyeY, eyeZ, mouseAngle, stateLights, stateOrbity
    
    for i in pygame.event.get():
        if i.type == QUIT or (i.type==KEYDOWN and i.key==K_ESCAPE):
            pygame.quit()
            sys.exit()
        if i.type == MOUSEBUTTONDOWN:
            if i.button == 1:
                currentPlanet += 1
                if currentPlanet > 8:
                    currentPlanet = 0
                cameraX = (planety[currentPlanet][0])*sin(radians(planety[currentPlanet][4]))
                cameraZ = (planety[currentPlanet][0])*cos(radians(planety[currentPlanet][4]))
                cameraY = 10
                mouseAngle = [0,-90]
            elif i.button == 3:
                currentPlanet -= 1
                if currentPlanet < 0:
                    currentPlanet = 8
                cameraX = (planety[currentPlanet][0])*sin(radians(planety[currentPlanet][4]))
                cameraZ = (planety[currentPlanet][0])*cos(radians(planety[currentPlanet][4]))
                cameraY = 10
                mouseAngle = [0,-90]
        if i.type == KEYDOWN:
            if i.key == K_o:
                stateOrbity = not stateOrbity
            if i.key == K_l:
                stateLights = not stateLights
    
    key = pygame.key.get_pressed()
    if key[K_UP]:
        cameraX += (sin(radians(mouseAngle[0]))*cos(radians(mouseAngle[1])))/10
        cameraZ += (cos(radians(mouseAngle[0]))*cos(radians(mouseAngle[1])))/10
        cameraY += sin(radians(mouseAngle[1]))/10
    elif key[K_DOWN]:
        cameraX -= (sin(radians(mouseAngle[0]))*cos(radians(mouseAngle[1])))/10
        cameraZ -= (cos(radians(mouseAngle[0]))*cos(radians(mouseAngle[1])))/10
        cameraY -= sin(radians(mouseAngle[1]))/10
    if key[K_LEFT]:
        cameraX += (sin(radians(mouseAngle[0]+90)))/20
        cameraZ += (cos(radians(mouseAngle[0]+90)))/20
    elif key[K_RIGHT]:
        cameraX += (sin(radians(mouseAngle[0]-90)))/20
        cameraZ += (cos(radians(mouseAngle[0]-90)))/20
    
    cameraX += (planety[currentPlanet][0])*sin(radians(planety[currentPlanet][4]+ planety[currentPlanet][2])) - (planety[currentPlanet][0])*sin(radians(planety[currentPlanet][4]))
    cameraZ += (planety[currentPlanet][0])*cos(radians(planety[currentPlanet][4]+ planety[currentPlanet][2])) - (planety[currentPlanet][0])*cos(radians(planety[currentPlanet][4]))
    
    mouseMove = pygame.mouse.get_rel()
    mouseAngle[0] -= mouseMove[0]/10
    mouseAngle[1] -= mouseMove[1]/10
    
    if mouseAngle[0] > 360:
        mouseAngle[0] = 0
    elif mouseAngle[0] < 0:
        mouseAngle[0] = 360
    if mouseAngle[1] >= 90:
        mouseAngle[1] = 89
    elif mouseAngle[1] <= -90:
        mouseAngle[1] = -89
    
    eyeX = cameraX + (sin(radians(mouseAngle[0]))*cos(radians(mouseAngle[1])))
    eyeZ = cameraZ + (cos(radians(mouseAngle[0]))*cos(radians(mouseAngle[1])))
    eyeY = cameraY + sin(radians(mouseAngle[1]))
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((width,height),DOUBLEBUF|OPENGL)
    pygame.event.set_grab(1)
    pygame.mouse.set_visible(0)
    InitGL(width, height)
    LoadTextures()
    while True:
        Keys()
        clock.tick(60)
        Scene(width, height)
        Draw()

main()

