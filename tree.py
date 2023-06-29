from node import Node
from Utility import *
from igraph import *
import ast 
import copy

class DynamicTree():

    def __init__(self):
        self.nodes = []
        #self.data = []


    def get_green_paths(self):
        paths = []
        for node in self.nodes:
            if node.name == 'green':
                paths.append(node.path)

        return paths


    def get_blue_paths(self):
        paths = []
        for node in self.nodes:
            if node.name == 'blue':
                paths.append(node.path)

        return paths


    def get_red_paths(self):
        paths = []
        for node in self.nodes:
            if node.name == 'red':
                paths.append(node.path)

        return paths


    def is_contained_path(self,element, father_type):
        if father_type == 'green':
            paths = self.get_green_paths()
        elif father_type == 'blue':
            paths = self.get_blue_paths()
        elif father_type == 'red':
            paths = self.get_red_paths()

        for path in paths:
            if (all(x in element.path for x in path)):
                return (True,path)

        return (False, [])
                

    def create_maximize(self, node_type, father_type):
        # key = father, value = list of tuple -> ([0] payoff, [1] full path)
        # payoff = 3-list of payoff -> [1,0,1]
        # full path = list of tuple -> [ ('red', 2), ('blue', 28), ('green', 43) ]
        maximize = {}

        for element in reversed(self.nodes):
            father_time = self.is_contained_path(element, father_type)
            if element.name == node_type and element.parent == father_type and father_time[0] is True:
                father = (father_type, father_time[1])
                father = str(father)

                if father in maximize:
                    maximize[father].append((element.value, element.path))

                else:
                    maximize[father] = [ (element.value ,element.path) ]  
                    #maximize[father] = [ ([1,1,1],element.path) ] # for testing purposes

        return maximize


    def create_leafs(self, reachable_turn, falle_turn, stale_turn, absent=0):
 
        green_paths = self.get_green_paths()
        blue_paths = self.get_blue_paths()
        red_paths = self.get_red_paths()

        if (absent == 0):
            if len(falle_turn) > 0: # or stalemate:
                for node in self.nodes:
                    # if all the players can still play
                    if node.name == 'green':
                        for path in green_paths: 
                            for i in range(len(reachable_turn['green'])): 
                                child = Node('payoffs', 'green')
                                for element in path:
                                    child.path.append(element)
                                    
                                    #if falla... falla case
                                    for falla in falle_turn: 
                                        if element == (falla.player,falla.destination):
                                            if falla.player == 'red':
                                                child.value[0] = child.value[0] + falla.points
                                            if falla.player == 'blue':
                                                child.value[1] = child.value[1] + falla.points
        
                                        if ('green',reachable_turn['green'][i]) == (falla.player,falla.destination):
                                            child.value[2] = child.value[2] + falla.points
                                    
                                    #if stallo...
                                    for stale_player in stale_turn:
                                        if element == (stale_player, stale_turn[stale_player]):
                                            if stale_player == 'red':
                                                child.value[0] = -1
                                            if stale_player == 'blue':
                                                child.value[1] = -1
                                        
                                        if ('green', reachable_turn['green'][i]) == (stale_player, stale_turn[stale_player]):
                                            child.value[2] = -1

                                child.path.append(('green',reachable_turn['green'][i]))
                                self.nodes.append(child)
                        break
            else:
                green_paths = self.get_green_paths()
                for node in self.nodes:
                    if node.name == 'green':
                        for path in green_paths: 
                            for i in range(len(reachable_turn['green'])): 
                                child = Node('payoffs', 'green')
                                for element in path:
                                    child.path.append(element)

                                    #if stallo...
                                    for stale_player in stale_turn:
                                        if element == (stale_player, stale_turn[stale_player]):
                                            if stale_player == 'red':
                                                child.value[0] = -1
                                            if stale_player == 'blue':
                                                child.value[1] = -1

                                        if ('green', reachable_turn['green'][i]) == (stale_player, stale_turn[stale_player]):
                                            child.value[2] = -1
    
                                child.path.append(('green',reachable_turn['green'][i]))
                                self.nodes.append(child)
                        break

        """ # stalemate detected
        if absent == 'green':
            if len(falle_turn) > 0:
                for node in self.nodes:
                    # if all the players can still play
                    if node.name == 'blue':
                        for path in blue_paths: 
                            for i in range(len(reachable_turn['blue'])): 
                                child = Node('payoffs', 'blue')  
                                for element in path:
                                    child.path.append(element)
                                    for falla in falle_turn: 
                                        if element == (falla.player,falla.destination):
                                            if falla.player == 'red':
                                                child.value[0] = child.value[0] + falla.points
        
                                        if ('blue',reachable_turn['blue'][i]) == (falla.player,falla.destination):
                                            child.value[2] = child.value[2] + falla.points
                                child.path.append(('blue',reachable_turn['blue'][i]))
                                self.nodes.append(child)
                        break
            else:
                green_paths = self.get_green_paths()
                for node in self.nodes:
                    if node.name == 'blue':
                        for path in blue_paths: 
                            for i in range(len(reachable_turn['blue'])): 
                                child = Node('payoffs', 'blue')
                                for element in path:
                                    child.path.append(element)
                                child.path.append(('blue',reachable_turn['blue'][i]))
                                self.nodes.append(child)
                        break """


    def create_children(self, reachable_turn, falle_turn, stale_turn):
        # create nodes
        for key in reachable_turn:
            if key == 'red':
                """
                # da vedere se serve (sarebbe il codice per impilare un albero sopra di un altro ma potrebbe non essere necessario se ne risolviamo uno alla volta)
                if len(self.nodes) > 0:
                    for node in self.nodes:
                        if node.name == 'green':
                            for i in range(len(reachable_turn['green'])):
                                child = Node(key, None)
                                self.nodes.append(child)
                else:
                """
                # red has no parent since it is the root 
                child = Node(key, None)
                self.nodes.append(child)

            if key == 'blue':
                for node in self.nodes:
                    # we need to create, foreach red point, (#reachable paths * #red points) blue points
                    if node.name == 'red':
                        for i in range(len(reachable_turn['red'])):
                            child = Node(key, 'red')
                            child.path.append(('red',reachable_turn['red'][i]))
                            self.nodes.append(child)

            if key == 'green':
                j = len(reachable_turn['red'])
                # we need to create, foreach blue point, (#reachable paths * #blue points) green points
                # also, we need to append each and every red possible path to it 
                for node in self.nodes:
                    if node.name == 'blue':
                        j = j-1
                        for i in range(len(reachable_turn['blue'])):
                            child = Node(key,'blue')
                            child.path.append((node.parent,reachable_turn['red'][j-1]))
                            child.path.append(('blue',reachable_turn['blue'][i]))
                            self.nodes.append(child)

        # create the leafs
        green_paths = self.get_green_paths()
        blue_paths = self.get_blue_paths()
        red_paths = self.get_red_paths()

        if len(green_paths) > 0 and len(blue_paths) > 0 and len(red_paths) > 0:
            self.create_leafs(reachable_turn, falle_turn, stale_turn)

        if len(green_paths) == 0 and len(blue_paths) > 0 and len(red_paths) > 0:
            self.create_leafs(reachable_turn, falle_turn, stale_turn,'green')

        if len(green_paths) > 0 and len(blue_paths) == 0 and len(red_paths) > 0:
            self.create_leafs(reachable_turn, falle_turn, stale_turn,'blue')

        if len(green_paths) > 0 and len(blue_paths) > 0 and len(red_paths) == 0:
            self.create_leafs(reachable_turn, falle_turn, stale_turn,'red')


    def find_equilibrium(self):
        best_moves = set()
        # found the fathers of the leafs
        for i in range(2,-1,-1):
            if i == 2:
                maximize = self.create_maximize('payoffs', 'green')
                #print(" ----------------------------- maximize green ----------------------------- ")
                #print_dictionary(maximize)
            if i == 1:
                maximize = self.create_maximize('green', 'blue')
                #print('print(" ----------------------------- maximize blue ----------------------------- ")')
                #print_dictionary(maximize)
            if i == 0:
                maximize = self.create_maximize('blue', 'red')
                #print('print(" ----------------------------- maximize red ----------------------------- ")')
                #print_dictionary(maximize)

            max_value = ([-1,-1,-1],[])
            for key in maximize:
                for element in maximize[key]:
                    if element[0][i] >= max_value[0][i]:
                        #print(element, ' >= ', max_value)
                        max_value = element
                
                #if max_value == ([0,0,0],[]):
                #    return False

                maximize[key] = max_value
                
            best_moves.add(str(max_value[1][-1]))

            for key in maximize:
                father = ast.literal_eval(key)
                for node in self.nodes:
                    if node.name == father[0] and node.path == father[1]:
                        node.value = maximize[key][0]
                        node.trail = maximize[key][1]
            
            
            #print(" ----------------------------- maximize ----------------------------- ")
            #
            #for key, value in maximize.items():
            #    print(key, ' : ', value)
            #
            #print(" ----------------------------- end maximize ----------------------------- ")
            
                            
            #self.display_data()

        #print()
        #print(" *********** best_moves *********** ", best_moves)
        #print()

        return best_moves

    def debug_falle(falle_turn, starting_points):
        print('################################################################')
        if len(falle_turn) != 0:
            print('timeline: ')
            print_dictionary(starting_points)
            for falla in falle_turn:
                print(falla.triangle)
        else: 
            print('Niente falle in questa timeline')

    def solve_tree(self, original_maxn, board, players, stalemate):
        previous = players
        for node in self.nodes:
            if node.name == 'payoffs':
                fictious_board = copy.deepcopy(board)
                #print()
                #print('############################################# TIMELINE #############################################')

                starting_points = {
                                node.path[0][0]: node.path[0][1],
                                node.path[1][0]: node.path[1][1],
                                node.path[2][0]: node.path[2][1]
                                }
                subtree = DynamicTree()

                # i have first to update the fictious board!!!
                update_board(fictious_board, previous, starting_points, stalemate)

                reachable_turn = find_reachable(fictious_board, starting_points, stalemate)
                falle_turn = find_falle(fictious_board, starting_points, reachable_turn)
                stale_turn = find_stale(fictious_board, starting_points, reachable_turn)

                subtree.create_children(reachable_turn, falle_turn, stale_turn)

                # ----------------------------------------------- chiamata ricorsiva ----------------------------------------------- 
                sub_previous = copy.deepcopy(starting_points)
                sub_stalemate = copy.deepcopy(stalemate)
                for subnode in subtree.nodes:
                    if subnode.name == 'payoffs':
                        sub_fictious_board = copy.deepcopy(fictious_board)
                        sub_starting_points = {
                                            subnode.path[0][0]: subnode.path[0][1],
                                            subnode.path[1][0]: subnode.path[1][1],
                                            subnode.path[2][0]: subnode.path[2][1]
                                            }
                        subsubtree = DynamicTree()

                        #print_dictionary(sub_previous)
                        #print_dictionary(sub_starting_points)
                        #print_dictionary(sub_stalemate)
                        update_board(sub_fictious_board, sub_previous, sub_starting_points, sub_stalemate)

                        sub_reachable_turn = find_reachable(sub_fictious_board, sub_starting_points, sub_stalemate)
                        sub_falle_turn = find_falle(sub_fictious_board, sub_starting_points, sub_reachable_turn)
                        sub_stale_turn = find_stale(sub_fictious_board, sub_starting_points, sub_reachable_turn)

                        subsubtree.create_children(sub_reachable_turn, sub_falle_turn, sub_stale_turn)
                        sub_best_moves = subsubtree.find_equilibrium()

                        sub_dict_best_moves = {}
                        for val in sub_best_moves:
                            val = val.replace('(','')
                            val = val.replace(')','')
                            val = val.split(',')
                            val[0] = val[0].replace("'","")
                            val[0] = val[0].replace("'","")
                            val[1] = int(val[1])
                            sub_dict_best_moves[val[0]] = val[1]

                        sub_value_best_move = []

                        for sub_sub_node in reversed(subsubtree.nodes):
                            if sub_sub_node.path == [('red',sub_dict_best_moves['red']),('blue',sub_dict_best_moves['blue']),('green',sub_dict_best_moves['green'])]:
                                sub_value_best_move = subnode.value
                                break

                        subnode.value = sub_value_best_move
                # ------------------------------------------------------------------------------------------------------------------ 
                best_moves = subtree.find_equilibrium()

                dict_best_moves = {}
                for val in best_moves:
                    val = val.replace('(','')
                    val = val.replace(')','')
                    val = val.split(',')
                    val[0] = val[0].replace("'","")
                    val[0] = val[0].replace("'","")
                    val[1] = int(val[1])
                    dict_best_moves[val[0]] = val[1]

                value_best_move = []

                for sub_node in reversed(subtree.nodes):
                    if sub_node.path == [('red',dict_best_moves['red']),('blue',dict_best_moves['blue']),('green',dict_best_moves['green'])]:
                        value_best_move = sub_node.value
                        break

                node.value = value_best_move


        #self.display_data()
        #print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        return self.find_equilibrium()

        # aggiornare previous in qualche modo


    def display_data(self):
        for node in self.nodes:
            print('NAME: ', node.name, ' PARENT: ', node.parent, ' PATH: ', node.path, ' VALUE: ', node.value, 'TRAIL: ', node.trail)


    def debug_data(self, starting_points):
        print('---------------------------------------------------------------------------------------------------------------------')
        print('timeline: ')
        print_dictionary(starting_points)
        for node in self.nodes:
            print('NAME: ', node.name, ' PARENT: ', node.parent, ' PATH: ', node.path, ' VALUE: ', node.value, 'TRAIL: ', node.trail)

