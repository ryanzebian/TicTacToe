### Pytthon X-O game
import random
import os.path
board = [] #ex. [['x','o',' '],[' ',' ',' '],['o','x',' ']]
roundCount = 0
printWhenMark = False
winnerPlayerType = ''

def main():
    initBoard(3)
    mark(0,0,'x')
    mark(0,1,'O')
    mark(0,2,'x')

    mark(1,0,'O')
    mark(1,1,'x')
    mark(1,2,'O')

    mark(2,0,'x')
    mark(2,1,'O')
    mark(2,2,'O')

    printGame(board)
    result = checkPlayerWon()
    print('Player ', winnerPlayerType,' ',result)
    
def initBoard(size):
    global board
    board = []
    for r in range(size):
        columns = []
        for c in range(size):
            columns.append(' ')
        board.append(columns)
def printGame(b = None):
    if b == None:
        b = board
        
    for r in range(len(b)):
        print(*b[r],sep='\t|')
        if(r == len(b)-1):
            continue
        print('-'*7,'|','-'*5,'|','-'*7)
    print()

def mark(row=int,col=int,char=str):
    board[row][col]=char
    global roundCount
    global winnerPlayerType
    roundCount+=1
    if(printWhenMark):
        printGame(board)
    if(checkPlayerWon()):
        print("Game Over! Winner is ",winnerPlayerType)
    if(roundCount >= 9 and winnerPlayerType == ''):
        winnerPlayerType = 'No Winner'
        print("Game Over! ",winnerPlayerType)

def checkPlayerWon():
    #find r in a row(vertical, Horizental, or Diagonal)
    return checkHorizental() or checkVertical() or checkDiagonal()

def checkHorizental(): 
    isWinner = True

    for r in range(len(board)):
        isWinner = True
        tempRow = 'startRow'
        for c in range(len(board[r])):
            value = board[r][c]
            if((value != tempRow and tempRow !='startRow') or value == ' '):
                isWinner = False
                break
            tempRow = value
        if(isWinner):
            print('is Winner:', isWinner)
            global winnerPlayerType
            winnerPlayerType = tempRow
            break

    return isWinner
            
def checkVertical():
    isWinner = True
    for c in range(len(board[0])):
        isWinner = True
        tempCol = 'startCol'	        
        for r in range(len(board)):
            value = board[r][c]
            if((value != tempCol and tempCol !='startCol') or value == ' '):
                       isWinner = False
                       break
            tempCol = value
        if(isWinner):
            global winnerPlayerType
            winnerPlayerType = tempCol
            break
    return isWinner
            
def checkDiagonal():
    isWinner = True
    tempCell = 'start'
    global winnerPlayerType

    #check \ diag
    for diag in range(len(board)):       
        value = board[diag][diag]
        if((value != tempCell and tempCell !='start') or value == ' '):
              isWinner = False
              break
        tempCell = value

    if(isWinner):
        winnerPlayerType = tempCell
        return isWinner
    
    #check / diag
    tempCell = 'start'
    rows = len(board)-1
    for diag in range(rows,-1,-1):
        value = board[diag][rows-diag]
        if((value != tempCell and tempCell !='start') or value == ' '):
              isWinner = False
              break
        tempCell = value
    
    if(isWinner):
        winnerPlayerType= tempCell
    return isWinner
    
    



