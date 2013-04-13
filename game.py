#Working as a two player game. Will show game over.

import pygame
from pygame.locals import *
import sys
import math

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
n = 5			#No of lines
font_size = 22	#Font size to display message
hll = []		#Horizantal line location
vll = []		#Vertical line location
hr = []			#Horizantal rectangles (for mouse clicking)
vr = []			#Vertical rectangles (for mouse clicking)
lock_hl = []	#Locked horizantal lines
lock_vl = []	#Locked vertical lines
count_green = 0	#Count to check who won
count_red = 0
count_blue = 0
count_yellow = 0
col = BLUE
circle_drawn = 0
total_player = 2

#General Instantiation
clk = pygame.time.Clock()
background = pygame.image.load("background.jpg")
win = pygame.display.set_mode((start_x*2+line_length*n,start_x*2+line_length*n))
pygame.display.set_caption('SquareX')
screen = pygame.display.get_surface()

#size = [800, 800]
#screen = pygame.display.set_mode(size)

def draw_circle (index, color, pos):
	#Global variable capture
	global count_green
	global count_red
	global count_yellow
	global count_blue
	global circle_drawn
	
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
	
	circle_drawn = 1
	if color==GREEN:
		count_green += 1
	elif color==RED:
		count_red += 1
	elif color==YELLOW:
		count_yellow += 1
	elif color==BLUE:
		count_blue += 1
	

def draw_hl (index, color):
	global col
	global circle_drawn
	if index not in lock_hl:
		pygame.draw.line(screen, color, hll[index][0], hll[index][1], line_width)
		lock_hl.append(index)
		#Checking if a square is made	
		if index in lock_hl and (index+1) in lock_hl and index in lock_vl and (index+n+1) in lock_vl:				#Down square is complete
			draw_circle(index,color,'down')
		if index in lock_hl and (index-1) in lock_hl and (index-1) in lock_vl and (index+n) in lock_vl:				#Top square is complete
			draw_circle(index,color,'up')
		if circle_drawn==0:
			if total_player==2:
				if col==BLUE:
					col = RED
				else:
					col = BLUE
			elif total_player==3:
				if col==BLUE:
					col = RED
				elif col==RED:
					col = YELLOW
				elif col==YELLOW:
					col = BLUE
			elif total_player==4:
				if col==BLUE:
					col = RED
				elif col==RED:
					col = YELLOW
				elif col==YELLOW:
					col = GREEN
				elif col==GREEN:
					col = BLUE
		circle_drawn = 0

def draw_vl (index, color):
	global col
	global circle_drawn
	if index not in lock_vl:
		pygame.draw.line(screen, color, vll[index][0], vll[index][1], line_width)
		lock_vl.append(index)
		#Checking if a square is made	
		if index in lock_vl and (index+n+1) in lock_vl and index in lock_hl and (index+1) in lock_hl:				#Right square is complete
			draw_circle(index,color,'right')
		if index in lock_vl and (index-n-1) in lock_vl and (index-n-1) in lock_hl and (index-n) in lock_hl:			#Left square is complete
			draw_circle(index,color,'left')
		if circle_drawn==0:
			if total_player==2:
				if col==BLUE:
					col = RED
				else:
					col = BLUE
			elif total_player==3:
				if col==BLUE:
					col = RED
				elif col==RED:
					col = YELLOW
				elif col==YELLOW:
					col = BLUE
			elif total_player==4:
				if col==BLUE:
					col = RED
				elif col==RED:
					col = YELLOW
				elif col==YELLOW:
					col = GREEN
				elif col==GREEN:
					col = BLUE
		circle_drawn = 0

