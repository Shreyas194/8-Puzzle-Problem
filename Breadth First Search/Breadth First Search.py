import copy

initial_box = [[1, 2, 3],
               [4, 0, 5],
               [6, 7, 8]]

final_box = [[4, 1, 2],
             [6, 5, 3],
             [0, 7, 8]]

# Movement to '0' element denoted as neighbours
nbrs = ["left", "right", "top", "bottom"]

class Graph:

    def __init__(self):
        self.parent = []
        self.path = []

    # Shift function to generate the child of the current state/node
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
    
    # BFS function to implement Breadth First Search
    def BFS(self, s_box, f_box):
 
        self.parent = []
        self.path = []
        
        # mark all the vertices as not visited
        visited = []
 
        # Create a queue for BFS
        queue = []
 
        # mark the source node as visited and enqueue it
        queue.append((s_box, 0))
        visited.append(s_box)
 
        while queue: 
            # dequeue a vertex from queue
            curr_box, curr_depth = queue.pop(0)
 
            for i in nbrs:
                nb_box = self.Shift(i,curr_box)
                if nb_box != -1:
                    if nb_box not in visited:                     
                        queue.append((nb_box, curr_depth + 1))
                        visited.append(nb_box)
                        self.parent.append([nb_box, curr_box])
                        if nb_box == f_box:
                            self.backtrack(f_box, s_box)
                            return curr_depth + 1
        
        return -1

    # backtrack function to traces back the path
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
    depth = g.BFS(initial_box, final_box)
    print("Final node present at depth " + str(depth))
    print("The path traverse is:")
    for i in g.path:
        print(i)
