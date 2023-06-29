class Edge:
    def __init__ (self, v1, v2, is_boarder = False, color, color2 = ""):
        self.v1 = v1
        self.v2 = v2
        self.is_boarder = is_boarder
        self.color = color
        self.color2 = color2