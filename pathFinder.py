import pygame
from pygame.locals import *
import sys
from math import floor, ceil
from pprint import pprint
import time
from path_algorithm import Path
from copy import deepcopy

squareSize = 20
amountOfSquares = 20
menuHeight = 100

boardWidth = squareSize * amountOfSquares
boardHeight = squareSize * amountOfSquares
winWidth = boardWidth
winHeight = boardHeight + menuHeight

fpsClock = 60

# colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (150, 150, 150)
red = (220, 20, 60)
blue = (0, 0, 255)
green = (0, 128, 0)
gold = (179, 161, 111)
darkBlue = (40, 49, 74)

board = [[0
          for _ in range(amountOfSquares)
          ]
         for _ in range(amountOfSquares)
         ]

boardOnlyObstacles = deepcopy(board)


def print_board(board):
    for row in board:
        print(row)


def main():

    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((winWidth, winHeight))
    display.fill(white)
    draw_menu(display)
    draw_grid(display)
    pygame.display.update()

    pygame.display.set_caption('Path finder')

    mouseClicked = False
    mouseX = 0
    mouseY = 0
    pressed = ""

    global font, fontSize
    fontSize = 38
    font = pygame.font.Font('freesansbold.ttf', fontSize)

    start = 0
    end = 0

    # mark start and end points

    while True:
        # get action made by player
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos

            elif event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos

                if mouseX < winWidth / 2 and mouseY > boardHeight and start == 0:
                    change_button_color_onclick(display, "START", color=grey)

                    while True:
                        event = pygame.event.wait()
                        if event.type == MOUSEBUTTONDOWN:
                            mouseX, mouseY = event.pos
                            if mouseY < boardHeight and start == 0:
                                # mark start
                                start = draw_clicked_box(
                                    mouseX, mouseY, display, color=green)
                                startCoordinates = get_matrix_coordinates_of_square(
                                    start, num=2)
                                pygame.display.update()
                                break
                            else:
                                continue

                elif mouseX > winWidth / 2 and mouseY > boardHeight and end == 0:
                    change_button_color_onclick(display, "FINISH", color=grey)

                    while True:
                        event = pygame.event.wait()
                        if event.type == MOUSEBUTTONDOWN:
                            mouseX, mouseY = event.pos
                            if mouseY < boardHeight and end == 0:
                                # mark end
                                end = draw_clicked_box(
                                    mouseX, mouseY, display, color=red)
                                endCoordinates = get_matrix_coordinates_of_square(
                                    end, num=3)
                                pygame.display.update()
                                break
                            else:
                                continue

        if start != 0:
            hide_menu(display, "START")
        if end != 0:
            hide_menu(display, "FINISH")

        pygame.display.update()
        if start != 0 and end != 0:
            break
        else:
            continue

    # draw obstacles
    while True:
        draw_run_buttion(display)
        pygame.display.update()
        # get action made by player
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos

            elif event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos

                if mouseY > boardHeight:
                    change_button_color_onclick(display, "FIND", color=grey)
                    pygame.display.update()

                    path = Path(board, start=startCoordinates,
                                finish=endCoordinates).pathCoordinates

                    for step in path:
                        XY = get_board_coordinates_from_boardYX(step)
                        if step == startCoordinates or step == endCoordinates:
                            continue
                        else:
                            draw_clicked_box(XY[0], XY[1], display, color=gold)
                            pygame.display.update()
                            time.sleep(0.1)
                    event = pygame.event.wait()
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                else:
                    clickedSquare = draw_clicked_box(mouseX, mouseY, display)
                    mark_square_on_matrix(clickedSquare)
                    pygame.display.update()
                    while True:
                        event = pygame.event.wait()
                        if event.type == MOUSEMOTION:
                            mouseX, mouseY = event.pos
                            clickedSquare = draw_clicked_box(
                                mouseX, mouseY, display)
                            mark_square_on_matrix(clickedSquare)
                            pygame.display.update()
                            continue
                        elif event.type == MOUSEBUTTONUP:
                            break

        pygame.display.update()
    clock.tick(fpsClock)


def draw_grid(display):
    for x in range(amountOfSquares):
        pygame.draw.line(display, grey, (x * squareSize, 0),
                         (x * squareSize, boardWidth))
    for y in range(amountOfSquares + 1):
        pygame.draw.line(display, grey, (0, y * squareSize),
                         (boardHeight, y * squareSize))


def draw_menu(display):
    boldness = 3
    # draw START BOX
    startPosX = 0
    startPosY = int(round(winHeight - menuHeight + boldness / 2, 0))
    pygame.draw.rect(display, green, (startPosX,
                                      startPosY, int(winWidth / 2), menuHeight), boldness)
    # draw FINISH BOX
    endPosX = int(winWidth / 2)
    endPosY = int(round(winHeight - menuHeight + boldness / 2, 0))
    pygame.draw.rect(display, red, (endPosX,
                                    endPosY, int(winWidth / 2), menuHeight), boldness)
    # display text
    display_text(display, "MARK START", green, x=winWidth /
                 4, y=boardHeight + menuHeight / 2)
    display_text(display, "MARK FINISH", red, x=winWidth /
                 4 + winWidth / 2, y=boardHeight + menuHeight / 2)


