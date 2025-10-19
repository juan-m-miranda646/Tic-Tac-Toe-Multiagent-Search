import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgent import minimax


class SimpleTicTacToe:
    """Minimal working version of Tic Tac Toe with Minimax AI."""

    def __init__(self):
        pygame.init()
        
        # initial Board Layout
        self.HEADER_H = 70 # title size
        self.CELL = 133 # pixels for each square
        self.size = 3 # board start size (3x3)
        
        self.window_w = self.CELL * 3 # width of board
        self.window_h = self.HEADER_H + self.CELL * 3 # height of board
        self.screen = pygame.display.set_mode((self.window_w, self.window_h)) # board creation
        pygame.display.set_caption("Tic-Tac-Toe") # title name
        
        # fonts
        self.font_title = pygame.font.SysFont(None, 36)
        self.font_ui = pygame.font.SysFont(None, 24)
        
        # setting up header interaction for selecting board size
        self.size_rect = pygame.Rect(self.window_w - 150, 20, 120, 30)
        
        # game states
        self.board = np.zeros((self.size, self.size), dtype=int)   # 0 = empty
        self.current_turn = 1                      # 1 = Player (X), -1 = AI (O)
        self.game_state = GameStatus(self.board)
        self.running = True
        
    def draw_header(self):
        # header background
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.window_w, self.HEADER_H))
        pygame.draw.line(self.screen, (180, 180, 180), (0, self.HEADER_H - 1), (self.window_w, self.HEADER_H - 1), 2)

        # title information
        title = self.font_title.render("Tic-Tac-Toe", True, (255, 255, 255))
        self.screen.blit(title, (12, 12))
        
        # select board size (3x3, 4x4, 5x5)
        pygame.draw.rect(self.screen, (30, 30, 30), self.size_rect, border_radius = 6)
        pygame.draw.rect(self.screen, (255, 255, 255), self.size_rect, 2, border_radius = 6)

        label = self.font_ui.render("Board size:", True, (255, 255, 255))
        self.screen.blit(label, (self.size_rect.x - 100, self.size_rect.y + 5))

        value = self.font_ui.render(f"{self.size}x{self.size}  ▾", True, (255, 255, 255))
        self.screen.blit(value, (self.size_rect.x + 10, self.size_rect.y + 5))
        
    # remake of board when changing size
    def recompute_window(self):
        # Resize the program for new board size
        self.window_w = self.CELL * self.size
        self.window_h = self.HEADER_H + self.CELL * self.size
        self.screen = pygame.display.set_mode((self.window_w, self.window_h))
        # adjust the selector position due to new board size
        self.size_rect.x = self.window_w - 150
        
    # reset option when changing board size
    def reset_board(self, new_size=None):
        """Reset board (and optionally change size)."""
        if new_size is not None and new_size != self.size:
            self.size = new_size
            self.recompute_window()

        self.board = np.zeros((self.size, self.size), dtype=int)
        self.current_turn = 1
        self.game_state = GameStatus(self.board)

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        self.draw_header()

        # create grid under header
        top = self.HEADER_H
        color = (255, 255, 255)
        edge_rect = pygame.Rect(0, top, self.CELL * self.size, self.CELL * self.size)
        pygame.draw.rect(self.screen, color, edge_rect, 2)
        # draw grid lines for the board
        for i in range(1, self.size):
            y = top + i * self.CELL
            x = i * self.CELL
            pygame.draw.line(self.screen, color, (0, y), (self.window_w, y), 3)
            pygame.draw.line(self.screen, color, (x, top), (x, top + self.CELL * self.size), 3)
        pygame.display.update()

    def draw_symbol(self, row, col, value):
        # calculate the center of a square
        cx = col * self.CELL + self.CELL // 2
        cy = self.HEADER_H + row * self.CELL + self.CELL // 2

        # constant values for squares
        half = 40
        stroke = 4
        radius = 45

        if value == 1:  # X
            pygame.draw.line(self.screen, (255, 0, 0), (cx - half, cy - half), (cx + half, cy + half), stroke)
            pygame.draw.line(self.screen, (255, 0, 0), (cx + half, cy - half), (cx - half, cy + half), stroke)
        elif value == -1:  # O
            pygame.draw.circle(self.screen, (0, 255, 0), (cx, cy), radius, stroke)
        pygame.display.update()

    def is_game_over(self):
        terminal = self.game_state.is_terminal()
        if terminal:
            final_scores = self.game_state.get_scores(terminal)
            print(f"🏁 Game Over! Final Scores: {final_scores}")
            return True
        return False

    def move(self, move, value):
        """Apply move and sync logical GameStatus."""
        row, col = move
        self.board[row][col] = value
        self.game_state = self.game_state.get_new_state(move)

    def play_ai(self):
        """AI uses Minimax algorithm to choose next move."""
        # For 3x3 board, do a complete search since the tree is not too deep: perfect play
        if self.size == 3:
            empties = int((self.board == 0).sum())
            depth = empties                    # search to terminal
        else:
            # For 4x4 / 5x5, set depth to a modest value
            # to avoid a large search search time
            depth = 4 if self.size == 4 else 3
        
        score, move = minimax(self.game_state, depth=depth, maximizingPlayer=False)
        if move:
            r, c = move
            self.move(move, -1)
            self.draw_symbol(r, c, -1)
            print(f"🤖 AI chose {move} (score={score})")

    def play_game(self):
        """Playable loop — alternates between player and AI until terminal."""
        self.draw_board()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    # the board size selector is interactable at all times
                    if self.size_rect.collidepoint(event.pos):
                        next_size = {3: 4, 4: 5, 5: 3}[self.size]  # cycle for size options
                        self.reset_board(new_size=next_size)
                        self.draw_board()
                        continue  # avoids making it a board click for the player

                    # setting the player's click on the board when it is his/her turn
                    if self.current_turn != 1:
                        continue

                    x, y = event.pos # x and y axis values from the mouse
                    
                    # adjustment in the y position due to header
                    if y < self.HEADER_H:
                        continue
                    row, col = (y - self.HEADER_H) // self.CELL, x // self.CELL
                    #row, col = y // 133, x // 133

                    # Skip invalid clicks
                    if row > self.size - 1 or col > self.size - 1 or self.board[row][col] != 0:
                        continue

                    # Player move (1)
                    self.move((row, col), 1)
                    self.draw_symbol(row, col, 1)

                    if self.is_game_over():
                        pygame.time.wait(1500)
                        self.running = False
                        break

                    # Switch to AI
                    self.current_turn = -1
                    pygame.display.update()

                    # AI move
                    self.play_ai()

                    if self.is_game_over():
                        pygame.time.wait(1500)
                        self.running = False
                        break

                    # 🔁 Switch back to player
                    self.current_turn = 1

            pygame.display.update()

        print("👋 Exiting game.")
        pygame.quit()


# --- Quick test harness ---
if __name__ == "__main__":
    game = SimpleTicTacToe()
    game.play_game()