import pygame
import sys
from random import randint
from degrees_to_velocuty import degrees_to_velocity


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Game():
    def __init__(self):
        pygame.init()
        WHITE = (255, 255, 255)
        screen_info = pygame.display.Info()
        self.W = screen_info.current_w
        self.H = screen_info.current_h
        self.screen = pygame.display.set_mode(
            (self.W, self.H),
            pygame.FULLSCREEN
        )
        self.screen_rect = self.screen.get_rect()
        self.edge = self.screen_rect.height - self.screen_rect.height * 0.10
        self.player_1 = Paddle(
            screen_rect=self.screen_rect,
            keys=(pygame.K_w, pygame.K_s),
            center=(self.screen_rect.width * 0.1, self.screen_rect.centery),
            color=WHITE
        )
        self.player_2 = Paddle(
            screen_rect=self.screen_rect,
            center=(self.screen_rect.width * 0.9, self.screen_rect.centery),
            color=WHITE,
            is_automatic=False,
        )
        self.ball = Ball(
            center=self.screen_rect.center,
            color=WHITE
        )
        self.all_sprites = pygame.sprite.Group()  # создаёт группу спрайтов
        self.all_sprites.add(self.player_1)  # добавляет игрока в группу
        self.all_sprites.add(self.player_2)
        self.all_sprites.add(self.ball)
        self.main_loop()

    def main_loop(self, game=True, FPS=30):
        self.FPS = FPS
        clock = pygame.time.Clock()
        self.game = game
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game = False
            # клавиши
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                game = False
            '''
            TODO:
            уменьшить количество повторейний, перенести в процессы ракетки
            '''
            if self.player_1.keys:
                if keys[self.player_1.keys[0]]:  # клавиша стрелка вверх
                    border = (0 + (self.player_1.rect.size[1] / 2))
                    if self.player_1.rect.centery > border:
                        self.player_1.rect.centery -= self.player_1.speed
                if keys[self.player_1.keys[1]]:  # клавиша стрелка вниз
                    border = (self.H - (self.player_1.rect.size[1] / 2))
                    if self.player_1.rect.centery < border:
                        self.player_1.rect.centery += self.player_1.speed
            if self.player_2.keys:
                if keys[self.player_2.keys[0]]:  # клавиша стрелка вверх
                    border = (0 + (self.player_2.rect.size[1] / 2))
                    if self.player_2.rect.centery > border:
                        self.player_2.rect.centery -= self.player_2.speed
                if keys[self.player_2.keys[1]]:  # клавиша стрелка вниз
                    border = (self.H - (self.player_2.rect.size[1] / 2))
                    if self.player_2.rect.centery < border:
                        self.player_2.rect.centery += self.player_2.speed

            # логика
            self.ball.rect.centerx += self.ball.speed_x
            self.ball.rect.centery += self.ball.speed_y
            if self.ball.rect.centerx < 0 + (self.ball.rect.size[0] // 2):
                self.ball.go_center(screen_rect=self.screen_rect)
                self.ball.rotate_ball()
            if self.ball.rect.centerx > self.W - (self.ball.rect.size[0] // 2):
                self.ball.go_center(screen_rect=self.screen_rect)
                self.ball.rotate_ball()

            # коллизия
            if self.ball.rect.centery < (0 + (self.ball.rect.size[1] // 2)):
                self.ball.speed_y *= -1
            border = (self.H - (self.ball.rect.size[1] // 2))
            if self.ball.rect.centery > border:
                self.ball.speed_y *= -1
            if self.ball.rect.colliderect(self.player_1) or self.ball.rect.colliderect(self.player_2):
                self.ball.speed_x *= -1

            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.screen.fill(BLACK)
            clock.tick(FPS)
        pygame.quit()


class Paddle(pygame.sprite.Sprite):
    '''
    TODO:
    добавить функционал бота
    '''
    def __init__(
            self,
            screen_rect=None,
            center=(0, 0),
            color=WHITE,
            size=None,
            keys=(pygame.K_UP, pygame.K_DOWN),
            speed=12,
            is_automatic=False
    ):
        super().__init__()
        if not size:
            size = (screen_rect.width * 0.01, screen_rect.height * 0.10)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = speed
        if not is_automatic:
            self.keys = keys


class Ball(pygame.sprite.Sprite):
    def __init__(
            self,
            center=None,
            color=WHITE,
            speed=12,
            size=(10, 10)
    ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_x = degrees_to_velocity(30, speed)[0]
        self.speed_y = degrees_to_velocity(30, speed)[1]

    def go_center(self, screen_rect=None):
        self.rect.center = screen_rect.center

    def rotate_ball(self):
        if randint(0, 1) == 1:
            ball_direction = degrees_to_velocity(randint(225, 315), 10)
        else:
            ball_direction = degrees_to_velocity(randint(45, 135), 10)
        self.speed_x = ball_direction[0]
        self.speed_y = ball_direction[1]


class Score:
    ''' табло '''
    pass


game = Game()
sys.exit()
