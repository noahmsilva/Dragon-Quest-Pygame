import pygame, random

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Dragon Quest Model')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit() 
    
    
class Game:
    # An object in this class represents a complete game.
    
    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object
    
        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')
    
        self.FPS = 144
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True  
        self.encounter = False
        
        # === game specific objects
        self.overworld_character = Character(self.surface)
        hero_chosen = self.overworld_character.chosen
        self.hero = Unit(hero_chosen)
        self.game_map = Map(self.surface)
        self.battle = Battle(self.surface)
        self.list_of_enemies = ["slime","ghost","jaskirat"]
        
    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.
    
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
                        
            if self.continue_game:
                self.draw()
                self.update()
                self.decide_continue()
            else:
                self.draw_end_screen()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second         
    
    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)    
            if event.type == pygame.KEYUP:
                self.handle_keyup(event)             
    
    def handle_keydown(self, event):
        
        if event.key == pygame.K_UP:
            self.overworld_character.velocity[1] = -1
        if event.key == pygame.K_DOWN:
            self.overworld_character.velocity[1] = 1
        if event.key == pygame.K_RIGHT:
            self.overworld_character.velocity[0] = 1
        if event.key == pygame.K_LEFT:
            self.overworld_character.velocity[0] = -1        
            
    def handle_keyup(self, event):
        # Hand the keyup user event, changing the velocity of the character
        # object depending on which keys are released.
        # - self is the Game that modifies the Paintbrush object.
        # - event is a key being released
        
        if event.key == pygame.K_UP:
            self.overworld_character.velocity[1] = 0
        if event.key == pygame.K_DOWN:
            self.overworld_character.velocity[1] = 0
        if event.key == pygame.K_RIGHT:
            self.overworld_character.velocity[0] = 0
        if event.key == pygame.K_LEFT:
            self.overworld_character.velocity[0] = 0           
    
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        
        self.surface.fill(self.bg_color) # clear the display surface first
        self.game_map.draw()
        self.overworld_character.draw()
        pygame.display.update() # make the updated surface appear on the display    
        
    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        self.overworld_character.move()
        self.encounter = self.game_map.random_encounter(self.overworld_character.velocity)
        
        if self.encounter == True:
            
            enemy_name = random.choice(self.list_of_enemies)
            
            enemy = Unit(enemy_name)
            
            self.battle.commence(enemy, self.hero)
            
            self.overworld_character.velocity = [0,0]
        
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        if self.hero.current_hp <= 0:
            self.continue_game = False
            print("game over")
            
    def draw_end_screen(self):
        
        self.surface.fill(pygame.Color("black"))
        font = pygame.font.SysFont('Arial', 24, 1)
        game_over_image = font.render("GAME OVER!", True, (148, 33 , 33))
        game_over_pos = (190, 160)
        
        self.surface.blit(game_over_image, game_over_pos)
        
        pygame.display.update() # make the updated surface appear on the display            
    
class Character:
    # An object in this class represents a character
    
    def __init__(self, surface):
        
        self.awaiting_character_select = True
        self.surface = surface
        self.velocity = [0,0]
        self.position = [15,100] 
        self.dimensions = [32,32]
        self.params = pygame.Rect(self.position,self.dimensions)
        
        # Do this until user choses
        while self.awaiting_character_select == True:
            
            text = "Click on the character you want to play as:"
            font = pygame.font.SysFont('Arial', 24, 1)
            prompt_image = font.render(text, True, pygame.Color('white'))
            text_pos = (50,15)
            
            self.rect_swordsman = pygame.Rect(125, 200, 32, 32)
            self.rect_archer = pygame.Rect(375, 200, 32, 32)
            
            self.surface.fill(pygame.Color("black"))
        
            self.surface.blit(pygame.image.load("swordsman.png"), self.rect_swordsman)
            self.surface.blit(pygame.image.load("archer.png"), self.rect_archer)
            self.surface.blit(prompt_image, text_pos)            
            
            pygame.display.update()
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.rect_swordsman.collidepoint(event.pos): # If user clicks on swordsman
                        self.chosen = "swordsman"
                        self.awaiting_character_select = False
                        self.character_image = pygame.image.load("swordsman.png")
                    elif self.rect_archer.collidepoint(event.pos): # If user clicks on archer
                        self.chosen = "archer"
                        self.awaiting_character_select = False
                        self.character_image = pygame.image.load("archer.png")
        
    def draw(self):
        
        self.surface.blit(self.character_image, self.params)
        
    def move(self):
        
        size = self.surface.get_size()
        
        for i in range(0,2):
            
            self.position[i] = (self.position[i] + self.velocity[i])
            
            if self.position[0] < 0 or self.position[1] < 80 or self.position[i] + self.dimensions[i] > size[i]:  # check left and top or right and bottom
                
                self.position[i] -= self.velocity[i] # undos the movement made if it made the paintbrush go out of bounds
            
        self.params = pygame.Rect(self.position, self.dimensions)
    
    
