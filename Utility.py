import igraph
from Falla import Falla

#---------------------------------------- Board Creation ----------------------------------------

def create_board(board):
    board.add_vertices(45)

    # OASIS: 0-10-14 RED, 10-40-14 GRAY, 10-36-40 BLUE, 40-14-44 GREEN
    # STARTING POINTS: 0 RED, 36 BLUE, 44 GREEN
    board.add_edges([
        (0,1),(0,2),
        (1,2),(1,3),(1,4),
        (2,4),(2,5),
        (3,6),(3,7),(3,4),
        (4,7),(4,8),(4,5),
        (5,8),(5,9),
        (6,10),(6,11),(6,7),
        (7,11),(7,12),(7,8),
        (8,12),(8,13),(8,9),
        (9,13),(9,14),
        (10,15),(10,16),(10,11),
        (11,16),(11,17),(11,12),
        (12,17),(12,18),(12,13),
        (13,18),(13,19),(13,14),
        (14,19),(14,20),
        (15,21),(15,22),(15,16),
        (16,22),(16,23),(16,17),
        (17,23),(17,24),(17,18),
        (18,24),(18,25),(18,19),
        (19,25),(19,26),(19,20),
        (20,26),(20,27),
        (21,28),(21,29),(21,22),
        (22,29),(22,30),(22,23),
        (23,30),(23,31),(23,24),
        (24,31),(24,32),(24,25),
        (25,32),(25,33),(25,26),
        (26,33),(26,34),(26,27),
        (27,34),(27,35),
        (28,36),(28,37),(28,29),
        (29,37),(29,38),(29,30),
        (30,38),(30,39),(30,31),
        (31,39),(31,40),(31,32),
        (32,40),(32,41),(32,33),
        (33,41),(33,42),(33,34),
        (34,42),(34,43),(34,35),
        (35,43),(35,44),
        (36,37),(37,38),(38,39),(39,40),(40,41),(41,42),(42,43),(43,44)
                ])
    #print(board)

    # setting up attributes for the nodes:
    # 		n_color -> tells us how many times you can walk on a given node
    #		list_walk -> tells us how many times you have walked on a given node
    #		region -> point of the graph on which the node is situated (r -> red, w -> gray, b -> blue, g -> green)
    for i in range(45):
        if i in [0, 44, 36]:
            board.vs[i]['n_color'] = 0

        elif i in [1, 2, 3, 5, 6, 9, 10, 14, 15, 20, 21, 27, 28, 35, 37, 38, 39, 40, 41, 42, 43]:
            board.vs[i]['n_color'] = 2

        else:
            board.vs[i]['n_color'] = 3

        if i < 10:
            board.vs[i]['region'] = 'red'
        if (i > 9 and i < 15) or (i > 15 and i < 20) or (i > 22 and i < 26) or i == 31 or i == 32 or i == 40:
            board.vs[i]['region'] = 'w'
        if i == 15 or i == 21 or i == 22 or (i < 31 and i > 27) or (i < 40 and i > 35):
            board.vs[i]['region'] = 'blue'
        if i == 20 or i == 26 or i == 27 or (i < 36 and i > 32) or (i < 45 and i > 40):
            board.vs[i]['region'] = 'green'

        board.vs[i]['list_walk'] = []
        board.vs[i]['occupied'] = 0

        #print(i, ' -> ', board.vs[i].attributes())

    board.vs[0]['list_walk'].append('r')
    board.vs[36]['list_walk'].append('b')
    board.vs[44]['list_walk'].append('g')

    board.vs[0]['occupied'] = 1
    board.vs[36]['occupied'] = 1
    board.vs[44]['occupied'] = 1

    # color edge is a representation of the thread: who has been on what edge and what thread has been placed
    for edge in board.es:
        edge['color'] = ''


#----------------------------------------  ----------------------------------------

def print_dictionary(dictionary):
    for key, value in dictionary.items():
        print(key, ' : ', value)


def update_board(board, previous, reachable_turn, stalemate):

    for key in reachable_turn:
        if stalemate[key] == 1:
            continue
        else:
            edge_index = board.get_eid(previous[key],reachable_turn[key])
            board.es[edge_index]['color'] = key
            board.vs[previous[key]]['occupied'] = 0
            board.vs[reachable_turn[key]]['list_walk'].append(key)
            board.vs[reachable_turn[key]]['occupied'] = 1


def find_reachable(board, players, stalemate):
    reachable_turn = {}
    
    for key in players:
        reachable = [
                    element for element in range(len(board.get_adjacency()[players[key]])) 
                                if board.get_adjacency()[players[key]][element] != 0 
                                and len(board.vs[element]['list_walk']) < board.vs[element]['n_color']
                                and board.es[board.get_eid(players[key],element)]['color'] == ''
                                and (board.vs[element]['occupied'] == 0
                                or (board.vs[element]['occupied'] == 1 and key == 'blue' and (players['red'] == element and stalemate['red'] == 0))
                                or (board.vs[element]['occupied'] == 1 and key == 'green' and ((players['red'] == element and stalemate['red'] == 0)
                                                                                           or (players['blue'] == element and stalemate['blue'] == 0))))
                    ]

        reachable_turn[key] = reachable

        if reachable == []:
            reachable.append(players[key])

    return reachable_turn


