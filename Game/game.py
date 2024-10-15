import pygame
import constants


class RPS:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0]
        p2 = self.moves[1]
        RPS = ["Rock", "Paper", "Scissors"]

        winner = -1
        if RPS.index(p1) - RPS.index(p2) in [-1, 2]:
            winner = 1
        if RPS.index(p1) - RPS.index(p2) in [1, -2]:
            winner = 0
        
        return winner
    

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False 

class Shooter:
    def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - constants.VEL > 0:  # LEFT
            yellow.x -= constants.VEL
        if keys_pressed[pygame.K_d] and yellow.x + constants.VEL + yellow.width < constants.BORDER.x:  # RIGHT
            yellow.x += constants.VEL
        if keys_pressed[pygame.K_w] and yellow.y - constants.VEL > 0:  # UP
            yellow.y -= constants.VEL
        if keys_pressed[pygame.K_s] and yellow.y + constants.VEL + yellow.height < constants.height - 10:  # DOWN
            yellow.y += constants.VEL

    def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - constants.VEL > constants.BORDER.x:  # LEFT
            red.x -= constants.VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + constants.VEL + red.width < constants.width:  # RIGHT
            red.x += constants.VEL
        if keys_pressed[pygame.K_UP] and red.y - constants.VEL > 0:  # UP
            red.y -= constants.VEL
        if keys_pressed[pygame.K_DOWN] and red.y + constants.VEL + red.height < constants.height - 10:  # DOWN
            red.y += constants.VEL

    def handle_bullets(yellow_bullets, red_bullets, yellow, red):
        for bullet in yellow_bullets:
            bullet.x += constants.BULLET_VEL
            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(constants.RED_HIT))
                yellow_bullets.remove(bullet)
            elif bullet.x > constants.width:
                yellow_bullets.remove(bullet)

        for bullet in red_bullets:
            bullet.x -= constants.BULLET_VEL
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(constants.YELLOW_HIT))
                red_bullets.remove(bullet)
            elif bullet.x < 0:
                red_bullets.remove(bullet)
