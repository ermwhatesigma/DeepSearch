import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
CARD_WIDTH = 90
CARD_HEIGHT = 110
CARD_MARGIN = 15

DECK_GRID_COLS = 4
DECK_CARD_WIDTH = 120
DECK_CARD_HEIGHT = 150
DECK_CARD_MARGIN = 15
SCROLL_AREA_HEIGHT = 350

GAME_TIME_LIMIT = 180 

CANNON_DECAY_RATE = 10
CANNON_DECAY_PER_FRAME = CANNON_DECAY_RATE / 60.0
MIN_CANNON_SEPARATION = 80 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
GREY = (200, 200, 200)
GOLD = (255, 215, 0)
BROWN = (139, 69, 19)
BROWNISH = (160, 82, 45)
LIGHT_BLUE = (150, 150, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)
TRANSPARENT_BLACK = (0, 0, 0, 150)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dot War")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 96)
button_font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 24)

MENU = 0
SELECT_DECK = 1 
PLAYING = 2
GAME_OVER = 3
game_state = MENU

TROOP_TYPES = {
    "warrior": {"color": BLUE, "radius": 15, "hp": 700, "damage": 80, "speed": 0.9, "cost": 3, "range": 20, "detection_radius": 120},
    "archer": {"color": GREEN, "radius": 12, "hp": 120, "damage": 60, "speed": 0.8, "cost": 3, "range": 100, "detection_radius": 140},
    "giant": {"color": RED, "radius": 25, "hp": 1100, "damage": 200, "speed": 0.6, "cost": 5, "range": 20, "detection_radius": 120},
    "minitank": {"color": BLACK, "radius": 14, "hp": 600, "damage": 200, "speed": 1, "cost": 4, "range": 20, "detection_radius": 120},
    "prince": {"color": GOLD, "radius": 16, "hp": 800, "damage": 140, "speed": 1.8, "cost": 5, "range": 20, "detection_radius": 120},
    "skellies": {"color": WHITE, "radius": 8, "hp": 2, "damage": 40, "speed": 1.1, "cost": 1, "range": 25, "detection_radius": 100},
    "goblins": {"color": GREEN, "radius": 9, "hp": 60, "damage": 45, "speed": 1.2, "cost": 2, "range": 20, "detection_radius": 110},
    "skeleton giant": {"color": GREY, "radius": 25, "hp": 1300, "damage": 150, "speed": 0.7, "cost": 6, "range": 25, "detection_radius": 120},
    "valkyrie": {"color": ORANGE, "radius": 18, "hp": 780, "damage": 100, "speed": 1.0, "cost": 4, "range": 20, "detection_radius": 120},
    "Royal giant": {"color": DARK_GRAY, "radius": 25, "hp": 1100, "damage": 260, "speed": 0.7, "cost": 6, "range": 80, "detection_radius": 160}
}
BUILDING_TYPES = {
    "cannon": {"color": BROWN, "width": 17, "height": 17, "hp": 550, "damage": 70, "cost": 3, "range": 100},
    "tesla": {"color": BROWNISH, "width": 20, "height": 20, "hp": 500, "damage": 90, "cost": 4, "range": 110}
}
TOWER_TYPES = {
    "king_tower": {"color": GOLD, "width": 60, "height": 80, "hp": 5986, "damage": 140, "range": 120},
    "princess_tower": {"color": GREY, "width": 40, "height": 60, "hp": 3052, "damage": 60, "range": 150}
}
SPELL_TYPES = {
    "arrows": {"color": YELLOW, "damage": 130, "radius": 100, "cost": 3},
    "fireball": {"color": ORANGE, "damage": 280, "radius": 50, "cost": 4}
}

player_troops = []
enemy_troops = []
player_towers = []
enemy_towers = []
active_spells = []
active_bombs = []
active_projectiles = []
player_elixir = 0.0
bot_elixir = 0.0
bot_action_cooldown = 0
max_elixir = 10.0
elixir_rate = 1 / 60
player_full_deck = [] 
player_hand = []
player_draw_pile = []
player_discard_pile = []
selected_card_index = -1
all_available_cards = list(TROOP_TYPES.keys()) + list(BUILDING_TYPES.keys()) + list(SPELL_TYPES.keys())
bot_full_deck = all_available_cards 
bot_hand = [] 
bot_draw_pile = []
bot_discard_pile = [] 
game_over = False
winner = None
game_timer = GAME_TIME_LIMIT
king_tower_active = {"player": False, "enemy": False}
player_selected_deck = [] 

deck_scroll_offset = 0
is_scrolling_deck = False
last_mouse_y = False


