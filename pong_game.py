import sys
import pygame
import numpy

pygame.init()

#reading from configuration file
file = open("config.txt", "r")
config = file.readlines()
width = int(config[1])
height = int(config[3])
difficulty = config[5]


size = width, height
position1 = [round(width/2), round(height/2)]  #the middle of the screen
destination = round(height/2)
speed = [2,2]   #speed of ball

black = 0, 0, 0
white = 255, 255, 255
player1_pos = [0, round(height/2) - 40, 20, 80]
player2_pos = [width - 20, round(height/2), 20, 80]
player1_points = 0
player2_points = 0
radius = 10

font = pygame.font.Font('freesansbold.ttf', 20)

#creating surface
screen = pygame.display.set_mode(size)

fps = pygame.time.Clock()
paused = False
single = True
multi = False

ball_pos1 = [round(width/2), round(height/2)]


def update():
    #movement of the ball
    ball_pos1[0] += speed[0]
    ball_pos1[1] += speed[1]

def render():
    #rendering text
    txt = 'Player1 : ' + str(player1_points) + '   Player2 : ' + str(player2_points)
    text = font.render(txt, True, white, black)
    textRect = text.get_rect()
    textRect.center = (round(width/2), 25)
    screen.fill(black)      #erasing the screen
    screen.blit(text, textRect)     #adding text to the screen

    #drawing ball and rackets
    pygame.draw.circle(screen, white, ball_pos1, radius, 0)
    pygame.draw.rect(screen, white, player1_pos, 0)
    pygame.draw.rect(screen, white, player2_pos, 0)

    pygame.display.update()
    fps.tick(60)

