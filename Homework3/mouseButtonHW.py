"""
Modified on Feb 20 2020
@author: lbg@dongseo.ac.kr
"""

import pygame
from sys import exit
import numpy as np
    
width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

background_image_filename = 'w1/image/curve_pattern.png'

background = pygame.image.load(background_image_filename).convert()
width, height = background.get_size()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolylineMouseButton")
font= pygame.font.SysFont("consolas",17) 
  
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pts = [] 
knots = []
count = 0
#screen.blit(background, (0,0))
screen.fill(WHITE)

# https://kite.com/python/docs/pygame.Surface.blit
clock= pygame.time.Clock()

def print_text(msg,color='BLACK',pos=(10,10)):
    textSurface = font.render(msg, True, pygame.Color(color), None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos
    screen.blit(textSurface, textRect)

def drawPoint(pt, color='GREEN', thick=3):
    # pygame.draw.line(screen, color, pt, pt)
    pygame.draw.circle(screen, color, pt, thick)

#HW2 implement drawLine with drawPoint
def drawLine(pt0, pt1, color='GREEN', thick=3):
    #drawPoint((100,100), color,  thick)
    pt0 = np.array(pt0, dtype=np.float32)
    pt1 = np.array(pt1, dtype=np.float32)

    drawPoint(pt0, color, thick)
    drawPoint(pt1, color, thick)

    #2nd equation
    #a0*p0+a1*p1 coordinate free system
    for t in np.arange(-0.5,1.5,0.001):
        l_t = (1-t)*pt0 + t*pt1
        drawPoint(l_t, color, thick)

def calculate_barycentric(cur_pos):
    p0,p1,p2 = pts[0], pts[1], pts[2]
    L = np.zeros((2,2))
    L[0] = np.subtract(p0,p2)
    L[1] = np.subtract(p1,p2)
    p_current = np.subtract(cur_pos,p2)
    L = L.transpose()
    p_current = p_current.transpose()
    L = np.dot(np.linalg.inv(L),p_current)
    L012 = np.append(L, 1-L[0]-L[1])
    return L012

def drawPolylines(color='GREEN', thick=3):
    if(count < 3): return
    for i in range(count-1):
        if i == 0:
            drawLine(pts[i], pts[i+2], color)
            print_text("pt" + str(i) + ' ' + str(tuple(pts[i])), 'RED', (10,10))
        
        drawLine(pts[i], pts[i+1], color)
        pos_y = 10 + ((i+1)*20)
        print_text('pt' + str(i+1) + ' ' + str(tuple(pts[i+1])),'RED', (10,pos_y))

    current_pos = pygame.mouse.get_pos()
    L012 = calculate_barycentric(current_pos)
    L012 = np.round(L012,2)
    pygame.draw.rect(screen, WHITE, (10, 70, 400, 30))
    print_text('pt  ' + str(current_pos) + ' -- ' + str(tuple(L012)),'RED', (10, 70))

#Loop until the user clicks the close button.
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0

while not done:   
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1            
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1            
        elif event.type == pygame.QUIT:
            done = True
        else:
            pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]
    pygame.draw.circle(screen, RED, pt, 0)

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0 :
        pts.append(pt) 
        count += 1
        pygame.draw.rect(screen, BLUE, (pt[0]-margin, pt[1]-margin, 2*margin, 2*margin), 5)
        print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button1)+" pressed:"+repr(pressed)+" add pts ...")
    else:
        print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button1)+" pressed:"+repr(pressed))

    if len(pts)==3:
        drawPolylines(GREEN, 1)
    elif len(pts)>3:
        del pts[0]
        count = count - 1
        pygame.draw.rect(screen, WHITE, (10, 10, 200, 160))

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()