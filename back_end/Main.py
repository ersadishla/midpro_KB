import Board
import json
import sys
import time

start = time.time()

class Node:
    def __init__(self, board, parent, next_turn, size):
        self.bitmask = board
        self.parent = parent
        self.next_turn = next_turn
        self.size = size
        self.alpha = "unupdated"
        self.beta = "unupdated"

    def generateChild(self):
        # if Board.checkTermination(self) == 1 or Board.checkTermination(self) == 0:
        #     return
        next = 2 if self.next_turn == 1 else 3
        children = list()
        for i in range(0, self.size**2 * 2, 2):
            if (self.bitmask >> i) & 3 == 0:
                temp = self.bitmask | (next << i)
                children.append(Node(temp, self.bitmask, self.next_turn*-1, self.size))
        Board.boardChild[self.bitmask] = children

    def __str__(self):
        a = Board.convertToBoard(self.bitmask, self.size)
        return str(a)

    bitmask = -1
    size = -1
    parent = -1
    next_turn = -1
    heur = -1
    alpha = -1
    beta = -1

state = json.loads(sys.argv[1])
size = json.loads(sys.argv[2])
next_t = json.loads(sys.argv[3])

obj = Node(Board.convertToNumber(state,size), 12, next_t, size)
Board.minimax(obj, -1000, 1000)
Board.traverse(obj,0)

end = time.time()

timeNeeded = end - start

parent = dict()

def createJSON(node):
    child = list()
    # print(parpar, node.bitmask)
    try:
        if (node.bitmask, node.parent) not in Board.status.keys(): # ADDITION #
            node.generateChild()
            for eachild in Board.boardChild[node.bitmask]:
                if Board.checkTermination(eachild) == 1:
                    pr = "prunned" if (eachild.bitmask, eachild.parent) in Board.status.keys() else "normal"
                    child += [{"id": str(eachild.bitmask), "time": str(timeNeeded), "children": "", "status": pr, "expand": 0, "alpha": str(eachild.alpha), "beta": str(eachild.beta) }]
                    continue
                child += [createJSON(eachild)]
    except(IndexError):
        return
    pr = "prunned" if (node.bitmask, node.parent) in Board.status.keys() else "normal"
    return {"id": str(node.bitmask), "time": str(timeNeeded), "children": child, "status": pr, "expand": 0, "alpha": str(node.alpha), "beta": str(node.beta) }

parent = createJSON(obj)

print(json.dumps(parent))
sys.stdout.flush()
