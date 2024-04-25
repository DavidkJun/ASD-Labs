import turtle
import random
import math
import numpy as np
import time

random.seed(3314)
matrix = [[random.uniform(0,2) for j in range(11)] for i in range(11)]
k = 1.0 - 1 * 0.005 - 4 * 0.005 - 0.27
multipliedMatrix = np.multiply(matrix, k)
matrix_for_dir = np.floor(multipliedMatrix)
print(matrix_for_dir)
print()
undir_matrix = np.maximum(matrix_for_dir, np.transpose(matrix_for_dir))
print(undir_matrix)

positions = []

def drawNumbers():
    global positions
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-300, 300)
    count = 1
    vertical_spacing = -120 * 1.2
    horizontal_spacing = 180 * 1.2
    for i in range(4):
        positions.append(turtle.position())
        turtle.color("white")
        turtle.write(count, align="center")
        turtle.color("black")
        count += 1
        turtle.goto(turtle.xcor(), turtle.ycor() + vertical_spacing)
    for i in range(3):
        positions.append(turtle.position())
        turtle.color("white")
        turtle.write(count, align="center")
        turtle.color("black")
        count += 1
        turtle.goto(turtle.xcor() + horizontal_spacing, turtle.ycor())
    for i in range(4):
        positions.append(turtle.position())
        turtle.color("white")
        turtle.write(count, align="center")
        turtle.color("black")
        count += 1
        turtle.goto(turtle.xcor() - horizontal_spacing / 1.5, turtle.ycor() - vertical_spacing)
    turtle.hideturtle()

rad = 16

def drawCircles():
    turtle.speed(0)
    def draw_circle(x, y):
        turtle.begin_fill()
        turtle.penup()
        turtle.goto(x, y - rad)
        turtle.pendown()
        turtle.circle(rad)
        turtle.end_fill()
    for pos in positions:
        draw_circle(pos[0], pos[1])

def calculateDistance(start, end):
    distance = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    return distance

def getOrto(x, y):
    orthogonal_vector = (-y, x)
    magnitude = math.sqrt(orthogonal_vector[0] ** 2 + orthogonal_vector[1] ** 2)
    unit_vector = (orthogonal_vector[0] / magnitude, orthogonal_vector[1] / magnitude)
    return np.array(unit_vector)

def getStartPosition(pos1, pos_top):
    vec = (pos_top - pos1)
    vec = vec / calculateDistance(pos1, pos_top)
    return pos1 + vec * rad

def drawArrow(pos1, pos2, directed, k):
    pos1 = np.array(pos1)
    pos2 = np.array(pos2)
    arr_vec = pos2 - pos1
    middle = (pos2 + pos1) / 2
    orto = getOrto(*arr_vec)
    dist_coef = k / calculateDistance(pos1, pos2) * 110
    side = 1 if dist_coef > 40 else -1
    orto = orto * side
    pos_top = middle + orto * dist_coef + orto * 40
    turtle.penup()
    pos_start = getStartPosition(pos1, pos_top)
    turtle.goto(pos_start[0], pos_start[1])
    turtle.pendown()
    turtle.goto(pos_top[0], pos_top[1])
    pos_end = getStartPosition(pos2, pos_top)
    turtle.goto(pos_end[0], pos_end[1])
    turtle.penup()
    if directed:
        drawDirectedArrow(pos_end, pos_top, pos2)

def drawDirectedArrow(pos_end, pos_top, pos2):
    width = 14 / 2
    length = 14
    orto2 = getOrto(*(pos_top - pos2))
    vec_back = (pos_top - pos_end) / calculateDistance(pos_top, pos_end)
    a = pos_end + vec_back * length
    turtle.goto(a + orto2 * width)
    turtle.pendown()
    turtle.begin_fill()
    turtle.goto(pos_end)
    turtle.penup()
    turtle.goto(a - orto2 * width)
    turtle.pendown()
    turtle.goto(pos_end)
    turtle.penup()
    turtle.goto(a - orto2 * width)
    turtle.pendown()
    turtle.goto(a + orto2 * width)
    turtle.end_fill()
    turtle.penup()

