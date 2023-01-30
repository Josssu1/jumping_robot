# Complete your game here

import pygame
import random as r

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

class Game:
    # initialize the game
    def __init__(self):
        pygame.init()
        self.new_game()
        self.starting_screen()
        self.main_loop()

    # setting up new game, everything that needs to be done only once
    def new_game(self):
        self.download_images()
        self.clock = pygame.time.Clock()
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.robot = [self.images[2], self.window_width/2-self.images[2].get_width()/2, self.window_height-200-self.images[2].get_height()]
        self.create_platforms()
        self.create_enemies()
        self.create_coins()
        self.left_input = False
        self.right_input = False
        self.jump_speed = 10
        self.score = 0

    # the static screen including all the instructions. Whaits for user to press space to start the game
    def starting_screen(self):
        start = False
        while start == False:
            self.window.fill((200, 153, 204))
            font = pygame.font.SysFont("Arial", 32)
            text1 = font.render("Move with arrow keys", True, (255, 255, 255))
            text2 = font.render("Collect coins while avoiding all enemies", True, (255, 255, 255))
            text3 = font.render("Do not fall! Good luck! ", True, (255, 255, 255))
            text4 = font.render("Press space to start ", True, (255, 255, 255))
            self.window.blit(text1, (self.window_width / 2 - text1.get_width() / 2, 50))
            self.window.blit(text2, (self.window_width / 2 - text2.get_width() / 2, 50 + text1.get_height()))
            self.window.blit(text3, (self.window_width / 2 - text3.get_width() / 2, 50 + text1.get_height() + text2.get_height()))
            self.window.blit(text4, (self.window_width / 2 - text4.get_width() / 2, self.window_height - 100))
            self.window.blit(self.robot[0], (self.robot[1], self.robot[2]))
            pygame.display.flip()
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    start = True
                if event.type == pygame.QUIT:
                    exit()
        
    # downloading different sprites used in the game and saving them into a list
    def download_images(self):
        self.images = []
        for image in ["coin.png", "monster.png", "robot.png"]:
            self.images.append(pygame.image.load(image))

    # creates all the platforms and assigns random speed to each one
    def create_platforms(self):
        self.platforms = []
        self.platforms.append([0, self.window_width, self.window_height-200, 0])
        n_platforms = 1000
        for i in range(1, n_platforms):
            platform_length = 250
            platform_start =  self.window_width / 2 - platform_length / 2
            platform_gap = 200
            platform_speed = r.randrange(-4, 4)
            self.platforms.append([platform_start, platform_start + platform_length, self.platforms[i-1][2] - platform_gap, platform_speed])

    # creates enemies into random locations
    def create_enemies(self):
        self.enemies = []
        n_enemies = 600
        self.enemies.append([r.randrange(0, self.window_width - self.images[1].get_width()), -200])
        for i in range(0, n_enemies):
            enemy_x = r.randrange(100, self.window_width-100-self.images[1].get_width())
            enemy_y = self.enemies[i-1][1] - r.randrange(300, 700, 50)
            self.enemies.append([enemy_x, enemy_y])
    
    # creates coins into random locations
    def create_coins(self):
        self.coins = []
        n_coins = 600
        self.coins.append([r.randrange(0, self.window_width - self.images[0].get_width()), -300])
        for i in range(0, n_coins):
            coin_x = r.randrange(0, self.window_width - self.images[0].get_width())
            coin_y = self.coins[i-1][1] - r.randrange(300, 700, 50)
            self.coins.append([coin_x, coin_y])

    # the main loop of the game
    def main_loop(self):
        while True:
            # checks for user input
            self.check_events()
            # moves the character based on user input 
            self.move()
            # checks if the player makes contact with an enemy, ends the game
            if self.check_enemy_collision():
                break
            # check if the player makes contact with a coin, removes the coin and increases the score
            self.check_coin_collision()
            # checks if there is platform below the players character
            self.check_collision()
            # updates the window
            self.update_window()
            # checks if player fells out of the screen
            if self.game_over():
                break
        # displays the score after the game has ended and asks the player to play again
        self.end_screen()

    # checks for user inputs
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.jump()
                if event.key == pygame.K_LEFT:
                    self.left_input = True
                if event.key == pygame.K_RIGHT:
                    self.right_input = True
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_input = False
                if event.key == pygame.K_RIGHT:
                    self.right_input = False
                
            if event.type == pygame.QUIT:
                exit()

    # updates the window
    def update_window(self):
        self.window.fill((200, 153, 204))
        # lowers every platform by one pixel and moves them horizontally based on their speed
        for platform in self.platforms:
            platform[2] += 1
            platform[0] += platform[3]
            platform[1] += platform[3]
            # checks if platform touches the ends of the screen and changes the direction they are moving
            if platform[0] <= 0 or platform[1] >= self.window_width:
                platform[3] *= -1
            pygame.draw.line(self.window, (255, 255, 255), (platform[0], platform[2]), (platform[1], platform[2]), 7)
        # lowers every enemy by one pixel
        for enemy in self.enemies:
            enemy[1] += 1
            self.window.blit(self.images[1], (enemy[0], enemy[1]))
            pygame.draw.line(self.window, (255, 0, 0), (enemy[0]-20, enemy[1]+self.images[1].get_height()), (enemy[0]+self.images[1].get_width()+20, enemy[1]+self.images[1].get_height()), 7)
        # lowers every coin by one pixel
        for coin in self.coins:
            coin[1] += 1
            self.window.blit(self.images[0], (coin[0], coin[1]))
        # lowers the robot by one pixel
        self.robot[2] += 1
        self.window.blit(self.robot[0], (self.robot[1], self.robot[2]))
        # displaying the current score
        font = pygame.font.SysFont("Arial", 24)
        self.score += 1
        score_text = font.render(f"score: {self.score // 30}", True, (255, 255, 255))
        self.window.blit(score_text, (self.window_width - score_text.get_width() - 10, 10))

        pygame.display.flip()
        self.clock.tick(60)

    # if user presses the space bar the robot jumps
    def jump(self):
        if not self.check_collision():
            return
        jump_height = 220
        for i in range(0, int(jump_height/self.jump_speed)):
            self.robot[2] -= self.jump_speed
            self.move()
            self.check_coin_collision()
            if self.check_enemy_collision():
                break
            self.update_window()

    # moving the character horizontally according to user input
    def move(self):
        velocity = 7
        if self.left_input:
            self.robot[1] += -velocity
        if self.right_input:
            self.robot[1] += velocity
        if self.robot[1] < -self.images[2].get_width()/2:
            self.robot[1] = self.window_width-self.images[2].get_width()/2
        if self.robot[1] > self.window_width-self.images[2].get_width()/2:
            self.robot[1] = -self.images[2].get_width()/2

    # checks for every platform if the player is directly on top of it
    def check_collision(self):
        for platform in self.platforms:
            if platform[2] - self.robot[2] < self.images[2].get_height()+10 and platform[2] - self.robot[2] >= self.images[2].get_height() and self.robot[1] + self.images[2].get_width() > platform[0] and self.robot[1] < platform[1]:
                self.robot[2] = platform[2] - self.images[2].get_height()
                self.robot[1] += platform[3]
                return True
        self.robot[2] += self.jump_speed
        return False 

    # checks for every enemy if the player is making contact with them
    def check_enemy_collision(self):
        for enemy in self.enemies:
            if self.robot[1] + self.images[2].get_width() - enemy[0] >= 10 and enemy[0] + self.images[1].get_width() - self.robot[1] >= 10 and self.robot[2] + self.images[2].get_height() - enemy[1] >= 10 and enemy[1] + self.images[1].get_height() - self.robot[2] >= 10:
                return True
        return False

    # checks for every coin if the player is making contact with them, the coin is then removed and the score increased
    def check_coin_collision(self):
        for coin in self.coins:
            if self.robot[1] + self.images[2].get_width() - coin[0] >= 0 and coin[0] + self.images[0].get_width() - self.robot[1] >= 0 and self.robot[2] + self.images[2].get_height() - coin[1] >= 0 and coin[1] + self.images[0].get_height() - self.robot[2] >= 0:
                self.coins.remove(coin)
                self.score += 300 * 2
            
    # checks if the user falls off the screen
    def game_over(self):
        if self.robot[2] + self.images[2].get_height() >= self.window_height:
            return True
        return False

    # displaying the final score after the game has ended and asks to play again
    def end_screen(self):
        new_game = False
        while new_game == False:
            self.window.fill((200, 153, 204))
            font = pygame.font.SysFont("Arial", 32)
            text1 = font.render("Game over!", True, (255, 255, 255))
            text2 = font.render(f"Your score: {self.score // 30}", True, (255, 255, 255))
            text3 = font.render("Press space to play again ", True, (255, 255, 255))
            self.window.blit(text1, (self.window_width / 2 - text1.get_width() / 2, 50))
            self.window.blit(text2, (self.window_width / 2 - text2.get_width() / 2, 50 + text1.get_height()))
            self.window.blit(text3, (self.window_width / 2 - text3.get_width() / 2, self.window_height - 100))
            pygame.display.flip()
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    new_game = True
                if event.type == pygame.QUIT:
                    exit()
        self.new_game()
        self.main_loop()

Game()