#Algo A*

import math

class plus_court_chemin:
    def __init__(self, plan):
        self.plan = plan
        self.height = len(plan)
        self.width = len(plan[0])
        
        self.find_start_end()
        self.x_start, self.y_start = self.start
        self.x_end, self.y_end = self.end
        
        self.create_heuristice_map()
        self.algo_main()
          
    def find_start_end(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.plan[i][j] == -1:
                    self.start = (i,j)
                if self.plan[i][j] == -2:
                    self.end = (i,j)

    def get_distance(self, x1, y1, x2, y2): #retourner la distance entre pos (x1, y1) et pos (x2, y2). Attention: la variation selon x,y doit etre entre [-1,1]
        value_at_start = self.plan[x1][y1]
        value_at_end   = self.plan[x2][y2]
        
        if value_at_start < 0: value_at_start = 1
        if value_at_end < 0: value_at_end = 1
        
        varie_x = x2 - x1; varie_y = y2 - y1
        distance = math.sqrt( varie_x ** 2 + varie_y ** 2 ) * 0.5 * (value_at_start + value_at_end)
        return distance  

    def heuristic_from_point(self, x, y): #retourner la fonction heuristique a la position "pos", c'est la distance d'oiseau entre cette pos et la pos fini
        return self.get_distance(x, y, self.x_end, self.y_end)        

    def create_heuristice_map(self):
        self.h_map = []
        for i in range(self.height):
            h_line = []
            for j in range(self.width):
                h_line.append( self.heuristic_from_point(i, j) )
            self.h_map.append( h_line.copy() )
            
    def out_of_plan(self, x, y):
        if ((x > -1) and (x < self.height)) and ((y > -1) and (y < self.width)):
            return False
        return True  
               
    def pop_min_heuristic(self):
        pos_min, dis_h_min = None, math.inf
        for (pos, distance) in self.to_explore.items():
            distance_h = distance + self.h_map[ pos[0] ][ pos[1] ]
            if distance_h < dis_h_min:
                pos_min, dis_h_min = pos, distance_h
        dis_min = self.to_explore.pop(pos_min) 
        
        return (pos_min, dis_min)
            
    def dict_pos_can_get(self, pos):
        x = pos[0]; y = pos[1]
        l_pos = {}
        for varie_x in [-1, 0, 1]:
            for varie_y in [-1, 0, 1]:
                new_x = x + varie_x; new_y = y + varie_y
                if ((varie_x != 0) or (varie_y != 0)) and not self.out_of_plan(new_x, new_y):
                    if self.plan[new_x][new_y] != 0:
                        l_pos[ (new_x, new_y) ] = self.get_distance(x, y, new_x, new_y)
        return l_pos
               
    def algo_main(self):    
        self.to_explore = { self.start : 0 }
        self.way = { self.start : [self.start] }
        alre_collected = {}
        is_collected_end = False
        
        while len(self.to_explore) != 0 and not is_collected_end:
            pos_explore, distance = self.pop_min_heuristic()
            alre_collected[ pos_explore ] = distance
            dict_pos_get = self.dict_pos_can_get(pos_explore)
            
            for pos_get, longer in dict_pos_get.items():
                distance_need = distance + longer
                if (pos_get not in alre_collected) and (distance_need < self.to_explore.get(pos_get, math.inf)):
                    self.to_explore[pos_get] = distance_need
                    self.way[pos_get] = self.way[pos_explore] + [pos_get]
                    
                    if pos_get == self.end:
                        is_collected_end = True
                        alre_collected[ pos_get ] = distance_need
                        
        self.shortest_way = self.way.get(self.end, [])
        self.shortest_distance = alre_collected.get(self.end, [])
          
    def print_map(self, plan):
        for i in range(len(plan)):
            for j in range(len(plan[0])):
                print(f'{plan[i][j]:.2f}', end=' ')
            print()      
        print()    
            
if __name__ == "__main__":
    level = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 0, 0, 0, 0, 0], [-1, 1, 0, 1, 0, 1, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 1, 0, 0, 0], [0, 2, 1, 1, 0, 0, 2, 1, 0, 0], [0, 1, 0, 1, 0, 0, 1, 1, 0, 0], [0, 1, 0, 1, 0, 0, 1, 1, 2, 0], [0, 1, 0, 2, 0, 0, 1, 1, 1, -2], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    algo = plus_court_chemin(level)
    print(algo.shortest_distance)
    print(algo.shortest_way)