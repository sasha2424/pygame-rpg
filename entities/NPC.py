from entities.Entity import Entity
from spritesheet.SpriteSheet import SpriteSheet
from spritesheet.Animation import Animation
from Utils import *
import pygame

from Rendering import Render_Queue, queue_render

class Dialogue:
    def __init__(self):
        self.conv = {}
        self.stage = 0
        self.selection = -1
        self.selection_marker = '*'
        self.delay_timer = -1

        self.dialogue_ended = False

        self.spritesheet = SpriteSheet("dialogue_box")

        x = 465
        y = 421
        self.top_left = self.spritesheet.image_at((x,y,14,15),(0,0,0))
        self.top_right = self.spritesheet.image_at((x+45,y,14,15),(0,0,0))
        self.bottom_left = self.spritesheet.image_at((x,y+47,14,11),(0,0,0))
        self.bottom_right = self.spritesheet.image_at((x+45,y+47,14,11),(0,0,0))

        self.top = self.spritesheet.image_at((x+16,y,27,15),(0,0,0))
        self.left = self.spritesheet.image_at((x,y+17,14,28),(0,0,0))
        self.bottom = self.spritesheet.image_at((x+16,y+47,27,11),(0,0,0))
        self.right = self.spritesheet.image_at((x+45,y+17,14,28),(0,0,0))

        self.center = self.spritesheet.image_at((x+16,y+17,27,28),(0,0,0))

        self.is_open = False
        self.open_animation_state = 0 #0 - 1
        self.font = pygame.font.Font('freesansbold.ttf', 15)

        self.text_color = (0,0,0)
        self.prompt = None
        self.prompt_old_size = (0,0)

        self.animation_finished = False

    def select_up(self):
        if len(self.conv[self.stage][1]) == 0:
            return
        self.selection -= 1
        self.selection %= len(self.conv[self.stage][1])
        self.update_prompt()

    def select_down(self):
        if len(self.conv[self.stage][1]) == 0:
            return
        self.selection += 1
        self.selection %= len(self.conv[self.stage][1])
        self.update_prompt()

    def render_prompt(self):
        text = self.conv[self.stage][0]
        options = self.conv[self.stage][1]

        lines = text.splitlines()
        options_lines = [option[1].splitlines() for option in options]
        num_lines = len(lines)
        for option in options_lines:
            num_lines+=len(option)
        line_height = self.font.size(' ')[1]

        selection_width = self.font.size(self.selection_marker)[0]
        selection_marker_surface = self.font.render(self.selection_marker, False, self.text_color)

        height = line_height * num_lines
        width = 0
        for line in lines:
            width = max(self.font.size(line)[0],width)
        for option in options_lines:
            for line in option:
                width = max(self.font.size(line)[0] + selection_width,width)

        text_box = pygame.Surface((width,height))
        text_box.fill((255,255,255))
        text_box.set_colorkey((255,255,255))

        y = 0
        for line in lines:
            line_surface = self.font.render(line, False, self.text_color)
            text_box.blit(line_surface, (0, y * line_height))
            y += 1

        for i,option in enumerate(options_lines):
            for j,line in enumerate(option):
                line_surface = self.font.render(line, False, self.text_color)
                text_box.blit(line_surface, (selection_width, y * line_height))
                if j == 0 and i == self.selection:
                    text_box.blit(selection_marker_surface,(0,y*line_height))
                y += 1
        return text_box

    def reset(self):
        self.prompt = None
        self.prompt_old_size = (0,0)

        self.stage = 0
        self.selection = -1
        self.delay_timer = 0

        self.dialogue_ended = False

    def run(self, needs_open):
        if needs_open and not self.dialogue_ended:
            self.open()
        elif self.is_open:
            self.close()
        else:
            self.reset()

    def open(self):
        #run when dialogue open
        self.is_open = True

        if self.open_animation_state < 1:
            self.open_animation_state += .1
        if self.open_animation_state >= 1:
            self.animation_finished = True

        delay = self.conv[self.stage][2]
        if delay > 0:
            self.delay_timer += 1
            if self.delay_timer >= delay:
                self.transition()


    def close(self):
        #run when dialogue closed
        if self.open_animation_state > 0:
            self.open_animation_state -= .1

        if self.open_animation_state <= 0:
            self.is_open = False
            self.reset()
        pass

    def transition(self):
        if not self.animation_finished:
            return

        #check if dialogue needs to be closed
        if self.conv[self.stage][4]:
            self.dialogue_ended = True
            return

        next_stage = self.conv[self.stage][3]
        if not next_stage == -1:
            self.stage = next_stage
        else:
            options = self.conv[self.stage][1]
            #no transitions
            if len(options) == 0:
                return
            #no selection
            if self.selection < 0:
                return

            self.stage = options[self.selection][0]

        self.prompt_old_size = (self.prompt.get_width(),self.prompt.get_height())
        self.update_prompt()
        self.open_animation_state = 0
        self.animation_finished = False
        self.selection = -1
        self.delay_timer = 0

    def update_prompt(self):
        self.prompt = self.render_prompt()

    def add_stage(self, id, text, options=[], delay=-1, next_stage=-1,end=False):
        self.conv[id] = (text, options,delay,next_stage,end)

    def draw(self, X, Y):
        if self.is_open:
            if self.prompt == None:
                self.update_prompt()

            r = self.open_animation_state

            c_w = 14
            c_h = 15
            e_w = 27
            e_h = 28
            c2_w = 14
            c2_h = 11

            dx = (self.prompt.get_width() - self.prompt_old_size[0])*r + self.prompt_old_size[0]
            dy = (self.prompt.get_height() - self.prompt_old_size[1])*r + self.prompt_old_size[1]

            # Top and Bottom Edges
            border_x = -dx / 2
            border_y = -c2_h - dy
            while border_x < dx / 2 - e_w:
                queue_render(Y, self.top,(X + border_x, Y - c2_h - dy - c_h),(0,0,e_w,c_h))
                queue_render(Y, self.bottom,(X + border_x, Y - c2_h),(0,0,e_w,c2_h))
                border_x += e_w
            queue_render(Y, self.top,(X + border_x, Y - c2_h - dy - c_h),(0,0,dx/2 - border_x + 1,c_h))
            queue_render(Y, self.bottom,(X + border_x, Y - c2_h),(0,0,dx/2 - border_x + 1,c2_h))

            while border_y < -c2_h - e_w:
                queue_render(Y, self.left,(X - dx / 2 - c_w, Y + border_y),(0,0,c_w,e_h))
                queue_render(Y, self.right,(X + dx / 2, Y + border_y),(0,0,c2_w,e_h))
                border_y += e_h
            queue_render(Y, self.left,(X - dx / 2 - c_w, Y + border_y),(0,0,c_w,-c2_h - border_y + 1))
            queue_render(Y, self.right,(X + dx / 2, Y + border_y),(0,0,c2_w,-c2_h - border_y + 1))

            center_x = -dx / 2
            while center_x < dx / 2 - e_w:
                center_y = -c2_h - dy
                while center_y < -c2_h - e_w:
                    queue_render(Y, self.center,(X + center_x, Y + center_y),(0,0,e_w,e_h))
                    center_y += e_h
                queue_render(Y, self.center,(X + center_x, Y + center_y),(0,0,e_w,-c2_h - center_y + 1))
                center_x += e_w
            center_y = -c2_h - dy
            while center_y < -c2_h - e_w:
                queue_render(Y, self.center,(X + center_x, Y + center_y),(0,0,dx/2 - center_x + 1,e_h))
                center_y += e_h
            queue_render(Y, self.center,(X + center_x, Y + center_y),(0,0,dx/2 - center_x + 1,-c2_h - center_y + 1))

            # Corners
            queue_render(Y, self.top_left,(X - dx / 2 - c_w, Y - c2_h - dy - c_h),(0,0,c_w,c_h))
            queue_render(Y, self.top_right,(X + dx / 2, Y - c2_h - dy - c_h),(0,0,c2_w,c_h))
            queue_render(Y, self.bottom_left,(X - dx / 2 - c_w, Y - c2_h),(0,0,c_w,c2_h))
            queue_render(Y, self.bottom_right,(X + dx / 2, Y - c2_h),(0,0,c2_w,c2_h))

            if r >= 1:
                queue_render(Y, self.prompt,(X - dx / 2, Y - c2_h - dy))


