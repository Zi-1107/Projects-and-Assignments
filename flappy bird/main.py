import pygame as pg
import sys
import random
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 800
GRAVITY = 0.3
global score
score = 0

def rotate_b(bird):
    return pg.transform.rotozoom(bird, -bird_resultant_movement*5, 1)

def update_highest_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def check_collision(pipes):
    for p in pipes:
        if bird_hitbox.colliderect(p):
            hit_s.play()
            return False

    if bird_hitbox.bottom > SCREEN_HEIGHT or 0 > bird_hitbox.bottom:
        hit_s.play()
        return False
    return True
    
def print_score(g_active):
    if g_active == True:
        score_pic = game_font.render(f"Score:{str(int(score))}", True, (250, 250, 250))
        score_rect = score_pic.get_rect(center = (SCREEN_WIDTH/2, 100))
        screen.blit(score_pic, score_rect)
    else:
        score_pic = game_font.render(f"Score:{str(int(score))}", True, (250, 250, 250))
        score_rect = score_pic.get_rect(center = (SCREEN_WIDTH/2, 100))
        screen.blit(score_pic, score_rect)

        highest_score = game_font.render(f"High Score:{str(int(high_score))}", True, (250, 250, 250))
        high_score_rect = score_pic.get_rect(center = (SCREEN_WIDTH/2 - 40, 150))
        screen.blit(highest_score, high_score_rect)


def spawn():
    height_choice = random.choice(bottom_pipehieght)
    bottom_pipe = pipe.get_rect(midtop = (550, height_choice))
 
    top_pipe = pipe.get_rect(midbottom = (550, height_choice - 300))
    return bottom_pipe, top_pipe

def draw_p(pipes):
    for p in pipes:
        if p.bottom > SCREEN_HEIGHT:
            screen.blit(pipe, p)
        else:
            flip_pipe =  pg.transform.flip(pipe, False, True)
            screen.blit(flip_pipe, p)

def move_p(pipes):
    global score

    for p in pipes:
        p.centerx  -= 10
        
    for p in pipes:    
        if p.centerx < -100:
            pipes.remove(p)

    for p in pipes:
        if p.centerx < bird_hitbox.centerx :
            try:
                # score += 2.85714285714285714   
                score_s.play()
            except Exception as err:
                print(f"Error {err}, Score = {score}")
            
    return pipes

def d_floor():
    screen.blit(ground, (floorx, 760))
    screen.blit(ground, (floorx + 512, 760))

def d_gfloor():
    screen.blit(background, (gfloorx, 0))
    screen.blit(background, (gfloorx + 512, 0))
pg.mixer.pre_init()
pg.init()
flap_s = pg.mixer.Sound(r"C:\Users\ACER\Desktop\VS Code\flappy bird\sound\sfx_wing.wav")

score_s = pg.mixer.Sound(r"C:\Users\ACER\Desktop\VS Code\flappy bird\sound\sfx_point.wav")

hit_s = pg.mixer.Sound(r"C:\Users\ACER\Desktop\VS Code\flappy bird\sound\sfx_die.wav")

fps = pg.time.Clock()
screen = pg.display.set_mode((512, 800))
score = 0
high_score = 0
game_active = True
game_font = pg.font.Font(r"C:\Users\ACER\Desktop\VS Code\flappy bird\asset\04B_19.TTF" , 32)

background = pg.image.load(r"flappy bird\asset\sky.jpeg").convert_alpha()
background = pg.transform.scale2x(background)
gfloorx = 0


bird = pg.transform.scale2x(pg.image.load(r"flappy bird\asset\bird.png").convert_alpha())
bird_d = pg.transform.scale2x(pg.image.load(r"flappy bird\asset\bird_d.png").convert_alpha())
bird_u = pg.transform.scale2x(pg.image.load(r"flappy bird\asset\bird_u.png").convert_alpha())
birdlist = [bird_u, bird, bird_d]
bird_index = 0
current_bird = birdlist[bird_index]
bird_resultant_movement = 0
bird_hitbox = current_bird.get_rect(center = (64, 500))

FLAPBIRD = pg.USEREVENT + 1
pg.time.set_timer(FLAPBIRD, 250)

pipe = pg.image.load(r"flappy bird\asset\pipe.png").convert_alpha()
pipe = pg.transform.scale2x(pipe)
pipelist = []
bottom_pipehieght = [430, 467, 520]

SPAWNPIPE = pg.USEREVENT
pg.time.set_timer(SPAWNPIPE, 1200)

ground = pg.image.load(r"flappy bird\asset\land1.jpeg").convert_alpha()
ground =  pg.transform.scale2x(ground)
floorx = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and game_active == True:
                bird_resultant_movement = 0
                bird_resultant_movement -= 8
                print(bird_hitbox.centery)
                flap_s.play()
            if event.key == pg.K_SPACE and game_active == False:
                game_active = True
                pipelist.clear()
                bird_hitbox.center = (64, 500)
                bird_resultant_movement = -1
                score = 0

        if event.type == SPAWNPIPE:
            pipelist.extend(spawn())
        if event.type == FLAPBIRD:
            if bird_index >= 2:
                bird_index = 0
            bird_index += 1
            current_bird = birdlist[bird_index]


    # d_gfloor()
    # gfloorx -= 0.01
    # pg.display.update()
    # if  gfloorx < -521:
    #     gfloorx = 0

    screen.blit(background, (0, 0))

    # floor
    d_floor()
    floorx -= 3
    if  floorx < -521:
        floorx = 0

    

    if game_active == True:

        # pipes
        pipelist = move_p(pipelist)
        draw_p(pipelist)


        # bird
        bird_resultant_movement += GRAVITY
        bird_hitbox.centery += bird_resultant_movement
        rotated_bird = rotate_b(current_bird)
        # screen.blit(bird, bird_hitbox)
        screen.blit(rotated_bird, bird_hitbox)
        game_active = check_collision(pipelist) 
        print_score(game_active)
        score += (1/84)
    else:
        high_score = update_highest_score(score, high_score)
        print_score(game_active)

    pg.display.update()
    fps.tick(70)
 
pg.quit()