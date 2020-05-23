import pygame
from pygame.locals import *
import sys
from math import floor, ceil
import time
from math import sqrt, inf, fabs


squareSize = 20
amountOfSquares = 25
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


def get_clear_board():
    return [[0
             for _ in range(amountOfSquares)
             ]
            for _ in range(amountOfSquares)
            ]


def get_board_with_only_obstacles(board):
    boardOnlyObstacles = []
    rowOnlyObstacles = []
    for row in board:
        for number in row:
            if number == 1:
                rowOnlyObstacles.append(1)
            else:
                rowOnlyObstacles.append(0)
        boardOnlyObstacles.append(rowOnlyObstacles)
        rowOnlyObstacles = []
    return boardOnlyObstacles


def print_board(board):
    for row in board:
        print(row)


def create_named_graph(graph):
    i = 0
    for row in graph:
        i += len(row)
    height = len(graph)
    width = len(graph[0])
    namedGraph = []
    namedRow = []
    number = 0
    for y in range(height):
        for x in range(width):
            if graph[y][x] != 0:
                namedRow.append(0)
                continue
            number += 1
            namedRow.append(number)
        namedGraph.append(namedRow)
        namedRow = []

    return namedGraph


def get_vertex_position(namedGraph, vertex):
    size = len(namedGraph)

    for y in range(size):
        for x in range(size):
            if namedGraph[y][x] == vertex:
                return [y, x]


def get_row(board, x):
    return board[x]


def get_column(board, y):
    column = []
    for row in board:
        column.append(row[y])
    return column


def celculate_cost_of_travel(baseVertex, neighborVertex, namedGraph):
    baseVertexMatrixYX = get_vertex_position(namedGraph, baseVertex)
    baseVertexX = baseVertexMatrixYX[0]
    baseVertexY = baseVertexMatrixYX[1]

    neighborVertexMatrixYX = get_vertex_position(namedGraph, neighborVertex)
    neighborVertexX = neighborVertexMatrixYX[0]
    neighborVertexY = neighborVertexMatrixYX[1]

    if baseVertexMatrixYX == neighborVertexMatrixYX:
        return 0

    elif baseVertexY == neighborVertexY and fabs(baseVertexX - neighborVertexX) == 1:
        return 1

    elif baseVertexX == neighborVertexX and fabs(baseVertexY - neighborVertexY) == 1:
        return 1

    elif fabs(baseVertexX - neighborVertexX) == 1 and fabs(baseVertexY - neighborVertexY) == 1:
        return round(sqrt(2), 3)

    else:
        return 0


def getQ(namedGraph):
    Q = []
    for row in namedGraph:
        for number in row:
            if number == 0:
                continue
            else:
                Q.append(number)
    return Q


def get_smallest_DU(DU, S):

    cheapsetVertexes = []
    DUn = {}
    for vertex in DU:
        if vertex not in S:
            DUn[vertex] = DU[vertex]

    lowestDU = min(DUn.values())

    for vertex in range(1, len(DU)+1):
        try:
            if DUn[vertex] == lowestDU:
                cheapsetVertexes.append(vertex)
        except:
            continue

    return cheapsetVertexes


def get_neighbors(namedGraph, vertex):
    neighbourNames = []
    vertexPosition = get_vertex_position(namedGraph, vertex)
    y = vertexPosition[0]
    x = vertexPosition[1]
    try:
        if y - 1 < 0 or namedGraph[y - 1][x] == 0:
            pass
        else:
            neighbourNames.append(namedGraph[y - 1][x])
    except:
        pass
    try:
        if y - 1 < 0 or namedGraph[y - 1][x + 1] == 0:
            pass
        else:
            neighbourNames.append(namedGraph[y - 1][x + 1])
    except:
        pass
    try:
        if namedGraph[y][x + 1] == 0:
            pass
        else:
            neighbourNames.append(namedGraph[y][x + 1])
    except:
        pass
    try:
        if namedGraph[y + 1][x + 1] == 0:
            pass
        else:
            neighbourNames.append(namedGraph[y + 1][x + 1])
    except:
        pass
    try:
        if namedGraph[y + 1][x] == 0:
            pass
        else:
            neighbourNames.append(namedGraph[y + 1][x])
    except:
        pass
    try:
        if x - 1 < 0 or namedGraph[y + 1][x - 1] == 0:
            pass
        else:
            neighbourNames.append(namedGraph[y + 1][x - 1])
    except:
        pass
    try:
        if x - 1 < 0 or namedGraph[y][x - 1] == 0:
            pass
        else:
            neighbourNames.append(namedGraph[y][x - 1])
    except:
        pass
    try:
        if y - 1 < 0 or x - 1 < 0 or namedGraph[y - 1][x - 1] == 0:
            pass
        else:
            neighbourNames.append(namedGraph[y - 1][x - 1])
    except:
        pass
    return list(set(neighbourNames))