def drawSelfLoop(position, loop_size, directed):

    turtle.penup()
    turtle.goto(position[0], position[1] + rad)
    turtle.pendown()
    turtle.circle(loop_size)
    if directed:

        arrow_start_angle = 120
        arrow_length = 15
        arrow_width = 10


        arrow_pos_x = position[0] + loop_size * math.cos(math.radians(arrow_start_angle))
        arrow_pos_y = position[1] + 0.25*rad + loop_size * math.sin(math.radians(arrow_start_angle))


        arrow_dir_x = arrow_length * math.cos(math.radians(arrow_start_angle + 190))
        arrow_dir_y = arrow_length * math.sin(math.radians(arrow_start_angle + 190))


        turtle.penup()
        turtle.goto(arrow_pos_x, arrow_pos_y)
        turtle.pendown()
        turtle.begin_fill()
        turtle.goto(arrow_pos_x + arrow_dir_x, arrow_pos_y + arrow_dir_y)
        turtle.goto(arrow_pos_x - arrow_width, arrow_pos_y - arrow_width)
        turtle.goto(arrow_pos_x, arrow_pos_y)
        turtle.end_fill()

drawNumbers()
drawCircles()
drawNumbers()


for i in range(11):
    for j in range(i + 1):
        if undir_matrix[i][j]:
            if i == j:
                drawSelfLoop(positions[i],30,True)
            else:
                if i == 7:
                    k = 350
                elif i == 8 and 200 <= calculateDistance(positions[i], positions[j]) <= 280:
                    k = 50
                elif i > 8:
                    k = 30
                else:
                    k = 120
                drawArrow(positions[i], positions[j], directed=True, k=k)

time.sleep(6)
turtle.hideturtle()


turtle.clear()

drawNumbers()
drawCircles()
drawNumbers()

for i in range(11):
    for j in range(i + 1):
        if undir_matrix[i][j]:
            if i == j:
                drawSelfLoop(positions[i],30,False)
            else:
                if i == 7:
                    k = 350
                elif i == 8 and 200 <= calculateDistance(positions[i], positions[j]) <= 280:
                    k = 50
                elif i > 8:
                    k = 30
                else:
                    k = 120
                drawArrow(positions[i], positions[j], directed=False, k=k)

time.sleep(6)
def calculateDegreesForDir(matrix):
    degrees = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                degrees[i] += 1
    return degrees

degrees_for_dir = calculateDegreesForDir(matrix_for_dir)
print("Степені вершин напрямленого графа:", degrees_for_dir)

def calculateDegreesForUndir(matrix):
    degrees = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                degrees[i] += 1
    return degrees
degrees_for_undir = calculateDegreesForUndir(undir_matrix)
print("Степені вершин ненапрямленого графа:", degrees_for_undir)


def calculateOutDegrees(matrix):
    out_degrees = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                out_degrees[i] += 1
    return out_degrees

def calculateInDegrees(matrix):
    in_degrees = [0] * len(matrix)
    for j in range(len(matrix)):
        for i in range(len(matrix)):
            if matrix[i][j] > 0:
                in_degrees[j] += 1
    return in_degrees
out_degrees = calculateOutDegrees(matrix_for_dir)
in_degrees = calculateInDegrees(matrix_for_dir)

print("Напівстепені виходу напрямленого графа:", out_degrees)
print("Напівстепені заходу напрямленого графа:", in_degrees)

def is_graph_regular(matrix):
    degrees = [sum(row) for row in matrix]
    if all(degree == degrees[0] for degree in degrees):
        return True, degrees[0]
    else:
        return False, None

is_regular, degree = is_graph_regular(matrix_for_dir)
if is_regular:
    print(f"Граф однорідний зі ступенем однорідності r: {degree}")
else:
    print("Граф не однорідний.")


