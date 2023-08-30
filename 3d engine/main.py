import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from draw import *


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw_sphere()
        # draw_polygon()
        # draw_cube()
        # draw_pyramid()
        draw_cone(height=2, sides=20, radius=1)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
