import pygame
import random
import sys
import numpy as np
import collections

class CatchGameEnv(object):
    def __init__(self):
        pygame.init()
        self.GAME_COLOR = (255, 255, 0)
        self.COLOR_BLACK = (0, 0, 0)
        self.CATCHER_WIDTH = 98
        self.CATCHER_HEIGHT = 30
        self.BALL_SPEED = 10
        self.GAME_HEIGHT = 500
        self.GAME_WIDTH = 500

    def returnXPos(self):
        positions = [(47, 0), (147, 100), (247, 200), (347, 300), (447, 400)]
        return random.choice(positions)
        
    def returnFrames(self):
        return np.array(list(self.frames))

    def reset(self):
        self.CATCHER_X = 200
        self.CATCHER_Y = 470
        self.BALL_Y = 20
        self.BALL_X, self.ZONE = self.returnXPos()

        self.GAME_OVER = False
        self.REWARD = 0
        self.frames = collections.deque(maxlen=4)

        self.screen = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HEIGHT))
        pygame.display.set_caption("RL Catch Game")
        self.clock = pygame.time.Clock()

        self.catcher_rect = pygame.Rect(self.CATCHER_X, self.CATCHER_Y, self.CATCHER_WIDTH, self.CATCHER_HEIGHT)

    def mainGame(self, action):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move catcher
        if action == 1:  # Move left
            self.CATCHER_X -= 100
            if self.CATCHER_X < 0:
                self.CATCHER_X = 0
        elif action == 2:  # Move right
            self.CATCHER_X += 100
            if self.CATCHER_X > self.GAME_WIDTH - self.CATCHER_WIDTH:
                self.CATCHER_X = self.GAME_WIDTH - self.CATCHER_WIDTH

        # Ball movement
        self.BALL_Y += self.BALL_SPEED
        
        # Collision detection (catch success)
        self.catcher_rect.x = self.CATCHER_X
        ball_rect = pygame.Rect(self.BALL_X, self.BALL_Y, 15, 15)
        if self.catcher_rect.colliderect(ball_rect):
            self.REWARD = 1
            self.GAME_OVER = True

        # Ball missed
        if self.BALL_Y > self.GAME_HEIGHT:
            self.REWARD = -1
            self.GAME_OVER = True
        
        # Render game
        self.screen.fill(self.COLOR_BLACK)
        pygame.draw.rect(self.screen, self.GAME_COLOR, self.catcher_rect)
        pygame.draw.circle(self.screen, self.GAME_COLOR, (self.BALL_X, self.BALL_Y), 15, 0)
            
        pygame.display.flip()
        self.clock.tick(10)

        if self.GAME_OVER:
            self.reset()

        return self.GAME_OVER, self.returnFrames(), self.REWARD


if __name__ == '__main__':
    num_wins = 0

    for i in range(100):
        game = CatchGameEnv()
        game.reset()
        game_over = False
        while not game_over:
            action = random.randint(0, 2)
            game_over, _, reward = game.mainGame(action)
            if reward == 1:
                num_wins += 1

    # Final game session
    game = CatchGameEnv()
    game.reset()
    game_over = False
    while not game_over:
        action = random.randint(0, 2)
        game_over, _, _ = game.mainGame(action)
