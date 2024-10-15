import os
import pickle
import hashlib
import pygame
from constants import USER_DATA_DIR, MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH, white, black

# Default user statistics structure
default_stats = {
    "total_games": 0,
    "wins": 0,
    "losses": 0,
    "win_rate": 0.0,
    "loss_rate": 0.0,
    "password": ""
}

# Ensure the user data directory exists
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

# Function to hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load statistics for a specific user
def load_user_stats(username):
    user_file = os.path.join(USER_DATA_DIR, f"{username}.pkl")
    if os.path.exists(user_file):
        with open(user_file, 'rb') as f:
            return pickle.load(f)
    return default_stats.copy()

# Function to save statistics for a specific user
def save_user_stats(username, stats):
    user_file = os.path.join(USER_DATA_DIR, f"{username}.pkl")
    with open(user_file, 'wb') as f:
        pickle.dump(stats, f)

# Function to update user stats based on game result
def update_user_stats(stats, result):
    stats["total_games"] += 1
    if result == "win":
        stats["wins"] += 1
    elif result == "lose":
        stats["losses"] += 1
    else:
        stats["ties"] += 1
    stats["win_rate"] = stats["wins"] / stats["total_games"]
    stats["loss_rate"] = stats["losses"] / stats["total_games"]

# Function for user login
def login(win):
    username = ""
    password = ""
    input_rect = pygame.Rect(200, 200, 300, 50)
    font = pygame.font.Font(None, 32)
    active = False
    is_username = True  # Toggle between username and password input
    login_successful = False
    user_data = None

    while not login_successful:
        win.fill(black)
        text_surface = font.render(f"Username: {username}", True, white)
        password_surface = font.render(f"Password: {'*' * len(password)}", True, white)
        win.blit(text_surface, (input_rect.x, input_rect.y))
        win.blit(password_surface, (input_rect.x, input_rect.y + 60))

        pygame.draw.rect(win, white, input_rect, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        if is_username and len(username) > 0:
                            username = username[:-1]
                        elif not is_username and len(password) > 0:
                            password = password[:-1]
                    elif event.key == pygame.K_TAB:
                        is_username = not is_username
                    elif event.key == pygame.K_RETURN:
                        if is_username:
                            if len(username) == 0:
                                username = "player"
                            user_data = load_user_stats(username)
                            if user_data["password"] == "":
                                # First time login, set password
                                user_data["password"] = hash_password(password)
                                save_user_stats(username, user_data)
                                login_successful = True
                            elif user_data["password"] == hash_password(password):
                                login_successful = True
                        else:
                            is_username = not is_username  # Switch back to username input after enter
                    else:
                        if is_username and len(username) < MAX_USERNAME_LENGTH:
                            username += event.unicode
                        elif not is_username and len(password) < MAX_PASSWORD_LENGTH:
                            password += event.unicode

        pygame.display.update()

    return username, user_data
