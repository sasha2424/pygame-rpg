

class Animation:
    """
    Class to store and handle sprite animation
    """
    def __init__(self,sheet):
        self.spritesheet = sheet

        self.state = None
        self.animation_dict = {}
        self.animation = []
        self.animation_frame = 0
        self.animation_tick = 0
        self.animation_time = 4

        self.frozen = False

    def add_animation(self, name, animation):
        self.animation_dict[name] = animation

    def add_animation_from_sheet(self, name, rect, image_count, colorkey = None):
        self.animation_dict[name] = self.spritesheet.load_strip(rect, image_count, colorkey)
        if len(self.animation) == 0:
            self.animation = self.animation_dict[name]

    def set(self,name):
        self.state = name
        self.animation = self.animation_dict[name]

    def get_state(self):
        return self.state

    def get_image(self):
        self.animation_frame %= len(self.animation)
        return self.animation[self.animation_frame]

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False

    def update(self):
        if self.frozen:
            return
        self.animation_tick += 1
        if self.animation_tick >= self.animation_time:
            self.animation_tick = 0
            self.animation_frame += 1
            self.animation_frame %= len(self.animation)
