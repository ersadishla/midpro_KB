# Stores the children of a board
boardChild = dict()
status = dict()

# Function to convert from board to number representation
def convertToNumber(arr, n):
    res = 0
    rep = -1
    for i in range(0,n):
        for j in range(0,n):
            cell = arr[i][j]
            if cell is 'X': rep = 2
            elif cell is 'O': rep = 3
            elif cell is '-': rep = 0
            res = res | (rep << (i*(n*2) + j*2))
    return res

# Function to convert number representation to board
def convertToBoard(num, n):
    arr = [0] * n
    for i in range(0,n):
        temp = list()
        for j in range(0,n):
            key = num & 3
            if key is 0: temp.append('-') # Empty cell is filled with '-'
            elif key is 2: temp.append('X')
            elif key is 3: temp.append('O')
            num >>= 2
        arr[i] = temp
    return arr

# Check whether the board is full
def isFull(node):
    a = node.bitmask
    for i in range(0,node.size**2):
        if a & 2 == 0: return False
        a >>= 2
    return True

# Check for horizontal
def checkHorz(node):
    comp = 0
    x = (1<<(node.size*2)) - 1
    for i in range(0,node.size):
        comp = (comp << 2) | (2 if node.next_turn == -1 else 3)
    for i in range(0, node.size):
        if (node.bitmask >> (i*node.size*2)) & x == comp: return True
    return False

# Check for vertical
def checkVert(node):
    comp = 0
    x = 0
    for i in range(0, node.size):
        comp = (comp << (node.size*2)) | (2 if node.next_turn == -1 else 3)
        x = (x << (node.size*2)) | 3
    for i in range(0, node.size):
        if (node.bitmask & x) == comp: return True
        x <<= 2
        comp <<= 2
    return False

# Check for diagonal
def checkDiag(node):
    comp1 = (2 if node.next_turn == -1 else 3)
    x1 = 3
    comp2 = ((2 if node.next_turn == -1 else 3) << (2*node.size)-2)
    x2 = 3 << ((2*node.size)-2)

    for i in range(0, node.size-1):
        comp1 = (comp1 << ((2*node.size)+2) | (2 if node.next_turn == -1 else 3))
        x1 = (x1 << ((2*node.size)+2) | 3)
        comp2 = (comp2 << ((2*node.size)-2) | (2 if node.next_turn == -1 else 3) << ((2*node.size)-2))
        x2 = (x2 << ((2*node.size)-2) | 3 << ((2*node.size)-2))

    if (node.bitmask & x1) == comp1: return True
    if (node.bitmask & x2) == comp2: return True
    return False

# Check whether the board are termination state
def checkTermination(node):
    if checkHorz(node) is True:
        return 1
    if checkVert(node) is True:
        return 1
    if checkDiag(node) is True:
        return 1
    if isFull(node) is True: return 0
    return -1

def traverse(node, depth):
    if checkTermination(node) == 1:
        return
    if checkTermination(node) == 0:
        return
    node.generateChild()
    for child in boardChild[node.bitmask]:
        traverse(child, depth+1)

# do the minimax with alpha-beta pruning
def minimax(node, alpha, beta):
    if checkTermination(node) == 1:
        return (1 if node.next_turn == -1 else -1)
    if checkTermination(node) == 0:
        return 0

    if node.next_turn is 1:
        node.generateChild()
        c = False
        for i in boardChild[node.bitmask]:
            i.alpha = 'anjg'
            if c is True:
                #doPrunning(i)
                status[(i.bitmask, i.parent)] = 1; # CHANGED #
                return alpha
            alpha = max(alpha, minimax(i, alpha, beta))
            
            if beta < alpha:
                c = True
        return alpha

    if node.next_turn is -1:
        node.generateChild()
        c = False
        for i in boardChild[node.bitmask]:
            i.beta = 'bgst'
            if c is True:
                #doPrunning(i)
                status[(i.bitmask, i.parent)] = 1; # CHANGED #
                return beta
            beta = min(beta, minimax(i, alpha, beta))
            if beta < alpha:
                c = True
        return beta

def doPrunning(node):
    status[(node.bitmask, node.parent)] = 1
    if checkTermination(node) == 1:
        status[(node.bitmask, node.parent)] = 1
        return
    if checkTermination(node) == 0:
        status[(node.bitmask, node.parent)] = 1
        return

    node.generateChild()
    for each in boardChild[node.bitmask]:
        doPrunning(each)
