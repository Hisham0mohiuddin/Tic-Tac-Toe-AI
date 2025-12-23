import numpy as np
board = np.zeros((3,3),dtype=int)

class Game:
    def __init__(self,p1,p2):
        self.board = np.zeros(3,3)
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        self.playerSymbol = 1

    def getHash(self):
        self.board = str(self.board.reshape(3*3))
        return self.board
    
    
    def availablePositions(self):
        positions = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions

    def updateState(self, position):
        self.board[position] = self.playerSymbol
        # switch to another player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1
        
    # changing the manual looping to just cheking the sum
    def winning(self):
        if np.any(np.sum(self.board,axis=0)==3):
            return 1
        if( np.any(np.sum(self.board,axis=0) == -3)):
            return -1
        if np.any(np.sum(self.board,axis=1)==3) :
            return 1
        if np.any(np.sum(self.board,axis=1) == -3):
           return -1
        
        # diagonals 
        if (np.trace(self.board))==3 or (np.trace(np.fliplr(self.board)))==3:
            return 1
        if (np.trace(self.board))==-3 or (np.trace(np.fliplr(self.board)))==-3:
            return -1
        
        # tie
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # not end
        self.isEnd = False
        return None
    
    def giveReward(self):
        result = self.winning()
        # backpropagate reward
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)

print("""
0 1 2 
3 4 5
6 7 8
""")
marker = 1
symbols = {
    1: "X",
    -1: "O",
    0: "E"
}
while True:
    print(f"as the {symbols[marker]} what do u want to play:")
    c = int(input("enter the index no of what u want to select: "))
    
    row_in = c // 3
    col_in = c % 3
    if(board[row_in][col_in]!= 0):
        print("cell used already")
        continue
    board[row_in][col_in]=marker

    if(winning(board)):
        print(f"player {symbols[marker]} has won")
        break
    for i in board:
        print(i)
        print("",end="")
    marker *=-1