def get_zero_number_from_board_coordinates(namedGraph, start):
    return(namedGraph[start[0]][start[1]])


class Dijkstra:
    def __init__(self, start, graph, display, startSquare, endSquare):
        """calculate dijkstra algorithm
        Arguments:
            start {[list]} -- [y, x]
        """
        self.namedGraph = create_named_graph(graph)
        Q = getQ(self.namedGraph)
        S = []
        DU = {number: inf
              for number in Q
              }

        self.startingNumber = get_zero_number_from_board_coordinates(
            self.namedGraph, start)

        DU[self.startingNumber] = 0

        PU = {number: -1
              for number in Q
              }

        while len(Q) > 0:

            cheapsestVertexes = get_smallest_DU(DU, S)

            for vertex in cheapsestVertexes:

                S.append(vertex)
                Q.remove(vertex)
                neighbors = get_neighbors(self.namedGraph, vertex)

                for neighborVertex in neighbors:

                    boardCoordinates = get_vertex_position(
                        self.namedGraph, neighborVertex)
                    pyCoordinates = get_board_coordinates_from_boardYX(
                        boardCoordinates)
                    draw_clicked_box(
                        pyCoordinates[0], pyCoordinates[1], display, color=gold)
                    draw_clicked_box(
                        startSquare[0], startSquare[1], display, color=green)
                    draw_clicked_box(
                        endSquare[0], endSquare[1], display, color=red)
                    draw_grid(display)
                    pygame.display.update()

                    costOfTravel = celculate_cost_of_travel(
                        vertex, neighborVertex, self.namedGraph)

                    if DU[neighborVertex] > DU[vertex] + costOfTravel:
                        DU[neighborVertex] = DU[vertex] + costOfTravel
                        PU[neighborVertex] = vertex
                    else:
                        pass
        self.PU = PU
        self.DU = DU

    def get_route(self, finish, path):

        finishNumberName = self.namedGraph[finish[0]][finish[1]]

        while True:
            path.append(finishNumberName)
            stepBackNumber = self.PU[finishNumberName]

            if stepBackNumber == -1:
                return

            stepBackNumberCoordinates = get_vertex_position(
                self.namedGraph, stepBackNumber)
            Dijkstra.get_route(self, stepBackNumberCoordinates, path)
            return list(reversed(list(tuple(path))))

    def get_route_YX_coordinates(self, path):
        coordinatesPath = []
        for numberName in path:
            for y in range(len(self.namedGraph)):
                for x in range(len(self.namedGraph)):
                    if self.namedGraph[y][x] == numberName:
                        coordinatesPath.append([y, x])
        return coordinatesPath


class Path:

    def __init__(self, graph, display, startSquare, endSquare, start, finish):
        path = []
        dijkstra = Dijkstra(start, graph, display, startSquare, endSquare)
        shortestPath = dijkstra.get_route(finish, path)
        self.pathCoordinates = dijkstra.get_route_YX_coordinates(shortestPath)


