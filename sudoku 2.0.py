# An interactive game of Sudoku developed in pygame(GUI)

import sys
import pygame
import random
import time

from pygame.locals import *
from copy import deepcopy

#Defining game window parameters
WINDOWHEIGHT = 500
WINDOWWIDTH = 500
BOXSIZE = 50 #where digits are filled
LEFTMARGIN = 25 
TOPMARGIN = 20
BOXMARGIN = 2
BOXEFF = BOXSIZE - 2*BOXMARGIN #effective box size

#frames per second
FPS = 30


#pygame doesn't prvide support for colours so we need to define our own colours based on RGB format
#            R    G    B
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)

RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)

GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
ORIGINAL = (128, 128, 255) #this colour is used for the boxes that are already filled

# setting colours of the different game parameters
BOXCOLOUR = GRAY #before filling the value
HIGHLIGHT = CYAN #on mouse hover
CLICKED = BLUE #upon finalizing the selected value
BGCOLOUR = NAVYBLUE #Background colour
TEXTCOLOUR = BLACK 
LINECOLOUR = ORANGE #boundary lines

#initializing pygame
pygame.init()

#building the surface object with height = 500 and width = 500
DISPLAYSURF=pygame.display.set_mode((WINDOWHEIGHT,WINDOWWIDTH))
FPSCLOCK=pygame.time.Clock() #for frames per second
pygame.display.set_caption('Sudoku Masters') #To title the window opened

#Font
smallFont=pygame.font.Font('./arial.ttf',16)
largeFont=pygame.font.Font('./arial.ttf',28)
largeFont.set_italic(True)


def main():
	while True:
		smallFont.set_bold(False)
		pygame.mixer.music.load('./intro.mp3') #file containing the music to be played were loaded
		pygame.mixer.music.play(-1,0.0)
		
		welcomeScr()
				
		DISPLAYSURF.fill(BGCOLOUR) #setting the background of our surface 
		smallFont.set_bold(True)

		mousex = 0
		mousey = 0
		board = [[0 for x in range(9)] for x in range(9)]
		fillUp(board)

		displayedBoard = [[0 for x in range(9)] for x in range(9)]
		originalBoard = [[0 for x in range(9)] for x in range(9)]
		for i in range(9):
			for j in range(9):
				displayedBoard[i][j]=board[i][j]
		
		makeSpaces(displayedBoard,board) #make spaces in the board for player to fill in

		for i in range(9):
			for j in range(9):
				originalBoard[i][j]=displayedBoard[i][j]

		keyPressed = None
		clickedPrev = False

		while True:#main game loop
			
			mouseClicked = False
			
			DISPLAYSURF.fill(BGCOLOUR) # drawing the window
			displayCurrent(displayedBoard,originalBoard)

			#Event Handling
		
			#some of the types :
			#1- QUIT
			#2- ACTIVEEVENT
			#3- KEYDOWN
			#4- KEYUP
			#5- MOUSEMOTION
			#6- MOUSEBUTTONUP
			#7- MOUSEBUTTONDOWN
			
			for event in pygame.event.get():

				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				
				elif event.type==MOUSEMOTION:
					mousex,mousey=event.pos #to get the mouse position
					
				elif event.type==MOUSEBUTTONUP and not clickedPrev:
					mousex,mousey=event.pos
					mouseClicked=True
					clickedPrev=True
				elif event.type==KEYUP and clickedPrev:
					keyPressed=event.key #get the key that is pressed after mouse hover

			row,col = getBoxAtPixel(mousex,mousey)#extract info about mouse position
			
			if row!=None and col!=None:
				if originalBoard[row][col]==0:
					highLight(row,col,displayedBoard,originalBoard)
				if mouseClicked==True:
					if originalBoard[row][col]==0:
						displayedBoard[row][col]='?'

			if keyPressed!=None:
				clickedPrev=False
				for i in range(9):
					for j in range(9):
						if displayedBoard[i][j]=='?':
							displayedBoard[i][j]=pressedKey(keyPressed)
							keyPressed=None
							break
					else:
						continue
					break
			
			#Displaying all the information we have built on the background to the surface
			pygame.display.update()
			if hasWon(displayedBoard):#check for win
				pygame.mixer.music.stop()
				res=endScreen()
				if not res:
					pygame.quit()
					sys.exit()
				else:
					break #restart game
			
			pygame.display.update()
			FPSCLOCK.tick(FPS)


def pressedKey(keyPr):
	if keyPr==K_1:
		return 1
	elif keyPr==K_2:
		return 2
	elif keyPr==K_3:
		return 3
	elif keyPr==K_4:
		return 4
	elif keyPr==K_5:
		return 5
	elif keyPr==K_6:
		return 6
	elif keyPr==K_7:
		return 7
	elif keyPr==K_8:
		return 8
	elif keyPr==K_9:
		return 9
	else:
		return 0
	
	
