#new space game

from subprocess import HIGH_PRIORITY_CLASS
from tkinter import font
import pygame, os, Button, random

#init
pygame.init()
pygame.font.init()
pygame.mixer.init()
random.seed()

#colors
WHITE = (255, 255, 255)

#fonts
header_font = pygame.font.SysFont("Broadway", 100, bold = True)
standard_font = pygame.font.SysFont("Broadway", 70)
score_font = pygame.font.SysFont("Broadway", 50)

#root
FPS = 60
root = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = root.get_width(), root.get_height()

#variables
r_w, r_h = 130, 70



#images
rocket_image = pygame.transform.scale(pygame.image.load(os.path.join("materials", "rocket.png")), (r_w, r_h))
background_image = pygame.transform.scale(pygame.image.load(os.path.join("materials", "background.png")), (WIDTH, HEIGHT))
exit_image = pygame.transform.scale(pygame.image.load(os.path.join("materials", "exit.png")), (70, 70))
komet_image = pygame.image.load(os.path.join("materials", "komet.png"))
komet_image1 = pygame.image.load(os.path.join("materials", "komet1.png"))

#sound
background = pygame.mixer.Sound(os.path.join("materials", "background.mp3"))
death_sound = pygame.mixer.Sound(os.path.join("materials", "death_sound.mp3"))


#widgets
EXIT_BUTTON = Button.Button(WIDTH-120, 50, exit_image, 1)
GAME_OVER = header_font.render("Game over", True, WHITE)
RESTART_TEXT = standard_font.render("Restart", True, WHITE) 
RESTART_BUTTON = Button.Button(WIDTH/2-RESTART_TEXT.get_width()/2, 300, RESTART_TEXT, 1)
QUIT_TEXT = standard_font.render("QUIT game", True, WHITE) 
QUIT_BUTTON = Button.Button(WIDTH/2-QUIT_TEXT.get_width()/2, 400, QUIT_TEXT, 1)


def show_window():
    global start_time
    global started
    global kometlist
    global SPEED
    global spawn_rate
    global Vel
    if start_time % 100 == True:
        SPEED += 0.2
        Vel += 0.2
        try:
            spawn_rate -= 1
        except:
            pass
    root.blit(background_image, (0, 0))
    SCORE_TEXT = score_font.render("Score: " + str(start_time), True, WHITE)
    if started == True:    
        start_time += 1    
        rocket = pygame.Rect(r_x, r_y, r_w, r_h)
        add_komet()
        for kometen in kometlist:
            if kometen[2] == 1:
                kometen[0] -= SPEED
                root.blit(komet_image, (kometen[0], kometen[1]))
                komet = pygame.Rect(kometen[0], kometen[1], komet_image.get_height()-30, komet_image.get_height()-30)
                check_collision(rocket, komet)
            elif kometen[2] == 2:
                kometen[0] -= SPEED + 5
                root.blit(komet_image1, (kometen[0], kometen[1]))
                komet = pygame.Rect(kometen[0], kometen[1], komet_image1.get_height()-30, komet_image1.get_height()-30)
                check_collision(rocket, komet)
        root.blit(SCORE_TEXT, (WIDTH/2 - SCORE_TEXT.get_width()/2, HEIGHT*3/50))
    else:
        end_screen(SCORE_TEXT)
    if EXIT_BUTTON.draw(root):
        quit()
    root.blit(rocket_image, (r_x, r_y))       
    pygame.display.update()

def add_komet():
    global kometlist
    if start_time % spawn_rate + 1 == True: 
        kometlist.append([WIDTH, random.randint(0, HEIGHT-50), random.randint(1, 2)])
    

def check_collision(rocket, komet):
    global started
    if rocket.colliderect(komet):
        death_sound.play()
        started = False
        SCORE_REACHED = score_font.render("Score: " + str(start_time), True, WHITE)
        end_screen(SCORE_REACHED)
    
def end_screen(SCORE_REACHED): 
    check_highscore()
    root.blit(GAME_OVER, (WIDTH/2-GAME_OVER.get_width()/2, 100))
    root.blit(SCORE_REACHED, (WIDTH/2- SCORE_REACHED.get_width()/2, 200))
    root.blit(score_font.render("High Score = " + str(check_highscore()), True, WHITE), (WIDTH/2-220, HEIGHT-100))
    if RESTART_BUTTON.draw(root):
        background.stop()
        start_game()
        
    if QUIT_BUTTON.draw(root):
        quit()

def start_game():
    global r_x, r_y, start_time, SPEED, started, kometlist, spawn_rate, Vel
    start_time = 0
    r_x, r_y = WIDTH/3, HEIGHT/2-50
    SPEED = 10
    started = True 
    kometlist = [[WIDTH, 400, 1]]
    spawn_rate = 51
    Vel = 12
    background.play()

def check_highscore():
    high_score_file = open("highscore.txt", "r")
    high_score = int(high_score_file.read())
    high_score_file.close()
    if high_score < start_time:
        high_score_file = open("highscore.txt", "w")
        high_score_file.write(str(start_time))
        high_score_file.close()
        high_score_file = open("highscore.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
    return high_score
        
    
        

def r_movement(keys_pressed):
    global r_x
    global r_y
    if keys_pressed[pygame.K_a] and r_x - Vel > 0:  # Left
       r_x = r_x - Vel
    if keys_pressed[pygame.K_d] and r_x + Vel + r_w < WIDTH:  # Right
       r_x = r_x + Vel
    if keys_pressed[pygame.K_w] and r_y - Vel > 0:  # Up
       r_y = r_y - Vel
    if keys_pressed[pygame.K_s] and r_y + Vel + r_h < HEIGHT:  # Up
       r_y = r_y + Vel

def quit():
    pygame.display.quit()
    exit()

def main():
    clock = pygame.time.Clock()
    run = True 
    while run: 
        global start_time
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        r_movement(keys_pressed)
        show_window()
    quit()

if __name__ == "__main__":
    start_game()
    main()