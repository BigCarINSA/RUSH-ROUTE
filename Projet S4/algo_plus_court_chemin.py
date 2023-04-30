import math

class plus_court_chemin:
    def __init__(self, plan):
        self.plan = plan
        self.height = len(plan)
        self.width = len(plan[0])
        
        self.find_start_end()
        self.x_start, self.y_start = self.start
        self.x_end, self.y_end = self.end
        
        self.reset_distance_map() 
        self.algo_main()
        self.shortese_distance = self.distance_map[self.x_end][self.y_end]
        self.way = self.way_map[self.x_end][self.y_end]    

    def find_start_end(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.plan[i][j] == -1:
                    self.start = (i,j)
                if self.plan[i][j] == -2:
                    self.end = (i,j)

    def reset_distance_map(self):       
        self.distance_map = []
        self.way_map = {}
        
        for i in range( self.height ):
            distance_map_line = []
            self.way_map[i] = {}
            
            for j in range( self.width ):
                distance_map_line.append(-1.0)
                self.way_map[i][j] = []
                
            self.distance_map.append( distance_map_line.copy() )   

        self.distance_map[self.x_start][self.y_start] = 0.0
        self.way_map[self.x_start][self.y_start].append( (self.x_start, self.y_start) )  
            
    def out_of_plan(self, x, y):
        if ((x > -1) and (x < self.height)) and ((y > -1) and (y < self.width)):
            return False
        return True
            
    def change_distance_around(self, x, y):
        count = 0
        for varie_x in range(-1,2):
            for varie_y in range(-1,2):
                x_new = x + varie_x
                y_new = y + varie_y
                
                if (not self.out_of_plan( x_new, y_new ) ) and (self.plan[x_new][y_new] != 0):
                    value_at_pos = self.plan[x][y]
                    value_at_new_pos = self.plan[x_new][y_new]
                    
                    if value_at_pos < 0: value_at_pos = 1
                    if value_at_new_pos < 0: value_at_new_pos = 1
                    distance = math.sqrt( varie_x ** 2 + varie_y ** 2 ) * 0.5 * (value_at_pos + value_at_new_pos)  
                    distance_at_new = self.distance_map[x][y] + math.sqrt( varie_x ** 2 + varie_y ** 2 ) * 0.5 * (value_at_pos + value_at_new_pos)
                    
                    if (self.distance_map[x_new][y_new] == -1) or (self.distance_map[x_new][y_new] > distance_at_new):
                        self.distance_map[x_new][y_new] = distance_at_new   
                        self.way_map[x_new][y_new] = self.way_map[x][y] + [ (x_new, y_new) ]
                        count += 1
        return(count)

    def print_map(self, plan):
        for i in range(len(plan)):
            for j in range(len(plan[0])):
                print(f'{plan[i][j]:.2f}', end=' ')
            print()      
        print()      
               
    def algo_main(self):    
        count = 1
        while count != 0:
            count = 0
            for x in range( self.height ):
                for y in range( self.width ):
                    if self.distance_map[x][y] != -1:
                        count += self.change_distance_around(x, y)
        
if __name__ == "__main__":
    level = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 0, 0, 0, 0, 0], [-1, 1, 0, 1, 0, 1, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 1, 0, 0, 0], [0, 2, 1, 1, 0, 0, 2, 1, 0, 0], [0, 1, 0, 1, 0, 0, 1, 1, 0, 0], [0, 1, 0, 1, 0, 0, 1, 1, 2, 0], [0, 1, 0, 2, 0, 0, 1, 1, 1, -2], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    algo = plus_court_chemin(level)
    print(algo.shortese_distance)