#Takes a partially filled-in grid and attempts to assign values to
#all unassigned locations in such a way to meet the requirements
#for Sudoku solution (non-duplication across rows, columns, and boxes)	
def fillUp(board):
	#box is a list variable that keeps the record of row and col in findUnassigned() function    
	box = [0,0]
	#If there is no unassigned location, we are done
	if not findUnassigned(board,box): 
		return True
	for i in range(1,10): #consider digits 1 to 9
		if(isSafe(board,box[0],box[1],i)): #if looks promising
			board[box[0]][box[1]]=i
			if(fillUp(board)): #solvable
				return True
			board[box[0]][box[1]]=0 #failure, unmake & try again
	return False #backtrack

def isSafe(board,row,col,num):
	for i in range (9):
		if board[i][col]==num: #checking in current column
			return False
		if board[row][i]==num: #checking in current row
			return False
	for i in range (row//3*3,row//3*3+3): #checking in current 3x3 grid
		for j in range (col//3*3,col//3*3+3):
			if board[i][j]==num:
				return False
	return True

def makeSpaces(displayedBoard,board):
	ctr=0
	while ctr<50: #make 50 empty cells
		for i in range(0,9):
			a=random.randint(0,8)
			
			while displayedBoard[i][a]==0:
				a=random.randint(0,8)
			displayedBoard[i][a]=0
			
			ctr+=1
			
			if not unique(displayedBoard):
				displayedBoard[i][a]=board[i][a]
				ctr-=1
				
		for i in range(0,9):
			a=random.randint(0,8)
			while displayedBoard[a][i]==0:
				a=random.randint(0,8)
			displayedBoard[a][i]=0
			ctr+=1
			if not unique(displayedBoard):
				displayedBoard[a][i]=board[a][i]
				ctr-=1

def unique(displayedBoard):
	
	testBoard = [[0 for x in range(9)] for x in range(9)]
	for i in range(9):
		for j in range(9):
			testBoard[i][j]=displayedBoard[i][j]
	if not fillUp(testBoard):
		return False
	
	for asdf in range(5):#changed to 5 from 4
		board1 = [[0 for x in range(9)] for x in range(9)]
		for i in range(9):
			for j in range(9):
				board1[i][j]=displayedBoard[i][j]

		board2 = [[0 for x in range(9)] for x in range(9)]
		for i in range(9):
			for j in range(9):
				board2[i][j]=displayedBoard[i][j]

		fillUp(board1)
		fillUp(board2)
		for i in range(0,9):
			for j in range(0,9):
				if board1[i][j]!=board2[i][j]:
					return False
	return True

def findUnassigned(board,box):
	unassigned=[]
	for i in range (9):
		for j in range(9):
			if board[i][j]==0:
				unassigned.append([i,j])
				if len(unassigned)>1:
					break
		else:
			continue
		break
	
	if len(unassigned)==0:
		return False
	else:
		random.shuffle(unassigned)
		box[0]=unassigned[0][0]
		box[1]=unassigned[0][1]
		return True

def welcomeScr():
	
	#first screen displaying 'Welcome to Sudoku Masters'
	DISPLAYSURF.fill(BGCOLOUR)
	welcomeMessage=largeFont.render('Welcome to Sudoku Masters',True,WHITE)
	welcomeRect=welcomeMessage.get_rect() # welcome rectangle is used to position the text on the display surface
	welcomeRect.center=(WINDOWWIDTH/2,WINDOWHEIGHT/2) #center of display surface
	DISPLAYSURF.blit(welcomeMessage,welcomeRect) #placing the text on screen and at the mid of the display surface 
	pygame.display.update() #updating the display surface
	time.sleep(2) #pause for a two seconds for the 'Welcome to Sudoku Masters' text
	
	#second screen showing the name of the author
	DISPLAYSURF.fill(BGCOLOUR)
	welcomeMessage=largeFont.render('Created by: $hikhar $harma',True,CYAN)
	welcomeRect=welcomeMessage.get_rect()
	welcomeRect.center=(WINDOWWIDTH/2,WINDOWHEIGHT/2)
	DISPLAYSURF.blit(welcomeMessage,welcomeRect)
	pygame.display.update()
	time.sleep(1.5)
	
	#3rd and final screen where the actual sudoku is drawn
	DISPLAYSURF.fill(BGCOLOUR)
	pygame.display.update()

def displayCurrent(displayedBoard,originalBoard):
	for row in range(9):
		for col in range(9):
			if displayedBoard[row][col]!=0:
				#parameters passed to Rect() functions are 'x','y' coordinate of starting point and 'width' and 'height'
				currBox=pygame.Rect(LEFTMARGIN+BOXMARGIN+BOXSIZE*col,TOPMARGIN+BOXMARGIN+BOXSIZE*row,BOXEFF,BOXEFF)
				if originalBoard[row][col]==0:
					#if its a blank i.e value to be added by gamer
					pygame.draw.rect(DISPLAYSURF,CLICKED,currBox)
				else:
					#if value is already filled
					pygame.draw.rect(DISPLAYSURF,ORIGINAL,currBox)
				data=smallFont.render(str(displayedBoard[row][col]),True,TEXTCOLOUR)
				dataRect=data.get_rect()
				dataRect.center=currBox.center
				DISPLAYSURF.blit(data,dataRect)
			else:
				pygame.draw.rect(DISPLAYSURF,BOXCOLOUR,(LEFTMARGIN+BOXMARGIN+BOXSIZE*col,TOPMARGIN+BOXMARGIN+BOXSIZE*row,BOXEFF,BOXEFF))
	
	#Drawing orange line to margin the 3x3 grid
	for row in range(8):
		width=2
		if row==2 or row==5:
			width=4
		pygame.draw.line(DISPLAYSURF,LINECOLOUR,(LEFTMARGIN,TOPMARGIN+(row+1)*BOXSIZE),(WINDOWWIDTH-LEFTMARGIN,TOPMARGIN+(row+1)*BOXSIZE),width)
	for col in range(8):
		width=2
		if col==2 or col==5:
			width=4
		pygame.draw.line(DISPLAYSURF,LINECOLOUR,(LEFTMARGIN+(col+1)*BOXSIZE,TOPMARGIN),(LEFTMARGIN+(col+1)*BOXSIZE,TOPMARGIN+9*BOXSIZE),width)
	pygame.draw.rect(DISPLAYSURF,LINECOLOUR,(LEFTMARGIN,TOPMARGIN,BOXSIZE*9,BOXSIZE*9),4)
	pygame.display.update()

def leftTopCoordsOfBox(boxx, boxy):
	left=LEFTMARGIN+boxx*BOXSIZE+BOXMARGIN
	top=TOPMARGIN+boxy*BOXSIZE+BOXMARGIN
	return (left,top)

def getBoxAtPixel(x,y):
	for row in range(0,9):
		for col in range(0,9):
			left, top = leftTopCoordsOfBox(col, row)
			boxRect = pygame.Rect(left,top,BOXEFF,BOXEFF)
			
			if boxRect.collidepoint(x, y):
				return (row, col)
	return (None,None)

def highLight(row,col,displayedBoard,originalBoard):
	
	if originalBoard[row][col]!=0:
		return
	currBox=pygame.Rect(LEFTMARGIN+BOXMARGIN+BOXSIZE*col,TOPMARGIN+BOXMARGIN+BOXSIZE*row,BOXEFF,BOXEFF)
	pygame.draw.rect(DISPLAYSURF,HIGHLIGHT,currBox) #Drawing highlighted box woth cyan colour
	if displayedBoard[row][col]==0:
		return
	data=smallFont.render(str(displayedBoard[row][col]),True,TEXTCOLOUR)
	dataRect=data.get_rect()
	dataRect.center=currBox.center
	DISPLAYSURF.blit(data,dataRect)

def hasWon(sud):
	for i in range(9):
		for j in range(9):
			if sud[i][j]==0:
				return False
	zippedsud = zip(*sud)

	boxedsud=[]
	for li,line in enumerate(sud):
	    for box in range(3):
	        if not li % 3: boxedsud.append([])    # build a new box every 3 lines
	        boxedsud[box + li/3*3].extend(line[box*3:box*3+3])

	for li in range(9):
	    if [x for x in [set(sud[li]), set(zippedsud[li]), set(boxedsud[li])] if x != set(range(1,10))]:
	        return False
	return True

def endScreen():
	pygame.mixer.music.load('./game_over.mp3')
	pygame.mixer.music.play(-1,0.0)
	queryBox=pygame.Rect(WINDOWWIDTH/2-150,WINDOWHEIGHT/2-120,300,200)
	queryMsg=largeFont.render("!! YOU WON !!",True,RED)
	msgRect=queryMsg.get_rect()
	msgRect.center=queryBox.center
	pygame.draw.rect(DISPLAYSURF,YELLOW,queryBox)
	pygame.draw.rect(DISPLAYSURF,ORANGE,queryBox,3)
	DISPLAYSURF.blit(queryMsg,msgRect)
	pygame.display.update()
	time.sleep(2)
	while True:
		queryBox=pygame.Rect(WINDOWWIDTH/2-150,WINDOWHEIGHT/2-120,300,200)
		queryMsg=largeFont.render("PLAY AGAIN? (Y/N)",True,RED)
		msgRect=queryMsg.get_rect()
		msgRect.center=queryBox.center
		pygame.draw.rect(DISPLAYSURF,YELLOW,queryBox)
		pygame.draw.rect(DISPLAYSURF,ORANGE,queryBox,3)
		DISPLAYSURF.blit(queryMsg,msgRect)
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type==KEYUP:
				if event.key==K_y:
					pygame.mixer.music.stop()
					return True
				elif event.key==K_n:
					pygame.mixer.music.stop()
					return False
		pygame.display.update()
		FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
