from random import randint
from datetime import datetime
import pygame
from sys import exit



pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1366, 768)) # ROZLISENI
pygame.display.set_caption('test')

WHITE = (255,255,255)
BLACK = (0,0,0)


pygame.font.init()
myfont = pygame.font.Font('Spline_Sans/static/SplineSans-Bold.ttf', 45)
# TEXTY ZOBRAZOVANE
textsurface1 = myfont.render('Pro další měření zmáčkni <- ', False, WHITE)
textsurface2 = myfont.render('Přerušení během měření je nutné držet <- ', False, WHITE)
textsurface3 = myfont.render('Pro spuštění je nutné kliknou myší', False, WHITE)
textsurface4 = myfont.render('Proběhlo 15 měření a test bude ukončen', False, WHITE)


posx = 500
posy = 100
start_time = 0
view_time_set = 0
view_time = 0
check = False
holding_check = False
check_right = False
check_mouse = False

list_casu = []
mereni = 15
i=0
datum = datetime.now()
datum = datum.strftime("%d.%m.%Y %H:%M:%S")
print(datum)

screen.blit(textsurface3,(200, 300))

# ZADANI NAZVU TXT
def start_console ():
    txt_name = input("Zadej název dokumentu: např.: jmeno-prijmeni_20C ")
    return txt_name
txt_name = start_console()
# VYTVORENI KRUHU
def circle (posx,posy,color):
    return (pygame.draw.circle(screen, color, (posx, posy), 30))
# VYTVORENI TXT + ZAPSANI
def txt (txt_name, list_casu,datum):
    with open('docs/' + txt_name + '.txt', 'w') as f:
        f.write(txt_name)
        f.write("\n \n")
        f.write(datum)
        f.write("\n \n")
        for times in list_casu:
            f.write(str(times) + ';')
    pygame.quit()


while True:
    for event in pygame.event.get():
# EXIT
        if event.type == pygame.QUIT:
            txt(txt_name, list_casu, datum)
            exit()
# KLIK ESC, LEVA SIPKA, PRAVA SIPKA - ( moznost editovat cas)
        if event.type == pygame.KEYDOWN:
# LEVA KLAVESA KLIK - 1. ( Zapnout randit)
            if event.key == pygame.K_LEFT and holding_check == False and i < 15: # tady dat AND pokud neni předtim přerušeno

                view_time_set = (randint(10,50) * 1000)
                #view_time_set = 1000
                view_time = pygame.time.get_ticks() + view_time_set
                check = True
                posx = randint(30,1336)
                posy = randint(30,738)
                screen.fill((BLACK))
                check_right = False
# LEVA KLAVESA KLIK - po preruseni
            elif event.key == pygame.K_LEFT and holding_check == True:
                view_time = pygame.time.get_ticks() + view_time_set
                holding_check = False
                check = True
                print("AGAIN AGAIN AGAIN AGAIN AGAIN")
                screen.fill((BLACK))
                check_right = False
# PRAVÁ KLAVESA KLIK
            elif event.key == pygame.K_RIGHT and (int(view_time/1000)) <= (int(pygame.time.get_ticks()/1000)) and check_right == True and i < 15:
                check = False
                check_right = False
                list_casu.append((pygame.time.get_ticks()) - (int(view_time/1000))*1000)
                i += 1
                screen.blit(textsurface1,(300,300))
# EXIT ESC
            elif event.key == pygame.K_ESCAPE: txt(txt_name, list_casu, datum), pygame.exit()
# PUSTENI LEVE KLAVESY
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and (int(view_time/1000)) > (int(pygame.time.get_ticks()/1000)):
                holding_check = True
                check = False
                print("PAUSE")
                screen.blit(textsurface2,(400, 300))
            elif event.key == pygame.K_LEFT and (int(view_time / 1000)) <= (int(pygame.time.get_ticks() / 1000)):
                check_right = True
# KLIK MYS
        elif event.type == pygame.MOUSEBUTTONDOWN:
            screen.fill(BLACK)
            check_mouse = True

# ZOBRAZ. KRUHU
    if (int(view_time/1000)) == (int(pygame.time.get_ticks()/1000)) and check == True:
        circle(posx, posy, WHITE)
        print("Objevil se kruh !")
        check = False
# ZOBRAZ. ZPRAVY KONEC
    if i == 15:
        screen.fill(BLACK)
        screen.blit(textsurface4, (300, 300))
# TERMINAL ZPRAVA MOUSE
    if check_mouse == False: print("MOUSE MOUSE MOUSE MOUSE")
# INFO TERMINAL
    if i == 0: print( i+1 ,(int(view_time / 1000)), (int(pygame.time.get_ticks() / 1000)) )
    else: print( i+1 ,(int(view_time / 1000)), (int(pygame.time.get_ticks() / 1000)), "měření", i , list_casu[i-1] )

    pygame.display.update()
    clock.tick(60)
