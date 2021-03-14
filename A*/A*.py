import copy

initial_box = [[1, 2, 3],
               [4, 0, 5],
               [6, 7, 8]]

final_box = [[4, 1, 2],
             [6, 5, 3],
             [0, 7, 8]]

nbrs = ["left", "right", "top", "bottom"]

class Graph:

    def __init__(self):
        self.parent = []
        self.path = []

    def Shift(self, s, b):
        box = copy.deepcopy(b)
        pos = -1
        for i in range(len(box)):
            for j in range(len(box[i])):
                if box[i][j] == 0:
                    pos = [i, j]

        x, y = pos
        if s == "left" and y-1>=0:
            box[x][y], box[x][y-1] = box[x][y-1], box[x][y]
        elif s == "right" and y+1<=2:
            box[x][y], box[x][y+1] = box[x][y+1], box[x][y]
        elif s == "top" and x-1>=0:
            box[x][y], box[x-1][y] = box[x-1][y], box[x][y]
        elif s == "bottom" and x+1<=2:
            box[x][y], box[x+1][y] = box[x+1][y], box[x][y]
        else:
            return -1
        return box
 
    # number of mismatched elements
    def H1(self, box_1, box_2):
        mismatched = 0
        for x in range(len(box_1)):
            for y in range(len(box_1)):
                if box_1[x][y] != box_2[x][y]:
                    mismatched += 1
        return mismatched
    
    # distance of elements from the final box
    def H2(self, box_1, box_2):
        distance = 0
        for x1 in range(len(box_1)):
            for y1 in range(len(box_1)):
                if box_1[x1][y1] != box_2[x1][y1]:
                    found = False
                    i,j = -1,-1
                    for x2 in range(len(box_2)):
                        for y2 in range(len(box_2)):
                            if box_1[x1][y1] == box_2[x2][y2]:
                                found = True
                                i,j = x2,y2
                                break
                        if found:
                            break

                    distance += abs(x1-i) + abs(y1-j)
        return distance

    # Astar function to implement A* Algorithm
    def Astar(self, s_box, f_box, func):
        self.parent = []
        self.path = []

        open_l = []
        close_l = []

        open_l.append([0 + func(s_box, f_box), s_box])
 
        while open_l:
            
            pop = min(open_l)
            open_l.remove(pop)

            close_l.append(pop)
            f_val, curr_box = pop
            
            if curr_box == f_box:
                self.backtrack(f_box, s_box)
                return f_val, len(open_l) + len(close_l)

            for i in nbrs:
                nb_box = self.Shift(i,curr_box)
                
                if nb_box != -1:
                    f_new = (f_val - func(curr_box, f_box) + 1) + func(nb_box, f_box)
                    if nb_box == f_box:
                        self.parent.append([nb_box, curr_box])                        
                        self.backtrack(f_box, s_box)
                        return f_new, len(open_l) + len(close_l)

                    elif nb_box not in close_l:
                        fi = -1
                        for i in range(len(open_l)):
                            if open_l[i][1] == nb_box:
                                fi = open_l[i][0]
                                break
                        
                        if nb_box not in open_l:
                            open_l.append([f_new, nb_box])
                            self.parent.append([nb_box, curr_box])
                        
                        elif f_new < fi:
                            for e in range(len(open_l)):
                                if open_l[e][1] == nb_box:
                                    open_l[e][0] = f_new
                                    break

                            for e in range(len(self.parent)):
                                if self.parent[e][0] == nb_box:
                                    self.parent[e][1] = curr_box
                                    break
        
        return -1, len(open_l) + len(close_l)

    def backtrack(self, final, initial):
        self.path.append(final)
        while self.path[-1] != initial:
            for back in self.parent:
                if back[0] == self.path[-1]:                        
                    p = back[1]
                    break
            self.path.append(p)
        self.path.reverse()
 

if __name__ == "__main__":
    g = Graph()
    depth, nodes = g.Astar(initial_box, final_box, g.H1)
    print("Final node present at depth " + str(depth) + " and the number of nodes generated are " + str(nodes))
    print("The path traverse is:")
    for i in g.path:
        print(i)
