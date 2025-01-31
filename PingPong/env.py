import pygame
import random
import numpy as np
import gymnasium as gym
from gymnasium import spaces

# konstant
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_WIDTH = 15
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class PingPongGame(gym.Env):
    def __init__(self):
        super(PingPongGame, self).__init__()
        
      
        self.action_space = spaces.Discrete(3)  # 0 = do nothing, 1 = move up, 2 = move down
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0]), high=np.array([SCREEN_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_WIDTH]), dtype=np.float32)
        
     
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ping Pong Game")
        self.clock = pygame.time.Clock()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
   
        self.player1_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.player2_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2 - BALL_WIDTH // 2
        self.ball_speed_x = BALL_SPEED_X
        self.ball_speed_y = BALL_SPEED_Y
        self.player1_score = 0
        self.player2_score = 0

        self.state = np.array([self.player1_y, self.player2_y, self.ball_x, self.ball_y], dtype=np.float32)
        return self.state, {}

    def step(self, action):
        reward = 0

        # left paddle
        if action == 1 and self.player1_y > 0:  # up
            self.player1_y -= PADDLE_SPEED
        elif action == 2 and self.player1_y < SCREEN_HEIGHT - PADDLE_HEIGHT:  # down
            self.player1_y += PADDLE_SPEED
        
        # right paddle
        if self.ball_y < self.player2_y + PADDLE_HEIGHT // 2:
            self.player2_y -= PADDLE_SPEED  # up 
        elif self.ball_y > self.player2_y + PADDLE_HEIGHT // 2:
            self.player2_y += PADDLE_SPEED  # down

        # ekranic durs chga
        if self.player2_y < 0:
            self.player2_y = 0
        if self.player2_y > SCREEN_HEIGHT - PADDLE_HEIGHT:
            self.player2_y = SCREEN_HEIGHT - PADDLE_HEIGHT

        # arjeqner@ noracvi
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # gndaki harvac@ verevi u nerqevi pateri het
        if self.ball_y <= 0 or self.ball_y >= SCREEN_HEIGHT - BALL_WIDTH:
            self.ball_speed_y = -self.ball_speed_y

        # taxtakneri het harvac
        if (self.ball_x <= 30 + PADDLE_WIDTH and self.player1_y < self.ball_y < self.player1_y + PADDLE_HEIGHT) or \
           (self.ball_x >= SCREEN_WIDTH - 30 - PADDLE_WIDTH and self.player2_y < self.ball_y < self.player2_y + PADDLE_HEIGHT):
            self.ball_speed_x = -self.ball_speed_x

        # miavor
        if self.ball_x <= 0:
            self.player2_score += 1
            reward = -10
            self.ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
            self.ball_y = SCREEN_HEIGHT // 2 - BALL_WIDTH // 2
            self.ball_speed_x = -self.ball_speed_x
        elif self.ball_x >= SCREEN_WIDTH - BALL_WIDTH:
            self.player1_score += 1
            reward = 10
            self.ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
            self.ball_y = SCREEN_HEIGHT // 2 - BALL_WIDTH // 2
            self.ball_speed_x = -self.ball_speed_x

        # stugir ete mek@ haxtum e
        done = False
        if self.player1_score >= 5:
            done = True
            reward = 100
        elif self.player2_score >= 5:
            done = True
            reward = -100

        # miavorner@ noracvi
        self.state = np.array([self.player1_y, self.player2_y, self.ball_x, self.ball_y], dtype=np.float32)

        return self.state, reward, done, False, {}

    
    def render(self, mode="human"):
        self.screen.fill(BLACK)

        # mejteci ketagcer
        for i in range(0, SCREEN_HEIGHT, 20):  # chap erkar karch gcer
            pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH // 2 - 2, i, 4, 10))  # poqr uxxankyunner

        # paddles
        pygame.draw.rect(self.screen, WHITE, (30, self.player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))  # Player 1 paddle
        pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH - 30 - PADDLE_WIDTH, self.player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))  # Player 2 paddle

        # gndak
        pygame.draw.ellipse(self.screen, WHITE, (self.ball_x, self.ball_y, BALL_WIDTH, BALL_WIDTH))

        # miavorneri patkerum
        font = pygame.font.SysFont("Arial", 30)
        player1_score_text = font.render(str(self.player1_score), True, WHITE)
        self.screen.blit(player1_score_text, (SCREEN_WIDTH // 4, 20))

        player2_score_text = font.render(str(self.player2_score), True, WHITE)
        self.screen.blit(player2_score_text, (SCREEN_WIDTH * 3 // 4 - player2_score_text.get_width(), 20))
        
        #if mode != "training":
        pygame.display.flip()
        self.clock.tick(FPS)

        return self.screen


    def close(self):
        pygame.quit()
