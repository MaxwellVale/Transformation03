from display import *
from matrix import *
from draw import *
import sys

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         translate: create a translation matrix,
                    then multiply the transform matrix by the translation matrix -
                    takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge matrix
         display: clear the screen, then
                  draw the lines of the edge matrix to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge matrix to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing

See the file script for an example of the file format
"""
def parse_file( fname, points, transform, screen, color ):
    file = open(fname, 'r')
    lines = file.read().strip().split('\n')

    index = 0
    while index < len(lines) and lines[index] != "quit":

        if lines[index] == "line":
            nextLine = map(int, lines[index + 1].strip().split(' '))
            add_edge(points, nextLine[0], nextLine[1], nextLine[2], nextLine[3], nextLine[4], nextLine[5])
            index += 2
        elif lines[index] == "ident":
            ident(transform)
            index += 1
        elif lines[index] == "scale":
            nextLine = map(int, lines[index + 1].strip().split(' '))
            matrix_mult(make_scale(nextLine[0], nextLine[1], nextLine[2]), transform)
            index += 2
        elif lines[index] == "move":
            nextLine = map(int, lines[index + 1].strip().split(' '))
            matrix_mult(make_translate(nextLine[0], nextLine[1], nextLine[2]), transform)
            index += 2
        elif lines[index] == "rotate":
            nextLine = lines[index + 1].strip().split(' ')
            angle = int(nextLine[1])
            if nextLine[0] == 'x':
                rotateMatrix = make_rotX(angle)
            elif nextLine[0] == 'y':
                rotateMatrix = make_rotY(angle)
            else:
                rotateMatrix = make_rotZ(angle)
            matrix_mult(rotateMatrix, transform)
            index += 2
        elif lines[index] == "apply":
            matrix_mult(transform, points)
            for i in range(len(points)):
                intPoint = map(int, points[i])
                points[i] = intPoint
            index += 1
        elif lines[index] == "display":
            clear_screen(screen)
            draw_lines(points, screen, color)
            display(screen)
            index += 1
        elif lines[index] == "save":
            nextLine = lines[index + 1].strip()
            clear_screen(screen)
            draw_lines(points, screen, color)
            save_extension(screen, nextLine)
            index += 2
        else:
            index += 1
