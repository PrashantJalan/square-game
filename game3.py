#With working one time mouse clicks. Now need to implement on server

import pygame
from pygame.locals import *
import sys

# Initialize the game engine
pygame.init()

#Color definition
BLACK = (  0,   0,   0)
GRAY =  (112, 138, 144)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW = (204, 204, 0)

#Variable declaration
fps = 40
line_length = 50
line_width = 5
dot_radius = 4
start_x = (line_length*3)/2
start_y = (line_length*3)/2
n = 10			#No of lines
hll = []		#Horizantal line location
vll = []		#Vertical line location
hr = []			#Horizantal rectangles (for mouse clicking)
vr = []			#Vertical rectangles (for mouse clicking)
lock_hl = []	#Locked horizantal lines
lock_vl = []	#Locked vertical lines

#General Instantiation
clk = pygame.time.Clock()
win = pygame.display.set_mode((start_x*2+line_length*n,start_x*2+line_length*n))
pygame.display.set_caption('SquareX')
screen = pygame.display.get_surface()

#size = [800, 800]
#screen = pygame.display.set_mode(size)
def draw_circle (index, color, pos):
	if pos=='down':
		x = hll[index][0][0] + line_length/2
		y = hll[index][0][1] + line_length/2
	if pos=='up':
		x = hll[index][0][0] + line_length/2
		y = hll[index][0][1] - line_length/2
	if pos=='right':
		x = vll[index][0][0] + line_length/2
		y = vll[index][0][1] + line_length/2
	if pos=='left':
		x = vll[index][0][0] - line_length/2
		y = vll[index][0][1] + line_length/2
	pygame.draw.circle(screen, color, [x, y], dot_radius*3)
	

def draw_hl (index, color):
	if index not in lock_hl:
		pygame.draw.line(screen, color, hll[index][0], hll[index][1], line_width)
		lock_hl.append(index)
		#Checking if a square is made	
		if index in lock_hl and (index+1) in lock_hl and index in lock_vl and (index+n+1) in lock_vl:				#Down square is complete
			draw_circle(index,color,'down')
		if index in lock_hl and (index-1) in lock_hl and (index-1) in lock_vl and (index+n) in lock_vl:				#Top square is complete
			draw_circle(index,color,'up')

def draw_vl (index, color):
	if index not in lock_vl:	
		pygame.draw.line(screen, color, vll[index][0], vll[index][1], line_width)
		lock_vl.append(index)
		#Checking if a square is made	
		if index in lock_vl and (index+n+1) in lock_vl and index in lock_hl and (index+1) in lock_hl:				#Right square is complete
			draw_circle(index,color,'right')
		if index in lock_vl and (index-n-1) in lock_vl and (index-n-1) in lock_hl and (index-n) in lock_hl:			#Left square is complete
			draw_circle(index,color,'left')
		

def main():
	
	#For background
	screen.fill(WHITE)

	#Making the horizantal lines						
	for i in range(0,n):
		for j in range(0,n+1):
			hll.append([[start_x+i*line_length, start_y+j*line_length], [start_x+(i+1)*line_length, start_y+j*line_length]])
			temp_rec = pygame.Rect((start_x+i*line_length+line_width, start_y+j*line_length-line_width, line_length-2*line_width,2*line_width))
			hr.append(temp_rec)
			pygame.draw.line(screen, GRAY, [start_x+i*line_length, start_y+j*line_length], [start_x+(i+1)*line_length, start_y+j*line_length], line_width)

	#Making the vertical lines
	for i in range(0,n+1):
		for j in range(0,n):	
			vll.append([[start_x+i*line_length, start_y+j*line_length], [start_x+i*line_length, start_y+(j+1)*line_length]])
			temp_rec = pygame.Rect((start_x+i*line_length-line_width, start_y+j*line_length+line_width, 2*line_width, line_length-2*line_width))
			vr.append(temp_rec)
			if j == n-1 :
				vll.append([[start_x+i*line_length, start_y+(j+1)*line_length], [start_x+i*line_length, start_y+(j+2)*line_length]])
				temp_rec = pygame.Rect((0,0,1,1))
				vr.append(temp_rec)
			pygame.draw.line(screen, GRAY, [start_x+i*line_length, start_y+j*line_length], [start_x+i*line_length, start_y+(j+1)*line_length], line_width)

	k=0
	prev_click = False
	col = GREEN
	while True:
		#Making the dots-
		for i in range(0,n+1):
			for j in range(0,n+1):
				pygame.draw.circle(screen, BLACK, [start_x+i*line_length, start_y+j*line_length], dot_radius)
		
		for event in pygame.event.get():
			#For the exit button
			if event.type == QUIT:
				sys.exit(0)
			
			#For mouse clicks
			if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				flag = 0
				i = 0
				for item in hr:
					if item.collidepoint(pos):
						draw_hl(i, col)
						flag = 1
						break
					i = i+1
				if flag==0:
					i = 0
					for item in vr:
						if item.collidepoint(pos):
							draw_vl(i, col)
							break
						i = i+1
				
		pygame.display.update()
		clk.tick(fps)

if __name__ == "__main__":
	main()