class AI():
    weightOnWins = 0
    weightOnLoss = 1 #sum of weights should equal to 1

    
    def __init__(self,playerType):
        self.__playerType = playerType
        self.__currentMatch = {}
        self.__currentMoves = {}
        self.__movesMade = 0
        self.__fileName = ''
        self.__LoadLearningFile()
        
    def __LoadLearningFile(self):
        if(self.__playerType == 'x'):
            fileName = 'MachineLearningFileX'
        else:
            fileName = 'MachineLearningFileO'
        if(not os.path.isfile(fileName)):
            fw = open(fileName,'w')
            fw.write('{}')
            fw.close()
        f = open(fileName,'r')
        self.__logicTree = eval(f.readline())
        f.close()
        print(fileName)
        self.__fileName = fileName
        
    def analyzeBoard(self,board):
        moves = []
        for r in range(len(board)):
            for c in range(len(board[r])):
                if(self.__playerType == board[r][c]):
                    print('my move at row', r," Column",c)

                elif(board[r][c]== ' '):
                        print("possible move at row ",r," Column",c)
                        moves.append([r,c])
                else:
                    print('Not my move at row',r,' Column',c)
                          

        print(moves)

    def choicesForTurn(self):
        choices = []
        for r in range(len(board)):
            for c in range(len(board[r])):
                if(board[r][c] == ' '):
                    choices.append([r,c])
        return choices

    def stupidTurn(self):
        possibleMoves = self.choicesForTurn()
        choiceIndex = random.randint(0,len(possibleMoves)-1)
        row = possibleMoves[choiceIndex][0]
        col = possibleMoves[choiceIndex][1]
        mark(row,col,self.__playerType)
        
        print("Your Turn.")
        
    def Turn(self):
        #checkTwice For Matches Ended
        self.checkMatchEnded()
        possibleMoves = self.choicesForTurn()
        choiceIndex = random.randint(0,len(possibleMoves)-1)
        row = possibleMoves[choiceIndex][0]
        col = possibleMoves[choiceIndex][1]
        self.__currentMatch[self.__movesMade] =(tuple(tuple(rows) for rows in board))  
        mark(row,col,self.__playerType)
        self.__movesMade +=1        
        self.__currentMoves[self.__movesMade] = [row,col]
        self.checkMatchEnded()
    def move(self,r,c,playerType):
        self.__currentMatch[self.__movesMade] =(tuple(tuple(rows) for rows in board))  
        mark(r,c,self.__playerType)
        self.__movesMade +=1        
        self.__currentMoves[self.__movesMade] = [r,c]
        
    def checkMatchEnded(self):
        
        if(winnerPlayerType == ''):
            #The Game Has not Yet Ended
            print("Your Turn.")
            return False
        if(winnerPlayerType == "No Winner"):
            #The Game was a tie
            print("Tie Game: Well Played!")
            self.recordMatch(0,1,0)
        elif(winnerPlayerType == self.__playerType):
            #AI Won update the W/L ratio
            print("Victory!")
            self.recordMatch(1,0,0)
        else:
            #AI Lost update the W/L ratio
            print("I shall have my revenge!")
            self.recordMatch(0,0,1)

        raise Exception('End of Game')
    def recordMatch(self,win,draw,loss):
        #write to a file
        #sample {((' ', ' ', ' '), (' ', ' ', ' '), (' ', ' ', ' ')): {(1, 0): {'w': 1, 'd': 0, 'l': 0}}}
        #logicTree[scenario] = {(decision):{win:winRate,draw:drawRate,loss:lossRate}
        print('recording the match')

        #self__currentMatch -> One Turn before How the MatchBoard was 
        #self.__movesMade -> Total Number of Moves Made
        #self.__currentMoves -> row column of the moves made

        #Check the boarder Conditions Since Checking is Being done twice and their may be an issue with the index 

        #update the Logic Tree
        for i in range(self.__movesMade):
             row = self.__currentMoves[i+1][0]
             col = self.__currentMoves[i+1][1]
             boardScenario = self.__currentMatch[i]             
             if(boardScenario in self.__logicTree):
                 decisions = self.__logicTree[boardScenario]
                 movePlayed = (row,col)
                 if(movePlayed in decisions):
                    print('Move Played exists')
                    print(decisions[movePlayed])
                    winRate = decisions[movePlayed]
                    decisions[movePlayed]['w'] = winRate['w'] + win
                    decisions[movePlayed]['d'] = winRate['d'] + draw
                    decisions[movePlayed]['l'] = winRate['l'] + loss
                    
                    
                 else:
                    decisions[movePlayed] = {'w':win,'d':draw,'l':loss}
                    
             else:
                 self.__logicTree[boardScenario] = {(row,col):{'w':win,'d':draw,'l':loss}}   
                 
        #write to some file
        fr = open(self.__fileName,'w')
        fr.write(str(self.__logicTree))

    def CurrentMatchHistory(self):
        return self.__currentMatch
        
##run for testing
#initBoard(3)
#al = AI('x')
#al.Turn()
printGame()
def move(r,c,pType):
        mark(r,c,pType)
        al.Turn()
        printGame()

def save():
    al.recordMatch(0,0,1)

