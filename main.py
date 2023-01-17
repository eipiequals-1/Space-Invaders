import pygame as pg
from pygame.math import Vector2 as vec2
import time

class Ship:
    def __init__(self, pos, vel, image):
        self.pos = vec2(pos)
        self.vel = vec2(vel)
        self.image = image
        self.size = [image.get_rect().w, image.get_rect().h]
        self.pos -= vec2(self.size) / 2

    def render(self, dt, surface):
        surface.blit(self.image, self.pos)

    def input(self, dt):
        pass

    def update(self, dt):
        self.pos += self.vel * dt


class Defender(Ship):
    def __init__(self, pos):
        super().__init__(pos, vec2(0, 0), pg.image.load("./assets/texture/spaceship.png"))

    def update(self, dt):
        super().update(dt)
        # check bounds
        if self.pos.x < 0: self.pos.x = 0
        elif self.pos.x + self.size[0] > Game.WIDTH: self.pos.x = Game.WIDTH - self.size[0]

        if self.pos.y < 0: self.pos.y = 0
        elif self.pos.y + self.size[1] > Game.HEIGHT: self.pos.y = Game.HEIGHT - self.size[1]

    def input(self, dt):
        speed = 200 
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.vel.x = -speed
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.vel.x = speed
        else:
            self.vel.x = 0
        
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.vel.y = -speed
        elif keys[pg.K_s] or keys[pg.K_DOWN]:
            self.vel.y = speed
        else:
            self.vel.y = 0


class Enemy(Ship):
    def __init__(self, pos):
        super().__init__(pos, vec2(0, 0), pg.image.load("./assets/texture/alien1.png"))
 

class Game:
    WIDTH = 600
    HEIGHT = 800
    FPS = 60

    def __init__(self):
        self.screen = pg.display.set_mode([self.WIDTH, self.HEIGHT])
        pg.display.set_caption("Space Invaders")
        self.running = True

        self.background_image = pg.image.load("./assets/texture/bg.png")
        # create entities
        self.player = Defender(vec2(self.WIDTH / 2, self.HEIGHT * 0.90))
        
        # create array of enemies
        self.enemies = []
        for y in range(5):
            for x in range(10):
                sprite_width, sprite_height = 50, 50
                position = vec2(75 + x * sprite_width, 0 + y * sprite_height)
                vel = vec2(0, 50)
                self.enemies.append(Enemy(position))
                self.enemies[len(self.enemies) - 1].vel = vel

        # for time purposes
        self.last_time = time.time()

    def run(self):
        while self.running:
            dt = self.tick()
            self.input(dt)
            self.update(dt)
            self.render(dt)

    def input(self, dt):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

        keys = pg.key.get_pressed()
        # check if the escape key was pressed
        if keys[pg.K_ESCAPE]:
            self.running = False

        self.player.input(dt)

    def tick(self):
        time.sleep(max(1.0 / self.FPS - (time.time() - self.last_time), 0))
        current_time = time.time()
        delta_time = current_time - self.last_time 
        self.last_time = current_time
        return delta_time

    def update(self, dt):
        self.player.update(dt)
        
        for i in range(len(self.enemies) - 1, -1, -1):
            enemy = self.enemies[i]
            enemy.update(dt)

    def render(self, dt):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, (0, 0))
        
        self.player.render(dt, self.screen)
        for enemy in self.enemies:
            enemy.render(dt, self.screen)
        pg.display.update()


def main():
    pg.init()

    game = Game()
    game.run()

    pg.quit()

if __name__ == "__main__":
    main()
