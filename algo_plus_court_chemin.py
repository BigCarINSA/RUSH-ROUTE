'''
    Algorith utilisé: A*
        - À chaque coordonnée x du labyrinthe, on definie une valeur heuristique h(x) qui est la distance à vol d'oiseau entre cette coordonnée x et la coordonnée finale x_end.
        - Au debut, on enregistre à la position de départ, le poids est h(x_start); tous les autres coordonnées sont infinites.
        - À chaque fois, on:
            + Choisit des noeuds x qui a le poids cumulé f(x) minimal (au debut, la liste contient seulement noeud de départ)
            + Calcule le poid nouveau des noeuds adjacents y de x (dans notre case, c'est les 8 coordonnées autours de x):
                    f(y) = p(y) + h(y) avec p(x) est la distance "plus court" on a trouvé pour aller à y
            + Si ces poids sont inférieurs à ses valeurs précédents, on les enregiste et les ajoute dans la file de priorité
          -> Notre boucle est terminée si la position x concide avec le position final ou la file de priorité est vide.  
          
    Pseudo-code:
    
    Input: un labyrinthe (liste 2D)
    Output: le plus court chemin entre position départ et position finale
    
    Algorithm:
        1. Trouver les valeurs heuristique h(x) à tout les coordonnées
        
        2. to_explore <- (la position de départ, 0) // on ajout la position de départ à to_explore avec son distance: 0
        3. way[position_depart] = position_depart   // on mise à jour le chemin à la position de départ 
        4. visited    <-  null
         
        5. while (to_explore n'est pas vide) and (on trouve pas la position finale):
        6.     x <- to_explore.pop_min()            //trouver la coordonnée x qui a le poids minimal dans to_explore
        7.     visited <- x                         //ajout la position x dans la liste collected 
        8.     if (x == position_finale):           //si x est la position finale, on sort le boucle 
        9.         exit_boucle
                   
        10.     for all y in adjecent(x):            //pour chaque noeud adjacente de x
        11.         if (y not in visited) and (distance(y) < ancienne_distance(y)): //si y n'est pas dans visited et y a le poids moins court 
        12.             to_explore <- y             //ajout la position y dans to_explore
        13.             updated_way[y]
    
'''
import math

