import pygame
import os

# Initialize Pygame
pygame.init()

# Character dimensions
CHAR_WIDTH = 50
CHAR_HEIGHT = 100

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

def create_pixel_art_character(color):
    # Create a surface for the character
    surface = pygame.Surface((CHAR_WIDTH, CHAR_HEIGHT), pygame.SRCALPHA)

    # Simple pixel art design
    # Head
    pygame.draw.rect(surface, color, (15, 5, 20, 20))
    # Eyes
    pygame.draw.rect(surface, WHITE, (18, 10, 4, 4))
    pygame.draw.rect(surface, WHITE, (28, 10, 4, 4))
    pygame.draw.rect(surface, BLACK, (19, 11, 2, 2))
    pygame.draw.rect(surface, BLACK, (29, 11, 2, 2))
    # Mouth
    pygame.draw.rect(surface, BLACK, (22, 18, 6, 2))
    # Hair spikes
    pygame.draw.rect(surface, YELLOW, (10, 0, 5, 10))
    pygame.draw.rect(surface, YELLOW, (20, 0, 5, 12))
    pygame.draw.rect(surface, YELLOW, (30, 0, 5, 10))
    # Body
    pygame.draw.rect(surface, color, (10, 25, 30, 40))
    # Arms
    pygame.draw.rect(surface, color, (5, 30, 10, 20))
    pygame.draw.rect(surface, color, (35, 30, 10, 20))
    # Legs
    pygame.draw.rect(surface, color, (15, 65, 8, 25))
    pygame.draw.rect(surface, color, (27, 65, 8, 25))
    # Belt
    pygame.draw.rect(surface, BLACK, (10, 60, 30, 5))
    # Gi symbol
    pygame.draw.circle(surface, WHITE, (25, 52), 3)

    return surface

def main():
    # Create assets directory if it doesn't exist
    os.makedirs("assets/characters", exist_ok=True)

    # Create player1 (blue)
    player1_surface = create_pixel_art_character(BLUE)
    pygame.image.save(player1_surface, "assets/characters/player1.png")
    print("Created player1.png")

    # Create player2 (green)
    player2_surface = create_pixel_art_character(GREEN)
    pygame.image.save(player2_surface, "assets/characters/player2.png")
    print("Created player2.png")

    pygame.quit()

if __name__ == "__main__":
    main()
