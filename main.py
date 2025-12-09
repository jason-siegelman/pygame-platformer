import pygame

# --- Setup ---
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 74) # Default font, size 74

# --- Constants ---
GRAVITY = 0.8
FRICTION = 0.9 
ACCELERATION = 1.0
JUMP_STRENGTH = -18
TILE_SIZE = 50

# --- Global Variables ---
score = 0
game_state = 'PLAYING'
player_rect = pygame.Rect(100, 100, 40, 60)
x_pos = float(player_rect.x)
y_pos = float(player_rect.y)
x_speed = 0
y_speed = 0
x_accel = 0
can_jump = False
facing_right = True

# --- Camera Variables ---
scroll_x = 0
scroll_y = 0

# --- Animations ---
frame_speed = 0.1
frame_index = 0

# Player Run Animation
char_image_path = 'assets/kenney_new-platformer-pack-1.1/Sprites/Characters/Default/'
player_run_image_a = pygame.image.load(char_image_path + 'character_beige_walk_a.png').convert_alpha()
player_run_image_b = pygame.image.load(char_image_path + 'character_beige_walk_b.png').convert_alpha()
run_animation = [player_run_image_b, player_run_image_a]

# Coin Image Animation
coin_image_path = 'assets/kenney_new-platformer-pack-1.1/Sprites/Tiles/Default/coin_gold.png'
coin_side_image_path = 'assets/kenney_new-platformer-pack-1.1/Sprites/Tiles/Default/coin_gold_side.png'
coin_image_original = pygame.image.load(coin_image_path).convert_alpha()
coin_side_image_original = pygame.image.load(coin_side_image_path).convert_alpha()
coin_image = pygame.transform.smoothscale(coin_image_original, (TILE_SIZE, TILE_SIZE))
coin_side_image = pygame.transform.smoothscale(coin_side_image_original, (TILE_SIZE, TILE_SIZE))
coin_animation = [coin_image, coin_side_image]

# --- Level Design ---
# Each character represents a 50x50 tile
# 16 rows x 48 columns
level_map = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W       C                    C                 W",
    "W      WWW                  WWW                W",
    "W             P                                W",
    "W            WWW                               W",
    "W                                              W",
    "W      W            C     W          W         W",
    "W     WW           WWW    WW        WW         W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# Initialize Walls and Coins
walls = []
coins = []

def reset_level():
    global score, game_state, player_rect, x_pos, y_pos, x_speed, y_speed, x_accel, can_jump, facing_right, scroll_x, scroll_y, coins

    # --- Game Variables ---
    score = 0
    game_state = 'PLAYING'

    # --- Player Variables ---
    player_rect = pygame.Rect(100, 100, 40, 60)
    x_pos = float(player_rect.x)
    y_pos = float(player_rect.y)
    x_speed = 0
    y_speed = 0
    x_accel = 0
    can_jump = False
    facing_right = True

    # --- Camera Variables ---
    scroll_x = 0
    scroll_y = 0

    # --- Level Setup ---
    walls.clear()
    coins.clear()

    # Parse level map to create walls and coins
    for row_index, row in enumerate(level_map): # Iterate through each row
        for col_index, tile in enumerate(row): # Iterate through each character in the row
            
            # Calculate the x, y position of the tile
            x = col_index * TILE_SIZE 
            y = row_index * TILE_SIZE
            
            # Create walls, coins, and set player start position
            if tile == 'W':
                walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile == 'C':
                coins.append(pygame.Rect(x , y , TILE_SIZE, TILE_SIZE))
            elif tile == 'P':
                player_rect.x = x
                player_rect.y = y
                x_pos = float(player_rect.x)
                y_pos = float(player_rect.y)

reset_level()

running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Input Handling
    keys = pygame.key.get_pressed()

    if game_state == 'PLAYING':
        
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
        
        # Movement - X Axis
        x_speed += x_accel
        x_pos += x_speed
        player_rect.x = x_pos

        # Update facing direction
        if x_speed > 0:
            facing_right = True
        elif x_speed < 0:
            facing_right = False
        
        # Collision Detection - X Axis
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

        # Movement - Y Axis
        y_speed += GRAVITY
        y_pos += y_speed
        player_rect.y = y_pos

        # Check for falling off the screen
        if player_rect.bottom > 1000:
            game_state = 'GAME_OVER'

        # Collision Detection - Y Axis
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

        # Collect Coins
        for coin in coins[:]:
            if player_rect.colliderect(coin):
                coins.remove(coin)
                score += 1
                print(f"Score: {score}")

        # 4. Camera Logic

        # Center the camera on the player
        # (Goal: Player Center - Screen Center)
        target_x = player_rect.centerx - (SCREEN_WIDTH // 2)
        target_y = player_rect.centery - (SCREEN_HEIGHT // 2)

        # Lerp the camera position for smooth movement
        scroll_x += (target_x - scroll_x) * 0.1
        scroll_y += (target_y - scroll_y) * 0.1

        # 5. Drawing

        # Clear Screen
        screen.fill((30, 30, 30))
        
        # Draw Walls relative to Camera
        for wall in walls:
            # Create a temp rect for drawing only
            draw_rect = pygame.Rect(int(wall.x - scroll_x), int(wall.y - scroll_y), wall.width, wall.height)
            pygame.draw.rect(screen, (100, 200, 100), draw_rect)

        # Update Animation Frame
        if abs(x_speed) > 0.5:
            frame_index += frame_speed
            if frame_index >= len(run_animation):
                frame_index = 0
        else:
            frame_index = 0  # Reset to first frame when not moving

        # Calculate Player Draw Position relative to Camera
        current_image = run_animation[int(frame_index)]
        player_draw_rect = current_image.get_rect()
        player_draw_rect.midbottom = (int(player_rect.centerx - scroll_x), int(player_rect.bottom - scroll_y))

        # Flip the image based on facing direction
        if not facing_right:
            current_image = pygame.transform.flip(current_image, True, False)

        # Draw the current frame of the run animation
        screen.blit(current_image, player_draw_rect)

        # Draw coins relative to Camera
        coin_image = coin_animation[int((pygame.time.get_ticks() / 300) % len(coin_animation))]
        for coin in coins:
            draw_rect = pygame.Rect(int(coin.x - scroll_x), int(coin.y - scroll_y), coin.width, coin.height)
            screen.blit(coin_image, draw_rect)
            # pygame.draw.ellipse(screen, (255, 223, 0), draw_rect)

        pygame.display.flip()
        clock.tick(60)
    
    elif game_state == 'GAME_OVER':
        # Clear Screen
        screen.fill((0, 0, 0))
        
        # Render Game Over Text
        game_over_text = game_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

        if keys[pygame.K_r]:
            reset_level()

        pygame.display.flip()
        clock.tick(60)

pygame.quit()