class NPC(Entity):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

        self.dialogue = None
        self.interact_range = 100
        self.can_interact = True

    def update(self, local_entities, player):
        if dist(self.x, self.y, player.x, player.y) < self.interact_range:
            self.dialogue.run(True)
        if dist(self.x, self.y, player.x, player.y) > self.interact_range:
            self.dialogue.run(False)
        pass

    def interact(self, key):
        if key == "e":
            self.dialogue.transition()
        if key == "up_arrow":
            self.dialogue.select_up()
        if key == "down_arrow":
            self.dialogue.select_down()


class Rick(NPC):

    def __init__(self, x, y, z):
        super().__init__(x, y, z)

        self.spritesheet = SpriteSheet("rick", (4*30,4*40))
        self.animation = Animation(self.spritesheet)
        self.animation.add_animation_from_sheet("down", (0,0,30,40), 4, (0,0,0))
        self.animation.add_animation_from_sheet("right", (0,40,30,40), 4, (0,0,0))
        self.animation.add_animation_from_sheet("left", (0,80,30,40), 4, (0,0,0))
        self.animation.add_animation_from_sheet("up", (0,120,30,40), 4, (0,0,0))
        self.image = self.animation.get_image()

        self.sprite_shift_x = 15
        self.sprite_shift_y = 40

        self.add_collision_sphere(0,0,10,10)

        self.canMove = True

        self.dialogue = Dialogue()
        self.dialogue.add_stage(0, "E", next_stage=1)
        self.dialogue.add_stage(1, "Hello!", next_stage=2)
        self.dialogue.add_stage(2, "How are you?", [(3, "Good"), (4, "OK"), (5, "Bad")])
        self.dialogue.add_stage(3, "That is great!\nI am doing Fine as well", next_stage = 6)
        self.dialogue.add_stage(4, "Well at least you aren't bad\nThat would be...\nBAD!!", next_stage = 6)
        self.dialogue.add_stage(5, "Thats not very good is it :(\n:(\n:(", next_stage = 6)
        self.dialogue.add_stage(6, "Please select a class:", [(7, "MAGE\n(spooky)"), (8, "FIGHTER\n(less spooky)")])
        self.dialogue.add_stage(7, "WOW A MAGE\npress [ENTER] to continue", next_stage = 9)
        self.dialogue.add_stage(8, "WOW A FIGHER\npress [ENTER] to continue", next_stage = 9)
        self.dialogue.add_stage(9, "Bye   ", [], delay=50, end=True)


    def draw(self, dx, dy):
        super().draw(dx, dy)
        self.dialogue.draw(self.x - dx,self.y - dy - 50)
