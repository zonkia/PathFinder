from math import sqrt, inf, fabs
from pprint import pprint
from copy import deepcopy
import time


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


def create_graph_with_weights(graph, namedGraph):
    i = 0
    for row in graph:
        i += len(row)

    graphWithWeights = []
    row = []

    for y in range(i):
        for x in range(i):
            vertexPosX = get_vertex_position(namedGraph, x + 1)
            vertexPosY = get_vertex_position(namedGraph, y + 1)

            if vertexPosX == None or vertexPosY == None:
                continue

            if x == y:
                row.append(0)

            # poziome y = y:
            elif vertexPosX[0] == vertexPosY[0] and fabs(vertexPosX[1] - vertexPosY[1]) == 1:
                row.append(1)

            # pionowe x = x
            elif vertexPosX[1] == vertexPosY[1] and fabs(vertexPosX[0] - vertexPosY[0]) == 1:
                row.append(1)

            elif fabs(vertexPosX[0] - vertexPosY[0]) == 1 and fabs(vertexPosX[1] - vertexPosY[1]) == 1:
                row.append(round(sqrt(2), 3))

            else:
                row.append(0)

        graphWithWeights.append(row)
        row = []
    return graphWithWeights


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
    def __init__(self, start, graph):
        """calculate dijkstra algorithm

        Arguments:
            start {[list]} -- [y, x]
        """
        self.namedGraph = create_named_graph(graph)

        graphWithWeights = create_graph_with_weights(graph, self.namedGraph)

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

                    costOfTravel = graphWithWeights[vertex -
                                                    1][neighborVertex - 1]

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

            stepBackNumberCoordinates = Dijkstra.get_numberName_coordinates(self,
                                                                            stepBackNumber)
            Dijkstra.get_route(self, stepBackNumberCoordinates, path)
            return list(reversed(list(tuple(path))))

    def get_numberName_coordinates(self, numberName):
        for y in range(len(self.namedGraph)):
            for x in range(len(self.namedGraph)):
                if self.namedGraph[y][x] == numberName:
                    return [y, x]

    def get_route_YX_coordinates(self, path):
        coordinatesPath = []

        for numberName in path:
            for y in range(len(self.namedGraph)):
                for x in range(len(self.namedGraph)):
                    if self.namedGraph[y][x] == numberName:
                        coordinatesPath.append([y, x])
        return coordinatesPath


class Path:

    def __init__(self, graph, start, finish):
        path = []
        dijkstra = Dijkstra(start, graph)
        shortestPath = dijkstra.get_route(finish, path)
        self.pathCoordinates = dijkstra.get_route_YX_coordinates(shortestPath)