class Button:
    def __init__(self, x, y, width, height, text, color, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.rendered_text = button_font.render(self.text, True, self.text_color)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        surface.blit(self.rendered_text, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class GameObject:
    def __init__(self, x, y, hp, team):
        self.x = x
        self.y = y
        self.max_hp = hp
        self.hp = hp
        self.team = team
        self.alive = True
        self.hit_timer = 0

    def draw_health_bar(self, surface):
        if self.alive and self.hp < self.max_hp: 
            bar_width = 40
            bar_height = 5
            fill = (self.hp / self.max_hp) * bar_width
            bar_y = self.y - self.get_radius() - 15
            
            if hasattr(self, 'height'): 
                
                bar_y = self.y - self.height // 2 - 10
                
            border_rect = pygame.Rect(self.x - bar_width // 2, bar_y, bar_width, bar_height)
            fill_rect = pygame.Rect(self.x - bar_width // 2, bar_y, int(fill), bar_height)
            
            health_color = (0, 255, 0) if self.team == "player" else (255, 0, 0)
            
            pygame.draw.rect(surface, (100, 100, 100), border_rect)
            pygame.draw.rect(surface, health_color, fill_rect)

    def get_radius(self):
        if hasattr(self, 'radius'):
            return self.radius
        elif hasattr(self, 'width'):
            return (self.width + self.height) / 4 
        return 10


class Troop(GameObject):
    def __init__(self, x, y, troop_type, team):
        stats = TROOP_TYPES[troop_type]
        super().__init__(x, y, stats["hp"], team)
        self.type = troop_type
        self.color = stats["color"]
        self.radius = stats["radius"]
        self.damage = stats["damage"]
        self.speed = stats["speed"]
        self.range = stats["range"]
        self.detection_radius = stats["detection_radius"]
        self.target = None
        self.attack_cooldown = 0
    
    def is_building_targeter(self):
        return self.type == "giant" or self.type == "Royal giant"

    def find_target(self, enemies):
        closest_enemy = None
        min_dist = float('inf')
        is_bt = self.is_building_targeter()
        
        for e in enemies:
            if not e.alive:
                continue
                
            dist = math.hypot(self.x - e.x, self.y - e.y)
            
            if dist > self.detection_radius:
                continue

            if is_bt and not isinstance(e, (Tower, Building)):
                continue 
            
            if dist < min_dist:
                min_dist = dist
                closest_enemy = e
        
        self.target = closest_enemy

    def move(self, enemies):
        global player_towers, enemy_towers
        
        original_target_x = None
        original_target_y = None

        if self.target and self.target.alive:
            original_target_x = self.target.x
            original_target_y = self.target.y
        else:
            towers_to_check = enemy_towers if self.team == "player" else player_towers
            alive_towers = [t for t in towers_to_check if t.alive]
            
            princess_towers = [t for t in alive_towers if t.type == "princess_tower"]
            king_tower = next((t for t in alive_towers if t.type == "king_tower"), None)

            target_tower = None
            if princess_towers:
                target_tower = min(princess_towers, key=lambda t: math.hypot(self.x - t.x, self.y - t.y))
            elif king_tower:
                target_tower = king_tower
            
            if not target_tower:
                return 
            
            original_target_x = target_tower.x
            original_target_y = target_tower.y
        
        final_target_x = original_target_x
        final_target_y = original_target_y

        river_center = SCREEN_HEIGHT // 2
        
        is_crossing = (self.team == "player" and self.y > river_center and final_target_y < river_center) or \
                      (self.team == "enemy" and self.y < river_center and final_target_y > river_center)

        if is_crossing:
            left_bridge_x = SCREEN_WIDTH // 4
            right_bridge_x = SCREEN_WIDTH * 3 // 4
            
            bridge_y = river_center
            
            if self.x < SCREEN_WIDTH // 2:
                bridge_x = left_bridge_x
            else:
                bridge_x = right_bridge_x
                
            target_x = bridge_x
            target_y = bridge_y
        else:
            target_x = final_target_x
            target_y = final_target_y
        
        if self.target and math.hypot(self.x - self.target.x, self.y - self.target.y) <= self.range + self.target.get_radius():
             return 

        dist = math.hypot(self.x - target_x, self.y - target_y)

        if dist > self.speed: 
            angle = math.atan2(target_y - self.y, target_x - self.x)
            self.x += math.cos(angle) * self.speed
            self.y += math.sin(angle) * self.speed
        elif is_crossing:
             dist_to_final = math.hypot(self.x - final_target_x, self.y - final_target_y)
             if dist_to_final > self.speed:
                angle = math.atan2(final_target_y - self.y, final_target_x - self.x)
                self.x += math.cos(angle) * self.speed
                self.y += math.sin(angle) * self.speed

    def attack(self, all_enemies): 
        if self.attack_cooldown > 0:
            return
            
        if self.target and self.target.alive:
            target_radius = self.target.get_radius()
            dist = math.hypot(self.x - self.target.x, self.y - self.target.y)
            
            if dist <= self.range + target_radius:

                if self.type == "valkyrie":
                    splash_radius = 45

                    for enemy in all_enemies: 
                        if enemy.alive and enemy.team != self.team:
                            splash_dist = math.hypot(self.x - enemy.x, self.y - enemy.y)

                            if splash_dist <= splash_radius + enemy.get_radius():
                                enemy.hp -= self.damage
                                enemy.hit_timer = 10
                                if enemy.hp <= 0:
                                    enemy.alive = False
                                    
                                    if enemy is self.target:
                                        self.target = None 
                
                elif self.type in ["archer", "Royal giant"]:
                    active_projectiles.append(Projectile(self.x, self.y, self.target, self.damage, 7, self.team))
                    self.attack_cooldown = 60

                else:
                    self.target.hp -= self.damage
                    self.target.hit_timer = 10
                    if self.target.hp <= 0:
                        self.target.alive = False
                        self.target = None
                        
                self.attack_cooldown = 60 

    def update(self, enemies):
        if not self.alive:
            return

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.find_target(enemies)
        
        if self.target and self.target.alive:
            target_radius = self.target.get_radius()
            dist = math.hypot(self.x - self.target.x, self.y - self.target.y)
            if dist > self.range + target_radius:
                self.move(enemies) 
            
            self.attack(enemies)
        else: 
            self.move(enemies)
        
    def draw(self, surface):
        if self.alive:
            color = self.color
            if self.type == "skellies":
                pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius)
                pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius - 2)
            else:
                pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
            
            outline_color = (200, 200, 255) if self.team == "player" else (255, 200, 200)
            pygame.draw.circle(surface, outline_color, (int(self.x), int(self.y)), self.radius, 3)

            if self.type == "valkyrie":
                splash_radius = 45
                s = pygame.Surface((splash_radius * 2, splash_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (DARK_RED[0], DARK_RED[1], DARK_RED[2], 40), (splash_radius, splash_radius), splash_radius)
                pygame.draw.circle(s, (RED[0], RED[1], RED[2], 70), (splash_radius, splash_radius), splash_radius, 2)
                surface.blit(s, (int(self.x) - splash_radius, int(self.y) - splash_radius))

            if self.hit_timer > 0:
                self.hit_timer -= 1
                s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 0, 0, 120), (self.radius, self.radius), self.radius)
                surface.blit(s, (int(self.x) - self.radius, int(self.y) - self.radius))

            self.draw_health_bar(surface)

class Building(GameObject):
    def __init__(self, x, y, building_type, team):
        stats = BUILDING_TYPES[building_type]
        super().__init__(x, y, stats["hp"], team)
        self.type = building_type
        self.color = stats["color"]
        self.width = stats["width"]
        self.height = stats["height"]
        self.damage = stats["damage"]
        self.range = stats["range"]
        self.target = None
        self.attack_cooldown = 0
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)

    def find_target(self, enemies):
        closest_enemy = None
        min_dist = float('inf') 
        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist < min_dist:
                    min_dist = dist
                    closest_enemy = enemy
        
        if closest_enemy and min_dist <= self.range + closest_enemy.get_radius():
             self.target = closest_enemy
        else:
             self.target = None

    def attack(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            return
            
        if self.target and self.target.alive:
            target_radius = self.target.get_radius()
            dist = math.hypot(self.x - self.target.x, self.y - self.target.y)
            if dist <= self.range + target_radius:
                active_projectiles.append(Projectile(self.x, self.y, self.target, self.damage, 8, self.team))
                self.attack_cooldown = 90
            else:
                self.target = None

    def update(self, enemies):
        if not self.alive:
            return
            
        if self.type == "cannon" or self.type == "tesla":
            self.hp -= CANNON_DECAY_PER_FRAME
            if self.hp <= 0:
                self.alive = False
                return
        
        if not self.target or not self.target.alive:
            self.find_target(enemies)
        self.attack()

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)
            pygame.draw.rect(surface, BLACK, self.rect, 3)

            if self.hit_timer > 0:
                self.hit_timer -= 1
                s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                s.fill((255, 0, 0, 120))
                surface.blit(s, self.rect.topleft)

            self.draw_health_bar(surface)

