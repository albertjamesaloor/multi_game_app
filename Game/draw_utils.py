import pygame
import constants
from user_management import load_user_stats

def draw_rps_win(win, game, p, score_a, score_b):
    win.blit(constants.BACKGROUND, (0, 0))
    # rest of the code for drawing RPS

def draw_stats_win(win, username):
    stats = load_user_stats(username)

    win.blit(constants.BACKGROUND, (0, 0))
    header_font = pygame.font.SysFont("comicsans", 60)
    stats_font = pygame.font.SysFont("comicsans", 40)
    
    # Render RPS and Shooter stats
    rps_total_games = stats_font.render(f"Total Games: {stats['rps_total_games']}", 1, constants.white)
    win.blit(rps_total_games, (constants.width/4 - rps_total_games.get_width()/2, 200))
    # Render more stats as needed

    pygame.display.update()

def draw_shooter_win(win, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    win.blit(constants.SPACE, (0, 0))
    pygame.draw.rect(win, constants.black, constants.BORDER)
    win.blit(constants.YELLOW_SPACESHIP, (yellow.x, yellow.y))
    win.blit(constants.RED_SPACESHIP, (red.x, red.y))

    # Display health and other shooter-related stats
    red_health_text = constants.HEALTH_FONT.render(f"Health: {red_health}", 1, constants.white)
    win.blit(red_health_text, (constants.width - red_health_text.get_width() - 10, 10))
    pygame.display.update()

def draw_winner(win, text):
    draw_text = constants.WINNER_FONT.render(text, 1, constants.white)
    win.blit(draw_text, (constants.width / 2 - draw_text.get_width() // 2, constants.height / 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)