def draw_run_buttion(display):
    boldness = 3

    startPosX = int(winWidth / 4)
    startPosY = int(round(winHeight - menuHeight + boldness / 2, 0))
    pygame.draw.rect(display, white, (startPosX,
                                      startPosY, int(winWidth / 2), menuHeight), 0)
    pygame.draw.rect(display, green, (startPosX,
                                      startPosY, int(winWidth / 2), menuHeight), boldness)
    display_text(display, "FIND PATH", green, x=int(winWidth /
                                                    2), y=int(round(boardHeight + menuHeight / 2, 0)))


def change_button_color_onclick(display, section, color=grey):
    boldness = 3
    if section == "START":
        startPosX = 0
        startPosY = int(round(winHeight - menuHeight + boldness / 2, 0))
        pygame.draw.rect(display, color, (startPosX,
                                          startPosY, int(winWidth / 2), menuHeight), 0)
        display_text(display, "MARK START", green, x=winWidth /
                     4, y=boardHeight + menuHeight / 2)
        pygame.display.update()
        time.sleep(0.1)

        pygame.draw.rect(display, white, (startPosX,
                                          startPosY, int(winWidth / 2), menuHeight), 0)
        pygame.draw.rect(display, green, (startPosX,
                                          startPosY, int(winWidth / 2), menuHeight), boldness)
        display_text(display, "MARK START", green, x=winWidth /
                     4, y=boardHeight + menuHeight / 2)
        pygame.display.update()

    elif section == "FINISH":
        endPosX = int(winWidth / 2)
        endPosY = int(round(winHeight - menuHeight + boldness / 2, 0))
        pygame.draw.rect(display, color, (endPosX,
                                          endPosY, int(winWidth / 2), menuHeight), 0)
        display_text(display, "MARK FINISH", red, x=winWidth /
                     4 + winWidth / 2, y=boardHeight + menuHeight / 2)
        pygame.display.update()
        time.sleep(0.1)
        pygame.draw.rect(display, white, (endPosX,
                                          endPosY, int(winWidth / 2), menuHeight), 0)
        pygame.draw.rect(display, red, (endPosX,
                                        endPosY, int(winWidth / 2), menuHeight), boldness)
        display_text(display, "MARK FINISH", red, x=winWidth /
                     4 + winWidth / 2, y=boardHeight + menuHeight / 2)
        pygame.display.update()

    elif section == "FIND":
        PosX = int(winWidth / 4)
        PosY = int(round(winHeight - menuHeight + boldness / 2, 0))
        pygame.draw.rect(display, color, (PosX,
                                          PosY, int(winWidth / 2), menuHeight), 0)
        display_text(display, "FIND PATH", green, x=int(winWidth /
                                                        2), y=int(round(boardHeight + menuHeight / 2, 0)))
        pygame.display.update()
        time.sleep(0.1)
        pygame.draw.rect(display, white, (PosX,
                                          PosY, int(winWidth / 2), menuHeight), 0)
        pygame.draw.rect(display, green, (PosX,
                                          PosY, int(winWidth / 2), menuHeight), boldness)
        display_text(display, "FIND PATH", green, x=int(winWidth /
                                                        2), y=int(round(boardHeight + menuHeight / 2, 0)))
        pygame.display.update()


def hide_menu(display, section):
    boldness = 3
    if section == "START":
        startPosX = 0
        startPosY = int(round(winHeight - menuHeight + boldness / 2, 0))
        pygame.draw.rect(display, white, (startPosX,
                                          startPosY, int(winWidth / 2), menuHeight), 0)

    elif section == "FINISH":
        endPosX = int(winWidth / 2)
        endPosY = int(round(winHeight - menuHeight + boldness / 2))
        pygame.draw.rect(display, white, (endPosX,
                                          endPosY, int(winWidth / 2), menuHeight), 0)


def display_text(display, string, color, x, y):
    font = pygame.font.Font('freesansbold.ttf', int(round(menuHeight/4, 0)))
    text = font.render(string, True, color)
    textRect = text.get_rect()
    textRect.center = (int(x), int(y))
    display.blit(text, textRect)


def draw_clicked_box(mouseX, mouseY, display, color=black):
    if mouseY > boardHeight:
        pass
    else:
        boxX = int(floor(mouseX / squareSize) * squareSize)
        boxY = int(floor(mouseY / squareSize) * squareSize)

        if board[int(boxY/squareSize)][int(boxX/squareSize)] != 0:
            pass
        else:
            if boxX + squareSize > boardWidth or boxY + squareSize > boardHeight:
                return None
            else:
                pygame.draw.rect(display, color, (boxX, boxY,
                                                  squareSize, squareSize), 0)
                return [boxX, boxY]


def get_board_coordinates_from_boardYX(YX):
    y = YX[0] * squareSize
    x = YX[1] * squareSize
    return [x, y]


def mark_square_on_matrix(clickedSquare, num=1):
    if clickedSquare == None:
        pass
    else:
        y = int(clickedSquare[1]/squareSize)
        x = int(clickedSquare[0]/squareSize)
        board[y][x] = num
        return [y, x]


def get_matrix_coordinates_of_square(clickedSquare, num=1):
    if clickedSquare == None:
        pass
    else:
        y = int(clickedSquare[1]/squareSize)
        x = int(clickedSquare[0]/squareSize)
        return [y, x]


if __name__ == "__main__":
    main()