class Tower(GameObject):
    def __init__(self, x, y, tower_type, team):
        stats = TOWER_TYPES[tower_type]
        super().__init__(x, y, stats["hp"], team)
        self.type = tower_type
        self.color = stats["color"]
        self.width = stats["width"]
        self.height = stats["height"]
        self.damage = stats["damage"]
        self.range = stats["range"]
        self.target = None
        self.attack_cooldown = 0
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)

    def find_target(self, enemies):
        closest_enemy = None
        min_dist = float('inf')
        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist < min_dist:
                    min_dist = dist
                    closest_enemy = enemy
        
        if closest_enemy and min_dist <= self.range + closest_enemy.get_radius():
             self.target = closest_enemy
        else:
             self.target = None

    def attack(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            return
            
        if self.target and self.target.alive:
            target_radius = self.target.get_radius()
            dist = math.hypot(self.x - self.target.x, self.y - self.target.y)
            if dist <= self.range + target_radius:
                active_projectiles.append(Projectile(self.x, self.y, self.target, self.damage, 8, self.team))
                self.attack_cooldown = 90
            else:
                self.target = None

    def update(self, enemies):
        global king_tower_active, player_towers, enemy_towers
        if not self.alive:
            return

        if self.type == "king_tower":
            if not king_tower_active[self.team]:
                pt_down = False
                
                if self.team == "player":
                    if (len(player_towers) > 1 and not player_towers[1].alive) or \
                       (len(player_towers) > 2 and not player_towers[2].alive):
                        pt_down = True
                else:
                    if (len(enemy_towers) > 1 and not enemy_towers[1].alive) or \
                       (len(enemy_towers) > 2 and not enemy_towers[2].alive):
                        pt_down = True
                
                if pt_down:
                    king_tower_active[self.team] = True
                else:
                    return 

        if not self.target or not self.target.alive:
            self.find_target(enemies)
        self.attack()

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)
            pygame.draw.rect(surface, BLACK, self.rect, 3)
            
            if self.hit_timer > 0:
                self.hit_timer -= 1
                s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                s.fill((255, 0, 0, 120))
                surface.blit(s, self.rect.topleft)
            
            self.draw_health_bar(surface)

            
            hp_text = small_font.render(f"{int(self.hp)}", True, WHITE)
            text_x = self.x - hp_text.get_width() // 2
            text_y = self.y - hp_text.get_height() // 2
            
            overlay_height = self.height // 3
            overlay = pygame.Surface((self.width, overlay_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            
            
            overlay_rect = overlay.get_rect(center=(self.x, self.y)) 
            surface.blit(overlay, overlay_rect)

            surface.blit(hp_text, (text_x, text_y))


class Spell:
    def __init__(self, x, y, spell_type, team):
        self.x = x
        self.y = y
        self.type = spell_type
        self.team = team
        self.applied = False
        self.lifetime = 30 

        stats = SPELL_TYPES[spell_type]
        self.damage = stats["damage"]
        self.radius = stats["radius"]
        self.color = stats["color"]

    def update(self, all_targets):
        if not self.applied:
            
            for target in all_targets:
                if target.alive and target.team != self.team:
                    dist = math.hypot(self.x - target.x, self.y - target.y)
                    if dist <= self.radius + target.get_radius():
                        target.hp -= self.damage
                        target.hit_timer = 10
                        if target.hp <= 0:
                            target.alive = False
            
            self.applied = True
        
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            alpha = int((self.lifetime / 30) * 180) 
            
            effect_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            effect_surface.fill((0, 0, 0, 0))
            
            pygame.draw.circle(effect_surface, self.color + (alpha,), (self.radius, self.radius), self.radius)
            
            surface.blit(effect_surface, (self.x - self.radius, self.y - self.radius))

class Bomb:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.fuse_timer = 3 * 60 
        self.explosion_radius = 100
        self.damage = 400
        self.exploded = False
        self.lifetime = 0 

    def update(self, all_targets):
        if self.exploded:
            self.lifetime += 1
            return

        self.fuse_timer -= 1

        if self.fuse_timer <= 0:
            self.explode(all_targets)
            self.exploded = True

    def explode(self, all_targets):
        for target in all_targets:
            if target.alive and target.team != self.team:
                dist = math.hypot(self.x - target.x, self.y - target.y)
                if dist <= self.explosion_radius + target.get_radius():
                    target.hp -= self.damage
                    target.hit_timer = 10
                    if target.hp <= 0:
                        target.alive = False

    def draw(self, surface):
        if not self.exploded:
            color = DARK_GRAY
            radius = 15
            
            fuse_ratio = self.fuse_timer / (3 * 60)
            
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), radius)
            pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), radius, 2)
            
            indicator_radius = radius + 5
            
            arc_angle = 360 * fuse_ratio
            
            if self.fuse_timer % 30 < 15:
                 pygame.draw.arc(surface, RED, 
                                pygame.Rect(self.x - indicator_radius, self.y - indicator_radius, indicator_radius * 2, indicator_radius * 2), 
                                math.radians(90), math.radians(90 + arc_angle), 3)

        elif self.exploded and self.lifetime < 30: 
            alpha = int(max(0, (30 - self.lifetime) / 30) * 200)
            effect_surface = pygame.Surface((self.explosion_radius * 2, self.explosion_radius * 2), pygame.SRCALPHA)
            effect_surface.fill((0, 0, 0, 0))
            pygame.draw.circle(effect_surface, DARK_GRAY + (alpha,), (self.explosion_radius, self.explosion_radius), self.explosion_radius)
            surface.blit(effect_surface, (self.x - self.explosion_radius, self.y - self.explosion_radius))

class Projectile:
    def __init__(self, x, y, target, damage, speed, team):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = speed
        self.team = team
        self.alive = True

    def update(self):
        if not self.alive:
            return
            
        if not self.target or not self.target.alive:
            self.alive = False
            return

        target_x, target_y = self.target.x, self.target.y
        angle = math.atan2(target_y - self.y, target_x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed

        dist = math.hypot(self.x - target_x, self.y - target_y)
        if dist < self.target.get_radius():
            self.target.hp -= self.damage
            self.target.hit_timer = 10
            if self.target.hp <= 0:
                self.target.alive = False
            self.alive = False

    def draw(self, surface):
        if self.alive:
            pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), 5)

            
