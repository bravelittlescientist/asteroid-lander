import pygame

from astral.server.gameserver import GameServer
from astral.server import elements

from astral.client import local
from astral.client.gameclient import GameClient

class LunarServer(GameServer):
     def init(self):
        self.max_players = 2 
        # Draw terrain, initialize home base

     def player_joined(self, player):
        lander = ServerLunarLander()
        self.objects.add(lander)
        player.owns_object(lander)

class ServerLunarLander(elements.Mob):
    def init(self):
        super(ServerLunarLander, self).init();     
        self.x = 10
        self.y = 10
        self.width = 100
        self.width = 90
        self.template = "lunarlander"        

    def update(self, server):
        # Update position, speed
        pass

class ClientLunarLander(local.Mob):
    def init(self):
        self.template = "lunarlander"

class LunarClient(GameClient):
    def init(self):
        self.predict_owned = False
        self.remote_classes["lunarlander"] = ClientLunarLander

class Game(object):
    def __init__(self):
        self.player_number = raw_input("Are you player '1' or player '2'? ")
        if self.player_number == "1":
            self.server = LunarServer()
            self.server.host("127.0.0.1", 1111, "podsixnet")
        else:
            self.server = None
        self.client = LunarClient()
        self.client.connect("127.0.0.1", 1111, "podsixnet")
        self.client.announce({})
        self.screen = pygame.display.set_mode([640, 480])
        self.clock = pygame.time.Clock()
        self.running = True
    
    def draw(self):
        self.screen.fill([0, 0, 0])
        for mob in self.client.objects.values(): 
            if mob.template == "ball":
                pygame.draw.rect(self.screen, [255, 255, 255], [[mob.x, mob.y], [mob.width, mob.height]])
        pygame.display.flip()
    
    def input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.client.buffer_action("down")
        if keys[pygame.K_UP]:
            self.client.buffer_action("up")
  
    def update(self):
        if self.server:
            self.server.update()
        self.client.listen()
        self.dt = self.clock.tick(30)
        self.draw()
        self.input()

    def run(self):
        while self.running:
            self.update()

lander = Game()
lander.run()