while 1:
    keys = pygame.key.get_pressed()
    destination_speed = speed

    for event in pygame.event.get():
        #exiting game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            #pausing / unpausing game
            if event.key == pygame.K_SPACE:
                paused = not paused
            #switching to single mode
            if event.key == pygame.K_s:
                single = True
                multi = False
            #switching to multiplayer mode
            if event.key == pygame.K_m:
                single = False
                multi = True

    if not paused:
        update()
        render()

    #ball bouncing off horizontal edges of screen
    if ball_pos1[1] - radius < 0 or ball_pos1[1] + radius > height:
        speed[1] = -speed[1]


    if not paused:
        #moving left racket
        if keys[pygame.K_UP]:
            if player1_pos[1] < 5:      #checking if racket would move outside screen border
                player1_pos[1] = 0
            else:
                player1_pos[1] -= 5

        if keys[pygame.K_DOWN]:
            if player1_pos[1] + player1_pos[3] > height - 5:        #checking if racket would move outside screen border
                player1_pos[1] = height - player1_pos[3]
            else:
                player1_pos[1] += 5

        #multiplayer game
        if multi:
            #moving right racket
            if pygame.mouse.get_pos()[1] < player2_pos[1] + 0.5 * player2_pos[3]:
                if player2_pos[1] < 5:      #checking if racket would move outside screen border
                    player2_pos[1] = 0
                else:
                    player2_pos[1] -= 5

            if pygame.mouse.get_pos()[1] > player2_pos[1] + 0.5 * player2_pos[3]:
                if player2_pos[1] + player2_pos[3] > height - 5:        #checking if racket would move outside screen border
                    player2_pos[1] = height - player2_pos[3]
                else:
                    player2_pos[1] += 5
        #single player game - calculating where the ball is headed
        if single:

            if ball_pos1[0] == player1_pos[0] + player1_pos[2] + radius + speed[0] or (ball_pos1[0] == (round(width/2 + speed[0])) and ball_pos1[1] == (round(height/2) + speed[0]) and numpy.sign(speed[0]) == 1)  or (ball_pos1[0] == (round(width/2) +2*speed[0]) and ball_pos1[1] == (round(height/2) + 2*speed[0]) and numpy.sign(speed[0]) == 1):
                if numpy.sign(speed[1]) == 1 and width - player2_pos[2] - radius - ball_pos1[0] < height - ball_pos1[1]:
                    destination = height - ball_pos1[1] + player2_pos[2] + radius + ball_pos1[0] - width        #destination is where our ball is headed
                if numpy.sign(speed[1]) == -1 and width - player2_pos[2] - radius - ball_pos1[0] < ball_pos1[1]:
                    destination = ball_pos1[1] + player2_pos[2] + radius + ball_pos1[0] - width
                if numpy.sign(speed[1]) == 1 and width - player2_pos[2] - radius - ball_pos1[0] == height - ball_pos1[1]:
                    destination = height - radius
                if numpy.sign(speed[1]) == -1 and width - player2_pos[2] - radius - ball_pos1[0] == ball_pos1[1]:
                    destination = radius
                if numpy.sign(speed[1]) == 1 and width - player2_pos[2] - radius - ball_pos1[0] > height - ball_pos1[1]:
                    n = (width - player2_pos[2] - radius - ball_pos1[0] - height + ball_pos1[1])/height
                    m = int(n)
                    if m % 2 == 0:
                        destination = height - (width - player2_pos[2] - radius - ball_pos1[0] - height + ball_pos1[1] - m*height)
                    if m % 2 != 0:
                        destination = (width - player2_pos[2] - radius - ball_pos1[0] - height + ball_pos1[1] - m*height)
                if numpy.sign(speed[1]) == -1 and width - player2_pos[2] - radius - ball_pos1[0] > ball_pos1[1]:
                    n = (width - player2_pos[2] - radius - ball_pos1[0] - ball_pos1[1]) / height
                    m = int(n)
                    if m % 2 == 0:
                        destination = (width - player2_pos[2] - radius - ball_pos1[0] - ball_pos1[1] - m * height)
                    if m % 2 != 0:
                        destination = height - (width - player2_pos[2] - radius - ball_pos1[0] - ball_pos1[1] - m * height)




            #moving player2 racket where the ball is headed

            if difficulty == "hard":
                if player2_pos[1] + (player2_pos[3]) / 2 < destination:
                    if player2_pos[1] + player2_pos[3] > height - 5:  # checking if racket would move outside screen border
                        player2_pos[1] = height - player2_pos[3]
                    else:
                        player2_pos[1] += 5
                if player2_pos[1] + (player2_pos[3]) / 2 > destination:
                    if player2_pos[1] < 5:  # checking if racket would move outside screen border
                        player2_pos[1] = 0
                    else:
                        player2_pos[1] -= 5

            if difficulty == "medium":
                if ball_pos1[0] > round(3*width/4):
                    if player2_pos[1] + (player2_pos[3]) / 2 < destination:
                        if player2_pos[1] + player2_pos[3] > height - 5:  # checking if racket would move outside screen border
                            player2_pos[1] = height - player2_pos[3]
                        else:
                            player2_pos[1] += 5
                    if player2_pos[1] + (player2_pos[3]) / 2 > destination:
                        if player2_pos[1] < 5:  # checking if racket would move outside screen border
                            player2_pos[1] = 0
                        else:
                            player2_pos[1] -= 5

            if difficulty == "easy":
                if ball_pos1[0] > round(4*width/5):
                    if player2_pos[1] + (player2_pos[3]) / 2 < destination:
                        if player2_pos[1] + player2_pos[3] > height - 5:  # checking if racket would move outside screen border
                            player2_pos[1] = height - player2_pos[3]
                        else:
                            player2_pos[1] += 5
                    if player2_pos[1] + (player2_pos[3]) / 2 > destination:
                        if player2_pos[1] < 5:  # checking if racket would move outside screen border
                            player2_pos[1] = 0
                        else:
                            player2_pos[1] -= 5




    #ball bouncing off rackets

    if ball_pos1[0] - radius < player1_pos[0] + player1_pos[2]:
        if ball_pos1[1] + radius >= player1_pos[1] and ball_pos1[1] - radius <= player1_pos[1] + player1_pos[3]:
            speed[0] = -speed[0]
            ball_pos1[0] = player1_pos[0] + player1_pos[2] + radius

    if ball_pos1[0] + radius > player2_pos[0]:
        if ball_pos1[1] + radius >= player2_pos[1] and ball_pos1[1] - radius <= player2_pos[1] + player2_pos[3]:
            speed[0] = -speed[0]
            ball_pos1[0] = player2_pos[0] - radius



    #ball landing on vertical edge of screen - gaining points

    if ball_pos1[0] - radius <= 0 or ball_pos1[0] + radius >= width:
        if ball_pos1[0] - radius <= 0:
            player2_points +=1
        if ball_pos1[0] + radius >= width:
            player1_points +=1
        #reseting ball position
        ball_pos1[0] = position1[0]
        ball_pos1[1] = position1[1]
        speed[0] = -speed[0]
        update()
        render()
        paused = True

    #reseting points
    if keys[pygame.K_r]:
        player1_points = 0
        player2_points = 0
        ball_pos1[0] = position1[0]
        ball_pos1[1] = position1[1]
        update()
        render()
        paused = True

    #seting ball speed
    if keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3] or keys[pygame.K_4] or keys[pygame.K_5] or keys[pygame.K_6] or keys[pygame.K_7] or keys[pygame.K_8] or keys[pygame.K_9]:
        newspeed = event.key -48
        sign0 = numpy.sign(speed[0])
        sign1 = numpy.sign(speed[1])
        speed = [sign0 * newspeed, sign1 * newspeed]
