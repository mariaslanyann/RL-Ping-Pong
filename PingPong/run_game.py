from env import PingPongGame
import pygame
import time
import imageio


env = PingPongGame()
obs, _ = env.reset()

action = 0

frames = []

start_time = time.time()

max_duration = 10  # seconds

while True:

    elapsed_time = time.time() - start_time
    
  
    if elapsed_time >= max_duration:
        break
    
    should_exit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                action = 1  # Move up for player 1
            elif event.key == pygame.K_s:
                action = 2  # Move down for player 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                action = 0
            if event.key == pygame.K_s:
                action = 0

    _, _, done, _, _ = env.step(action)

    screen = env.render("training")
    frame = pygame.surfarray.array3d(screen)
    frame = frame.swapaxes(0, 1)
    frames.append(frame)


    if done or should_exit:
        break


gif_path = "ping_pong_game_vs.gif"
imageio.mimsave(gif_path, frames, duration=1/30) 


env.close()
