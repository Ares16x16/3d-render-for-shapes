import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys

# Define maze layout
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Constants
CELL_SIZE = 1.0
FOV = 60
PLAYER_SPEED = 0.1

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

glViewport(0, 0, width, height)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(FOV, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Player
player_pos = [1.2, 1.2]
player_dir = [1.0, 0.0]
player_plane = [0.0, 0.66]

# Movement
move_forward = False
move_backward = False
turn_left = False
turn_right = False


def draw_maze():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                glBegin(GL_QUADS)
                glVertex3f(j * CELL_SIZE, 0, i * CELL_SIZE)
                glVertex3f((j + 1) * CELL_SIZE, 0, i * CELL_SIZE)
                glVertex3f((j + 1) * CELL_SIZE, 0, (i + 1) * CELL_SIZE)
                glVertex3f(j * CELL_SIZE, 0, (i + 1) * CELL_SIZE)
                glEnd()


def update_player():
    global player_pos, player_dir, player_plane
    mouse_move = pygame.mouse.get_rel()
    mouse_sensitivity = 0.1
    player_dir[0] = player_dir[0] * math.cos(
        -mouse_move[0] * mouse_sensitivity
    ) - player_dir[1] * math.sin(-mouse_move[0] * mouse_sensitivity)
    player_dir[1] = player_dir[1] * math.cos(
        -mouse_move[0] * mouse_sensitivity
    ) + player_dir[0] * math.sin(-mouse_move[0] * mouse_sensitivity)
    if move_forward:
        if (
            maze[int(player_pos[1] + player_dir[1] * PLAYER_SPEED)][int(player_pos[0])]
            == 0
        ):
            player_pos[1] += player_dir[1] * PLAYER_SPEED
        if (
            maze[int(player_pos[1])][int(player_pos[0] + player_dir[0] * PLAYER_SPEED)]
            == 0
        ):
            player_pos[0] += player_dir[0] * PLAYER_SPEED

    if move_backward:
        if (
            maze[int(player_pos[1] - player_dir[1] * PLAYER_SPEED)][int(player_pos[0])]
            == 0
        ):
            player_pos[1] -= player_dir[1] * PLAYER_SPEED
        if (
            maze[int(player_pos[1])][int(player_pos[0] - player_dir[0] * PLAYER_SPEED)]
            == 0
        ):
            player_pos[0] -= player_dir[0] * PLAYER_SPEED


def setup_raycasting():
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    gluLookAt(
        player_pos[0],
        0,
        player_pos[1],
        player_pos[0] + player_dir[0],
        0,
        player_pos[1] + player_dir[1],
        0,
        1,
        0,
    )


def cast_rays():
    strip_width = 1
    max_distance = float("-inf")
    for x in range(width):
        camera_x = 2 * x / width - 1
        ray_dir_x = player_dir[0] + player_plane[0] * camera_x
        ray_dir_y = player_dir[1] + player_plane[1] * camera_x

        map_x = int(player_pos[0])
        map_y = int(player_pos[1])

        delta_dist_x = abs(1 / ray_dir_x)

        if ray_dir_y != 0:
            delta_dist_y = abs(1 / ray_dir_y)
        else:
            delta_dist_y = float("inf")

        step_x = 1 if ray_dir_x >= 0 else -1
        step_y = 1 if ray_dir_y >= 0 else -1

        side_dist_x = (map_x + 1 - player_pos[0]) * delta_dist_x
        side_dist_y = (map_y + 1 - player_pos[1]) * delta_dist_y

        hit = False
        side = None

        while not hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = "HORIZONTAL"
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = "VERTICAL"

            if maze[map_y][map_x] == 1:
                hit = True

        if side == "HORIZONTAL":
            distance = (map_x - player_pos[0] + (1 - step_x) / 2) / ray_dir_x
        else:
            distance = (map_y - player_pos[1] + (1 - step_y) / 2) / ray_dir_y

        line_height = int(height / distance)

        draw_start = int(-line_height / 2 + height / 2)
        if draw_start < 0:
            draw_start = 0

        draw_end = int(line_height / 2 + height / 2)
        if draw_end >= height:
            draw_end = height - 1

        darkness = min(1, max_distance / distance)

        glColor3f(darkness, darkness, darkness)

        glBegin(GL_QUADS)
        glVertex2f(x, draw_start)
        glVertex2f(x, draw_end)
        glVertex2f(x + strip_width, draw_end)
        glVertex2f(x + strip_width, draw_start)
        glEnd()

        max_distance = max(max_distance, distance)


def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    move_forward = True
                elif event.key == pygame.K_s:
                    move_backward = True
                elif event.key == pygame.K_a:
                    turn_left = True
                elif event.key == pygame.K_d:
                    turn_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    move_forward = False
                elif event.key == pygame.K_s:
                    move_backward = False
                elif event.key == pygame.K_a:
                    turn_left = False
                elif event.key == pygame.K_d:
                    turn_right = False

        update_player()
        setup_raycasting()
        cast_rays()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
