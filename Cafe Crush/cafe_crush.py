import os
import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set window dimensions
WIDTH, HEIGHT = 1568, 1080
GRID_SIZE = 6
TILE_SIZE = 110 # Adjust the tile size for smaller grid
GRID_POSITION_X = 500 # Position the grid more to the left
GRID_POSITION_Y = 100 # Position the grid more to the top
PADDING = 70 # Padding around the grid
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set window title
pygame.display.set_caption("Cafe Crush")

# Load background image 
background = pygame.image.load("Cafe Setting.png")

# Load drink images
drink_images = [
    pygame.image.load("Drink 1.png"),
    pygame.image.load("Drink 2.png"),
    pygame.image.load("Drink 3.png"),
    pygame.image.load("Drink 4.png"),
    pygame.image.load("Drink 5.png"),
    pygame.image.load("Drink 6.png"),
]

# Resize drink images to fit the grid tiles
drink_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in drink_images]

# Load custom fonts
font_cafe_crush = pygame.font.Font('Coffee Town.otf', 100)
font_menu = pygame.font.Font('VerdanteSans-Bold.otf', 40)
font_game = pygame.font.SysFont('VerdanteSans-Regular.otf', 30)

# Coffee facts
coffee_facts = [
    "Coffee is the second most traded commodity on earth.",
    "Coffee was discovered by a goat herder.",
    "Brazil is the largest producer of coffee.",
    "Coffee beans are actually seeds.",
    "The most expensive coffee is made from cat poop.",
    "Coffee is the second most traded commodity in the world, after oil.",
    "There are over 100 species of coffee plants, but two main ones are used for commercial coffee: Arabica and Robusta.",
    "Coffee was originally chewed, not brewed. Ancient African tribes would grind coffee berries and mix them with animal fat to create a form of energy bar.",
    "The word 'coffee' comes from the Arabic word 'qahwa', which originally referred to wine or other intoxicating liquors.",
    "Coffee is a fruit! It comes from the seeds of the coffee cherry.",
    "The average American drinks around 3.1 cups of coffee per day.",
    "Finland is the world’s top coffee consumer, with the average Finn drinking around 12 kg of coffee annually.",
    "Coffee was banned in Mecca in the 16th century due to its stimulating effects during religious gatherings.",
    "The coffee bean is actually a seed of the coffee fruit (called a cherry).",
    "The first coffee house opened in Istanbul in 1475.",
    "The first coffee advertisement was published in 1665 in England.",
    "Espresso has less caffeine per ounce than regular coffee, but people typically drink more of the latter.",
    "Decaffeinated coffee isn’t entirely caffeine-free; it still contains a small amount of caffeine.",
    "There is a 'coffee belt' around the world, where most coffee is grown, located between the Tropics of Cancer and Capricorn.",
    "Coffee can boost metabolism, making it a common ingredient in weight-loss supplements.",
]

# Missions
missions = [
    "Match 3 Cappuccinos in a row!",
    "Clear 5 Matcha Tiles in under 20 seconds!",
    "Make a 4-match combo!",
    "Score 1,000 points before the moves run out!",
    "Score 3,000 points before the moves run out!",
    "Score 5,000 points before the moves run out!",
]