def find_falle(board, players, reachable_turn):
    falle_turn = []

    for key in players:
        incident_nodes_player = []
        # PHASE 1
        # get all incident edges on the current position of the player
        for edge_id in board.incident(players[key]):
            # if this edge has already been visited by the player
            #print(board.es()[edge_id])
            if(board.es[edge_id]['color'] == key):
                # insert in a list the other end of the edge
                if board.get_edgelist()[edge_id][0] != players[key]:
                    incident_nodes_player.append(board.get_edgelist()[edge_id][0])
                else:
                    incident_nodes_player.append(board.get_edgelist()[edge_id][1])

        # PHASE 2
        candidates = []
        # foreach of the incident nodes obtained before
        for node in incident_nodes_player:
            already_visited = []
            # take all the adjacent nodes that were already visited by the player
            for element in range(len(board.get_adjacency()[node])):
                if board.get_adjacency()[node][element] != 0 and board.es[board.get_eid(node,element)]['color'] == key and element != players[key]:
                    already_visited.append(element)
                # keep all candidates in the same place, the index of the list of candidates correspond to the index of the node from which they were found
            candidates = [already_visited]

        # PHASE 3
        # if there exists an intercept of the candidates and the reachable nodes: that is a falla
        # example: starting from 4
        #          incident_nodes_player:  [2]
        #          candidates:  [[1]]
        #          reachable nodes from 4 not visited yet: [1, 3, 5, 7, 8]
        # since 1 is conteined in the candidates and in the latter list we check the 
        # corrispondent index of the sublist in incident_nodes_player and find 
        # the last element of the falla (red, incident_node, reachable/candidate)
        for reachable_node in reachable_turn[key]:
            for sub_list in candidates:
                for candidate in sub_list:
                    if candidate == reachable_node:
                        # order in which a falla is represented: (current position, node already visited, node to reach next)
                        # assignment of points: if all nodes are in the region gray, we give them 2 points, 
                        # if at least one node is in red, we assign 1 point, else 3 (we are in an opponent's region)
                        if board.vs[players[key]]['region'] == 'w' and board.vs[incident_nodes_player[candidates.index(sub_list)]]['region'] == 'w' and board.vs[reachable_node]['region'] == 'w':
                            falle_turn.append(Falla(key, reachable_node, (players[key], incident_nodes_player[candidates.index(sub_list)], reachable_node), 2))
                        elif board.vs[players[key]]['region'] == key or board.vs[incident_nodes_player[candidates.index(sub_list)]]['region'] == key or board.vs[reachable_node]['region'] == key:
                            falle_turn.append(Falla(key, reachable_node, (players[key], incident_nodes_player[candidates.index(sub_list)], reachable_node), 1))
                        else:
                            falle_turn.append(Falla(key, reachable_node, (players[key], incident_nodes_player[candidates.index(sub_list)], reachable_node), 3))

    return falle_turn


def find_stale(board, players, reachable_turn):
    stale_turn = {}
    for key in players:
        # Fase 1:
        colored_reachable = {}
        # scorro nodi raggiungibili
        for reachable_node in reachable_turn[key]:
            # scorro tutti gli archi incidenti al nodo
            for edge_id in board.incident(reachable_node):
                # se l'arco non è colorato
                if board.es[edge_id]['color'] == '':
                    # +1 sul dizionario del nodo raggiungibile
                    if reachable_node in colored_reachable:
                        colored_reachable[reachable_node] += 1
                    else:
                        colored_reachable[reachable_node] = 1

        # Fase 2:
        # scorro nodi raggiungibili
        for node in colored_reachable:
            # se hanno <= 3 archi non colorati
            if colored_reachable[node] <= 3: # e tutti i nodi raggiungibili sono occupati 
                # prendi tutti i suoi vicini
                incident_nodes = find_neighbors(board, node)
                
                # scorro i vicini del nodo raggiungibile
                for incident_node in incident_nodes:
                    # se l'arco che collega il nodo raggiungibile con i suoi vicini non è colorato
                    if board.es[board.get_eid(node, incident_node)]['color'] == '':
                        # se il nodo vicino è occupato o non walkable
                        if board.vs[incident_node]['occupied'] == 1 or len(board.vs[incident_node]['list_walk']) >= board.vs[incident_node]['n_color']:
                            flag_stale = 1
                        else:
                            flag_stale = 0
                            break 
                if flag_stale:  
                    stale_turn[key] = node

    return stale_turn

def check_stalemate(players, reachable_turn, stalemate, player, best_choice):
    if player == 'red':
        if stalemate['red'] == 1:
            return True

    if player == 'blue':
        if stalemate['blue'] == 1:
            return True

        if best_choice == players['red']:
            if len(reachable_turn[player]) == 1:
                stalemate['blue'] = 1
                return True
            else:
                return False
                
    if player == 'green':
        if stalemate['green'] == 1:
            return True
        
        if best_choice == players['red'] or best_choice == players['blue']:
            if len(reachable_turn[player]) == 1:
                stalemate['green'] = 1
                return True
            else:
                return False

def choose_move(players, reachable_turn, player, best_choice):
    if player == 'blue':
        if best_choice == players['red']:
            # next best choice
            reachable = reachable_turn[player]
            index_best_choice = reachable.index(best_choice)
            if index_best_choice != len(reachable)-1:
                return reachable[index_best_choice + 1]
            else:
                return reachable[index_best_choice - 1]
        
        else: 
            return best_choice
    
    elif player == 'green':
        if best_choice == players['red'] or best_choice == players['blue']:
            # next best choice
            reachable = reachable_turn[player]
            index_best_choice = reachable.index(best_choice)
            if index_best_choice != len(reachable)-1:
                return reachable[index_best_choice + 1]
            else:
                return reachable[index_best_choice - 1]
        
        else: 
            return best_choice

    else:
        return best_choice

def find_neighbors(board,node):
    incident_nodes = []
    ugly_list = board.get_adjacency()[node]
    for i in range(len(ugly_list)):
        if ugly_list[i] == 1:
            incident_nodes.append(i)
    
    return incident_nodes
    