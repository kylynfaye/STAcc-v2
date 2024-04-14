class RSO():
    def __init__(self, magnitude, x_pos, y_pos, z_pos, name=None):
        self.mag = magnitude
        self.xpos, self.ypos, self.zpos = x_pos, y_pos, z_pos
        self.name = name

    #def random_RSO_thing(self, user_input)