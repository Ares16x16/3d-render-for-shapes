import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def draw_cube():
    vertices = (
        (-1, -1, -1),
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, 1, 1),
    )

    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    )

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def draw_polygon(sides=3, radius=1.5, color=(1.0, 1.0, 0.0)):
    glBegin(GL_POLYGON)
    (r, g, b) = color
    glColor3f(r, g, b)  # Set color

    for side in range(sides):
        angle = (2 * math.pi * side) / sides  # Calculate angle for each side
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        glVertex2f(x, y)

    glEnd()


def draw_sphere(radius=1.0, subdivisions=20, color=(1.0, 1.0, 0.0)):
    slices = subdivisions
    stacks = subdivisions
    (r, g, b) = color
    glColor3f(r, g, b)  # Set color
    glPushMatrix()
    glTranslatef(0.0, 0.0, -radius)

    for i in range(stacks):
        lat0 = math.pi * (-0.5 + (i - 1) / stacks)
        z0 = radius * math.sin(lat0)
        zr0 = radius * math.cos(lat0)

        lat1 = math.pi * (-0.5 + i / stacks)
        z1 = radius * math.sin(lat1)
        zr1 = radius * math.cos(lat1)

        glBegin(GL_TRIANGLE_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * (j - 1) / slices
            x = math.cos(lng)
            y = math.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0, y * zr0, z0)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

    glPopMatrix()


from OpenGL.GL import *


def draw_pyramid(color=(1.0, 1.0, 0.0)):
    vertices = (
        (0, 1, 0),  # Top vertex
        (-1, -1, 1),  # Bottom front-left vertex
        (1, -1, 1),  # Bottom front-right vertex
        (1, -1, -1),  # Bottom back-right vertex
        (-1, -1, -1),  # Bottom back-left vertex
    )

    edges = ((0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1))

    (r, g, b) = color
    glColor3f(r, g, b)  # Set color

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def draw_cone(radius=1, height=1, sides=6, color=(1.0, 1.0, 0.0)):
    vertices = []
    angle_increment = 2 * math.pi / sides

    (r, g, b) = color
    glColor3f(r, g, b)  # Set color

    for i in range(sides):
        angle = i * angle_increment
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append((x, 0, y))

    vertices.append((0, height, 0))

    edges = []
    for i in range(sides):
        edges.append((i, (i + 1) % sides))
        edges.append((i, sides))

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
