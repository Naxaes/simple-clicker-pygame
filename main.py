import pygame; pygame.init()
import random


LEFT_MOUSE_BUTTON = 1


# -- Settings --
# App settings
FPS  = 60
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 480, 480
DEFAULT_FONT = pygame.font.SysFont('monospace', 32)

# Color settings
BACKGROUND_COLOR = (0,     0,   0)
TEXT_COlOR       = (255, 255, 255)
RECTANGLE_COLOR  = (255,   0,   0)

# Game settings
LIVES_AT_START       = 100
PADDING_FROM_EDGE    = 32
MIN_RECTANGLE_LENGTH = 8
MAX_RECTANGLE_LENGTH = 32
LENGTH_STEP_SIZE     = 4


def spawn_rectangle(rectangles):
    x = random.choice(range(PADDING_FROM_EDGE, WINDOW_WIDTH - PADDING_FROM_EDGE, 2*PADDING_FROM_EDGE))
    y = random.choice(range(PADDING_FROM_EDGE, WINDOW_WIDTH - PADDING_FROM_EDGE, 2*PADDING_FROM_EDGE))
    w = random.choice(range(MIN_RECTANGLE_LENGTH, MAX_RECTANGLE_LENGTH, LENGTH_STEP_SIZE))
    h = random.choice(range(MIN_RECTANGLE_LENGTH, MAX_RECTANGLE_LENGTH, LENGTH_STEP_SIZE))
    rectangles.append(pygame.Rect(x, y, w, h))


def draw_text(surface, text, position, font=DEFAULT_FONT):
    surface.blit(font.render(text, True, TEXT_COlOR), position)


def start_values():
    lives = LIVES_AT_START
    time  = 0.0
    spawn_timer = 1
    rectangle_list = []
    time_list = []
    return lives, time, spawn_timer, rectangle_list, time_list


def main():
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock  = pygame.time.Clock()

    lives, time, spawn_timer, rectangle_list, time_list = start_values()

    running = True
    while running:
        # Update time
        dt    = clock.tick(FPS) / 1000
        time += dt

        # Update event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset game
                    lives, time, spawn_timer, rectangle_list, time_list = start_values()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_MOUSE_BUTTON:
                    for index, rectangle in enumerate(rectangle_list):
                        if rectangle.collidepoint(event.pos):
                            lives += 1
                            rectangle_list.remove(rectangle)
                            time_list.remove(time_list[index])
                            break
        # Update logic
        spawn_timer -= dt
        if spawn_timer <= 0:
            spawn_rectangle(rectangle_list)
            time_list.append(time)
            spawn_timer = min(0.1 + 10 / (time*2), 1)

        # Update display
        screen.fill(BACKGROUND_COLOR)
        for index, rectangle in enumerate(rectangle_list):
            if time_list[index] + 2 < time:
                rectangle_list.remove(rectangle)
                time_list.remove(time_list[index])
                lives -= 1
            else:
                pygame.draw.rect(screen, RECTANGLE_COLOR, rectangle)

        draw_text(screen, 'SCORE: ' + str(lives), (4, 4))
        draw_text(screen, 'TIME: {:.3}'.format(time), (256, 4))

        pygame.display.update()


if __name__ == '__main__':
    main()