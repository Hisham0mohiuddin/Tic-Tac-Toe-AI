import numpy as np
board = np.zeros((3,3),dtype=int)

# changing the manual looping to just cheking the sum
def winning(b):
    if np.any(np.sum(b,axis=0)==3) or np.any(np.sum(b,axis=0) == -3):
        return True
    elif np.any(np.sum(b,axis=1)==3) or np.any(np.sum(b,axis=1) == -3):
        return True
    
    # diagonals 
    if abs(np.trace(b))==3 or abs(np.trace(b.T))==3:
        return True
    
    return False

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