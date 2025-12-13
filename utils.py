# utils.py
import pygame
import os

# --- Load Images Function ---
def load_image(path, filenames, resize=None):
    images = []
    for filename in filenames:
        image = pygame.image.load(os.path.join(path, filename)).convert_alpha()
        if resize:
            image = pygame.transform.smoothscale(image, resize)
        images.append(image)
    return images

