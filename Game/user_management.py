import os
import pickle
import hashlib
import pygame
from constants import USER_DATA_DIR, MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH, white, black, width, height, THE_OTHER_BLUE, LIGHTGREY, Dark_Red, get_font
from button import mainButton
from scan_server import scan_network_and_check_port

# Default user statistics structure
default_stats = {
    "rps_total_games": 0,
    "rps_wins": 0,
    "rps_losses": 0,
    "rps_win_rate": 0.0,
    "rps_loss_rate": 0.0,
    "shooter_total_games": 0,
    "shooter_red_wins": 0,
    "shooter_yellow_wins": 0,
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
def update_user_rps_stats(stats, result):
    stats["rps_total_games"] += 1
    if result == "win":
        stats["rps_wins"] += 1
    elif result == "lose":
        stats["rps_losses"] += 1
    stats["rps_win_rate"] = stats["rps_wins"] / stats["rps_total_games"]
    stats["rps_loss_rate"] = stats["rps_losses"] / stats["rps_total_games"]

def update_user_shooter_stats(stats, result):
    stats["shooter_total_games"] += 1
    if result == "Yellow Wins!":
        stats["shooter_yellow_wins"] += 1
    elif result == "Red Wins!":
        stats["shooter_red_wins"] += 1
# Function for user login
def login(win):
    username = ""
    password = ""
    input_rect = pygame.Rect(width/2- 150, height/2 - 25, 300, 50)
    font = pygame.font.Font(None, 32)
    active = True
    is_username = True  # Toggle between username and password input
    login_successful = False
    user_data = None
    found_server = ""
    connection_status = "Please connect to the server."

    while not login_successful:
        win.fill(black)
        text_surface = font.render(f"Username: {username}", True, white)
        password_surface = font.render(f"Password: {'*' * len(password)}", True, white)
        notice_surface = font.render("Use arrow keys to toggle between username and password.", True, white)
        connection_surface = font.render(connection_status, True, white)
                    

        MOUSE_POS = pygame.mouse.get_pos()


        CONNECT_BUTTON = mainButton(image=None, pos=(width * 0.85, height * 0.1), 
                            text_input="CONNECT", font=get_font(50), base_color=THE_OTHER_BLUE, hovering_color=LIGHTGREY)
        PLAY_BUTTON = mainButton(image=None, pos=(width / 2, height * 0.7), 
                            text_input="PLAY", font=get_font(65), base_color=Dark_Red, hovering_color=white)
        
        win.blit(text_surface, (input_rect.x + 3, input_rect.y + 13))
        win.blit(password_surface, (input_rect.x + 3, input_rect.y + 60))
        win.blit(notice_surface, (width/2 - notice_surface.get_width()/2, 600))
        win.blit(connection_surface, (width/2 - connection_surface.get_width()/2, 120))

        
        for button in [PLAY_BUTTON, CONNECT_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(win)

        pygame.draw.rect(win, white, input_rect, 2)
        
        
        for event in pygame.event.get():
            
            if "Connecting" in connection_status:

                # Call the server connection function if it hasn’t connected
                found_server = scan_network_and_check_port(5555)
                if found_server:
                    connection_status = "Connected to server."
                else:
                    connection_status = "Connection failed. Please retry." 

                pygame.display.update()
                pygame.time.delay(50)  

        
                
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONNECT_BUTTON.checkForInput(MOUSE_POS):
                    connection_status = "Connecting..."
                elif PLAY_BUTTON.checkForInput(MOUSE_POS):
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


            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        if is_username and len(username) > 0:
                            username = username[:-1]
                        elif not is_username and len(password) > 0:
                            password = password[:-1]
                    elif event.key == pygame.K_UP:
                        is_username = not is_username
                    elif event.key == pygame.K_DOWN:
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

    return username, user_data, found_server
