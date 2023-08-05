import sys

import pygame
import time
import random
pygame.font.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("minesweeper")

BG = pygame.transform.scale(pygame.image.load("space picture.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
BOARD = pygame.transform.scale(pygame.image.load("grid.png"), (SCREEN_HEIGHT*6/7, SCREEN_HEIGHT*6/7))

BOARD_ROW = 20
BOARD_COL = 20

FONT = pygame.font.SysFont("comicsans", 20)

ROOM_WIDTH = BOARD.get_width()/BOARD_ROW
ROOM_HEIGHT = BOARD.get_height()/BOARD_COL

BLANK_WIDTH = SCREEN_WIDTH/2 - BOARD.get_width()/2
BLANK_HEIGHT = SCREEN_HEIGHT/2 - BOARD.get_height()/2

MINECOUNT = 70

BOMB = pygame.transform.scale(pygame.image.load("bomb.jpg"),(ROOM_WIDTH, ROOM_HEIGHT))
VOID = pygame.transform.scale(pygame.image.load("blank.jpg"), (ROOM_WIDTH, ROOM_HEIGHT))
FLAG = pygame.transform.scale(pygame.image.load("flag.jpg"), (ROOM_WIDTH, ROOM_HEIGHT))
GREEN_FLAG = pygame.transform.scale(pygame.image.load("greenflag.png"), (ROOM_WIDTH, ROOM_HEIGHT))
CRATE = pygame.transform.scale(pygame.image.load("crate.png"), (ROOM_WIDTH, ROOM_HEIGHT))
NUMBER1 = pygame.transform.scale(pygame.image.load("one1.png"), (ROOM_WIDTH, ROOM_HEIGHT))
NUMBER2 = pygame.transform.scale(pygame.image.load("two2.png"), (ROOM_WIDTH, ROOM_HEIGHT))
NUMBER3 = pygame.transform.scale(pygame.image.load("three3.png"), (ROOM_WIDTH, ROOM_HEIGHT))
NUMBER4 = pygame.transform.scale(pygame.image.load("four4.png"), (ROOM_WIDTH, ROOM_HEIGHT))
NUMBER5 = pygame.transform.scale(pygame.image.load("five5.png"), (ROOM_WIDTH, ROOM_HEIGHT))
NUMBER6 = pygame.transform.scale(pygame.image.load("six6.png"), (ROOM_WIDTH, ROOM_HEIGHT))
GAMEOVER = pygame.transform.scale(pygame.image.load("gameover.png"), (BOARD.get_width()/2, BOARD.get_height()/2))
PLAYAGAIN = pygame.transform.scale(pygame.image.load("playagain.png"), (GAMEOVER.get_width()/2, GAMEOVER.get_height()/10))
GAMECLEAR = pygame.transform.scale(pygame.image.load("gameclear.png"), (BOARD.get_width()/2, BOARD.get_height()/2))


class values:
    boardclicked = False
    redflag = True
    gameover = False
    flagsinrooms = 0
    mineleft = MINECOUNT
    gameovertime = 0
    Ans = {}
    rooms = {}
    win = False
    minerooms = []

class constants:
    mine = "mine"
    void = 0
    flag = "flag"
    crate = "crate"
    number1 = 1
    number2 = 2
    number3 = 3
    number4 = 4
    number5 = 5
    number6 = 6

def restart():
    values.boardclicked = False
    values.redflag = True
    values.gameover = False
    values.flagsinrooms = 0
    values.mineleft = MINECOUNT
    values.gameovertime = 0
    values.Ans = {}
    values.rooms = {}
    values.win = False
    values.minerooms = []



def roomCord(pos):
    roomcord = (((pos[0]-BLANK_WIDTH)//ROOM_WIDTH)+1, ((pos[1]-BLANK_HEIGHT)//ROOM_HEIGHT)+1)
    return roomcord


def around(rc):
    ar = [(rc[0]-1, rc[1]-1), (rc[0], rc[1]-1), (rc[0]+1, rc[1]-1), (rc[0]-1, rc[1]), (rc[0]+1, rc[1]), (rc[0]-1, rc[1]+1), (rc[0], rc[1]+1), (rc[0]+1, rc[1]+1)]
    delr = []
    for r in ar:
        if not 0 < r[0] < 21 or not 0 < r[1] < 21:
            delr.append(r)
    for dr in delr:
        ar.remove(dr)
    return ar


def genAns(firstclicked):
    minecnt = 0

    while minecnt < MINECOUNT:
        x = random.randint(1, BOARD_ROW)
        y = random.randint(1, BOARD_COL)
        mineset1 = True
        surroundedmine = 0

        if x == firstclicked[0] and y == firstclicked[1]:
            mineset1 = False

        armine = True
        hassix = False
        for r1 in around((x, y)):
            if values.Ans[r1] != constants.mine:
                armine = False
            if values.Ans[r1] == constants.number6:
                hassix = True
        if armine or hassix:
            mineset1 = False

        if values.Ans[(x, y)] == constants.mine:
            mineset1 = False

        if mineset1:
            values.Ans[(x, y)] = constants.mine
            values.minerooms.append((x, y))
            minecnt += 1
            for r3 in around((x, y)):
                if values.Ans[r3] != constants.mine:
                    values.Ans[r3] += 1


def roomExpansion(rc):
    step = 1
    exprooms = []
    exprooms.append(rc)
    nextrooms = {}
    nextrooms[step] = [rc, 0]
    while True:
        afterroom = []
        nextappended = False
        for r1 in nextrooms[step]:
            if r1 != 0:
                for r2 in around(r1):
                    exist1 = False
                    for r3 in exprooms:
                        if r2 == r3:
                            exist1 = True
                    if not exist1:
                        if values.Ans[r2] != constants.mine:
                            exprooms.append(r2)

                    exist2 = False
                    for r6 in around(r2):
                        if values.Ans[r6] == constants.mine:
                            exist2 = True
                    for r4 in nextrooms:
                        for r5 in nextrooms[r4]:
                            if r2 == r5:
                                exist2 = True
                    if not exist2:
                        afterroom.append(r2)
                        nextappended = True

        if not nextappended:
            break
        step += 1
        nextrooms[step] = afterroom

    return exprooms



def draw(elapsed_time):
    WIN.blit(BG, (0, 0))
    WIN.blit(BOARD, (SCREEN_WIDTH/2-BOARD.get_width()/2, SCREEN_HEIGHT/2-BOARD.get_height()/2))

    if values.redflag:
        WIN.blit(FLAG, (SCREEN_WIDTH/2-ROOM_WIDTH/2, 10))
    else:
        WIN.blit(GREEN_FLAG, (SCREEN_WIDTH/2-ROOM_WIDTH/2, 10))

    for r in values.rooms:
        if values.rooms[r] == constants.crate:
            WIN.blit(CRATE, (SCREEN_WIDTH/2-BOARD.get_width()/2+ROOM_WIDTH*(r[0]-1), SCREEN_HEIGHT/2-BOARD.get_width()/2+ROOM_HEIGHT*(r[1]-1)))
        elif values.rooms[r] == constants.flag:
            WIN.blit(FLAG, (SCREEN_WIDTH/2-BOARD.get_width()/2+ROOM_WIDTH*(r[0]-1), SCREEN_HEIGHT/2-BOARD.get_width()/2+ROOM_HEIGHT*(r[1]-1)))
        elif values.rooms[r] == constants.void:
            WIN.blit(VOID, (SCREEN_WIDTH/2-BOARD.get_width()/2+ROOM_WIDTH*(r[0]-1), SCREEN_HEIGHT/2-BOARD.get_width()/2+ROOM_HEIGHT*(r[1]-1)))
        elif values.rooms[r] == constants.number1:
            WIN.blit(NUMBER1, (SCREEN_WIDTH/2-BOARD.get_width()/2+ROOM_WIDTH*(r[0]-1), SCREEN_HEIGHT/2-BOARD.get_width()/2+ROOM_HEIGHT*(r[1]-1)))
        elif values.rooms[r] == constants.number2:
            WIN.blit(NUMBER2, (SCREEN_WIDTH/2-BOARD.get_width()/2+ROOM_WIDTH*(r[0]-1), SCREEN_HEIGHT/2-BOARD.get_width()/2+ROOM_HEIGHT*(r[1]-1)))
        elif values.rooms[r] == constants.number3:
            WIN.blit(NUMBER3, (SCREEN_WIDTH/2-BOARD.get_width()/2+ROOM_WIDTH*(r[0]-1), SCREEN_HEIGHT/2-BOARD.get_width()/2+ROOM_HEIGHT*(r[1]-1)))
        elif values.rooms[r] == constants.number4:
            WIN.blit(NUMBER4, (SCREEN_WIDTH/2-BOARD.get_width()/2+ROOM_WIDTH*(r[0]-1), SCREEN_HEIGHT/2-BOARD.get_width()/2+ROOM_HEIGHT*(r[1]-1)))
        elif values.rooms[r] == constants.number5:
            WIN.blit(NUMBER5, (SCREEN_WIDTH/2-BOARD.get_width()/2+ROOM_WIDTH*(r[0]-1), SCREEN_HEIGHT/2-BOARD.get_width()/2+ROOM_HEIGHT*(r[1]-1)))
        elif values.rooms[r] == constants.number6:
            WIN.blit(NUMBER6, (SCREEN_WIDTH/2-BOARD.get_width()/2+ROOM_WIDTH*(r[0]-1), SCREEN_HEIGHT/2-BOARD.get_width()/2+ROOM_HEIGHT*(r[1]-1)))
        elif values.rooms[r] == constants.mine:
            WIN.blit(BOMB, (SCREEN_WIDTH/2-BOARD.get_width()/2+ROOM_WIDTH*(r[0]-1), SCREEN_HEIGHT/2-BOARD.get_width()/2+ROOM_HEIGHT*(r[1]-1)))

    if values.gameover:
        WIN.blit(GAMEOVER, (SCREEN_WIDTH/2-GAMEOVER.get_width()/2, SCREEN_HEIGHT/2-GAMEOVER.get_height()/2))
        WIN.blit(PLAYAGAIN, (SCREEN_WIDTH/2-PLAYAGAIN.get_width()/2, SCREEN_HEIGHT/2 + GAMEOVER.get_height()/2 + 10))
        time_text = FONT.render(f"Time: {round(values.gameovertime)}s", 1, "white")
        WIN.blit(time_text, (BLANK_WIDTH, 10))
    elif values.win:
        WIN.blit(GAMECLEAR, (SCREEN_WIDTH/2-GAMEOVER.get_width()/2, SCREEN_HEIGHT/2-GAMECLEAR.get_height()/2))
        WIN.blit(PLAYAGAIN, (SCREEN_WIDTH/2-PLAYAGAIN.get_width()/2, SCREEN_HEIGHT/2 + GAMECLEAR.get_height()/2 + 10))
    else:
        time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
        WIN.blit(time_text, (BLANK_WIDTH, 10))


    mine_count = FONT.render(f"Mine Left: {values.mineleft}", 1, "red")
    WIN.blit(mine_count, (SCREEN_WIDTH - BLANK_WIDTH - mine_count.get_width(), 10))

    pygame.display.update()



def main():
    run = True

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    r = 1
    c = 1
    while c <= BOARD_COL:
        while r <= BOARD_ROW:
            values.rooms[(r, c)] = constants.crate
            values.Ans[(r, c)] = constants.void
            r += 1
        r = 1
        c += 1

    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                rc = roomCord(pos)
                if not values.gameover and not values.win:
                    if BLANK_WIDTH < pos[0] < SCREEN_WIDTH-BLANK_WIDTH and BLANK_HEIGHT < pos[1] < SCREEN_HEIGHT-BLANK_HEIGHT:
                        if values.redflag:
                            if values.rooms[rc] == constants.crate:
                                if not values.boardclicked:
                                    genAns(rc)
                                    for r in roomExpansion(rc):
                                        values.rooms[r] = values.Ans[r]
                                    values.boardclicked = True
                                if values.Ans[rc] == constants.mine:
                                    values.rooms[rc] = constants.mine
                                    values.mineleft -= 1
                                    values.gameover = True
                                    for r in values.rooms:
                                        if values.Ans[r] == constants.mine:
                                            values.rooms[r] = values.Ans[r]
                                    values.gameovertime = elapsed_time
                                else:
                                    for r in roomExpansion(rc):
                                        if values.rooms[r] == constants.crate:
                                            values.rooms[r] = values.Ans[r]


                        if not values.redflag:
                            if values.rooms[rc] == constants.crate:
                                if values.mineleft == 0:
                                    values.win = True
                                values.rooms[rc] = constants.flag
                                values.mineleft -= 1
                            elif values.rooms[rc] == constants.flag:
                                values.rooms[rc] = constants.crate
                                values.mineleft += 1
                            else:
                                pass
                        else:
                            pass

                    if SCREEN_WIDTH/2-GREEN_FLAG.get_width()/2 < pos[0] < SCREEN_WIDTH/2+GREEN_FLAG.get_width()/2 and 10 < pos[1] < 10+GREEN_FLAG.get_height():
                        values.redflag = not values.redflag

                elif values.gameover or values.win:
                    if SCREEN_WIDTH/2-PLAYAGAIN.get_width()/2 < pos[0] < SCREEN_WIDTH/2-PLAYAGAIN.get_width()/2+PLAYAGAIN.get_width() and SCREEN_HEIGHT/2 + GAMEOVER.get_height()/2 < pos[1] < SCREEN_HEIGHT/2 + GAMEOVER.get_height()/2 + PLAYAGAIN.get_height():
                        restart()
                        main()

                if values.mineleft == 0:
                    allmatch = True
                    for rc in values.minerooms:
                        if values.rooms[rc] != constants.flag:
                            allmatch = False
                    if allmatch:
                        values.win = True


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    values.redflag = not values.redflag





        draw(elapsed_time)
    pygame.quit()


if __name__ == "__main__":
    main()