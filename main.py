import pygame

pygame.init()

#some variables
WIDTH = 800 # Set the width and height of the output window, in pixels
HEIGHT = 600
p_width = 40  # Set the player width and height
p_height = 60
p_x = 50    # Set the player positions 
p_y = 440
vel = 10

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])

def playerMovement(x, y, vel):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel

    return (x,y)

# Run until the user asks to quit
running = True

while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    p_x, p_y = playerMovement(p_x, p_y, vel)
    
    #Draw the player
    pygame.draw.rect(screen, (000, 100, 0), (p_x, p_y, p_width, p_height), 3)

    # Flip the display
    pygame.display.flip()

pygame.quit()