class plus_court_chemin:
    '''
    Un class pour trouver le plus court du chemin dans un labyrinthe.
 
          
        :param: plan: liste 2D du labyrinthe qu'on veut trouver le plus court du chemin.       
    '''
    def __init__(self, plan):
        self.plan = plan
        self.height = len(plan)
        self.width = len(plan[0])
        
        #Trouver les positions de départ et finale
        self.find_start_end()
        self.x_start, self.y_start = self.start
        self.x_end, self.y_end = self.end
        
        #Creer le tableau d'heuristique
        self.create_heuristice_map()
        self.algo_main()
          
    def find_start_end(self): #Trouver les positions de départ et finale
        for i in range(self.height):
            for j in range(self.width):
                if self.plan[i][j] == -1:
                    self.start = (i,j)
                if self.plan[i][j] == -2:
                    self.end = (i,j)

    def get_distance(self, x1, y1, x2, y2):
        '''
        Trouver la distance entre pos (x1, y1) et pos (x2, y2). Cette distance dépende de la valeur du cellule en (x1, y1) et (x2, y2). 
        Attention: la variation selon x,y doit etre entre [-1,1]
            :Parameters: x1, y1, x2, y2 (Number): coordonnées des cellules
            :Returns: (Number): distance entre les deux coordonnées
        '''
        value_at_start = self.plan[x1][y1]
        value_at_end   = self.plan[x2][y2]
        
        if value_at_start < 0: value_at_start = 1
        if value_at_end < 0: value_at_end = 1
        
        varie_x = x2 - x1; varie_y = y2 - y1
        if (abs(varie_x) > 1) or (abs(varie_y) > 1): distance = math.sqrt( varie_x ** 2 + varie_y ** 2 ) * value_at_end
        else: distance = math.sqrt( varie_x ** 2 + varie_y ** 2 ) * 0.5 * (value_at_start + value_at_end)
        return distance  

    def heuristic_from_point(self, x, y): #retourner la fonction heuristique a la position "pos", c'est la distance d'oiseau entre cette pos et la pos fini
        return self.get_distance(x, y, self.x_end, self.y_end)        

    def create_heuristice_map(self): #Créer le tableau d'heuristique de chaque coordonnées
        self.h_map = []
        for i in range(self.height):
            h_line = []
            for j in range(self.width):
                h_line.append( self.heuristic_from_point(i, j) )
            self.h_map.append( h_line.copy() )
            
    def out_of_plan(self, x, y): #Verifie si la position (x,y) est dehors du labyrinthe
        if ((x > -1) and (x < self.height)) and ((y > -1) and (y < self.width)):
            return False
        return True  
               
    def pop_min_heuristic(self): 
        '''
        Trouver le position avec le plus petit heuristique de chaque noeud de la liste self.to_explore.
            :return: - un tuple (pos, distance) contient la position correspondant et sa distance
        '''
        pos_min, dis_h_min = None, math.inf
        for (pos, distance) in self.to_explore.items():
            distance_h = distance + self.h_map[ pos[0] ][ pos[1] ]
            if distance_h < dis_h_min:
                pos_min, dis_h_min = pos, distance_h
        dis_min = self.to_explore.pop(pos_min) 
        
        return (pos_min, dis_min)
            
    def dict_pos_can_get(self, pos):
        '''
        Trouver des noeuds adjacents de "pos" et les enregistre dans une dictionnaire où les valeurs sont des distances entre ces noeuds avec "pos"
        Les noeuds adjacents sont des coordonnées autours de "pos".
            :return: - un dictionnaire contenant les noeuds adjacents de "pos" 
        '''
        x = pos[0]; y = pos[1]
        l_pos = {}
        for varie_x in [-1, 0, 1]:
            for varie_y in [-1, 0, 1]:
                new_x = x + varie_x; new_y = y + varie_y
                if ((varie_x != 0) or (varie_y != 0)) and not self.out_of_plan(new_x, new_y):
                    if self.plan[new_x][new_y] != 0:
                        l_pos[ (new_x, new_y) ] = self.get_distance(x, y, new_x, new_y)
        return l_pos
               
    def algo_main(self):  #fonction principal de l'algorithme A*
        
        #  Au debut, on enregistre à la position de départ, le poids est h(x_start); tous les autres coordonnées sont infinites.
        self.to_explore = { self.start : 0 }
        self.way = { self.start : [self.start] }
        alre_collected = {}
        is_collected_end = False #Pour savoir si on a trouvé la position finale
        
        #boucle de l'algorithme
        while len(self.to_explore) != 0 and not is_collected_end:
            pos_explore, distance = self.pop_min_heuristic()  #Choisir des noeuds x qui a le poids cumulé f(x) minimal
            alre_collected[ pos_explore ] = distance          #Le poids est minimale donc la distance qu'on a trouvé est le plus court pour arriver à cette position 
            dict_pos_get = self.dict_pos_can_get(pos_explore) #Trouver les noeuds adjacents de "pos_explore"
            
            print(f'Position: {pos_explore}, distance: {distance}, heristice {self.h_map[ pos_explore[0] ][ pos_explore[1] ]}') #Affichage
            
            if pos_explore == self.end: #Si on a trouvé la position finale, on change is_collected_end pour terminer le boucle
                is_collected_end = True
            else:                       #Sinon on continue notre boucle            
                for pos_get, longer in dict_pos_get.items(): #Pour chaque noeud adjacente de "pos_explore"
                    distance_need = distance + longer        #On calcule la distance pour arriver à ce noeud adjacente en passant de "pos_explore"
                    if (pos_get not in alre_collected) and (distance_need < self.to_explore.get(pos_get, math.inf)): #Si le noeud adjacente n'a pas encore été trouvé ou si la distance est inférieur à l'ancienne distance
                        self.to_explore[pos_get] = distance_need      #On l'ajoute dans la pile de priorité
                        self.way[pos_get] = self.way[pos_explore] + [pos_get]
                    print(f'    Position: {pos_get}, distance: {distance_need}, heristic {self.h_map[ pos_get[0] ][ pos_get[1] ]}')

            
        self.shortest_way = self.way.get(self.end, [])
        self.shortest_distance = alre_collected.get(self.end, [])
          
    def print_map(self, plan): #fonction pour afficher le tableau de plan pour mieux controller
        for i in range(len(plan)):
            for j in range(len(plan[0])):
                print(f'{plan[i][j]:.2f}', end=' ')
            print()      
        print()                

if __name__ == "__main__":
    level = [[0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, -2, 1, 1, 1, 1, 0, 0, 0, 0, 2], [0, 0, 0, 0, 2, 1, 0, 2, 2, 2, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 2, 0], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 1], [1, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0], [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 1, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 1, 1, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 1, 1, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0], [0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, -1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    algo = plus_court_chemin(level)
    print(algo.shortest_distance)
    print(algo.shortest_way)