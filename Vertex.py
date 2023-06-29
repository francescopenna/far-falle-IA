class Vertex:
    def __init__ (self, id, adj_list, n_free_adj = 0, n_color, list_walk = []):
        #list of adjacent vertices
        self.id = id
        self.adj_list = adj_list
        self.n_free_adj = n_free_adj
        #numero di colori
        self.n_color = n_color
        #who passed
        self.list_walk = list_walk

""" v1.n_color = 3
list_walk.add("red")
if len(list_walk) < v1.n_color --> posso passare  """