def find_pendant_and_isolated_vertices(matrix):
    pendant_vertices = []
    isolated_vertices = []
    for i in range(len(matrix)):

        connections = sum(1 for j in range(len(matrix[i])) if matrix[i][j] > 0)

        if connections == 1:
            pendant_vertices.append(i)
        elif connections == 0:
            isolated_vertices.append(i)

    return pendant_vertices, isolated_vertices

pendant_vertices, isolated_vertices = find_pendant_and_isolated_vertices(undir_matrix)
print("Висячі вершини:", pendant_vertices)
print("Ізольовані вершини:", isolated_vertices)

def find_paths(matrix):
    size = len(matrix)
    paths_2 = [[[] for _ in range(size)] for _ in range(size)]
    paths_3 = [[[] for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            for k in range(size):
                if matrix[i][k] > 0 and matrix[k][j] > 0:
                    paths_2[i][j].append([i, k, j])

    for i in range(size):
        for j in range(size):
            for path in paths_2[i][j]:
                for k in range(size):
                    if matrix[j][k] > 0:
                        paths_3[i][k].append(path + [k])

    return paths_2, paths_3

matrix = matrix_for_dir

paths_2, paths_3 = find_paths(matrix)

print("Шляхи довжиною 2:")
for i in range(len(paths_2)):
    for j in range(len(paths_2[i])):
        if paths_2[i][j]:
            print(f"Шляхи від {i + 1} до {j + 1}: {paths_2[i][j]}")

print("\nШляхи довжиною 3:")
for i in range(len(paths_3)):
    for j in range(len(paths_3[i])):
        if paths_3[i][j]:
            print(f"Шляхи від {i + 1} до {j + 1}: {paths_3[i][j]}")

def reachConnectMatrix(matrix):
    n = len(matrix)
    I_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    square_m = np.linalg.matrix_power(matrix, 2)
    cubic_m = np.linalg.matrix_power(matrix, 3)
    tetra_m = np.linalg.matrix_power(matrix, 4)
    sum_res = sumMatrix(sumMatrix(sumMatrix(sumMatrix(I_matrix, matrix), square_m), cubic_m), tetra_m)
    reach_matrix = [[1 if sum_res[i][j] != 0 else 0 for j in range(n)] for i in range(n)]
    transposed = transposeMatrix(reach_matrix)
    con_matrix = elementProduct(reach_matrix, transposed)
    return reach_matrix, con_matrix

def sumMatrix(matrix1, matrix2):
    return [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]

def transposeMatrix(matr):
    return [[matr[j][i] for j in range(len(matr))] for i in range(len(matr))]

def elementProduct(matrix1, matrix2):
    return [[matrix1[i][j] * matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]

def findComponents(con_matrix):
    unique_components = set(tuple(row) for row in con_matrix)
    con_components = []
    for component in unique_components:
        indices = [i + 1 for i, row in enumerate(con_matrix) if tuple(row) == component]
        con_components.append(indices)
    return con_components

def draw_condensation_graph(components):
    turtle.speed(1)
    turtle.clear()
    num_components = len(components)
    angle_step = 360 / num_components
    radius = 200
    for i, component in enumerate(components):
        angle = angle_step * i
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        turtle.up()
        turtle.goto(x, y)
        turtle.down()
        turtle.circle(40)
        turtle.up()
        turtle.goto(x, y + 15)
        turtle.write(f"С{i + 1}", False, 'center', ('Arial', 30, 'normal'))

    turtle.done()

graph = matrix_for_dir
reach_matrix, con_matrix = reachConnectMatrix(graph)

def print_matrix(matrix, description):
    print(description)
    for row in matrix:
        print(row)


reach_matrix, con_matrix = reachConnectMatrix(graph)
print_matrix(reach_matrix, "Матриця досяжності:")
print_matrix(con_matrix, "Матриця сильної зв'язності:")

components = findComponents(con_matrix)
print("componets:" ,components)
draw_condensation_graph(components)
