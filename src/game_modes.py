import pygame
import sys
sys.path.append('.')
from main import main as single_player_mode
from npc_opponent import NPC

def show_main_menu():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((300, 600))
    pygame.display.set_caption("Tetris - Main Menu")

    font = pygame.font.SysFont("comicsans", 40)
    clock = pygame.time.Clock()

    run = True
    while run:
        screen.fill((0, 0, 0))

        # Draw menu options
        single_player_text = font.render("Single Player", True, (255, 255, 255))
        multi_player_text = font.render("Multi Player", True, (255, 255, 255))

        screen.blit(single_player_text, (50, 200))
        screen.blit(multi_player_text, (50, 300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if 50 < mouse_pos[0] < 250 and 200 < mouse_pos[1] < 240:
                    # Single player mode
                    single_player_mode()
                elif 50 < mouse_pos[0] < 250 and 300 < mouse_pos[1] < 340:
                    # Multi player mode
                    multi_player_mode()

        clock.tick(30)

def multi_player_mode():
    """Multiplayer mode against NPC"""
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Tetris - Multi Player")

    # Create NPC opponent
    npc = NPC()

    font = pygame.font.SysFont("comicsans", 40)
    clock = pygame.time.Clock()

    # Game variables
    player_grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    npc_grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    player_score = 0
    npc_score = 0

    run = True
    while run:
        screen.fill((0, 0, 0))

        # Draw player area
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 300, 600), 1)
        for i in range(len(player_grid)):
            for j in range(len(player_grid[i])):
                pygame.draw.rect(screen, player_grid[i][j],
                                 (j*30, i*30, 30, 30), 0)

        # Draw NPC area
        pygame.draw.rect(screen, (255, 255, 255), (300, 0, 300, 600), 1)
        for i in range(len(npc_grid)):
            for j in range(len(npc_grid[i])):
                pygame.draw.rect(screen, npc_grid[i][j],
                                 (300 + j*30, i*30, 30, 30), 0)

        # Display scores
        player_score_text = font.render(f"Player: {player_score}", True, (255, 255, 255))
        npc_score_text = font.render(f"NPC: {npc.score}", True, (255, 255, 255))

        screen.blit(player_score_text, (10, 10))
        screen.blit(npc_score_text, (310, 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                # Player controls
                if event.key == pygame.K_LEFT:
                    print("Player moved left")
                elif event.key == pygame.K_RIGHT:
                    print("Player moved right")
                elif event.key == pygame.K_DOWN:
                    print("Player moved down")
                elif event.key == pygame.K_UP:
                    print("Player rotated")

        # Simulate NPC making a move every second
        if clock.get_rawtime() > 1000:
            npc_move = npc.make_move(npc_grid)
            print(f"NPC would make move: {npc_move}")
            clock.tick()

        # Update NPC score
        npc.score = npc_score + int(clock.get_rawtime() / 1000)

    pygame.quit()

if __name__ == "__main__":
    show_main_menu()