class Map:
    
    def __init__(self, surface):
        
        self.surface = surface
        self.color = pygame.Color('brown')
        self.params = pygame.Rect([0,80],[500,320])
        
    def draw(self):
        # Draw the Map on the surface
        # - self is the Map
        
        pygame.draw.rect(self.surface, self.color,self.params)
        
    def random_encounter(self, velocity):
        
        chance_of_encounter = False
        
        for i in range(0,2): # Check for an encounter everytime user moves
            
            if velocity[i] != 0:
                
                chance_of_encounter = True
        
        if chance_of_encounter == True:
            
            i = random.randrange(288)
            
            if i == 1:
                
                return True
                
            print(i) 
            
        return False        
        
class Battle:
    
    def __init__(self, surface):
        
        self.surface = surface
        self.background_color = pygame.Color('dark blue')
        self.background_params = pygame.Rect([0,80],[500,320])    
        self.rect_enemy = pygame.Rect(202, 200, 96, 96)
        self.rect_attack1 = pygame.Rect([175,0],[32,80])
        self.rect_attack2 = pygame.Rect([207,0],[32,80])
        self.rect_defend = pygame.Rect([239,0],[32,80])
        self.rect_flee = pygame.Rect([271,0],[32,80])
        
        
    def draw(self):
        # Draw the Map on the surface
        # - self is the Map
        
        self.surface.fill(pygame.Color("black"))
        
        pygame.draw.rect(self.surface, self.background_color, self.background_params)   
        #pygame.draw.rect(self.surface, pygame.Color("white"), self.rect_attack)
        self.surface.blit(pygame.image.load("attack1.png"), self.rect_attack1)
        self.surface.blit(pygame.image.load("attack2.png"), self.rect_attack2)
        self.surface.blit(pygame.image.load("defend.png"), self.rect_defend)
        self.surface.blit(pygame.image.load("flee.png"), self.rect_flee)
        
        self.surface.blit(pygame.image.load("enemy_" + self.enemy.name + ".png"), self.rect_enemy)
        
        hero_hp_text = str(self.hero.current_hp) + "/" + str(self.hero.health) # hero health
        enemy_text = self.enemy.name.capitalize() + "! | " + str(self.enemy.current_hp) + "/" + str(self.enemy.health) # enemy health
        hero_attack1_pp_text = str(self.hero.attack1_current_pp) # hero attack 1 pp
        hero_attack2_pp_text = str(self.hero.attack2_current_pp) # hero attack 2 pp
        
        font = pygame.font.SysFont('Arial', 24, 1)
        enemy_image = font.render(enemy_text, True, pygame.Color('white'))
        enemy_text_pos = (340,25)    
        hero_image = font.render(hero_hp_text, True, pygame.Color('white'))
        hero_text_pos = (60, 25)
        
        #------------------------
        
        font_options = pygame.font.SysFont('Arial', 24, 1)
        hero_attack1_pp_image = font_options.render(hero_attack1_pp_text, True, pygame.Color('black'))
        hero_attack2_pp_image = font_options.render(hero_attack2_pp_text, True, pygame.Color('black'))
        hero_attack1_pp_text_pos = (180, 48)
        hero_attack2_pp_text_pos = (218, 48)   
        
        self.surface.blit(enemy_image, enemy_text_pos)  
        self.surface.blit(hero_image, hero_text_pos)
        self.surface.blit(hero_attack1_pp_image, hero_attack1_pp_text_pos)
        self.surface.blit(hero_attack2_pp_image, hero_attack2_pp_text_pos)
        
         
        
        pygame.display.update() # make the updated surface appear on the display    

    def commence(self, enemy, hero):
        # Draws the intro animation to fight encounter
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.
        
        self.hero = hero
        self.enemy = enemy
        self.can_attack = True
        self.close_clicked = False
        self.continue_game = True 
        self.game_Clock = pygame.time.Clock()
        
        pygame.draw.circle(self.surface, pygame.Color('black'), [250,200], 25)
        pygame.display.update()
        pygame.time.delay(500)
        pygame.draw.circle(self.surface, pygame.Color('black'), [250,200], 100)
        pygame.display.update()
        pygame.time.delay(500)
        pygame.draw.circle(self.surface, pygame.Color('black'), [250,200], 175)
        pygame.display.update()
        pygame.time.delay(500)      
        
        while self.can_attack:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(144) # run at most with FPS Frames Per Second  
        
    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        
        pass
        
        
    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event.pos)
        
    def handle_mouse_up(self, position):
        # handles the MOUSEBUTTONUP event
        # USER CHOOSES ATTACK
        # -self is the Game object         
        
        # FIRST ATTACK
        if self.rect_attack1.collidepoint(position) and self.hero.attack1_current_pp > 0 and self.can_attack == True : # If user clicks on the first attack
            
            slice_pos = (175, 360)
            self.rect_slice= pygame.Rect(200, 210, 100, 100)
                          
            self.surface.blit(pygame.image.load("slice_frame1.png"), self.rect_slice)
            pygame.display.update()
            pygame.time.delay(60)
            self.draw()
            
            self.surface.blit(pygame.image.load("slice_frame2.png"), self.rect_slice)
            pygame.display.update()
            pygame.time.delay(60)
            self.draw()
            
            self.surface.blit(pygame.image.load("slice_frame3.png"), self.rect_slice)
            pygame.display.update()
            pygame.time.delay(60)
            self.draw()            
            
            pygame.time.delay(500) # delay before attack
            self.hero.attack1_current_pp = self.hero.attack1_current_pp - 1
            self.attacks(self.hero, self.enemy, self.hero.attack)
            
            if self.enemy.current_hp > 0 and self.can_attack == True:
                
                self.attacks(self.enemy, self.hero, self.enemy.attack) # Swaps attacker and defender positions         
        
        # SECOND ATTACK
        if self.rect_attack2.collidepoint(position) and self.hero.attack2_current_pp > 0 and self.can_attack == True : # If user clicks on the second attack
            
            
            pygame.draw.circle(self.surface, pygame.Color('red'), [250,260], 175)
            pygame.display.update()
            pygame.time.delay(500)
            self.draw()
            
            pygame.draw.circle(self.surface, pygame.Color('red'), [250,260], 100)
            pygame.display.update()
            pygame.time.delay(500)
            self.draw()
            
            pygame.draw.circle(self.surface, pygame.Color('red'), [250,260], 25)
            pygame.display.update()            
            pygame.time.delay(500)    
            self.draw()
            
            self.hero.attack2_current_pp = self.hero.attack2_current_pp - 1
            self.attacks(self.hero, self.enemy, self.hero.attack2)
            
            if self.enemy.current_hp > 0 and self.can_attack == True:
                
                self.attacks(self.enemy, self.hero, self.enemy.attack) # Swaps attacker and defender positions      
        
        # DEFEND MOVE
        if self.rect_defend.collidepoint(position) and self.can_attack == True : # If user clicks on defend
            pygame.time.delay(500) # delay before attack
            
            print("The hero is defending!")
            
            self.hero.defense = self.hero.defense + self.hero.increased_defence # Raise defense
            
            if self.enemy.current_hp > 0 and self.can_attack == True:
                
                self.attacks(self.enemy, self.hero, self.enemy.attack) # Swaps attacker and defender positions    
            
            self.hero.defense = self.hero.defense - self.hero.increased_defence # Remove defense
         
        # RUN MOVE   
        if self.rect_flee.collidepoint(position) and self.can_attack == True : # If user clicks on flee
            pygame.time.delay(500) # delay before attack
            
            print("The hero fled!")
            
            self.can_attack = False
            
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        pass        
    
    def attacks(self, attacker, defender, attack):
        # Used to attack for both player and enemy
        
        attacker_name = attacker.name
        self.str_connected = ""
        self.str_crit = ""
        
        print("The " + attacker_name + " attacks!")
        
        new_damage = 0
        
        i = random.randrange(100)
        
        if i >= defender.dodge_chance: # Check to see if move dodges       
            print("The move will land!")
            self.str_connected = "The " + attacker_name.capitalize() + "'s move hit!"
            new_damage = attack
            i = random.randrange(100)
            if i <= attacker.crit_chance:
                new_damage = attack * 2
                print("CRIT")
                self.str_crit = "CRIT!"
            if new_damage < defender.defense: # Atleast deal 1 damage
                new_damage = 1
            else:
                new_damage = new_damage - defender.defense
        else:
            print("The move missed")
            self.str_connected = attacker_name.capitalize() + "'s move missed!"
        
        defender.current_hp = defender.current_hp - new_damage
        print(str(new_damage) + " damage is dealt!")
        
        if defender.current_hp <= 0:
            
            defender.current_hp = 0 # No negative numbers displayed   
        
        self.draw() # Update health
        
        self.text_attack() # Display attack info
            
        pygame.time.delay(1000) # Display attack's text
            
        self.check_for_deaths(attacker, defender)
        
    def check_for_deaths(self, attacker, defender):
        
        if defender.current_hp <= 0:
            
            pygame.time.delay(1000) # Delay before deaths
            self.winner_declared(attacker.name.upper() + " WINS!")         
            self.can_attack = False # Stop combat phase
            
                
    def winner_declared(self, winner):
        
        font = pygame.font.SysFont('Arial', 24, 1)
        
        winner_image = font.render(winner, True, pygame.Color('white'))
        winner_text_pos = (175, 360)
                      
        
        self.surface.blit(winner_image, winner_text_pos)
        
        pygame.display.update() # make the updated surface appear on the display   
        
        pygame.time.delay(500)
        pygame.time.delay(500)
        pygame.time.delay(500) # Done to avoid windows thinking it froze
                
    def text_attack(self):
        
        font = pygame.font.SysFont('Arial', 24, 1)
        
        connected_image = font.render(self.str_connected, True, pygame.Color('white'))
        connected_text_pos = (175, 310)
            
        
        crit_image1 = font.render(self.str_crit, True, (148, 33 , 33))
        crit_image2 = font.render(self.str_crit, True, pygame.Color('Red'))
        crit_text_pos1 = (175, 340)
        crit_text_pos2 = (177, 338)
                      
        
        self.surface.blit(crit_image1, crit_text_pos1)
        self.surface.blit(crit_image2, crit_text_pos2)
        self.surface.blit(connected_image, connected_text_pos)         
        
        pygame.display.update() # make the updated surface appear on the display    
                
    