# Create game grid
def create_grid():
    grid = [[random.choice(drink_images) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    while True:
        matches = detect_matches(grid)
        if not matches:
            break
        remove_and_drop(grid, matches)
    return grid

# Function to swap two tiles
def swap_tiles(grid, pos1, pos2):
    grid[pos1[0]][pos1[1]], grid[pos2[0]][pos2[1]] = grid[pos2[0]][pos2[1]], grid[pos1[0]][pos1[1]]

# Function to detect matches
def detect_matches(grid):
    matches = set()
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matches.update([(row, col), (row, col + 1), (row, col + 2)])
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matches.update([(row, col), (row + 1, col), (row + 2, col)])
    return list(matches)

# Function to detect possible moves
def detect_possible_moves(grid):
    possible_moves = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if col < GRID_SIZE - 1:
                swap_tiles(grid, (row, col), (row, col + 1))
                if detect_matches(grid):
                    possible_moves.append((row, col))
                swap_tiles(grid, (row, col), (row, col + 1))
            if row < GRID_SIZE - 1:
                swap_tiles(grid, (row, col), (row + 1, col))
                if detect_matches(grid):
                    possible_moves.append((row, col))
                swap_tiles(grid, (row, col), (row + 1, col))
    return possible_moves

# Function to remove matches and drop new drinks
def remove_and_drop(grid, matches):
    for row, col in matches:
        grid[row][col] = None

    for col in range(GRID_SIZE):
        empty_cells = []
        for row in range(GRID_SIZE - 1, -1, -1):
            if grid[row][col] is None:
                empty_cells.append(row)
            elif empty_cells:
                target_row = empty_cells.pop(0)
                grid[target_row][col], grid[row][col] = grid[row][col], None
                empty_cells.append(row)
        for row in empty_cells:
            grid[row][col] = random.choice(drink_images)

# Function to animate the swapping of tiles
def animate_swap(grid, pos1, pos2):
    frames = 10  # Number of frames for the animation (adjusted for faster animation)
    for frame in range(frames + 1):
        screen.blit(background, (0, 0))
        screen.blit(grid_background, (GRID_POSITION_X, GRID_POSITION_Y))  # Draw the grid background

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if (row, col) == pos1:
                    x = col * TILE_SIZE + PADDING + (pos2[1] - pos1[1]) * TILE_SIZE * frame / frames
                    y = row * TILE_SIZE + PADDING + (pos2[0] - pos1[0]) * TILE_SIZE * frame / frames
                elif (row, col) == pos2:
                    x = col * TILE_SIZE + PADDING + (pos1[1] - pos2[1]) * TILE_SIZE * frame / frames
                    y = row * TILE_SIZE + PADDING + (pos1[0] - pos2[0]) * TILE_SIZE * frame / frames
                else:
                    x = col * TILE_SIZE + PADDING
                    y = row * TILE_SIZE + PADDING
                screen.blit(grid[row][col], (GRID_POSITION_X + x, GRID_POSITION_Y + y))

        pygame.display.flip()
        pygame.time.delay(10)  # Adjusted delay for faster animation

# Function to animate a hint by shaking a tile
def animate_hint(grid, pos):
    frames = 5  # Number of frames for the hint animation
    shake_distance = 5  # Distance to shake the tile
    for frame in range(frames):
        screen.blit(background, (0, 0))
        screen.blit(grid_background, (GRID_POSITION_X, GRID_POSITION_Y))  # Draw the grid background

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * TILE_SIZE + PADDING
                y = row * TILE_SIZE + PADDING
                if (row, col) == pos:
                    if frame % 2 == 0:
                        x += shake_distance
                    else:
                        x -= shake_distance
                screen.blit(grid[row][col], (GRID_POSITION_X + x, GRID_POSITION_Y + y))

        pygame.display.flip()
        pygame.time.delay(10)  # Adjusted delay for hint animation

# Function to shuffle the board
def shuffle_board(grid):
    flat_grid = [tile for row in grid for tile in row]
    random.shuffle(flat_grid)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            grid[row][col] = flat_grid.pop()

selected_tile = None
last_action_time = time.time()
score = 0
game_state = "menu"
start_time = None
shuffle_count = 3
current_mission = random.choice(missions)
current_coffee_fact = random.choice(coffee_facts)

# Initialize the game grid
grid = create_grid()

# Function to draw a rounded rectangle
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Create a transparent surface for the grid background with padding
grid_background = pygame.Surface((GRID_SIZE * TILE_SIZE + 2 * PADDING, GRID_SIZE * TILE_SIZE + 2 * PADDING), pygame.SRCALPHA)
grid_background.fill((0, 0, 0, 0))  # Transparent surface

# Draw the grid background with rounded corners on the grid background surface
draw_rounded_rect(grid_background, (150, 150, 150, 150), (PADDING, PADDING, GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE), 20)  # Adjust alpha to 64

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Function to draw the main menu
def draw_main_menu():
    screen.blit(background, (0, 0))
    draw_text('Cafe Crush', font_cafe_crush, (255, 255, 255), screen, WIDTH // 4 - 190, HEIGHT // 3)
    draw_text('Start Game', font_menu, (255, 255, 255), screen, WIDTH // 2 - 100, HEIGHT // 2)
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 110, HEIGHT // 2 - 10, 220, 50), 2)  # Outline for Start Game
    draw_text('Settings', font_menu, (255, 255, 255), screen, WIDTH // 2 - 100, HEIGHT // 2 + 60)
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 110, HEIGHT // 2 + 50, 220, 50), 2)  # Outline for Settings
    draw_text('Quit', font_menu, (255, 255, 255), screen, WIDTH // 2 - 100, HEIGHT // 2 + 120)
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 110, HEIGHT // 2 + 110, 220, 50), 2)  # Outline for Quit
    pygame.display.flip()

# Function to draw the pause menu
def draw_pause_menu():
    screen.blit(background, (0, 0))
    draw_text('Paused', font_menu, (255, 255, 255), screen, WIDTH // 2 - 50, HEIGHT // 4)
    draw_text('Resume', font_menu, (255, 255, 255), screen, WIDTH // 2 - 50, HEIGHT // 2)
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 60, HEIGHT // 2 - 10, 120, 50), 2)  # Outline for Resume
    draw_text('Exit to Menu', font_menu, (255, 255, 255), screen, WIDTH // 2 - 100, HEIGHT // 2 + 60)
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 110, HEIGHT // 2 + 50, 220, 50), 2)  # Outline for Exit to Menu
    pygame.display.flip()

# Function to draw the game over screen
def draw_game_over():
    screen.blit(background, (0, 0))
    draw_text('Game Over', font_menu, (255, 255, 255), screen, WIDTH // 2 - 100, HEIGHT // 4)
    draw_text(f'Score: {score}', font_menu, (255, 255, 255), screen, WIDTH // 2 - 100, HEIGHT // 2)
    draw_text('Press any key to return to menu', font_menu, (255, 255, 255), screen, WIDTH // 2 - 200, HEIGHT // 2 + 50)
    pygame.display.flip()

# Game loop
running = True
while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if game_state == "menu":
                if WIDTH // 2 - 110 <= x <= WIDTH // 2 + 110:
                    if HEIGHT // 2 - 10 <= y <= HEIGHT // 2 + 40:
                        game_state = "playing"
                        start_time = current_time
                        score = 0
                        grid = create_grid()
                        shuffle_count = 3
                        current_mission = random.choice(missions)
                        current_coffee_fact = random.choice(coffee_facts)
                    elif HEIGHT // 2 + 50 <= y <= HEIGHT // 2 + 100:
                        pass  # Settings button (not implemented)
                    elif HEIGHT // 2 + 110 <= y <= HEIGHT // 2 + 160:
                        running = False
            elif game_state == "playing":
                row, col = (y - GRID_POSITION_Y - PADDING) // TILE_SIZE, (x - GRID_POSITION_X - PADDING) // TILE_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    last_action_time = current_time  # Update the last action time
                    if selected_tile:
                        # Check if the selected tile is adjacent to the clicked tile
                        if abs(selected_tile[0] - row) + abs(selected_tile[1] - col) == 1:
                            animate_swap(grid, selected_tile, (row, col))
                            swap_tiles(grid, selected_tile, (row, col))
                            matches = detect_matches(grid)
                            if matches:
                                print("Match detected!")
                                remove_and_drop(grid, matches)
                                match_length = len(matches)
                                if match_length == 3:
                                    score += 10
                                elif match_length == 4:
                                    score += 20
                                elif match_length >= 5:
                                    score += 50
                                # Display a random coffee fact
                                current_coffee_fact = random.choice(coffee_facts)
                                # Detect new matches after dropping new drinks
                                while True:
                                    matches = detect_matches(grid)
                                    if not matches:
                                        break
                                    remove_and_drop(grid, matches)
                                    match_length = len(matches)
                                    if match_length == 3:
                                        score += 10
                                    elif match_length == 4:
                                        score += 20
                                    elif match_length >= 5:
                                        score += 50
                                # Select a new mission if the current one is completed
                                current_mission = random.choice(missions)
                            else:
                                # Swap back if no matches are found
                                animate_swap(grid, (row, col), selected_tile)
                                swap_tiles(grid, selected_tile, (row, col))
                        selected_tile = None
                    else:
                        selected_tile = (row, col)
                # Check for shuffle button click
                if WIDTH - 150 <= x <= WIDTH - 50 and HEIGHT - 50 <= y <= HEIGHT - 10 and shuffle_count > 0:
                    shuffle_board(grid)
                    shuffle_count -= 1
            elif game_state == "paused":
                if WIDTH // 2 - 60 <= x <= WIDTH // 2 + 60:
                    if HEIGHT // 2 - 10 <= y <= HEIGHT // 2 + 40:
                        game_state = "playing"
                    elif HEIGHT // 2 + 50 <= y <= HEIGHT // 2 + 100:
                        game_state = "menu"
            elif game_state == "game_over":
                game_state = "menu"
        elif event.type == pygame.KEYDOWN:
            if game_state == "playing" and event.key == pygame.K_p:
                game_state = "paused"

    if game_state == "menu":
        draw_main_menu()
    elif game_state == "playing":
        # Draw the background image
        screen.blit(background, (0, 0))

        # Draw the grid background
        screen.blit(grid_background, (GRID_POSITION_X, GRID_POSITION_Y))

        # Draw the individual squares and gems on the grid surface
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Draw the gem inside the rounded rectangle
                screen.blit(grid[row][col], (GRID_POSITION_X + col * TILE_SIZE + PADDING, GRID_POSITION_Y + row * TILE_SIZE + PADDING))

        # Draw the score
        draw_text(f'Score: {score}', font_game, (255, 255, 255), screen, 10, 10)

        # Draw the current mission
        draw_text(f'Mission: {current_mission}', font_game, (255, 255, 255), screen, 10, 50)

        # Draw the timer
        if start_time:
            elapsed_time = current_time - start_time
            remaining_time = max(0, 180 - elapsed_time)
            if remaining_time <= 10:
                color = (255, 0, 0) if int(remaining_time * 10) % 2 == 0 else (255, 255, 255)
            else:
                color = (255, 255, 255)
            draw_text(f'Time: {int(remaining_time)}', font_game, color, screen, WIDTH - 150, 20)
            if remaining_time == 0:
                game_state = "game_over"

        # Draw the shuffle button
        draw_text(f'Shuffle ({shuffle_count})', font_game, (255, 255, 255), screen, WIDTH - 140, HEIGHT - 45)

        # Draw the coffee fact
        draw_text(current_coffee_fact, font_game, (255, 255, 255), screen, WIDTH // 2 - 300, HEIGHT - 50)

        # Check if it's time to show a hint
        if current_time - last_action_time > 10:
            possible_moves = detect_possible_moves(grid)
            if possible_moves:
                hint_pos = random.choice(possible_moves)
                animate_hint(grid, hint_pos)
            last_action_time = current_time  # Reset the last action time after showing a hint

    elif game_state == "paused":
        draw_pause_menu()
    elif game_state == "game_over":
        draw_game_over()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()