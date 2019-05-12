import pygame
from App.Classes.ExampleRectangle import ExampleRectangle

pygame.init()

# Create global constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOUR = (0, 0, 0)

# Create window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('BrainChild')

# Initial example rectangle
x = 50
y = 50
width = 40
height = 60
speed = 5

exampleRectangle = ExampleRectangle(100, 100, 20, 20)
print(exampleRectangle.x)

# Keep running until user clicks the exit button
running = True
while running:

    # Initial frame rate limit
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move the rectangle about
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # Fills the window with the background colour
    window.fill(BACKGROUND_COLOUR)

    # Draws the example rectangle
    pygame.draw.rect(window, (255, 0, 0), (x, y, width, height))
    exampleRectangle.draw(window)

    # Sends update to the actual window
    pygame.display.update()

pygame.quit()