def end_game (screen):
	global col
	global background
	global n
	global hll
	global vll
	global hr
	global vr
	global lock_hl 
	global lock_vl
	global count_green
	global count_red
	global count_blue
	global count_yellow
	global circle_drawn
	global total_player

	screen.fill(WHITE)
	background = pygame.transform.scale(background, (start_x*2+line_length*n,start_x*2+line_length*n))
	screen = pygame.display.set_mode((start_x*2+line_length*n,start_x*2+line_length*n))
	screen.blit(background, (0,0))
	
	restart = pygame.image.load("restart2.png")
	restart = pygame.transform.scale(restart, (50,50))
	screen.blit(restart, (screen.get_width() - 57, 10))
	restart_rect = pygame.Rect(screen.get_width() - 57, 10,50,50)
	
	fontobject = pygame.font.Font(None,font_size)
	fontobject2 = pygame.font.Font(None,font_size+5)
	count = [count_blue, count_green, count_red, count_yellow]
	
	
	#Removing all zero entries
	i = len(count)-1
	while i>=0:
		if count[i]==0:
			count.pop(i)
		i = i-1
		
	maximum = max(count)
	
	if len(set(count))!=1:			#No tie
		screen.blit(fontobject.render("Congratulations!", 1, BLACK),((screen.get_width() / 2)-60, (screen.get_height() / 2) - 40))
		screen.blit(fontobject.render("won the game", 1, BLACK),((screen.get_width() / 2)-50, (screen.get_height() / 2) + 40))
		if maximum==count_blue:
			screen.blit(fontobject2.render("BLUE", 1, BLUE),((screen.get_width() / 2)-25, (screen.get_height() / 2)))
		elif maximum==count_green:
			screen.blit(fontobject2.render("GREEN", 1, GREEN),((screen.get_width() / 2)-30, (screen.get_height() / 2)))
		elif maximum==count_red:
			screen.blit(fontobject2.render("RED", 1, RED),((screen.get_width() / 2)-20, (screen.get_height() / 2)))
		elif maximum==count_yellow:
			screen.blit(fontobject2.render("YELLOW", 1, YELLOW),((screen.get_width() / 2)-45, (screen.get_height() / 2)))
	else:
		screen.blit(fontobject.render("There was a tie between", 1, BLACK),((screen.get_width() / 2)-90, (screen.get_height() / 2) - 70))
		temp = -40
		if maximum==count_blue:
			screen.blit(fontobject2.render("BLUE", 1, BLUE),((screen.get_width() / 2)-25, (screen.get_height() / 2) + temp))
			temp = temp+30
		if maximum==count_green:
			screen.blit(fontobject2.render("GREEN", 1, GREEN),((screen.get_width() / 2)-35, (screen.get_height() / 2) + temp))
			temp = temp+30
		if maximum==count_red:
			screen.blit(fontobject2.render("RED", 1, RED),((screen.get_width() / 2)-20, (screen.get_height() / 2) + temp))
			temp = temp+30
		if maximum==count_yellow:
			screen.blit(fontobject2.render("YELLOW", 1, YELLOW),((screen.get_width() / 2)-45, (screen.get_height() / 2) + temp))
			temp = temp+30
	
	while True:
		for event in pygame.event.get():
			#For the exit button
			if event.type == QUIT:
				sys.exit(0)
						
			#For mouse clicks
			if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:

				pos = pygame.mouse.get_pos()
				if restart_rect.collidepoint(pos):
					hll = []		#Horizantal line location
					vll = []		
					hr = []			
					vr = []			
					lock_hl = []	
					lock_vl = []	
					count_green = 0	
					count_red = 0
					count_blue = 0
					count_yellow = 0
					col = BLUE
					circle_drawn = 0
					total_player = 2
					n = 5
					start_screen(screen)

		pygame.display.update()
		clk.tick(fps)


