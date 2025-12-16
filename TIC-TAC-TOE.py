
print("hello world")


board = [["E","E","E"],["E","E","E"],["E","E","E"]]
winning = [
    [0,1,2],[3,4,5],[6,7,8],  # rows
    [0,3,6],[1,4,7],[2,5,8],  # cols
    [0,4,8],[2,4,6]           # diagonals
]

print("""
0 1 2 
3 4 5
6 7 8
""")
marker = "X"
while True:
    print(f"as the {marker} what do u want to play:")
    c = int(input("enter the index no of what u want to select: "))
    
    row_in = c // 3
    col_in = c % 3
    
    board[row_in][col_in]=marker
    wins= True
    # now to check if tying or winning 
    for i in winning:
        wins= True
        for j in i :
            r_in  = int(j//3)
            c_in = int(j%3)
            if board[r_in][c_in]==marker:
                continue
            else:
                wins = False
        if(wins):
            print("U win yay")
            break
    if(wins):
        break
    for i in board:
        print(i)
        print("",end="")
    if marker =="X":
        marker = "O"
    else:
        marker = "X"