class Unit:
    # An object here represents a hero or enemy unit
    
    def __init__(self, name):
        
        self.name = name
        
        if self.name == "slime":
            self.slime_class()
        elif self.name == "ghost":
            self.ghost_class()
        elif self.name == "jaskirat":
            self.jaskirat_class()   
        elif self.name == "swordsman":
            self.hero_swordsman_class()
        elif self.name == "archer":
            self.hero_archer_class()
        
    def slime_class(self):
        self.health = 15
        self.attack = 5
        self.defense = 2
        self.speed = 9
        self.current_hp = self.health
        self.line_up_chance = -1
        self.dodge_chance = 1
        self.crit_chance = 1
        self.character_image = pygame.image.load("enemy_slime.png")        
        
    def ghost_class(self):
        self.health = 13
        self.attack = 9
        self.defense = 1
        self.speed = 9
        self.current_hp = self.health
        self.line_up_chance = -1
        self.dodge_chance = 9
        self.crit_chance = 4
        self.character_image = pygame.image.load("enemy_ghost.png")       
        
    def jaskirat_class(self):
        self.health = 10
        self.attack = 1
        self.defense = 1
        self.speed = 0
        self.current_hp = self.health
        self.line_up_chance = -1
        self.dodge_chance = 0
        self.crit_chance = 100
        self.character_image = pygame.image.load("enemy_jaskirat.png")     
    
    def hero_swordsman_class(self):
        self.health = 20 # Total damage a user can take before dying
        self.attack = 6 # Total damage a user can deal in a turn
        self.attack2 = 8
        self.defense = 4 # Total damage a user can nullify per attack
        self.speed = 5 # Order of which player moves first
        self.current_hp = 20
        self.line_up_chance = -1 # Chance to strike all enemies
        self.dodge_chance = 5 # Chance for user to dodge attack
        self.crit_chance = 10 # % Chance to deal a critical hit
        self.attack1_max_pp = 15
        self.attack1_current_pp = 15
        self.attack2_max_pp = 7
        self.attack2_current_pp = 7
        self.increased_defence = 5
        self.character_image = pygame.image.load("swordsman.png")
        
    def hero_archer_class(self):
        self.health = 16
        self.attack = 4
        self.attack2 = 11
        self.defense = 3
        self.speed = 9
        self.current_hp = 16
        self.line_up_chance = 20
        self.dodge_chance = 9
        self.crit_chance = 7
        self.attack1_max_pp = 18
        self.attack1_current_pp = 18
        self.attack2_max_pp = 5
        self.attack2_current_pp = 5       
        self.increased_defence = 3
        self.character_image = pygame.image.load("archer.png")
        
    
    
main()

# ---------------------------------------------------------------------- GOALS
# DONE - Game over @ 0 hero hp
# DONE - Fix Time Freezes
# Make arguments in Unit class for efficiency (Remove enemy_ from pngs)
# Attack 2, PP, Defend, Run (32 pixels per button)
# DONE - Attack animations
# Defend and Run animations
# Speed Calc
# Exp
# Make handle_mouse_up more efficient

# Defending adds additional evasiveness
# Line up
# Moving Map
# Different attack icons per character

# Typing

# ---------------------------------------------------------------------- KNOWN BUGS
# Attacks can be bufferred by clicking twice
# Fix close button during combat