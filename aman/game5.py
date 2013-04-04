"""
Use up/down to move racket 1 (red color) and  w/s to move racket 2 (blue color)
"""
import pygame,sys
import math,random
from pygame.locals import *

table = pygame.image.load('table2.jpg')
button = pygame.image.load('button.jpg')
w,h=table.get_width()+100,table.get_height()+8
pygame.init()
clk = pygame.time.Clock()
win = pygame.display.set_mode((w,h))
pygame.display.set_caption('Table Tennis')
screen = pygame.display.get_surface()

red=pygame.Color(255,0,0)			
black=pygame.Color(0,0,0)
blue=pygame.Color(0,0,255)
white=pygame.Color(255,255,255)

# some global varibles

width,height=10,60
gap = (w-table.get_width())/2
rp = gap/2 - width/2
radius=10
millisec = 0.0
speed = 1.5

def disp(msg):
	font = pygame.font.Font(None, 36)
	text = font.render(msg, 1,black)
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	screen.blit(text, textpos)

class racket:

	def __init__(self,place):
		self.pos=place
		self.rack=None
		
	def move(self,place,scr,color,up,down):
		y=place[1]
		for event in pygame.event.get():
		        if event.type == QUIT:
		                sys.exit(0)
		        elif event.type == KEYDOWN:

		                if pygame.key.get_pressed()[up] and not (y<=2):
		                        y -=10
		                if pygame.key.get_pressed()[down] and not(y>=h-4-height):
		                        y +=10
		if pygame.key.get_pressed()[up] and not (y<=2):
		        y-=10
		if pygame.key.get_pressed()[down] and not(y>=h-4-height):
		        y+=10

		self.pos =(place[0],y,place[2],place[3])
		self.rack=pygame.draw.rect(scr,color,self.pos)

class ball:

	def __init__(self,place,v=(0.0,0.0)):
		self.pos = place
		self.velx=v[0]
		self.vely=v[1]
		self.obj=None
		self.ready=1
		self.team1=0
		self.team2=0

	def draw(self,scr,color,place,rad):
		self.pos = place
		self.obj = pygame.draw.circle(scr,color,place,rad)
	
	def check_collision(self,rec):
		if (self.obj.colliderect(rec[0]) or self.obj.colliderect(rec[1])):
			if self.ready:							# collision with up/down wall 
				self.vely = -self.vely
				self.ready=0
		elif (self.obj.colliderect(rec[2]) or self.obj.colliderect(rec[3])):
			if self.ready:							# collision with rackets
				self.velx = -self.velx 
				self.ready=0
		else:
			self.ready=1

	def move(self,time,scr,color,place,rad):

		self.pos=(int(self.pos[0]+time*self.velx),int(self.pos[1]+time*self.vely))
		self.draw(scr,color,self.pos,rad)
		if not(gap/2<self.pos[0]<w-gap/2) or not (0<self.pos[1]<h) :
			self.velx,self.vely=0.0,0.0
			#disp("Game Over")
			return 0
		return 1

def new_game():
	degree=random.randint(60,120)
	velocity=(speed*math.sin(degree*math.pi/180),speed*math.cos(degree*math.pi/180))
	tt_ball=ball((w/2,h/2),velocity)
	tt_ball.draw(screen,white,tt_ball.pos,radius)
	racket1=racket((rp,2,width,height))
	racket2=racket((gap+table.get_width()+rp,2,width,height))
	tt = pygame.image.load('table2.jpg')

	while True:
		screen.fill(black)
		screen.blit(tt,(gap,2))
		millisec = clk.tick(35)	
		up_wall = pygame.draw.rect(screen,white,(rp+5,0,table.get_width()+gap,4))		# walls to detect up and down collision of ball
		down_wall = pygame.draw.rect(screen,white,(rp+5,h-4,table.get_width()+gap,4))
	
		racket1.move(racket1.pos,screen,red,K_w,K_s)
		racket2.move(racket2.pos,screen,blue,K_UP,K_DOWN)
	
		rec = [up_wall,down_wall,racket1.rack,racket2.rack]
		tt_ball.check_collision(rec)
		end = tt_ball.move(int(millisec*0.2),screen,white,tt_ball.pos,radius)	
		if not end:
			return 0
		pygame.display.update()
	#	pygame.display.flip()

def main():
	new=1	
	while True:	
		screen.fill(black)
		game=button.copy()
		font = pygame.font.Font(None, 25)
		text = font.render("New Game", 1,black)
		game.blit(text,(10,10))
		table.blit(game,(200-game.get_width()/2,100-game.get_height()/2))
		screen.blit(table,(gap,0))
		if not new:
			disp("Game Over ")
		pygame.display.update()
		chk=pygame.Rect((195,70), game.get_size())
		ms =pygame.Rect( (pygame.mouse.get_pos()),(2,2))
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			if event.type == MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0] and ms.colliderect(chk)  :
					new = new_game()
		clk.tick(40)
		

if __name__ == "__main__":
	main()
