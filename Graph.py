class Graph:
    def __init__ (self, n_vertices, n_edges, v_list = [], e_list = []):
        self.n_vertices = n_vertices
        self.n_edges = n_edges
        #list of vertices
        self.v_list = v_list
        #list of edges
        self.e_list = e_list

    def add_edges(self):
        for e in self.e_list:
            self.e_list.append(e)
    
    def add_vertices(self):
        for v in self.v_list:
            self.v_list.append(v)
    
    


