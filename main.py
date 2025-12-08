import pygame

# --- Setup ---
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# --- Constants ---
GRAVITY = 0.8
FRICTION = 0.9 
ACCELERATION = 1.0
JUMP_STRENGTH = -18

# --- Player Variables ---
player_rect = pygame.Rect(100, 100, 40, 60)
x_pos = float(player_rect.x)
y_pos = float(player_rect.y)
x_speed = 0
y_speed = 0
x_accel = 0
can_jump = False

# --- Player Animations ---
sprite_sheet_image = pygame.image.load('assets/raptor_sprite_sheet_v4.png').convert_alpha()
frame_speed = 0.1
frame_index = 0

# def get_image(frame_number, width, height, scale, color):
#     # Calculate the offset and create the image
#     x_offset = width * frame_number
#     frame_rect = pygame.Rect(x_offset, 0, width, height)
#     image = sprite_sheet_image.subsurface(frame_rect)
    
#     # Resize the image and remove the background
#     image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
#     image.set_colorkey(color)
    
#     # Return the image
#     return image

char_image_path = 'assets/kenney_new-platformer-pack-1.1/Sprites/Characters/Default/'

run_animation = [char_image_path + 'character_beige_walk_a.png', char_image_path + 'character_beige_walk_b.png']

# for frame_index in range(0, 4):
#     run_animation.append(get_image(frame_index, 704, 768, 0.15, (255, 255, 255)))

# --- Camera Variables ---
scroll_x = 0
scroll_y = 0

# --- Massive Level Design ---
# I added walls much further out (up to 2000px)
walls = [
    pygame.Rect(0, 550, 2400, 50),    # Huge Floor (3 screens wide)
    pygame.Rect(0, 0, 50, 600),       # Left Wall Boundary
    pygame.Rect(2350, 0, 50, 600),    # Far Right Wall Boundary
    
    # Obstacle Course
    pygame.Rect(300, 400, 200, 20),
    pygame.Rect(600, 300, 20, 100),   # Tall wall
    pygame.Rect(700, 450, 200, 20),
    pygame.Rect(1000, 350, 100, 20),
    pygame.Rect(1200, 250, 100, 20),  # High platform
    pygame.Rect(1400, 500, 50, 50),   # Block
    pygame.Rect(1600, 400, 200, 20),  
    pygame.Rect(1900, 300, 50, 20),
]

running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Input Handling
    keys = pygame.key.get_pressed()
    
    x_speed *= FRICTION
    x_accel = 0
    
    if keys[pygame.K_LEFT]:
        x_accel = -ACCELERATION
    if keys[pygame.K_RIGHT]:
        x_accel = ACCELERATION
    
    if keys[pygame.K_SPACE] and can_jump:
        y_speed = JUMP_STRENGTH
        can_jump = False

    # 3. Physics Engine
    
    # X Movement
    x_speed += x_accel
    x_pos += x_speed
    player_rect.x = x_pos
    
    for wall_rect in walls:
        if player_rect.colliderect(wall_rect):
            if x_speed > 0: 
                player_rect.right = wall_rect.left
                x_speed = 0
                x_pos = player_rect.x
            elif x_speed < 0: 
                player_rect.left = wall_rect.right
                x_speed = 0
                x_pos = player_rect.x

    # Y Movement
    y_speed += GRAVITY
    y_pos += y_speed
    player_rect.y = y_pos
    
    can_jump = False 
    for wall_rect in walls:
        if player_rect.colliderect(wall_rect):
            if y_speed > 0: 
                player_rect.bottom = wall_rect.top
                y_speed = 0
                y_pos = player_rect.y
                can_jump = True
            elif y_speed < 0: 
                player_rect.top = wall_rect.bottom
                y_speed = 0
                y_pos = player_rect.y

    # 4. Camera Logic
    # Center the camera on the player
    # (Goal: Player Center - Screen Center)
    target_x = player_rect.centerx - (SCREEN_WIDTH // 2)
    target_y = player_rect.centery - (SCREEN_HEIGHT // 2)

    # Lerp the camera position for smooth movement
    scroll_x += (target_x - scroll_x) * 0.1
    scroll_y += (target_y - scroll_y) * 0.1

    # 5. Drawing
    screen.fill((30, 30, 30))
    
    # Draw Walls relative to Camera
    for wall in walls:
        # Create a temp rect for drawing only
        draw_rect = pygame.Rect(int(wall.x - scroll_x), int(wall.y - scroll_y), wall.width, wall.height)
        pygame.draw.rect(screen, (100, 200, 100), draw_rect)
        
    # Update Animation Frame
    frame_index += frame_speed
    if frame_index >= len(run_animation):
        frame_index = 0

    # Calculate Player Draw Position relative to Camera
    current_image = run_animation[int(frame_index)]
    player_draw_rect = current_image.get_rect()
    player_draw_rect.midbottom = (int(player_rect.centerx - scroll_x), int(player_rect.bottom - scroll_y))

    # Draw the current frame of the run animation
    screen.blit(run_animation[int(frame_index)], player_draw_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()