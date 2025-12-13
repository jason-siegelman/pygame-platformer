import pygame
import os
from settings import *
from utils import load_image


# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 74) # Default font, size 74

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

# Player Run Animation
player_frame_index = 0
player_frame_speed = 0.1
player_run_files = ['character_beige_walk_b.png', 'character_beige_walk_a.png']
run_animation = load_image(BASE_CHAR_PATH, player_run_files)

# Coin Image Animation
coin_frame_index = 0
coin_frame_speed = 0.1
coin_image_files = ['coin_gold.png', 'coin_gold_side.png']
coin_animation = load_image(BASE_TILE_PATH, coin_image_files, (TILE_SIZE, TILE_SIZE))

# Enemy Image Animation
enemy_frame_index = 0
enemy_frame_speed = 0.1
enemy_image_files = ['barnacle_attack_a.png', 'barnacle_attack_b.png']
enemy_animation = load_image(BASE_ENEMY_PATH, enemy_image_files, (TILE_SIZE, TILE_SIZE))

# Initialize Walls, Coins and Enemies Lists
walls = []
coins = []
enemies = []

def reset_level():
    global score, game_state, player_rect, x_pos, y_pos, x_speed, y_speed, x_accel, can_jump, facing_right, scroll_x, scroll_y, walls, coins, enemies

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
    enemies.clear()

    # Parse level map to create walls and coins
    for row_index, row in enumerate(LEVEL_MAP): # Iterate through each row
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
            elif tile == 'E':
                # Create a dictionary for the enemy
                new_enemy = {
                    'rect': pygame.Rect(x, y, TILE_SIZE, TILE_SIZE),
                    'speed': 2
                }
                enemies.append(new_enemy)


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

        # 3. Player Movement and Collision
        
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

        # 4. Enemy Movement and Collision

        for enemy in enemies:
            # Move the enemy
            enemy['rect'].x += enemy['speed']

            # Reverse direction on wall collision
            for wall_rect in walls:
                if enemy['rect'].colliderect(wall_rect):
                    enemy['speed'] *= -1
                    if enemy['speed'] > 0:
                        enemy['rect'].left = wall_rect.right
                    else:
                        enemy['rect'].right = wall_rect.left
            
            # Check collision with player
            if player_rect.colliderect(enemy['rect']):
                game_state = 'GAME_OVER'

        # 5. Camera Logic

        # Center the camera on the player
        # (Goal: Player Center - Screen Center)
        target_x = player_rect.centerx - (SCREEN_WIDTH // 2)
        target_y = player_rect.centery - (SCREEN_HEIGHT // 2)

        # Lerp the camera position for smooth movement
        scroll_x += (target_x - scroll_x) * 0.2
        scroll_y += (target_y - scroll_y) * 0.2

        # Snap if close (The Anti-Jitter Fix)
        if abs(target_x - scroll_x) < 1:
            scroll_x = target_x
            
        if abs(target_y - scroll_y) < 1:
            scroll_y = target_y

        # 6. Drawing

        # Clear Screen
        screen.fill((30, 30, 30))
        
        # Draw Walls relative to Camera
        for wall in walls:
            draw_x = round(wall.x - scroll_x)
            draw_y = round(wall.y - scroll_y)
            draw_rect = pygame.Rect(draw_x, draw_y, wall.width, wall.height)
            pygame.draw.rect(screen, COLOR_WALL, draw_rect)

        # Draw Enemies relative to Camera
        enemy_frame_index += enemy_frame_speed
        if enemy_frame_index >= len(enemy_animation):
            enemy_frame_index = 0
        enemy_image = enemy_animation[int(enemy_frame_index)]
        for enemy in enemies:
            draw_x = round(enemy['rect'].x - scroll_x)
            draw_y = round(enemy['rect'].y - scroll_y)
            draw_rect = pygame.Rect(draw_x, draw_y, TILE_SIZE, TILE_SIZE)
            screen.blit(enemy_image, draw_rect)

        # Update Animation Frame
        if abs(x_speed) > 0.5:
            player_frame_index += player_frame_speed
            if player_frame_index >= len(run_animation):
                player_frame_index = 0
        else:
            player_frame_index = 0  # Reset to first frame when not moving

        # Calculate Player Draw Position relative to Camera
        current_image = run_animation[int(player_frame_index)]
        player_draw_rect = current_image.get_rect()

        # Center the image on the player's position
        true_center_x = x_pos + (player_rect.width / 2)
        true_bottom_y = y_pos + player_rect.height

        # Subtract camera scroll, then round to avoid subpixel rendering issues
        screen_x = round(true_center_x - scroll_x)
        screen_y = round(true_bottom_y - scroll_y)

        player_draw_rect.midbottom = (screen_x, screen_y)

        # Flip the image based on facing direction
        if not facing_right:
            current_image = pygame.transform.flip(current_image, True, False)

        # Draw the current frame of the run animation
        screen.blit(current_image, player_draw_rect)

        # Draw coins relative to Camera
        coin_frame_index += coin_frame_speed
        if coin_frame_index >= len(coin_animation):
            coin_frame_index = 0
        coin_image = coin_animation[int(coin_frame_index)]
        for coin in coins:
            draw_x = round(coin.x - scroll_x)
            draw_y = round(coin.y - scroll_y)
            draw_rect = pygame.Rect(draw_x, draw_y, coin.width, coin.height)
            screen.blit(coin_image, draw_rect)

        pygame.display.flip()
        clock.tick(60)
        pygame.display.set_caption(f"Platformer Run - FPS: {clock.get_fps():.2f}")
    
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