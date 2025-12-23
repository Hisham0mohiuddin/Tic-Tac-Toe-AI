import numpy as np
import pickle 


class Game:
    def __init__(self,p1,p2):
        self.board = np.zeros((3,3), dtype=int)
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        self.playerSymbol = 1

    def getHash(self):
        return str(self.board.reshape(9))
    
    def showBoard(self):
        symbols = {1: "X", -1: "O", 0: "."}
        for i in range(3):
            print(" ".join(symbols[self.board[i, j]] for j in range(3)))
        print()

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
    def reset(self):
        self.board = np.zeros((3,3), dtype=int)
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1


    def play(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                # check board status if it is end

                win = self.winning()
                if win is not None:
                    # self.showBoard()
                    # ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.winning()
                    if win is not None:
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    def playOneGame(self):
        self.reset()
        self.isEnd = False

        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
            self.updateState(action)
            self.showBoard()

            win = self.winning()
            if win is not None:
                self.giveReward()
                break

            # Player 2
            positions = self.availablePositions()
            action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
            self.updateState(action)
            self.showBoard()

            win = self.winning()
            if win is not None:
                self.giveReward()
                break




class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value
    def getHash(self, board):
        return str(board.reshape(9))

    def reset(self):
        self.states = []

    def addState(self, state):
        self.states.append(state)

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
            fr = open(file, 'rb')
            self.states_value = pickle.load(fr)
            fr.close()

    def chooseAction(self,positions,current_board,symbol):
        if np.random.uniform(0,1)<=self.exp_rate:
            indx = np.random.choice(len(positions))
            action = positions[indx]

        else:
            value_max = -1e9
            for p in positions:
                next_board = current_board.copy()
                next_board[p]= symbol 
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                if value >= value_max:
                    value_max = value
                    action = p
        return action
    
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]


if __name__ == "__main__":

    p1 = Player("p1", exp_rate=0.3)
    p2 = Player("p2", exp_rate=0.3)

    game = Game(p1, p2)

    print("Training...")
    game.play(rounds=20000)

    # turn off exploration
    p1.exp_rate = 0
    p2.exp_rate = 0

    print("\nLearned gameplay:\n")
    game.playOneGame()