#Space Enemies

import turtle
import sys
import os
import math
import random
import time
import winsound
import pygame

#Menu
print(48 * "-")
print(9 * " " + "S.P.A.C.E. I.N.V.A.D.E.R.S." + 10 * " ")
print(48 * "-")
print(14 * " " + "M.A.I.N. M.E.N.U." + 10 * " ")
print(48 * "-")
name=raw_input("Hello, what's your name?: ")
print ("Hi, "+(name)+"!")
while True:
    choice=raw_input("Would you like to play Space Enemies? Enter(Y/N):")    
    if choice in ["Y","y"]:
        print("Starting the game.....")
        time.sleep(1.5)
        break 
    
    if choice in ["N","n"]:
        print("Exiting the program...")
        time.sleep(1.5)
        sys.exit(0)
        
    elif choice not in ["Y", "y","N" ,"n"]:   
        print("Enter a valid sign!")
        time.sleep(1.5)
   

#Screen
wn=turtle.Screen()
wn.bgpic("stars.gif")
wn.title("Space Enemies")
wn.bgcolor("black")

#Register the shapes
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")


#Border
border_pen=turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()
    
#Score to 0
score=0

#Draw the score
score_pen=turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,276)
scorestring="Score: %s"%score
score_pen.write(scorestring, False, align="left", font=("Times",15,"bold"))
score_pen.hideturtle()   

#Draw pen
draw_pen=turtle.Turtle()
draw_pen.speed(0)
draw_pen.color("yellow")
draw_pen.penup()
draw_pen.setposition(0,315)
draw_pen.write("SPACE ENEMIES", False, align="center", font=("Times",22,"bold"))
draw_pen.hideturtle()   

#Lose pen
lose_pen=turtle.Turtle()
lose_pen.speed(0)
lose_pen.color("yellow")
lose_pen.penup()
lose_pen.setposition(0,0)
lose_pen.hideturtle()   
 
#Instructions pen
instpen=turtle.Turtle()
instpen.speed(0)
instpen.color("white")
instpen.penup()
instpen.setposition(0,-323)
instpen.hideturtle()
instpen.pendown()
instpen.write("PRESS 'LEFT' AND 'RIGHT' ARROW KEYS TO MOVE, PRESS 'SPACE' TO SHOOT",False, align="center", font=("HELVETICA",10,"italic"))

 
#Player
player=turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)        
playerspeed=15

#Choose number of enemies
number_of_enemies=5
#Empty list of enemies
enemies=[]

#Add enemies to the list
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:             
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x=random.randint(-200,200)
    y=random.randint(100,250)
    enemy.setposition(x,y)
    
enemyspeed=2       
       

#Bullet
bullet=turtle.Turtle()
bullet.color("yellow")
bullet.shape("square")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.005,2)
bullet.hideturtle()
bulletspeed=20

#Bullet states
bulletstate="ready"

#Functions
def move_left():
    x=player.xcor()
    x-=playerspeed
    if x < -280:
        x=-280
    player.setx(x)

def move_right():
    x=player.xcor()
    x+=playerspeed
    if x > 280:
        x=280
    player.setx(x)

def fire_bullet():
    global bulletstate
    if bulletstate=="ready":
        winsound.PlaySound("shoot.wav", winsound.SND_ASYNC)
        bulletstate="fire"
        x=player.xcor()
        y=player.ycor()+10
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(t1,t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 18:
        return True
    else:
        return False
        
        
    
#Keyboard bind
turtle.listen()
turtle.onkey(move_left, "Left")    
turtle.onkey(move_right, "Right")    
turtle.onkey(fire_bullet, "space")

 
#Background music using pygame 
pygame.mixer.init()
pygame.mixer.music.load("Chiptronical.mp3")
pygame.mixer.music.set_volume(0.68) 
pygame.mixer.music.play(-1,0)


 
#Main game loop
while True:
                    
    for enemy in enemies:
        
        #Move enemy
        x=enemy.xcor()
        x+=enemyspeed
        enemy.setx(x)        
             
        
        #Enemy collision with border
        if enemy.xcor()>280:
            for e in enemies:
                y=e.ycor()                
                y-=40
                e.sety(y)
            enemyspeed*=-1       
                
            
        if enemy.xcor()<-280:
            for e in enemies:
                y=e.ycor()
                y-=40                   
                e.sety(y)
            enemyspeed*=-1
                        
        if enemy.ycor()<-250:            
            for e in enemies:            
                y=-250
                x=250
                e.setx(x)
                e.sety(y)
                espeed=1

        
        #Check for collision with bullet and enemy
        if isCollision(bullet,enemy):
            winsound.PlaySound("invaderkilled.wav", winsound.SND_ASYNC)
            #Reset bullet           
            bullet.hideturtle()
            bulletstate="ready"
            bullet.setposition(0,-400)
            #Reset enemy
            x=random.randint(-200,200)
            y=random.randint(100,250)
            enemy.setposition(x,y)
            #Update the score
            score+=10
            scorestring="Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Times",15,"bold"))
                        
            
        #Player and enemy collision
        if isCollision(player, enemy):
            pygame.mixer.music.pause()            
            player.hideturtle()
            lose_pen.pendown()
            lose_pen.write("GAME OVER", False, align="center", font=("Times",16,"bold"))
            winsound.PlaySound("fail.wav", winsound.SND_ASYNC)
            time.sleep(2)
            for e in enemies:
                e.hideturtle()                
                enemyspeed=0
            time.sleep(1)
            lose_pen.clear()
            True            
            for e in enemies:
                e.showturtle()
                x=random.randint(-200,200)
                y=random.randint(100,250)
                e.setposition(x,y)                                
                enemyspeed=2                
                #Move enemy
                x=e.xcor()
                x+=espeed
                e.setx(x)                
            player.showturtle()
            score=0
            scorestring="Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Times",15,"bold"))
            pygame.mixer.music.unpause()
            break    
                                    
                     
       
    #Move the bullet    
    if bulletstate=="fire":
        y=bullet.ycor()
        y+=bulletspeed
        bullet.sety(y)
    
    #Check to see if bullet has reached the top
    if bullet.ycor()>275:
        bullet.hideturtle()
        bulletstate="ready"
        
    
    
delay=raw_input("Press enter to finish!")