def start_screen (screen):
	screen.fill(WHITE)
	global background
	global total_player
	global n
	
	fontobject0 = pygame.font.Font(None, 30)
		
	# Background load
	background = pygame.transform.scale(background, (800,600))
	screen = pygame.display.set_mode(background.get_size())
	screen.blit(background, (0,0))	
	
	#Buttons load
	start_button = pygame.image.load("start-button.png")
	center_s = [140,460]
	radius_s = 90
	start_button = pygame.transform.scale(start_button, (200,200))
	screen.blit(start_button,(40, 360 ))
	player_button = pygame.image.load("player-button.png")
	player_button2 = pygame.image.load("player-button2.png")
	
	man_2 = pygame.image.load("man.png")
	player_2 = [300,400]
	center_2 = [player_2[0]+64, player_2[1]+64]
	radius_2 = 60
	screen.blit(player_button2,player_2)
	screen.blit(man_2,[player_2[0]+47,player_2[1]+35])
	screen.blit(man_2,[player_2[0]+17,player_2[1]+35])	
	
	man_3 = pygame.transform.scale(man_2, (55,55))
	player_3 = [470,400]
	center_3 = [player_3[0]+64, player_3[1]+64]
	radius_3 = 60
	screen.blit(player_button,player_3)
	screen.blit(man_3,[player_3[0]+63,player_3[1]+37])
	screen.blit(man_3,[player_3[0]+37,player_3[1]+37])
	screen.blit(man_3,[player_3[0]+10,player_3[1]+37])	

	man_4 = pygame.transform.scale(man_2, (48,48))
	player_4 = [640,400]
	center_4 = [player_4[0]+64, player_4[1]+64]
	radius_4 = 60
	screen.blit(player_button,player_4)
	screen.blit(man_4,[player_4[0]+10,player_4[1]+40])
	screen.blit(man_4,[player_4[0]+30,player_4[1]+40])
	screen.blit(man_4,[player_4[0]+50,player_4[1]+40])	
	screen.blit(man_4,[player_4[0]+70,player_4[1]+40])
	
	small = [270,180]
	center_small = [small[0]+64, small[1]+64]
	radius_small = 60
	screen.blit(player_button2, small)
	screen.blit(fontobject0.render("Small", 1, BLACK),(small[0]+35, small[1]+37))
	screen.blit(fontobject0.render("grid", 1, BLACK),(small[0]+42, small[1]+63))	
	
	medium = [440, 180]
	center_medium = [medium[0]+64, medium[1]+64]
	radius_medium = 60
	screen.blit(player_button, medium)
	screen.blit(fontobject0.render("Medium", 1, BLACK),(medium[0]+25, medium[1]+37))
	screen.blit(fontobject0.render("grid", 1, BLACK),(medium[0]+42, medium[1]+63))
	
	large = [610, 180]
	center_large = [large[0]+64, large[1]+64]
	radius_large = 60
	screen.blit(player_button, large)
	screen.blit(fontobject0.render("Large", 1, BLACK),(large[0]+33, large[1]+37))
	screen.blit(fontobject0.render("grid", 1, BLACK),(large[0]+42, large[1]+63))	
	
	#SquareX
	fontobject = pygame.font.Font(None,60)
	screen.blit(fontobject.render("SquareX", 1, GRAY),((screen.get_width() / 2)-100, 40))
	
	while True:
		#Printing the icons
		screen.blit(man_4,[player_4[0]+10,player_4[1]+40])
		screen.blit(man_4,[player_4[0]+30,player_4[1]+40])
		screen.blit(man_4,[player_4[0]+50,player_4[1]+40])	
		screen.blit(man_4,[player_4[0]+70,player_4[1]+40])
		screen.blit(man_3,[player_3[0]+63,player_3[1]+37])
		screen.blit(man_3,[player_3[0]+37,player_3[1]+37])
		screen.blit(man_3,[player_3[0]+10,player_3[1]+37])
		screen.blit(man_2,[player_2[0]+47,player_2[1]+35])
		screen.blit(man_2,[player_2[0]+17,player_2[1]+35])

		screen.blit(fontobject0.render("Large", 1, BLACK),(large[0]+33, large[1]+37))
		screen.blit(fontobject0.render("grid", 1, BLACK),(large[0]+42, large[1]+63))
		screen.blit(fontobject0.render("Medium", 1, BLACK),(medium[0]+25, medium[1]+37))
		screen.blit(fontobject0.render("grid", 1, BLACK),(medium[0]+42, medium[1]+63))
		screen.blit(fontobject0.render("Small", 1, BLACK),(small[0]+35, small[1]+37))
		screen.blit(fontobject0.render("grid", 1, BLACK),(small[0]+42, small[1]+63))
	
		for event in pygame.event.get():
			#For the exit button
			if event.type == QUIT:
				sys.exit(0)

			#For mouse clicks
			if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				dist_s = math.sqrt((pos[0]-center_s[0])**2 + (pos[1]-center_s[1])**2)
				dist_2 = math.sqrt((pos[0]-center_2[0])**2 + (pos[1]-center_2[1])**2)
				dist_3 = math.sqrt((pos[0]-center_3[0])**2 + (pos[1]-center_3[1])**2)
				dist_4 = math.sqrt((pos[0]-center_4[0])**2 + (pos[1]-center_4[1])**2)
				dist_small = math.sqrt((pos[0]-center_small[0])**2 + (pos[1]-center_small[1])**2)
				dist_medium = math.sqrt((pos[0]-center_medium[0])**2 + (pos[1]-center_medium[1])**2)
				dist_large = math.sqrt((pos[0]-center_large[0])**2 + (pos[1]-center_large[1])**2)
				
				if dist_2<=radius_2:
					screen.blit(player_button2,player_2)
					screen.blit(player_button,player_3)
					screen.blit(player_button,player_4)
					total_player = 2
				elif dist_3<=radius_3:
					screen.blit(player_button2,player_3)
					screen.blit(player_button,player_2)
					screen.blit(player_button,player_4)
					total_player = 3
				elif dist_4<=radius_4:
					screen.blit(player_button2,player_4)
					screen.blit(player_button,player_3)
					screen.blit(player_button,player_2)
					total_player = 4
				elif dist_s<=radius_s:
					game_started(screen)
				elif dist_small<=radius_small:
					screen.blit(player_button2, small)
					screen.blit(player_button, medium)
					screen.blit(player_button, large)
					n = 5
				elif dist_medium<=radius_medium:
					screen.blit(player_button2, medium)
					screen.blit(player_button, small)
					screen.blit(player_button, large)
					n = 7
				elif dist_large<=radius_large:
					screen.blit(player_button2, large)
					screen.blit(player_button, medium)
					screen.blit(player_button, small)
					n = 11
						
		pygame.display.update()
		clk.tick(fps)