def main(board):

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
    path = 0

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
                            mouseXstart = mouseX
                            mouseYstart = mouseY
                            if mouseY < boardHeight and start == 0:
                                # mark start
                                start = draw_clicked_box(
                                    mouseX, mouseY, display, color=green)
                                startCoordinates = get_matrix_coordinates_of_square(
                                    start, num=2)
                                mark_square_on_matrix(start, num=2)
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
                            mouseXend = mouseX
                            mouseYend = mouseY
                            if mouseY < boardHeight and end == 0:
                                # mark end
                                end = draw_clicked_box(
                                    mouseX, mouseY, display, color=red)
                                endCoordinates = get_matrix_coordinates_of_square(
                                    end, num=3)
                                mark_square_on_matrix(end, num=3)
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
    draw_middle_buttion(display, string="FIND PATH")
    pygame.display.update()

    # draw obstacles
    while True:
        # get action made by player
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos

            elif event.type == MOUSEBUTTONDOWN and path == 0:
                mouseX, mouseY = event.pos

                if mouseY > boardHeight:
                    change_button_color_onclick(
                        display, "middle", color=grey, string="FIND PATH")
                    pygame.display.update()
                    boardOnlyObstacles = get_board_with_only_obstacles(board)

                    try:
                        path = Path(boardOnlyObstacles, display, start, end, start=startCoordinates,
                                    finish=endCoordinates).pathCoordinates
                    except:
                        draw_error(display)
                        pygame.display.update()
                        time.sleep(5)

                        return
                    else:
                        display.fill(white)
                        draw_grid(display)
                        draw_clicked_box(
                            mouseXstart, mouseYstart, display, color=green)
                        draw_clicked_box(
                            mouseXend, mouseYend, display, color=red)

                        obstacles = get_obstacles_pycoordinates(board)
                        draw_square(
                            start[0], start[1], display, color=green)
                        draw_square(
                            end[0], end[1], display, color=red)

                        for obstacle in obstacles:
                            XY = get_board_coordinates_from_boardYX(obstacle)
                            draw_square(XY[0], XY[1], display, color=black)

                        pygame.display.update()

                        for step in path:
                            XY = get_board_coordinates_from_boardYX(step)

                            if step == startCoordinates or step == endCoordinates:
                                continue

                            elif step != startCoordinates and step != endCoordinates:
                                draw_clicked_box(
                                    XY[0], XY[1], display, color=gold)
                                draw_grid(display)
                                pygame.display.update()
                                time.sleep(0.1)

                        draw_middle_buttion(display, string="RESET")
                        pygame.display.update()

                else:
                    clickedSquare = draw_clicked_box(mouseX, mouseY, display)
                    mark_square_on_matrix(clickedSquare)
                    pygame.display.update()
                    while True:
                        event = pygame.event.wait()
                        if event.type == MOUSEMOTION:
                            mouseX, mouseY = event.pos
                            boardPosition = get_matrix_coordinates_from_mouse_pos(
                                mouseX, mouseY)

                            if mouseY < boardHeight and board[boardPosition[0]][boardPosition[1]] == 0:
                                clickedSquare = draw_clicked_box(
                                    mouseX, mouseY, display)
                                draw_grid(display)
                                mark_square_on_matrix(clickedSquare)
                                pygame.display.update()
                                continue
                        elif event.type == MOUSEBUTTONUP:
                            break

            elif event.type == MOUSEBUTTONDOWN and path != 0:
                mouseX, mouseY = event.pos
                if mouseY > boardHeight:
                    return

        pygame.display.update()
    clock.tick(fpsClock)


def draw_grid(display):
    for x in range(amountOfSquares):
        pygame.draw.line(display, grey, (x * squareSize, 0),
                         (x * squareSize, boardWidth))
    for y in range(amountOfSquares + 1):
        pygame.draw.line(display, grey, (0, y * squareSize),
                         (boardHeight, y * squareSize))


def get_obstacles_pycoordinates(board):
    obstacles = []
    for y in range(amountOfSquares):
        for x in range(amountOfSquares):
            if board[y][x] == 1:
                obstacles.append([y, x])
    return obstacles


def draw_error(display):
    boldness = 3
    PosX = 0
    PosY = int(winHeight / 2 - menuHeight / 2)
    pygame.draw.rect(display, white, (PosX,
                                      PosY, int(winWidth), menuHeight), 0)
    pygame.draw.rect(display, red, (PosX,
                                    PosY, int(winWidth), menuHeight), boldness)
    display_text(display, "PATH DOESN'T EXIST", red,
                 x=winWidth / 2, y=winHeight / 2)


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


def draw_middle_buttion(display, string):
    boldness = 3

    startPosX = 0
    startPosY = int(round(winHeight - menuHeight + boldness / 2, 0))
    pygame.draw.rect(display, white, (startPosX,
                                      startPosY, int(winWidth), menuHeight), 0)
    pygame.draw.rect(display, green, (startPosX,
                                      startPosY, int(winWidth), menuHeight), boldness)
    display_text(display, string, green, x=int(winWidth /
                                               2), y=int(round(boardHeight + menuHeight / 2, 0)))


def change_button_color_onclick(display, section, color=grey, string=None):
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

    elif section == "middle":
        PosX = 0
        PosY = int(round(winHeight - menuHeight + boldness / 2, 0))
        pygame.draw.rect(display, color, (PosX,
                                          PosY, int(winWidth), menuHeight), 0)
        display_text(display, string, green, x=int(winWidth / 2),
                     y=int(round(boardHeight + menuHeight / 2, 0)))
        pygame.display.update()
        time.sleep(0.1)
        pygame.draw.rect(display, white, (PosX,
                                          PosY, int(winWidth), menuHeight), 0)
        pygame.draw.rect(display, green, (PosX,
                                          PosY, int(winWidth), menuHeight), boldness)
        display_text(display, string, green, x=int(winWidth / 2),
                     y=int(round(boardHeight + menuHeight / 2, 0)))
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


def draw_square(mouseX, mouseY, display, color=black):
    if mouseY > boardHeight:
        pass
    else:
        boxX = int(floor(mouseX / squareSize) * squareSize)
        boxY = int(floor(mouseY / squareSize) * squareSize)

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


def get_matrix_coordinates_from_mouse_pos(mouseX, mouseY):
    y = int(mouseY/squareSize)
    x = int(mouseX/squareSize)
    return [y, x]


if __name__ == "__main__":
    while True:
        board = get_clear_board()
        main(board)