def draw_card_visual(surface, rect, card_name, is_selected=False):
    
    cost = -1
    draw_type = 'troop'
    color = BLACK
    stats = {}
    
    if card_name in TROOP_TYPES:
        stats = TROOP_TYPES[card_name]
        cost = stats["cost"]
        size = stats["radius"] * 1.5
        color = stats["color"]
        draw_type = 'troop'
    elif card_name in BUILDING_TYPES:
        stats = BUILDING_TYPES[card_name]
        cost = stats["cost"]
        size = stats["width"] * 1.5
        color = stats["color"]
        draw_type = 'building'
    elif card_name in SPELL_TYPES:
        stats = SPELL_TYPES[card_name]
        cost = stats["cost"]
        color = stats["color"]
        draw_type = 'spell'
    else:
        return

    card_bg_color = WHITE if not is_selected else LIGHT_BLUE
    pygame.draw.rect(surface, card_bg_color, rect, border_radius=10)
    
    if is_selected:
        pygame.draw.rect(surface, GOLD, rect, 4, border_radius=10)
    else:
        pygame.draw.rect(surface, BLACK, rect, 2, border_radius=10)
    
    card_text = small_font.render(card_name.capitalize(), True, BLACK)
    surface.blit(card_text, (rect.centerx - card_text.get_width() // 2, rect.top + 5))

    center_x, center_y = rect.centerx, rect.centery + 10
    
    if draw_type == 'troop':
        if card_name == "skellies":
             pygame.draw.circle(surface, color, (center_x, center_y), size)
             pygame.draw.circle(surface, color, (center_x - size*0.5, center_y + size*0.5), size)
             pygame.draw.circle(surface, color, (center_x + size*0.5, center_y + size*0.5), size)
        else:
            pygame.draw.circle(surface, color, (center_x, center_y), size)
    elif draw_type == 'building':
        vis_rect_size = size
        vis_rect = pygame.Rect(center_x - vis_rect_size // 2, center_y - vis_rect_size // 2, vis_rect_size, vis_rect_size)
        pygame.draw.rect(surface, color, vis_rect)
    elif draw_type == 'spell':
        pygame.draw.rect(surface, color, (center_x - 15, center_y - 15, 30, 30), border_radius=5)
        pygame.draw.rect(surface, BLACK, (center_x - 15, center_y - 15, 30, 30), 2, border_radius=5)


    stat_bar_width = rect.width - 20
    stat_bar_height = 6
    stat_y_start = rect.bottom - 40
    stat_label_font = pygame.font.SysFont(None, 14)
    
    if draw_type == 'troop':
        MAX_HP = 1300.0 
        MAX_DMG = 300.0  
        
        hp = stats["hp"]
        damage = stats["damage"]
        
        hp_fill = (hp / MAX_HP) * stat_bar_width
        dmg_fill = (damage / MAX_DMG) * stat_bar_width
        
        hp_label = stat_label_font.render("HP", True, WHITE)
        hp_label_x = rect.left + 10 + 2
        hp_rect_bg = pygame.Rect(rect.left + 10, stat_y_start, stat_bar_width, stat_bar_height)
        hp_rect_fill = pygame.Rect(rect.left + 10, stat_y_start, hp_fill, stat_bar_height)
        
        pygame.draw.rect(surface, DARK_GRAY, hp_rect_bg, border_radius=2)
        pygame.draw.rect(surface, GREEN, hp_rect_fill, border_radius=2)
        surface.blit(hp_label, (hp_label_x, stat_y_start + stat_bar_height // 2 - hp_label.get_height() // 2))
        
        dmg_y = stat_y_start + stat_bar_height + 5
        dmg_label = stat_label_font.render("DMG", True, WHITE)
        dmg_label_x = rect.left + 10 + 2
        dmg_rect_bg = pygame.Rect(rect.left + 10, dmg_y, stat_bar_width, stat_bar_height)
        dmg_rect_fill = pygame.Rect(rect.left + 10, dmg_y, dmg_fill, stat_bar_height)
        
        pygame.draw.rect(surface, DARK_GRAY, dmg_rect_bg, border_radius=2)
        pygame.draw.rect(surface, RED, dmg_rect_fill, border_radius=2)
        surface.blit(dmg_label, (dmg_label_x, dmg_y + stat_bar_height // 2 - dmg_label.get_height() // 2))
        
    elif draw_type == 'building':
        hp = stats["hp"]
        damage = stats["damage"]
        hp_text = stat_label_font.render(f"HP: {hp}", True, BLACK)
        dmg_text = stat_label_font.render(f"DMG: {damage}", True, BLACK)
        surface.blit(hp_text, (rect.left + 10, stat_y_start))
        surface.blit(dmg_text, (rect.left + 10, stat_y_start + stat_bar_height + 5))
        
    elif draw_type == 'spell':
        damage = stats["damage"]
        dmg_text = stat_label_font.render(f"Damage: {damage}", True, BLACK)
        surface.blit(dmg_text, (rect.centerx - dmg_text.get_width() // 2, rect.bottom - 30))

    cost_text = font.render(str(cost), True, WHITE)
    pygame.draw.circle(surface, BLACK, (rect.left + 15, rect.top + 15), 12)
    pygame.draw.circle(surface, (255, 0, 255), (rect.left + 15, rect.top + 15), 10)
    surface.blit(cost_text, (rect.left + 15 - cost_text.get_width()//2, rect.top + 15 - cost_text.get_height()//2))


def setup_game():
    global player_troops, enemy_troops, player_towers, enemy_towers, active_spells, active_bombs, player_elixir, bot_elixir, bot_action_cooldown
    global player_hand, player_draw_pile, player_discard_pile, game_over, winner, bot_hand, bot_draw_pile, bot_discard_pile, player_full_deck, bot_full_deck, game_timer, king_tower_active, player_selected_deck
    global active_projectiles
    
    player_troops.clear()
    enemy_troops.clear()
    player_towers.clear()
    enemy_towers.clear()
    active_spells.clear()
    active_bombs.clear()
    active_projectiles.clear()

    
    player_towers.append(Tower(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, "king_tower", "player"))
    player_towers.append(Tower(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 250, "princess_tower", "player"))
    player_towers.append(Tower(SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - 250, "princess_tower", "player"))
    
    enemy_towers.append(Tower(SCREEN_WIDTH // 2, 100, "king_tower", "enemy"))
    enemy_towers.append(Tower(SCREEN_WIDTH // 4, 250, "princess_tower", "enemy"))
    enemy_towers.append(Tower(SCREEN_WIDTH * 3 // 4, 250, "princess_tower", "enemy"))
    
    player_elixir = 5.0
    bot_elixir = 5.0
    bot_action_cooldown = 0
    game_timer = GAME_TIME_LIMIT
    
    
    if not player_selected_deck:
        player_selected_deck = all_available_cards[:8] 
        
    player_full_deck = player_selected_deck
    
    for deck, hand, draw_pile, discard_pile in [
        (player_full_deck, player_hand, player_draw_pile, player_discard_pile),
        (bot_full_deck, bot_hand, bot_draw_pile, bot_discard_pile)
    ]:
        hand.clear()
        draw_pile.clear()
        discard_pile.clear()
        
        if deck:
            
            draw_pile.extend(deck)
            random.shuffle(draw_pile)
            for _ in range(4):
                if draw_pile:
                    hand.append(draw_pile.pop())

    game_over = False
    winner = None
    king_tower_active = {"player": False, "enemy": False}

def draw_arena():
    screen.fill((108, 168, 64))
    
    
    pygame.draw.rect(screen, (50, 150, 255), (0, SCREEN_HEIGHT // 2 - 20, SCREEN_WIDTH, 40))
    
    
    pygame.draw.rect(screen, BROWN, (SCREEN_WIDTH // 4 - 30, SCREEN_HEIGHT // 2 - 30, 60, 60))
    pygame.draw.rect(screen, BROWN, (SCREEN_WIDTH * 3 // 4 - 30, SCREEN_HEIGHT // 2 - 30, 60, 60))
    
    
    pygame.draw.line(screen, (255, 255, 255, 100), (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)


def draw_ui():
    global player_elixir, max_elixir, player_hand, selected_card_index, game_timer
    
    
    minutes = int(game_timer // 60)
    seconds = int(game_timer % 60)
    timer_text_str = f"{minutes:02}:{seconds:02}"
    timer_text = font.render(timer_text_str, True, WHITE)
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - 40, 10, 80, 35), border_radius=5)
    screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 15))

    
    elixir_bar_width = 300
    elixir_fill = (player_elixir / max_elixir) * elixir_bar_width
    pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH // 2 - elixir_bar_width // 2 - 2, SCREEN_HEIGHT - 172, elixir_bar_width + 4, 24), border_radius=5)
    pygame.draw.rect(screen, (255, 0, 255), (SCREEN_WIDTH // 2 - elixir_bar_width // 2, SCREEN_HEIGHT - 170, elixir_fill, 20), border_radius=5)
    elixir_text = font.render(f"{int(player_elixir)} / {int(max_elixir)}", True, WHITE)
    screen.blit(elixir_text, (SCREEN_WIDTH // 2 - elixir_text.get_width() // 2, SCREEN_HEIGHT - 170))

    
    hand_start_x = (SCREEN_WIDTH - (4 * CARD_WIDTH + 3 * CARD_MARGIN)) // 2
    
    for i, card_name in enumerate(player_hand):
        card_rect = pygame.Rect(hand_start_x + i * (CARD_WIDTH + CARD_MARGIN), SCREEN_HEIGHT - CARD_HEIGHT - CARD_MARGIN, CARD_WIDTH, CARD_HEIGHT)
        
        cost = -1
        if card_name in TROOP_TYPES:
            cost = TROOP_TYPES[card_name]["cost"]
        elif card_name in BUILDING_TYPES:
            cost = BUILDING_TYPES[card_name]["cost"]
        elif card_name in SPELL_TYPES:
            cost = SPELL_TYPES[card_name]["cost"]
        else:
            continue

        is_affordable = player_elixir >= cost
        
        card_bg_color = WHITE if is_affordable else GREY
        pygame.draw.rect(screen, card_bg_color, card_rect, border_radius=10)
        
        is_selected = (i == selected_card_index)
        draw_card_visual(screen, card_rect, card_name, is_selected)
        
        if i == selected_card_index:
            pygame.draw.rect(screen, GOLD, card_rect, 4, border_radius=10)


def draw_menu():
    screen.fill(LIGHT_BLUE)
    title_text = large_font.render("Dot War", True, BLACK) 
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//4))
    
    play_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2, 300, 70)
    deck_select_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 90, 300, 70)
    
    play_button = Button(play_button_rect.x, play_button_rect.y, play_button_rect.width, play_button_rect.height, "Play", GREEN, WHITE)
    deck_select_button = Button(deck_select_button_rect.x, deck_select_button_rect.y, deck_select_button_rect.width, deck_select_button_rect.height, "Select Deck", GOLD, BLACK)
    
    play_button.draw(screen)
    deck_select_button.draw(screen)
    return play_button, deck_select_button

def get_deck_select_rects():
    global all_available_cards, player_selected_deck, deck_scroll_offset

    available_area_rect = pygame.Rect(0, 50, SCREEN_WIDTH, SCROLL_AREA_HEIGHT)

    num_cards = len(all_available_cards)
    num_rows = math.ceil(num_cards / DECK_GRID_COLS)
    content_height = num_rows * (DECK_CARD_HEIGHT + DECK_CARD_MARGIN) + DECK_CARD_MARGIN
    
    max_scroll = max(0, content_height - SCROLL_AREA_HEIGHT)
    deck_scroll_offset = max(-max_scroll, min(0, deck_scroll_offset)) 
    
    start_x = (SCREEN_WIDTH - (DECK_GRID_COLS * DECK_CARD_WIDTH + (DECK_GRID_COLS - 1) * DECK_CARD_MARGIN)) // 2
    
    transformed_card_rects = {}

    for i, card_name in enumerate(all_available_cards):
        row = i // DECK_GRID_COLS
        col = i % DECK_GRID_COLS
        
        x = start_x + col * (DECK_CARD_WIDTH + DECK_CARD_MARGIN)
        y = DECK_CARD_MARGIN + row * (DECK_CARD_HEIGHT + DECK_CARD_MARGIN)
        
        card_rect_unscrolled = pygame.Rect(x, y, DECK_CARD_WIDTH, DECK_CARD_HEIGHT)
        
        transformed_rect = card_rect_unscrolled.copy()
        transformed_rect.y += available_area_rect.top + int(deck_scroll_offset) 
        transformed_card_rects[card_name] = transformed_rect
    
    deck_area_y = SCREEN_HEIGHT - (2 * CARD_HEIGHT + CARD_MARGIN) - 90
    deck_area_x = (SCREEN_WIDTH - (4 * (CARD_WIDTH + CARD_MARGIN) - CARD_MARGIN)) // 2

    button_width = 300
    button_height = 70
    
    can_start = len(player_selected_deck) == 8
    
    start_game_rect = pygame.Rect(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT - button_height - 10, button_width, button_height)
    start_game_button = Button(start_game_rect.x, start_game_rect.y, button_width, button_height, 
                               "Start Battle" if can_start else f"Need {8 - len(player_selected_deck)} More Cards", GREEN if can_start else GREY, WHITE)

    
    return transformed_card_rects, start_game_button, deck_area_x, deck_area_y, available_area_rect, content_height, max_scroll


def draw_deck_select():
    global deck_scroll_offset
    
    screen.fill(GREY)
    
    title_text = font.render(f"Select Your Deck (Cards: {len(player_selected_deck)}/8)", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 10))

    
    card_rects, start_game_button, deck_area_x, deck_area_y, available_area_rect, content_height, max_scroll = get_deck_select_rects() 
    
    pygame.draw.rect(screen, (220, 220, 220), available_area_rect)

    scroll_surface = pygame.Surface((SCREEN_WIDTH, content_height), pygame.SRCALPHA)
    scroll_surface.fill((0, 0, 0, 0)) 
    
    
    start_x = (SCREEN_WIDTH - (DECK_GRID_COLS * DECK_CARD_WIDTH + (DECK_GRID_COLS - 1) * DECK_CARD_MARGIN)) // 2
    
    for i, card_name in enumerate(all_available_cards):
        row = i // DECK_GRID_COLS
        col = i % DECK_GRID_COLS
        
        x = start_x + col * (DECK_CARD_WIDTH + DECK_CARD_MARGIN)
        y = DECK_CARD_MARGIN + row * (DECK_CARD_HEIGHT + DECK_CARD_MARGIN)
        
        card_rect = pygame.Rect(x, y, DECK_CARD_WIDTH, DECK_CARD_HEIGHT)
        
        is_selected = card_name in player_selected_deck
        draw_card_visual(scroll_surface, card_rect, card_name, is_selected)
        
    old_clip = screen.get_clip()
    screen.set_clip(available_area_rect)
    
    screen.blit(scroll_surface, (0, available_area_rect.top + int(deck_scroll_offset)))
    
    screen.set_clip(old_clip) 
    
    pygame.draw.rect(screen, BLACK, available_area_rect, 2) 

    deck_title = font.render("Your Deck:", True, BLACK)
    screen.blit(deck_title, (deck_area_x, deck_area_y - 30))

    for i in range(8):
        row = i // 4
        col = i % 4

        x = deck_area_x + col * (CARD_WIDTH + CARD_MARGIN)
        y = deck_area_y + row * (CARD_HEIGHT + CARD_MARGIN)
        
        deck_slot_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        
        pygame.draw.rect(screen, BLACK, deck_slot_rect, 2, border_radius=10)
        
        if i < len(player_selected_deck):
            card_name = player_selected_deck[i]
            temp_card_rect = pygame.Rect(deck_slot_rect.x, deck_slot_rect.y, CARD_WIDTH, CARD_HEIGHT)
            draw_card_visual(screen, temp_card_rect, card_name, is_selected=True)
            
            x_pos, y_pos = deck_slot_rect.right - 10, deck_slot_rect.top + 10
            pygame.draw.circle(screen, RED, (x_pos, y_pos), 10)
            x_text = small_font.render("X", True, WHITE)
            screen.blit(x_text, (x_pos - x_text.get_width()//2, y_pos - x_text.get_height()//2))

    start_game_button.draw(screen)

    return card_rects, start_game_button, deck_area_x, deck_area_y, available_area_rect, max_scroll

def draw_game_over(winner_name):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0,0))
    
    win_text = large_font.render(f"{winner_name} Wins!", True, GOLD if winner_name == "Player" else RED)
    screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, SCREEN_HEIGHT//2 - win_text.get_height()//2 - 100))
    
    button_width = 200
    button_height = 60
    
    play_again_rect = pygame.Rect(SCREEN_WIDTH//2 - button_width - 20, SCREEN_HEIGHT//2 + 50, button_width, button_height)
    menu_rect = pygame.Rect(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT//2 + 50, button_width, button_height)
    
    play_again_button = Button(play_again_rect.x, play_again_rect.y, button_width, button_height, "Play Again", GREEN, WHITE)
    menu_button = Button(menu_rect.x, menu_rect.y, button_width, button_height, "Menu", GREY, BLACK)
    
    play_again_button.draw(screen)
    menu_button.draw(screen)
    
    return play_again_button, menu_button


def bot_ai():
    global bot_elixir, bot_action_cooldown, enemy_troops, bot_hand, bot_draw_pile, bot_discard_pile, player_troops, active_spells

    if bot_action_cooldown > 0:
        bot_action_cooldown -= 1
        return

    playable_cards = []
    for card_name in bot_hand:
        cost = -1
        if card_name in TROOP_TYPES:
            cost = TROOP_TYPES[card_name]["cost"]
        elif card_name in BUILDING_TYPES:
            cost = BUILDING_TYPES[card_name]["cost"]
        elif card_name in SPELL_TYPES:
            cost = SPELL_TYPES[card_name]["cost"]

        if cost != -1 and bot_elixir >= cost:
            playable_cards.append(card_name)

    if not playable_cards:
        return

    player_building_targeters = [t for t in player_troops if isinstance(t, Troop) and t.is_building_targeter()]
    is_giant_present = len(player_building_targeters) > 0
    
    player_deployables = [u for u in player_troops if isinstance(u, (Troop, Building))]
    can_spell_value = 0
    spell_target_pos = None

    if player_deployables:
        
        deployable_targets = [u for u in player_deployables if u.y > SCREEN_HEIGHT // 2]
        
        if deployable_targets:
            
            cluster_targets = sorted(deployable_targets, key=lambda t: t.y, reverse=True)[:3] 
            if len(cluster_targets) >= 3:
                can_spell_value = 3
                spell_target_pos = (sum(t.x for t in cluster_targets)//len(cluster_targets), sum(t.y for t in cluster_targets)//len(cluster_targets))

    preferred_card = None
    
    
    bot_building_x = 0
    bot_building_y = 0
    
    if "cannon" in playable_cards:
        bot_building_x = SCREEN_WIDTH // 2 
        bot_building_y = random.randint(300, 350)
        
        is_too_close_bot = False
        
        for unit in enemy_troops:
             if isinstance(unit, Building):
                 dist = math.hypot(bot_building_x - unit.x, bot_building_y - unit.y)
                 if dist < MIN_CANNON_SEPARATION:
                     is_too_close_bot = True
                     break
        
        
        if is_giant_present and not is_too_close_bot:
            preferred_card = "cannon"
        
    elif "tesla" in playable_cards:
        bot_building_x = random.randint(SCREEN_WIDTH // 4 + 50, SCREEN_WIDTH * 3 // 4 - 50)
        bot_building_y = random.randint(300, 350)

        is_too_close_bot = False
        for unit in enemy_troops:
             if isinstance(unit, Building):
                 dist = math.hypot(bot_building_x - unit.x, bot_building_y - unit.y)
                 if dist < MIN_CANNON_SEPARATION:
                     is_too_close_bot = True
                     break
        
        if not is_too_close_bot:
            preferred_card = "tesla"

    
    if not preferred_card and can_spell_value >= 3:
        if "fireball" in playable_cards:
            preferred_card = "fireball"
        elif "arrows" in playable_cards:
            preferred_card = "arrows"

    
    if not preferred_card:
        
        troop_and_building_cards = [c for c in playable_cards if c not in SPELL_TYPES.keys()]
        if troop_and_building_cards:
            preferred_card = random.choice(troop_and_building_cards)
        elif playable_cards:
             preferred_card = random.choice(playable_cards) 

    
    if not preferred_card:
        return

    card_name = preferred_card
    
    cost = -1
    is_troop, is_building, is_spell = False, False, False

    if card_name in TROOP_TYPES:
        cost = TROOP_TYPES[card_name]["cost"]
        is_troop = True
    elif card_name in BUILDING_TYPES:
        cost = BUILDING_TYPES[card_name]["cost"]
        is_building = True
    elif card_name in SPELL_TYPES:
        cost = SPELL_TYPES[card_name]["cost"]
        is_spell = True
    else:
        return 

    
    if bot_elixir < cost:
        return
        
    bot_elixir -= cost
    
    if is_troop:
        x = random.choice([SCREEN_WIDTH // 4, SCREEN_WIDTH * 3 // 4])
        
        y = random.randint(50, SCREEN_HEIGHT // 2 - 100) 
        
        if card_name == "skellies":
            enemy_troops.append(Troop(x, y - 15, card_name, "enemy"))
            enemy_troops.append(Troop(x - 15, y + 15, card_name, "enemy"))
            enemy_troops.append(Troop(x + 15, y + 15, card_name, "enemy"))
        
        elif card_name == "goblins":
            enemy_troops.append(Troop(x, y - 10, card_name, "enemy")) 
            enemy_troops.append(Troop(x - 15, y + 5, card_name, "enemy"))
            enemy_troops.append(Troop(x + 15, y + 5, card_name, "enemy"))
            enemy_troops.append(Troop(x, y + 20, card_name, "enemy")) 
        
        else:
            enemy_troops.append(Troop(x, y, card_name, "enemy"))
            
    elif is_building:
        
        if card_name == "cannon" and preferred_card == "cannon":
            x, y = bot_building_x, bot_building_y
        elif card_name == "tesla" and preferred_card == "tesla":
            x, y = bot_building_x, bot_building_y
        else:
            
            x = random.randint(SCREEN_WIDTH // 4 + 50, SCREEN_WIDTH * 3 // 4 - 50)
            y = random.randint(300, 350)
            
        enemy_troops.append(Building(x, y, card_name, "enemy"))
        
    elif is_spell:
        
        if spell_target_pos:
            x, y = spell_target_pos
        else:
            
            x = random.randint(SCREEN_WIDTH // 4, SCREEN_WIDTH * 3 // 4)
            y = random.randint(SCREEN_HEIGHT // 2 + 100, SCREEN_HEIGHT - 200)

        active_spells.append(Spell(x, y, card_name, "enemy"))
    
    
    played_card = bot_hand.pop(bot_hand.index(card_name))
    bot_discard_pile.append(played_card)

    if not bot_draw_pile:
        bot_draw_pile.extend(bot_discard_pile)
        random.shuffle(bot_draw_pile)
        bot_discard_pile.clear()

    if bot_draw_pile:
        bot_hand.append(bot_draw_pile.pop())

    bot_action_cooldown = random.randint(90, 180)


def check_game_over(timer_expired=False):
    global game_over, winner, game_state, player_towers, enemy_towers
    
    player_king_down = not player_towers[0].alive
    enemy_king_down = not enemy_towers[0].alive
    
    
    if player_king_down and not game_over: 
        game_over = True
        winner = "Enemy"
        game_state = GAME_OVER
    elif enemy_king_down and not game_over:
        game_over = True
        winner = "Player"
        game_state = GAME_OVER
        
    
    elif timer_expired and not game_over:
        
        player_tower_count = sum(1 for t in player_towers if t.alive)
        enemy_tower_count = sum(1 for t in enemy_towers if t.alive)
        
        
        if player_tower_count > enemy_tower_count:
            winner = "Player"
        elif enemy_tower_count > player_tower_count:
            winner = "Enemy"
        else:
            
            player_hp = sum(t.hp for t in player_towers if t.alive)
            enemy_hp = sum(t.hp for t in enemy_towers if t.alive)

            if player_hp > enemy_hp:
                winner = "Player"
            elif enemy_hp > player_hp:
                winner = "Enemy"
            else:
                winner = "Draw"
            
        game_over = True
        game_state = GAME_OVER

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            mouse_pos = (mouse_x, mouse_y)

            if game_state == MENU:
                play_button, deck_select_button = draw_menu() 
                if play_button.is_clicked(mouse_pos):
                    if len(player_selected_deck) == 8:
                        setup_game()
                        game_state = PLAYING
                    else:
                        game_state = SELECT_DECK 
                elif deck_select_button.is_clicked(mouse_pos):
                    game_state = SELECT_DECK
                continue

            elif game_state == SELECT_DECK:
                
                card_rects, start_game_button, deck_area_x, deck_area_y, available_area_rect, content_height, max_scroll = get_deck_select_rects() 
                
                
                card_clicked = False
                if available_area_rect.collidepoint(mouse_pos):
                    for card_name, rect in card_rects.items():
                        if rect.collidepoint(mouse_pos):
                            if card_name in player_selected_deck:
                                player_selected_deck.remove(card_name)
                            elif len(player_selected_deck) < 8:
                                player_selected_deck.append(card_name)
                            card_clicked = True
                            break
                    
                    if not card_clicked:
                        is_scrolling_deck = True
                        last_mouse_y = mouse_y

                if not card_clicked:
                    
                    for i in range(len(player_selected_deck)):
                        row = i // 4
                        col = i % 4
                        x = deck_area_x + col * (CARD_WIDTH + CARD_MARGIN)
                        y = deck_area_y + row * (CARD_HEIGHT + CARD_MARGIN)
                        deck_slot_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                        
                        x_pos, y_pos = deck_slot_rect.right - 10, deck_slot_rect.top + 10
                        if math.hypot(mouse_x - x_pos, mouse_y - y_pos) < 10:
                            player_selected_deck.pop(i)
                            break

                if start_game_button.is_clicked(mouse_pos) and len(player_selected_deck) == 8:
                    setup_game()
                    game_state = PLAYING
                
                continue


            elif game_state == GAME_OVER:
                play_again_button, menu_button = draw_game_over(winner) 
                if play_again_button.is_clicked(mouse_pos):
                    setup_game()
                    game_state = PLAYING
                elif menu_button.is_clicked(mouse_pos):
                    
                    player_selected_deck.clear() 
                    game_state = MENU
                continue

            elif game_state == PLAYING:
                clicked_card = False
                hand_start_x = (SCREEN_WIDTH - (4 * CARD_WIDTH + 3 * CARD_MARGIN)) // 2
                
                
                for i in range(len(player_hand)):
                    card_rect = pygame.Rect(hand_start_x + i * (CARD_WIDTH + CARD_MARGIN), SCREEN_HEIGHT - CARD_HEIGHT - CARD_MARGIN, CARD_WIDTH, CARD_HEIGHT)
                    if card_rect.collidepoint(mouse_x, mouse_y):
                        if selected_card_index == i:
                            selected_card_index = -1 
                        else:
                            selected_card_index = i 
                        clicked_card = True
                        break
                
                
                if not clicked_card and selected_card_index != -1:
                    card_name = player_hand[selected_card_index]
                    
                    is_spell, is_troop, is_building = False, False, False
                    cost = -1

                    if card_name in SPELL_TYPES:
                        cost = SPELL_TYPES[card_name]["cost"]
                        is_spell = True
                    elif card_name in TROOP_TYPES:
                        cost = TROOP_TYPES[card_name]["cost"]
                        is_troop = True
                    elif card_name in BUILDING_TYPES:
                        cost = BUILDING_TYPES[card_name]["cost"]
                        is_building = True

                    
                    is_in_friendly_half = mouse_y >= SCREEN_HEIGHT // 2
                    is_valid_placement_zone = is_spell or is_in_friendly_half
                    
                    
                    can_place_near_broken = False
                    pt1 = player_towers[1] if len(player_towers) > 1 else None
                    pt2 = player_towers[2] if len(player_towers) > 2 else None
                    
                    if pt1 and not pt1.alive:
                        if math.hypot(mouse_x - pt1.x, mouse_y - pt1.y) < 100: 
                            can_place_near_broken = True

                    if pt2 and not pt2.alive:
                        if math.hypot(mouse_x - pt2.x, mouse_y - pt2.y) < 100:
                            can_place_near_broken = True
                            
                    
                    is_valid_placement = is_spell or is_in_friendly_half or can_place_near_broken

                    if cost != -1 and player_elixir >= cost and is_valid_placement:
                        
                        if is_building:
                            is_too_close = False
                            
                            for unit in player_troops:
                                if isinstance(unit, Building): 
                                    dist = math.hypot(mouse_x - unit.x, mouse_y - unit.y)
                                    if dist < MIN_CANNON_SEPARATION: 
                                        is_too_close = True
                                        break
                            if is_too_close:
                                selected_card_index = -1
                                continue
                        
                        player_elixir -= cost
                        
                        if is_spell:
                            active_spells.append(Spell(mouse_x, mouse_y, card_name, "player"))
                        elif is_troop:
                            if card_name == "skellies":
                                player_troops.append(Troop(mouse_x, mouse_y - 15, card_name, "player"))
                                player_troops.append(Troop(mouse_x - 15, mouse_y + 15, card_name, "player"))
                                player_troops.append(Troop(mouse_x + 15, mouse_y + 15, card_name, "player"))
                            
                            elif card_name == "goblins":
                                player_troops.append(Troop(mouse_x, mouse_y - 10, card_name, "player")) 
                                player_troops.append(Troop(mouse_x - 15, mouse_y + 5, card_name, "player"))
                                player_troops.append(Troop(mouse_x + 15, mouse_y + 5, card_name, "player"))
                                player_troops.append(Troop(mouse_x, mouse_y + 20, card_name, "player")) 
                            
                            else:
                                player_troops.append(Troop(mouse_x, mouse_y, card_name, "player"))
                        
                        elif is_building:
                            player_troops.append(Building(mouse_x, mouse_y, card_name, "player"))

                        
                        played_card = player_hand.pop(selected_card_index)
                        player_discard_pile.append(played_card)

                        if not player_draw_pile:
                            player_draw_pile.extend(player_discard_pile)
                            random.shuffle(player_draw_pile)
                            player_discard_pile.clear()

                        if player_draw_pile:
                            player_hand.append(player_draw_pile.pop())
                        
                        selected_card_index = -1
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if game_state == SELECT_DECK:
                is_scrolling_deck = False

        elif event.type == pygame.MOUSEMOTION:
            if game_state == SELECT_DECK and is_scrolling_deck:
                mouse_x, mouse_y = event.pos
                dy = mouse_y - last_mouse_y
                deck_scroll_offset += dy
                last_mouse_y = mouse_y
                
                num_cards = len(all_available_cards)
                num_rows = math.ceil(num_cards / DECK_GRID_COLS)
                content_height = num_rows * (DECK_CARD_HEIGHT + DECK_CARD_MARGIN) + DECK_CARD_MARGIN
                max_scroll = max(0, content_height - SCROLL_AREA_HEIGHT)
                deck_scroll_offset = max(-max_scroll, min(0, deck_scroll_offset))


    
    if game_state == PLAYING:
        if not game_over:
            
            
            if player_elixir < max_elixir:
                player_elixir += elixir_rate
            if bot_elixir < max_elixir:
                bot_elixir += elixir_rate
                
            
            game_timer -= 1 / 60
            if game_timer <= 0:
                game_timer = 0
                check_game_over(timer_expired=True)

            
            bot_ai()

            for p in active_projectiles:
                p.update()

            
            player_deployables = [u for u in player_troops if isinstance(u, (Troop, Building))]
            enemy_deployables = [u for u in enemy_troops if isinstance(u, (Troop, Building))]
            
            all_player_units = player_deployables + player_towers
            all_enemy_units = enemy_deployables + enemy_towers
            
            
            for spell in active_spells:
                targets = all_enemy_units if spell.team == "player" else all_player_units
                spell.update(targets)
            
            for bomb in active_bombs:
                targets = all_enemy_units if bomb.team == "player" else all_player_units
                bomb.update(targets)

            
            for unit in player_troops:
                unit.update(all_enemy_units) 
            for unit in enemy_troops:
                unit.update(all_player_units) 

            
            for tower in player_towers:
                
                tower.update(enemy_deployables) 
            for tower in enemy_towers:
                
                tower.update(player_deployables)

            
            
            for unit in player_troops + enemy_troops:
                if unit.alive and unit.hp <= 0:
                    unit.alive = False 
                    if isinstance(unit, Troop) and unit.type == "skeleton giant":
                        
                        active_bombs.append(Bomb(unit.x, unit.y, unit.team))

            player_troops = [t for t in player_troops if t.alive]
            enemy_troops = [t for t in enemy_troops if t.alive]
            active_spells = [s for s in active_spells if s.lifetime > 0]
            active_bombs = [b for b in active_bombs if b.lifetime < 30] 
            active_projectiles = [p for p in active_projectiles if p.alive]

            check_game_over()

        
        draw_arena()
        
        for spell in active_spells:
            spell.draw(screen)
        
        for bomb in active_bombs:
            bomb.draw(screen)

        for p in active_projectiles:
            p.draw(screen)

        
        all_units = player_troops + enemy_troops + player_towers + enemy_towers
        for unit in sorted(all_units, key=lambda u: u.y): 
            unit.draw(screen)
            
        draw_ui()

    elif game_state == MENU:
        draw_menu()
    
    elif game_state == SELECT_DECK:
        draw_deck_select()

    elif game_state == GAME_OVER:
        
        draw_arena()
        all_units = player_troops + enemy_troops + player_towers + enemy_towers
        for unit in sorted(all_units, key=lambda u: u.y):
            unit.draw(screen)
        
        for p in active_projectiles:
            p.draw(screen)
            
        draw_ui()
        
        draw_game_over(winner)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()