def game_started (screen):
	global col
	global background
	global n
	global hll
	global vll
	global hr
	global vr
	global lock_hl 
	global lock_vl
	global count_green
	global count_red
	global count_blue
	global count_yellow
	global circle_drawn
	global total_player
		
	screen.fill(WHITE)
	background = pygame.transform.scale(background, (start_x*2+line_length*n,start_x*2+line_length*n))
	screen = pygame.display.set_mode((start_x*2+line_length*n,start_x*2+line_length*n))
	screen.blit(background, (0,0))
	
	restart = pygame.image.load("restart2.png")
	restart = pygame.transform.scale(restart, (50,50))
	screen.blit(restart, (screen.get_width() - 57, 10))
	restart_rect = pygame.Rect(screen.get_width() - 57, 10,50,50)

	#SquareX
	fontobject = pygame.font.Font(None, font_size+5)
	screen.blit(fontobject.render("SquareX", 1, BLACK),((screen.get_width() / 2)-40, 10))	

	#Colorful cursors
	brush_red = pygame.image.load("brush_red.png")
	brush_green = pygame.image.load("brush_green.png")
	brush_yellow = pygame.image.load("brush_yellow.png")
	brush_blue = pygame.image.load("brush_blue.png")

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
	
	while True:
	
		#Ending the game condition
		total = count_blue + count_green + count_red + count_yellow
		if total>=n*n:
			end_game(screen)
			break			
			
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
				if restart_rect.collidepoint(pos):
					hll = []		#Horizantal line location
					vll = []		
					hr = []			
					vr = []			
					lock_hl = []	
					lock_vl = []	
					count_green = 0	
					count_red = 0
					count_blue = 0
					count_yellow = 0
					col = BLUE
					circle_drawn = 0
					total_player = 2
					n = 5
					start_screen(screen)
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

		#Player turn mark
		if col==RED:
			screen.blit(brush_red, (25,25))
		elif col==YELLOW:
			screen.blit(brush_yellow, (25,25))
		elif col==GREEN:
			screen.blit(brush_green, (25,25))
		elif col==BLUE:
			screen.blit(brush_blue, (25,25))
				
		pygame.display.update()
		clk.tick(fps)


def main():
	
	#For background
	screen.fill(WHITE)

	start_screen(screen)
	

if __name__ == "__main__":
	main()
