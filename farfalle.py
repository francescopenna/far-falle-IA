from igraph import *
import random
from Utility import *
from tree import DynamicTree
from Falla import Falla

board = Graph()
create_board(board)

#---------------------------------------- START OF THE GAME ----------------------------------------
players = {'red': 0, 'blue': 36, 'green': 44}
stalemate = {'red': 0, 'blue': 0, 'green': 0}
red = 0
blue = 36
green = 44

for i in range(26):
	continue_game = 0
	print()
	print('######################################### TURNO ', i+1,'#########################################')
	# inizialization of maxn tree
	maxn = DynamicTree()
	reachable_turn = {}
	falle_turn = []
	stale_turn = {}

	for key in players:
		print(key, ' is playing, starting from: ', players[key])
		# select all nodes with distance = 1, that i can still walk on and only if the connecting edge is empty
		reachable = [
					element for element in range(len(board.get_adjacency()[players[key]])) 
									if board.get_adjacency()[players[key]][element] != 0 
									and len(board.vs[element]['list_walk']) < board.vs[element]['n_color']
									and board.es[board.get_eid(players[key],element)]['color'] == ''
									and board.vs[element]['occupied'] == 0
					]

		# detect stalemate
		if len(reachable) == 0: #or (len(reachable) == 1 and reachable[0] == players[key]):
			print('Player ', key, 'is in a stalemate.')
			print()
			# guardaci bene
			reachable_turn[key] = [players[key]]
			stalemate[key] = 1
			#del players[key]
			#break

		elif stalemate[key] == 1:
			reachable_turn[key] = [players[key]]

		else:
			#------------------------------------- algoritmo di matte per checking di falle <3 -------------------------------------
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
			#		   incident_nodes_player:  [2]
			# 		   candidates:  [[1]]
			#		   reachable nodes from 4 not visited yet: [1, 3, 5, 7, 8]
			# since 1 is conteined in the candidates and in the latter list we check the 
			# corrispondent index of the sublist in incident_nodes_player and find 
			# the last element of the falla (red, incident_node, reachable/candidate)
			for reachable_node in reachable:
				for sub_list in candidates:
					for candidate in sub_list:
						if candidate == reachable_node:
							print('a move to ', reachable_node, ' would create a FALLA with ', 
									incident_nodes_player[candidates.index(sub_list)], ' starting from ', players[key])
							# order in which a falla is represented: (current position, node already visited, node to reach next)
							# assignment of points: if all nodes are in the region gray, we give them 2 points, 
							# if at least one node is in red, we assign 1 point, else 3 (we are in an opponent's region)
							if board.vs[players[key]]['region'] == 'w' and board.vs[incident_nodes_player[candidates.index(sub_list)]]['region'] == 'w' and board.vs[reachable_node]['region'] == 'w':
								falle_turn.append(Falla(key, reachable_node, (players[key], incident_nodes_player[candidates.index(sub_list)], reachable_node), 2))
							elif board.vs[players[key]]['region'] == key or board.vs[incident_nodes_player[candidates.index(sub_list)]]['region'] == key or board.vs[reachable_node]['region'] == key:
								falle_turn.append(Falla(key, reachable_node, (players[key], incident_nodes_player[candidates.index(sub_list)], reachable_node), 1))
							else:
								falle_turn.append(Falla(key, reachable_node, (players[key], incident_nodes_player[candidates.index(sub_list)], reachable_node), 3))
			#-----------------------------------------------------------------------------------------------------------------------
			reachable_turn[key] = reachable 
			#------------------------------------- algoritmo di matte per checking di stalli <3 ------------------------------------
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
			#-----------------------------------------------------------------------------------------------------------------------

	for key in reachable_turn:
		print(key,'->',reachable_turn[key])

	if stalemate['red'] == 1 and stalemate['blue'] == 1 and stalemate['green'] == 1:
		print('THE GAME IS OVER!')
		print()
		break
	
	maxn.create_children(reachable_turn, falle_turn, stale_turn)
	best_moves = maxn.solve_tree(maxn, board, players, stalemate)
	#maxn.display_data()

	#best_moves = maxn.find_equilibrium()
	# needed for the last turn of the game
	if best_moves == False:
		print('THE GAME IS OVER!')
		print()
		break
	#maxn.display_data()

	#print(best_moves)
	# update the position of the players in the board -> move always to the best move
	for key in reachable_turn:
		for val in best_moves:
			val = val.replace('(','')
			val = val.replace(')','')
			val = val.split(',')
			val[0] = val[0].replace("'","")
			val[0] = val[0].replace("'","")
			if val[0] == key:
				val[1] = int(val[1])
				
				check = check_stalemate(players, reachable_turn, stalemate, val[0], val[1])
				
				if check:
					continue
				
				best_choice = choose_move(players, reachable_turn, val[0], val[1])
				edge_index = board.get_eid(players[key],best_choice)
				board.es[edge_index]['color'] = key

				board.vs[players[key]]['occupied'] = 0
				players[key] = best_choice
				board.vs[players[key]]['list_walk'].append(key)
				board.vs[players[key]]['occupied'] = 1
				print(key, ' ends its turn at: ', players[key])
				print('')

				