import pygame

# CONSTANTS
windowWidth = 1000
windowHeight = 583
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
RED = (255, 0, 0)
GREEN = (30, 180, 90)
BROWN = (64, 41, 10, 0.5)
# example: [[pieceNum, "G3", "D5", 0], ["A1", "G2", 5]]
# first one: move G3 to D5 and take nothing
# second one@ move A1 to G2 and take piece with index 5
global allPieceMoveList
allPieceMoveList = []

pawnW = (pygame.image.load(r'pawnW.jpg'))
pawnW = pygame.transform.scale(pawnW, (30, 30))
pawnB = (pygame.image.load(r'pawnB.jpg'))
pawnB = pygame.transform.scale(pawnB, (30, 30))
bishopW = (pygame.image.load(r'bishopW.jpg'))
bishopW = pygame.transform.scale(bishopW, (30, 30))
bishopB = (pygame.image.load(r'bishopB.jpg'))
bishopB = pygame.transform.scale(bishopB, (30, 30))
knightW = (pygame.image.load(r'knightW.jpg'))
knightW = pygame.transform.scale(knightW, (30, 30))
knightB = (pygame.image.load(r'knightB.jpg'))
knightB = pygame.transform.scale(knightB, (30, 30))
castleW = (pygame.image.load(r'castleW.jpg'))
castleW = pygame.transform.scale(castleW, (30, 30))
castleB = (pygame.image.load(r'castleB.jpg'))
castleB = pygame.transform.scale(castleB, (30, 30))
queenW = (pygame.image.load(r'queenW.jpg'))
queenW = pygame.transform.scale(queenW, (30, 30))
queenB = (pygame.image.load(r'queenB.jpg'))
queenB = pygame.transform.scale(queenB, (30, 30))
kingW = (pygame.image.load(r'kingW.jpg'))
kingW = pygame.transform.scale(kingW, (30, 30))
kingB = (pygame.image.load(r'kingB.jpg'))
kingB = pygame.transform.scale(kingB, (30, 30))

# PYGAME SETUP
pygame.init()
pygame.font.init()
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Chess')

# pieceID Syntax
# 0 = None
# 1 = PawnWhite
# 2 = BishopWhite
# 3 = KnightWhite
# 4 = CastleWhite
# 5 = QueenWhite
# 6 = KingWhite
# 7 = PawnBlack
# 8 = BishopBlack
# 9 = KnightBlack
# 10 = CastleBlack
# 11 = QueenBlack
# 12 = KingBlack


class Piece():
  def __init__(self, name, pieceNum, pieceID, position):
    self.name = name
    self.pieceNum = pieceNum
    self.pieceID = pieceID
    self.position = position
    self.taken = False
    self.drawMoves = False
    self.moveListUpdated = False

    # moveList will be in the syntax (numRight,numUp) aka (2,0) means 2 right, 0 up
    self.moveList = []
    self.numOfMoves = 0
    # is it white
    if (self.pieceID >= 1) and (self.pieceID <= 6):
      self.color = "white"
    else:
      self.color = "black"

  def update(self, boardObj):
    if (self.moveListUpdated == False):
      self.updateMoveList(boardObj)
      self.removeIllegalMoves(boardObj)
        #print(self.name, " MoveList (AFTER): ", self.moveList)
      self.moveListUpdated = True


  
  def removeIllegalMoves(self, boardObj):
    movesToRemove = []
    for move in self.moveList:
      if (self.isThisMoveGoingToCauseCheck(move, boardObj)):
        movesToRemove.append(move)
    for move in movesToRemove:
      self.moveList.remove(move)
  
  def isThisMoveGoingToCauseCheck(self, move, boardObj):
    # get this piece's position
    # apply the move to the position to get the new boardPosition
    # check if the new boardPosition is in check
    positionInLetterNum = self.position

    
    letterList = ["a", "b", "c", "d", "e", "f", "g", "h"]
  
    fromPos_index1 = letterList.index(positionInLetterNum[0].lower())
    # 3
    fromPos_index0 = 8 - int(positionInLetterNum[1])


    # move = d7
    toPos_index1 = letterList.index(move[0].lower())
    # 
    toPos_index0 = 8 - int(move[1])

    tempBoardObj = boardObj
    tempBoardPosition = tempBoardObj.boardPosition  

    indexValueMoveFrom = tempBoardPosition[fromPos_index0][fromPos_index1]
    indexValueMoveTo = tempBoardPosition[toPos_index0][toPos_index1]
    
    tempBoardPosition[toPos_index0][toPos_index1] = indexValueMoveFrom
    tempBoardPosition[fromPos_index0][fromPos_index1] = 0
    # print("CHANGED BOARD: ")
    # printBoard(tempBoardPosition)
    # print("ACTUAL BOARD NOW:")
    boardObj.setBoardPosition(boardObj.boardObjectList)
    self.position = positionInLetterNum
    # hotfix of the boardObj.boardPosition changing
    
    
    if (tempBoardObj.isItCheck(self.color, tempBoardPosition, tempBoardObj) == True):
      return True
    else:
      return False

  def tryMovingPiece(self, moveToPosition, boardObj):
    
    if moveToPosition.lower() in self.moveList:
      print("Move in moveList")
      # FIND THE PIEFCE AT THE LOCATION
      aPieceWasTaken = False
      for piece in boardObj.boardObjectList:
        if ((piece.position).lower() == moveToPosition.lower() and piece.taken == False):
          takenPiece = piece
          print(piece.name," HAS BEEN THE TAKE'TH")
          aPieceWasTaken = True
      if (aPieceWasTaken == True):
        takenPiece.taken = True
        allPieceMoveList.append([self.pieceNum, self.position.lower(), moveToPosition.lower(), takenPiece.pieceNum])
      else:
        allPieceMoveList.append([self.pieceNum, self.position.lower(), moveToPosition.lower(), 0])
    
      # Move the piece
      self.position = moveToPosition
      for piece in boardObj.boardObjectList:
        piece.moveListUpdated = False
        piece.update(boardObj)
      self.numOfMoves += 1

      boardObj.boardPositionIsUpToDate = False


  def doMoveList(self, boardObj, list):
  # get the piece at position in list[1]
  # move the piece to the location at list[2]

    for move in list:
      for piece in boardObj.boardObjectList:
        if piece.pieceNum == move[0]:
          piece.update(boardObj)
          piece.tryMovingPiece(move[2], boardObj)
          print("moved Piece")
  
  def updateMoveList(self, boardObj):
    position = self.position
    self.moveList = []

    # GOING STRAIGHT UP PIECES
    pieceIDUpList = [4, 5, 10, 11]
    if self.pieceID in pieceIDUpList:
      self.addMoveInDirectionUntillHitPieceOrOffBoard(0, 1, boardObj)

    # GOING STRAIGHT DOWN PIECES
    pieceIDDownList = [4, 5, 10, 11]
    if self.pieceID in pieceIDDownList:
      self.addMoveInDirectionUntillHitPieceOrOffBoard(0, -1, boardObj)

    # GOING RIGHT PIECES
    pieceIDRightList = [4, 5, 10, 11]
    if self.pieceID in pieceIDRightList:
      self.addMoveInDirectionUntillHitPieceOrOffBoard(1, 0, boardObj)

    # GOING LEFT PIECES
    pieceIDLeftList = [4, 5, 10, 11]
    if self.pieceID in pieceIDLeftList:
      self.addMoveInDirectionUntillHitPieceOrOffBoard(-1, 0, boardObj)

    # TOP LEFT GOING PIECES
    pieceIDUpLeftList = [2, 5, 8, 11]
    if self.pieceID in pieceIDUpLeftList:
      self.addMoveInDirectionUntillHitPieceOrOffBoard(-1, 1, boardObj)

    # TOP RIGHT GOING PIECES
    pieceIDUpRightList = [2, 5, 8, 11]
    if self.pieceID in pieceIDUpRightList:
      self.addMoveInDirectionUntillHitPieceOrOffBoard(1, 1, boardObj)

    # BOTTOM RIGHT GOING PIECES
    pieceIDBottomRightList = [2, 5, 8, 11]
    if self.pieceID in pieceIDBottomRightList:
      self.addMoveInDirectionUntillHitPieceOrOffBoard(1, -1, boardObj)

    # BOTTOM LEFT GOING PIECES
    pieceIDBottomLeftList = [2, 5, 8, 11]
    if self.pieceID in pieceIDBottomLeftList:
      self.addMoveInDirectionUntillHitPieceOrOffBoard(-1, -1, boardObj)

    # KING
    pieceIDKing = [6, 12]
    if self.pieceID in pieceIDKing:
      self.addMoveInOneDirection(1, 0, boardObj, True)
      self.addMoveInOneDirection(1, 1, boardObj, True)
      self.addMoveInOneDirection(1, -1, boardObj, True)
      self.addMoveInOneDirection(0, 1, boardObj, True)
      self.addMoveInOneDirection(0, -1, boardObj, True)
      self.addMoveInOneDirection(-1, 1, boardObj, True)
      self.addMoveInOneDirection(-1, 0, boardObj, True)
      self.addMoveInOneDirection(-1, -1, boardObj, True)

    # KNIGHTS
    pieceIDKnight = [3, 9]
    if self.pieceID in pieceIDKnight:
      self.addMoveInOneDirection(1, 2, boardObj, True)
      self.addMoveInOneDirection(2, 1, boardObj, True)
      self.addMoveInOneDirection(1, -2, boardObj, True)
      self.addMoveInOneDirection(2, -1, boardObj, True)
      self.addMoveInOneDirection(-1, -2, boardObj, True)
      self.addMoveInOneDirection(-2, -1, boardObj, True)
      self.addMoveInOneDirection(-1, 2, boardObj, True)
      self.addMoveInOneDirection(-2, 1, boardObj, True)
    
    # WHITE PAWN
    pieceIDWhitePawn = [1]
    if self.pieceID in pieceIDWhitePawn:
      # if never moved
      if self.numOfMoves == 0:
        # if nothing 1 infront
        if (self.isThisPositionEmpty(boardObj, 0, 1)):
          self.addMoveInOneDirection(0, 2, boardObj, False)
          
      # if the piece 1 up 1 left isn't empty
      if (not (self.isThisPositionEmpty(boardObj, -1, 1))):
        self.addMoveInOneDirection(-1, 1, boardObj, True)

      # if the piece 1 up 1 right isn't empty
      if (not (self.isThisPositionEmpty(boardObj, 1, 1))):
        self.addMoveInOneDirection(1, 1, boardObj, True)

      # 1 straight up
      self.addMoveInOneDirection(0, 1, boardObj, False)
        
    # BLACK PAWN
    pieceIDBlackPawn = [7]
    if self.pieceID in pieceIDBlackPawn:
      # if never moved
      if self.numOfMoves == 0:
        # if nothing 1 down
        if (self.isThisPositionEmpty(boardObj, 0, -1)):
          self.addMoveInOneDirection(0, -2, boardObj, False)
          
      # if the piece 1 down 1 left isn't empty
      if (not (self.isThisPositionEmpty(boardObj, -1, -1))):
        self.addMoveInOneDirection(-1, -1, boardObj, True)

      # if the piece 1 down 1 right isn't empty
      if (not (self.isThisPositionEmpty(boardObj, 1, -1))):
        self.addMoveInOneDirection(1, -1, boardObj, True)

      # 1 straight up
      self.addMoveInOneDirection(0, -1, boardObj, False)

  # goingRight = -1 : going left
  # goingRight = 0 : not going sidways
  # goingRight = 1 : going right
  # goingUp = -1 : going down
  # goingUp = 0 : not going up or down
  # goingUp = 1 : going up
  def addMoveInDirectionUntillHitPieceOrOffBoard(self, right, up, boardObj):
    myPosition = self.position
    if (self.color == "black"):
      enemyColor = "white"
    else:
      enemyColor = "black"
      
    # Going Straight Up
    doneAdding = False
    while (not doneAdding):
      # is This next position On The Board?
      if (boardObj.isThisPositionOnBoard(myPosition, right, up) == True):
          # is This Position Empty?
        if (self.isThisPositionEmpty(boardObj, right, up) == True):
            # add the move
          self.addMove(boardObj, right, up)
        else:
            # position not empty so is it an enemy?
          pieceID = boardObj.getPieceIDInDirection(
          myPosition, right, up, boardObj.boardPosition)
          if (boardObj.isPieceIDColor(pieceID, enemyColor)):
              # It's enemy so add this piece to movelist and stop the loop
            self.addMove(boardObj, right, up)
            doneAdding = True
          # It's friendly so dont add this piece and stop the look
          else:
            doneAdding = True
      else:
        doneAdding = True
      if (right > 0):
        right += 1
      elif (right < 0):
        right -= 1
      else:
        pass
      if (up > 0):
        up += 1
      elif (up < 0):
        up -= 1
      else:
        pass

  def addMoveInOneDirection(self, right, up, boardObj, CanITakeEnemy):
    myPosition = self.position
    if (self.color == "black"):
      enemyColor = "white"
    else:
      enemyColor = "black"

    # is position on board
    if (boardObj.isThisPositionOnBoard(myPosition, right, up) == True):
      # is position empty
      if (self.isThisPositionEmpty(boardObj, right, up) == True):
        # add move
        self.addMove(boardObj, right, up)
      else:
          # position not empty so is it an enemy?
          pieceID = boardObj.getPieceIDInDirection(
          myPosition, right, up, boardObj.boardPosition)
          # if position is enemy then add move or dont add 
          if (boardObj.isPieceIDColor(pieceID, enemyColor) and CanITakeEnemy):
              # It's enemy so add this piece to movelist and stop the loop
            self.addMove(boardObj, right, up)
        
  # return True if
  def isThisPostionOnBoard(self, boardObj, right, up):
    if (boardObj.getPieceIDInDirection(boardObj, right, up, boardObj.boardPosition) == -1):
      return False
    else:
      return True

  def isThisPositionEmpty(self, boardObj, right, up):
    myPosition = self.position
    # Is it empty?
    if (boardObj.getPieceIDInDirection(myPosition, right, up, boardObj.boardPosition) == 0):
      return True
    else:
      return False

  def addMoveIfNoPieceThere(self, boardObj, right, up):
    myPosition = self.position
    # Is the position on the board?
    if (boardObj.getPieceIDInDirection(myPosition, right, up, boardObj.boardPosition) != -1):
        # Is there no piece on the position?
      if (boardObj.getPieceIDInDirection(myPosition, right, up, boardObj.boardPosition) == 0):
        self.addMove(boardObj, right, up)

  def addMoveIfThereIsAPieceThere(self, boardObj, right, up):
    myPosition = self.position
    # Is the position on the board?
    if (boardObj.getPieceIDInDirection(myPosition, right, up, boardObj.boardPosition) != -1):
      # Is there a piece on the position?
      if (boardObj.getPieceIDInDirection(myPosition, right, up, boardObj.boardPosition) != 0):
        self.addMove(boardObj, right, up)

  def addMove(self, boardObj, right, up):
    myPosition = self.position
    position = boardObj.getPositionInDirection(myPosition, right, up)
    position = position.lower()
    self.moveList.append(position)
      #print("added:" + position)


#                 a  b  c  d  e  f  g  h
# boardPieces = [[0, 0, 0, 0, 0, 0, 0, 0], 8
#                [0, 0, 0, 0, 0, 0, 0, 0], 7
#                [0, 0, 0, 0, 0, 0, 0, 0], 6
#                [0, 0, 0, 0, 0, 0, 0, 0], 5
#                [0, 0, 0, 0, 0, 0, 0, 0], 4
#                [0, 0, 0, 0, 0, 0, 0, 0], 3
#                [0, 0, 0, 0, 0, 0, 0, 0], 2
#                [0, 0, 0, 0, 0, 0, 0, 0]] 1

# E.G.
# a1 = boardPieces[7][0]
# e8 = boardPieces[0][4]
#
# 0 = None
# 1 = PawnWhite
# 2 = BishopWhite
# 3 = KnightWhite
# 4 = CastleWhite
# 5 = QueenWhite
# 6 = KingWhite
# 7 = PawnBlack
# 8 = BishopBlack
# 9 = KnightBlack
# 10 = CastleBlack
# 11 = QueenBlack
# 12 = KingBlack

# DEFAULT BOARD POSITION:
#self.boardPosition = [[10, 9, 8, 11, 12, 8, 9, 10],[7, 7, 7, 7, 7, 7, 7, 7],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[1, 1, 1, 1, 1, 1, 1, 1],[4, 3, 2, 5, 6, 2, 3, 4]]


class Board():
  def __init__(self, x, y, widthOfBoard, heightOfBoard):
    self.x = x
    self.y = y
    self.widthOfBoard = widthOfBoard
    self.heightOfBoard = heightOfBoard
    self.textColor = RED
    self.boardPosition = []
    self.boardObjectList = []
    self.drawMoveColor = BROWN
    self.drawMoveRadius = 20
    self.boardPositionIsUpToDate = False
    self.selectedPiece = ""
    self.DoIDrawMoves = False
    


  def update(self):
    if (self.boardPositionIsUpToDate == False):
      self.setBoardPosition(self.boardObjectList)
      self.boardPositionIsUpToDate = True


  def getPieceObjAtPos(self, position):
    boardObjectList = self.boardObjectList
    for piece in boardObjectList:
      if (piece.position.lower() == position.lower()) and (piece.taken == False):
        return piece
    print("THERE IS NO OBJECT AT POSITION (1):" + position)
    return -1
  
  def drawAllMoves(self):
    # A piece is selected
    if (self.selectedPiece != "!!"):
      # Drawing Moves is True
      if (self.DoIDrawMoves == True):
        clickedObj = self.getPieceObjAtPos(self.selectedPiece)
        # Is this position not a piece?
        if (clickedObj == -1):
          # no piece clicked so let them click again
          self.selectedPiece = "!!"
        else:
          # this position has a piece
          # get the piece's moves and draw them
          ClickedObjMoveList = clickedObj.moveList
          for move in ClickedObjMoveList:
            self.drawCircleMove(move, BROWN)
      
    objectFound = False
    for piece in self.boardObjectList:
      if (piece.taken == False):
        if piece.drawMoves == True:
          objectWhosMoveToDraw = piece
          objectFound = True
    if (objectFound):
      movesToDraw = objectWhosMoveToDraw.moveList
      for position in movesToDraw:
        self.drawCircleMove(position, self.drawMoveColor)

  def drawCircleMove(self, position, color):
    radius = self.drawMoveRadius
    heightOfBox = self.heightOfBoard / 8
    widthOfBox = self.widthOfBoard / 8
    # turning position into x,y cords
    letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    indexLetterPos = letters.index(position[0].lower())
    x = (indexLetterPos * widthOfBox) + (0.5 * widthOfBox) + (0.5 * radius)
    y = ((8 - int(position[1])) * heightOfBox) + (0.5 * heightOfBox) + (0.5 * radius)

    pygame.draw.circle(window, color, (x, y), radius)

  def drawBoard(self):

    heightOfBox = self.heightOfBoard / 8

    widthOfBox = self.widthOfBoard / 8

    # GREY PART
    for i in range(0, 4):
      for j in range(0, 4):
          drawBox(self.x + (widthOfBox * i * 2), self.y + (heightOfBox * j * 2), widthOfBox, heightOfBox, GREY)
          drawBox(self.x + widthOfBox + (widthOfBox * i * 2), self.y + heightOfBox + (heightOfBox * j * 2), widthOfBox, heightOfBox, GREY)
            # drawBox(x + (widthOfBox * i * 2), y, widthOfBox, heightOfBox, BLACK)
    # BLACK PART
    for i in range(0, 4):
      for j in range(0, 4):
          drawBox(self.x + widthOfBox + (widthOfBox * i * 2), self.y + (heightOfBox * j * 2), widthOfBox, heightOfBox, GREEN)
          drawBox(self.x + (widthOfBox * i * 2), self.y + heightOfBox + (heightOfBox * j * 2), widthOfBox, heightOfBox, GREEN)

      # LETTERS
  def drawLetters(self):
    sizeOfCharacter = 15
    letterGapFromBottom = 3
    numberGapFromSide = 3
    heightOfBox = self.heightOfBoard / 8

    widthOfBox = self.widthOfBoard / 8

    for i in range(97, 105):
      drawText(
          chr(i), self.x + (widthOfBox / 2) -
          (getLetterWidth(chr(i), sizeOfCharacter) / 2) +
          (i - 97) * widthOfBox,
          (self.y + self.heightOfBoard -
           (getLetterHeight(chr(i), sizeOfCharacter)) -
           letterGapFromBottom), sizeOfCharacter, self.textColor)

    for i in range(1, 9):
      drawText(
          str(i), self.x + numberGapFromSide,
          self.y + self.heightOfBoard - ((widthOfBox) * (i - 1) +
                                         (widthOfBox / 2)),
          sizeOfCharacter, self.textColor)

  # Drawing all the pons/pieces/king ect using the boardPosition
  # 0 = None
  # 1 = PawnWhite
  # 2 = BishopWhite
  # 3 = KnightWhite
  # 4 = CastleWhite
  # 5 = QueenWhite
  # 6 = KingWhite
  # 7 = PawnBlack
  # 8 = BishopBlack
  # 9 = KnightBlack
  # 10 = CastleBlack
  # 11 = QueenBlack
  # 12 = KingBlack

  def pieceIDtoName(self, pieceID):
    namesList = [
        "Nothing", "PawnW", "BishopW", "KnightW", "CastleW", "QueenW",
        "KingW", "PawnB", "BishopB", "KnightB", "CastleB", "QueenB",
        "KingB"
    ]
    name = namesList[pieceID]
    return name

  def drawAllBoardPieces(self):
    # starting at top left
    width = self.x + 10
    height = self.y + 10
    # row
    for row in range(0, len(self.boardPosition)):
      width = self.x + 10

      # column
      for column in range(0, len(self.boardPosition[0])):
        self.drawAPiece(self.boardPosition[row][column], width, height)
        width += self.widthOfBoard / 8

      height += self.heightOfBoard / 8

#                 a  b  c  d  e  f  g  h
# boardPieces = [[0, 0, 0, 0, 0, 0, 0, 0], 8
#                [0, 0, 0, 0, 0, 0, 0, 0], 7
#                [0, 0, 0, 0, 0, 0, 0, 0], 6
#                [0, 0, 0, 0, 0, 0, 0, 0], 5
#                [0, 0, 0, 0, 0, 0, 0, 0], 4
#                [0, 0, 0, 0, 0, 0, 0, 0], 3
#                [0, 0, 0, 0, 0, 0, 0, 0], 2
#                [0, 0, 0, 0, 0, 0, 0, 0]] 1

# E.G.
# a1 = boardPieces[7][0]
# e8 = boardPieces[0][4]
#

  def drawAPiece(self, pieceID, x, y):
    listOfPieceImage = [
        pawnW, bishopW, knightW, castleW, queenW, kingW, pawnB, bishopB,
        knightB, castleB, queenB, kingB
    ]
    if pieceID == 0:
      pass
    else:
      window.blit(listOfPieceImage[pieceID - 1], (x, y))

#                 a  b  c  d  e  f  g  h
# boardPieces = [[0, 0, 0, 0, 0, 0, 0, 0], 8
#                [0, 0, 0, 0, 0, 0, 0, 0], 7
#                [0, 0, 0, 0, 0, 0, 0, 0], 6
#                [0, 0, 0, 0, 0, 0, 0, 0], 5
#                [0, 0, 0, 0, 0, 0, 0, 0], 4
#                [0, 0, 0, 0, 0, 0, 0, 0], 3
#                [0, 0, 0, 0, 0, 0, 0, 0], 2
#                [0, 0, 0, 0, 0, 0, 0, 0]] 1

# E.G.
# a1 = boardPieces[7][0]
# e8 = boardPieces[0][4]
# position = "A2"

  def getPositionPieceID(self, position, boardPosition):
    #print(position)
    column = int(position[1])
    lettersList = ["a", "b", "c", "d", "e", "f", "g", "h"]
    if position[0].lower() in lettersList:
      row = lettersList.index(position[0].lower())
    # column = 2
    # row = 0
    # expected = [6][0]
    return boardPosition[8 - column][row]

  #
  def getPiecePositionUp(self, position, amount):
    column = int(position[1])
    column += amount
    position = position[0] + str(column)
    return position

  def getPiecePositionLeft(self, position, amount):
    lettersList = ["a", "b", "c", "d", "e", "f", "g", "h"]
    if position[0].lower() in lettersList:
      row = lettersList.index(position[0].lower())
    else:
      print("ERROR THIS IS BAD! THE POSITION ENTERED IS NOT IN LIST????")
    row -= amount
    letterForRow = lettersList[row]
    position = letterForRow + position[1]
    return position

  def getPiecePositionDown(self, position, amount):
    column = int(position[1])
    column -= amount
    position = position[0] + str(column)
    return position

  def getPiecePositionRight(self, position, amount):
    lettersList = ["a", "b", "c", "d", "e", "f", "g", "h"]
    if position[0].lower() in lettersList:
      row = lettersList.index(position[0].lower())
    else:
      print("ERROR THIS IS BAD! THE POSITION ENTERED IS NOT IN LIST????")
    row += amount
    letterForRow = lettersList[row]
    position = letterForRow + position[1]
    return position

  # -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=- -=-=- NOT COMPLETE -=-=-

  def getPositionInDirection(self, position, right, up):
    position = self.getPiecePositionRight(position, right)
    position = self.getPiecePositionUp(position, up)
    return position

  # isThisPositionOnBoard - fine
  # getPiecePositionRight - fine
  # getPiecePositionUp - fine
  # getPositionPieceID - fine
  

  
  def getPieceIDInDirection(self, position, right, up, boardPosition):
    # check if there is that is a position
    if (self.isThisPositionOnBoard(position, right, up) == False):
      return -1
    position = self.getPiecePositionRight(position, right)
    position = self.getPiecePositionUp(position, up)
    return self.getPositionPieceID(position, boardPosition)

  # def isThisPositionOnBoard(self, position, right, up):
  #   # SIDEWAYS
  #   lettersList = ["a", "b", "c", "d", "e", "f", "g", "h"]
  #   row = lettersList.index(position[0].lower())
  #   row += right
  #   if ((row < 0) or (row > 7)):
  #     return False

  #   # UP/DOWN
  #   num = int(position[1])
  #   num += up
  #   if ((num < 0) or (num < 8)):
  #     return False
  #   return True

  # def isTherePieceInDirection(self, position, right, up):
  #   pieceID = self.getPieceIDInDirection(position, right, up, self.boardPosition)
  #   if pieceID == 0:
  #     return False
  #   else:
  #     return True

  # use the other 4 getPieceIDRight ect to make one function that you can type -3,2,1 and stuff to get direction

#                 a  b  c  d  e  f  g  h
# boardPieces = [[0, 0, 0, 0, 0, 0, 0, 0], 8
#                [0, 0, 0, 0, 0, 0, 0, 0], 7
#                [0, 0, 0, 0, 0, 0, 0, 0], 6
#                [0, 0, 0, 0, 0, 0, 0, 0], 5
#                [0, 0, 0, 0, 0, 0, 0, 0], 4
#                [0, 0, 0, 0, 0, 0, 0, 0], 3
#                [0, 0, 0, 0, 0, 0, 0, 0], 2
#                [0, 0, 0, 0, 0, 0, 0, 0]] 1

# ONLY USE PIECES THAT THERE ARE 1 OF, SO ONLY KING

  def getKingPosition(self, color, boardPosition):
    positionStr = "King POS: "
    if (color.lower() == "black"):
      for y in range(0, len(boardPosition)):
          for x in range(0, len(boardPosition[0])):
            if boardPosition[y][x] == 12:
              positionStr = str(x) + str(y)

    if (color.lower() == "white"):
      for y in range(0, len(boardPosition)):
        for x in range(0, len(boardPosition[0])):
          if boardPosition[y][x] == 6:
            positionStr = str(x) + str(y)

    letterList = ["a", "b", "c", "d", "e", "f", "g", "h"]
    letterPos = letterList[int(positionStr[0])]
    numPos = 8 - int(positionStr[1])
    finalPos = str(letterPos) + str(numPos)
    return finalPos

      # turn positionStr e.g. "53" for

      # 0 = None

  # 1 = PawnWhite
  # 2 = BishopWhite
  # 3 = KnightWhite
  # 4 = CastleWhite
  # 5 = QueenWhite
  # 6 = KingWhite
  # 7 = PawnBlack
  # 8 = BishopBlack
  # 9 = KnightBlack
  # 10 = CastleBlack
  # 11 = QueenBlack
  # 12 = KingBlack

  def isThisPositionOnBoard(self, position, right, up):
    lettersList = ["a", "b", "c", "d", "e", "f", "g", "h"]
    posZeroIndex = lettersList.index(position[0].lower())
    applySideDirection = posZeroIndex + right

    if (applySideDirection >= 0) and (applySideDirection <= 7):
      sidePos = True
    else:
      sidePos = False

    applyUpDirection = int(position[1]) + up

    if (applyUpDirection >= 1) and (applyUpDirection <= 8):
      upPos = True
    else:
      upPos = False
    if (sidePos == False) or (upPos == False):
      return False
    else:
      return True

  def isPieceIDColor(self, pieceID, color):
    if color.lower() == "black":
      color = "black"
    elif color.lower() == "white":
      color = "white"
    else:
      print("error color input was not black or white")
    if color == "white":
      if (pieceID >= 1) and (pieceID <= 6):
        return True
      else:
        return False
    elif color == "black":
      if (pieceID >= 7) and (pieceID <= 12):
        return True
      else:
        return False
    else:
      return False


  # getPieceIDInDirection - fine
  # isThisPositionOnBoard - fine
  #
  #  
  # 
  #
  #


      
  def isItCheck(self, color, boardPosition, boardObj):
    color = color.lower()
    checkFound = False
    # WHITE KING CHECK STUFF
    if color == "white":
      if (checkFound == False):
        kingPos = boardObj.getKingPosition(color, boardPosition)
        # Check if pawn is checking the king
        if boardObj.getPieceIDInDirection(kingPos, 1, 1, boardPosition) == 7:
          checkFound = True
        else:
          pass
        if boardObj.getPieceIDInDirection(kingPos, -1, 1, boardPosition) == 7:
          checkFound = True

        # Check if king is checked in a straight line anywhere
        # Check if king is line of sight with a black queen or rook, if anything else is in the way then no check
        checkLeft = True
        checkRight = True
        checkUp = True
        checkDown = True
        # CHECKING LEFT QUEEN/ROOK
        i = 1
        for a in range(0, numOfSquareInDirectionOfPos(kingPos, "left")):
          if (checkLeft):
            piece = boardObj.getPieceIDInDirection(kingPos, -i, 0, boardPosition)
            if piece == 0:
              i += 1
                # if enemy is in line of sight
            elif piece == 10 or piece == 11:
              checkFound = True
            else:
                # if there is no enemy and no empty spot then friendly is there
              checkLeft = False

        # CHECKING RIGHT QUEEN/ROOK
        i = 1
        for a in range(0, numOfSquareInDirectionOfPos(kingPos, "right")):
          if (checkRight):
            piece = boardObj.getPieceIDInDirection(kingPos, i, 0, boardPosition)
            if piece == 0:
              i += 1
              # if enemy is in line of sight
            elif piece == 10 or piece == 11:
              checkFound = True
            else:
              # if there is no enemy and no empty spot then friendly is there
              checkRight = False

        # CHECKING UP QUEEN/ROOK
        i = 1
        for a in range(0, numOfSquareInDirectionOfPos(kingPos, "up")):
          if (checkUp):
            piece = boardObj.getPieceIDInDirection(kingPos, 0, 1, boardPosition)
            if piece == 0:
              i += 1
              # if enemy is in line of sight
            elif piece == 10 or piece == 11:
              checkFound = True
            else:
              # if there is no enemy and no empty spot then friendly is there
              checkUp = False

        # CHECKING DOWN QUEEN/ROOK
        i = 1
        for a in range(0, numOfSquareInDirectionOfPos(kingPos, "down")):
          if (checkDown):
            piece = boardObj.getPieceIDInDirection(kingPos, 0, -1, boardPosition)
            if piece == 0:
              i += 1
              # if enemy is in line of sight
            elif piece == 10 or piece == 11:
              checkFound = True
            else:
              # if there is no enemy and no empty spot then friendly is there
              checkDown = False

        # Checking diagonally for queen or bishopB
        # To find num of diagonal upleft for example, find num of squares up, find num of squares left, the smaller number is the one you will check for
        checkUpLeft = True
        checkUpRight = True
        checkDownLeft = True
        checkDownRight = True
        numOfSquaresUp = numOfSquareInDirectionOfPos(kingPos, "Up")
        numOfSquaresDown = numOfSquareInDirectionOfPos(kingPos, "Down")
        numOfSquaresLeft = numOfSquareInDirectionOfPos(kingPos, "Left")
        numOfSquaresRight = numOfSquareInDirectionOfPos(
            kingPos, "Right")
        # check upLeft
        i = 1
        for a in range(
                0,
                returnSmallestNumber(numOfSquaresUp,
                                     numOfSquaresLeft)):
            if (checkUpLeft):
                piece = boardObj.getPieceIDInDirection(
                    kingPos, -i, i, boardPosition)
                if piece == 0:
                    i += 1
                    # if enemy is in line of sight (queen and bishop)
                elif piece == 8 or piece == 11:
                    checkFound = True
                else:
                    # if there is no enemy and no empty spot then friendly is there
                    checkUpLeft = False

            # check upRight
        i = 1
        for a in range(
                0,
                returnSmallestNumber(numOfSquaresUp,
                                     numOfSquaresRight)):
            if (checkUpRight):
                piece = boardObj.getPieceIDInDirection(
                    kingPos, i, i, boardPosition)
                if piece == 0:
                    i += 1
                    # if enemy is in line of sight (queen and bishop)
                elif piece == 8 or piece == 11:
                    checkFound = True
                else:
                    # if there is no enemy and no empty spot then friendly is there
                    checkUpRight = False

            # check downLeft
        i = 1
        for a in range(
                0,
                returnSmallestNumber(numOfSquaresDown,
                                     numOfSquaresLeft)):
            if (checkDownLeft):
                piece = boardObj.getPieceIDInDirection(
                    kingPos, -i, -i, boardPosition)
                if piece == 0:
                    i += 1
                    # if enemy is in line of sight (queen and bishop)
                elif piece == 8 or piece == 11:
                    checkFound = True
                else:
                    # if there is no enemy and no empty spot then friendly is there
                    checkDownLeft = False

        # check downRight
        i = 1
        for a in range(
                0,
                returnSmallestNumber(numOfSquaresDown,
                                     numOfSquaresRight)):
            if (checkDownRight):
                piece = boardObj.getPieceIDInDirection(
                    kingPos, i, -i, boardPosition)
                if piece == 0:
                    i += 1
                    # if enemy is in line of sight (queen and bishop)
                elif piece == 8 or piece == 11:
                    checkFound = True
                else:
                    # if there is no enemy and no empty spot then friendly is there
                    checkDownRight = False

        # CHECK FOR KNIGHT
        # check if the positions exist around the king and put them in a list
        listOfKnightDirections = [(-2, 1), (-1, 2), (1, 2), (2, 1),
                                  (2, -1), (1, -2), (-1, -2), (-2, -1)]
        for direction in listOfKnightDirections:
            if (boardObj.isThisPositionOnBoard(kingPos, direction[0],
                                           direction[1])):
                positionID = boardObj.getPieceIDInDirection(
                    kingPos, direction[0], direction[1], boardPosition)
                if positionID == 9:
                    checkFound = True
        if (checkFound):
          return True
        else:
          return False

    # pieceID Syntax
    # 0 = None
    # 1 = PawnWhite
    # 2 = BishopWhite
    # 3 = KnightWhite
    # 4 = CastleWhite
    # 5 = QueenWhite
    # 6 = KingWhite
    # 7 = PawnBlack
    # 8 = BishopBlack
    # 9 = KnightBlack
    # 10 = CastleBlack
    # 11 = QueenBlack
    # 12 = KingBlack
    # BLACK KING CHECK
          
    if color == "black":
      if (checkFound == False):
        kingPos = boardObj.getKingPosition(color, boardPosition)
        # Check if pawn is checking the king
        if boardObj.getPieceIDInDirection(kingPos, 1, -1, boardPosition) == 1:
          checkFound = True
        else:
          pass
        if boardObj.getPieceIDInDirection(kingPos, -1, -1, boardPosition) == 1:
          checkFound = True

        # Check if king is checked in a straight line anywhere
        # Check if king is line of sight with a white queen or rook, if anything else is in the way then no check
        checkLeft = True
        checkRight = True
        checkUp = True
        checkDown = True
        # CHECKING LEFT QUEEN/ROOK
        i = 1
        for a in range(0, numOfSquareInDirectionOfPos(kingPos, "left")):
          if (checkLeft):
            piece = boardObj.getPieceIDInDirection(kingPos, -i, 0, boardPosition)
            if piece == 0:
              i += 1
                # if enemy is in line of sight
            elif piece == 5 or piece == 4:
              checkFound = True
            else:
                # if there is no enemy and no empty spot then friendly is there
              checkLeft = False

        # CHECKING RIGHT QUEEN/ROOK
        i = 1
        for a in range(0, numOfSquareInDirectionOfPos(kingPos, "right")):
          if (checkRight):
            piece = boardObj.getPieceIDInDirection(kingPos, i, 0, boardPosition)
            if piece == 0:
              i += 1
              # if enemy is in line of sight
            elif piece == 5 or piece == 4:
              checkFound = True
            else:
              # if there is no enemy and no empty spot then friendly is there
              checkRight = False

        # CHECKING UP QUEEN/ROOK
        i = 1
        for a in range(0, numOfSquareInDirectionOfPos(kingPos, "up")):
          if (checkUp):
            piece = boardObj.getPieceIDInDirection(kingPos, 0, 1, boardPosition)
            if piece == 0:
              i += 1
              # if enemy is in line of sight
            elif piece == 4 or piece == 5:
              checkFound = True
            else:
              # if there is no enemy and no empty spot then friendly is there
              checkUp = False

        # CHECKING DOWN QUEEN/ROOK
        i = 1
        for a in range(0, numOfSquareInDirectionOfPos(kingPos, "down")):
          if (checkDown):
            piece = boardObj.getPieceIDInDirection(kingPos, 0, -1, boardPosition)
            if piece == 0:
              i += 1
              # if enemy is in line of sight
            elif piece == 4 or piece == 5:
              checkFound = True
            else:
              # if there is no enemy and no empty spot then friendly is there
              checkDown = False

        # Checking diagonally for queen or bishopB
        # To find num of diagonal upleft for example, find num of squares up, find num of squares left, the smaller number is the one you will check for
        checkUpLeft = True
        checkUpRight = True
        checkDownLeft = True
        checkDownRight = True
        numOfSquaresUp = numOfSquareInDirectionOfPos(kingPos, "Up")
        numOfSquaresDown = numOfSquareInDirectionOfPos(kingPos, "Down")
        numOfSquaresLeft = numOfSquareInDirectionOfPos(kingPos, "Left")
        numOfSquaresRight = numOfSquareInDirectionOfPos(
            kingPos, "Right")
        # check upLeft
        i = 1
        for a in range(
                0,
                returnSmallestNumber(numOfSquaresUp,
                                     numOfSquaresLeft)):
            if (checkUpLeft):
                piece = boardObj.getPieceIDInDirection(
                    kingPos, -i, i, boardPosition)
                if piece == 0:
                    i += 1
                    # if enemy is in line of sight (queen and bishop)
                elif piece == 2 or piece == 5:
                    checkFound = True
                else:
                    # if there is no enemy and no empty spot then friendly is there
                    checkUpLeft = False

            # check upRight
        i = 1
        for a in range(
                0,
                returnSmallestNumber(numOfSquaresUp,
                                     numOfSquaresRight)):
            if (checkUpRight):
                piece = boardObj.getPieceIDInDirection(
                    kingPos, i, i, boardPosition)
                if piece == 0:
                    i += 1
                    # if enemy is in line of sight (queen and bishop)
                elif piece == 2 or piece == 5:
                    checkFound = True
                else:
                    # if there is no enemy and no empty spot then friendly is there
                    checkUpRight = False

            # check downLeft
        i = 1
        for a in range(
                0,
                returnSmallestNumber(numOfSquaresDown,
                                     numOfSquaresLeft)):
            if (checkDownLeft):
                piece = boardObj.getPieceIDInDirection(
                    kingPos, -i, -i, boardPosition)
                if piece == 0:
                    i += 1
                    # if enemy is in line of sight (queen and bishop)
                elif piece == 2 or piece == 5:
                    checkFound = True
                else:
                    # if there is no enemy and no empty spot then friendly is there
                    checkDownLeft = False

        # check downRight
        i = 1
        for a in range(
                0,
                returnSmallestNumber(numOfSquaresDown,
                                     numOfSquaresRight)):
            if (checkDownRight):
                piece = boardObj.getPieceIDInDirection(
                    kingPos, i, -i, boardPosition)
                if piece == 0:
                    i += 1
                    # if enemy is in line of sight (queen and bishop)
                elif piece == 2 or piece == 5:
                    checkFound = True
                else:
                    # if there is no enemy and no empty spot then friendly is there
                    checkDownRight = False

        # CHECK FOR KNIGHT
        # check if the positions exist around the king and put them in a list
        listOfKnightDirections = [(-2, 1), (-1, 2), (1, 2), (2, 1),
                                  (2, -1), (1, -2), (-1, -2), (-2, -1)]
        for direction in listOfKnightDirections:
            if (boardObj.isThisPositionOnBoard(kingPos, direction[0],
                                           direction[1])):
                positionID = boardObj.getPieceIDInDirection(
                    kingPos, direction[0], direction[1], boardPosition)
                if positionID == 3:
                    checkFound = True
    if (checkFound):
      return True
    else:
      return False

  def setBoardPosition(self, boardObjectList):
    self.boardPosition = self.turnBoardObjectListIntoBoardPosition(boardObjectList)
    self.boardObjectList = boardObjectList


#                 a  b  c  d  e  f  g  h
# boardPieces = [[0, 0, 0, 0, 0, 0, 0, 0], 8
#                [0, 0, 0, 0, 0, 0, 0, 0], 7
#                [0, 0, 0, 0, 0, 0, 0, 0], 6
#                [0, 0, 0, 0, 0, 0, 0, 0], 5
#                [0, 0, 0, 0, 0, 0, 0, 0], 4
#                [0, 0, 0, 0, 0, 0, 0, 0], 3
#                [0, 0, 0, 0, 0, 0, 0, 0], 2
#                [0, 0, 0, 0, 0, 0, 0, 0]] 1

# E.G.
# a1 = boardPieces[7][0]
# e8 = boardPieces[0][4]
#

  def turnBoardObjectListIntoBoardPosition(self, boardObjectList):
    # get the pieces that aren't taken
    placePieceList = []
    for piece in boardObjectList:
        if (piece.taken == False):
            placePieceList.append(piece)

    # put objects where they need to be
    boardNumberList = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

    for piece in placePieceList:
      position = piece.position
      letterList = ["a", "b", "c", "d", "e", "f", "g", "h"]

      fromPos_index1 = letterList.index(position[0].lower())
      fromPos_index0 = 8 - int(position[1])

      boardNumberList[fromPos_index0][fromPos_index1] = piece.pieceID
    return boardNumberList

def numOfSquareInDirectionOfPos(position, direction):
  direction = direction.lower()
  letterList = ["a", "b", "c", "d", "e", "f", "g", "h"]

  if direction == "left":
    num = letterList.index(position[0])
    return num
  elif direction == "right":
    num = letterList.index(position[0])
    return (7 - num)
  elif direction == "up":
    num = 8 - int(position[1])
    return (num)
  elif direction == "down":
    num = int(position[1]) - 1
    return (num)
  else:
    print("You didn't input a direction")
    return (num)


def returnSmallestNumber(a, b):
  if a == b:
    return a
  elif a > b:
    return b
  else:
    return a


def drawBox(x, y, width, height, color):
  pygame.draw.rect(window, (color), (x, y, width, height))


def drawText(text, x, y, size, color):
  arialFont = pygame.font.SysFont('arial', size)
  textRenderer = arialFont.render(text, False, color)
  window.blit(textRenderer, (x, y))


def drawBackGround():
  drawBox(0, 0, windowWidth, windowHeight, WHITE)


def getLetterWidth(letter, size):
  arialFont = pygame.font.SysFont('arial', size)
  textRenderer = arialFont.render(letter, False, BLACK)
  return textRenderer.get_width()


def getLetterHeight(letter, size):
  arialFont = pygame.font.SysFont('arial', size)
  textRenderer = arialFont.render(letter, False, BLACK)
  return textRenderer.get_height()

def printBoard(boardPosition):
  for line in boardPosition:
    print(line)


class Mouse():
  def __init__(self):
    self.turn = "White"
    self.firstClicked = "!!"
    self.secondClicked = "!!"

    self.firstPosition = ""

    self.leftClickLocked = False
    
    self.backButtonX = 460
    self.backButtonY = 265
    self.backButtonWidth = 130
    self.backButtonHeight = 70
    self.backButtonTextSize = 40

    self.printBoardButtonX = 700
    self.printBoardButtonY = 265
    self.printBoardButtonWidth = 130
    self.printBoardButtonHeight = 70
    self.printBoardButtonTextSize = 40

  def update(self, boardObj):
    self.isBackButtonClicked(boardObj)
    self.isPrintBoardButtonClicked(boardObj)
    self.ifClickedPutMovesOnBoard(boardObj)

    # Clicking Function
    # if they aren't holding left click then make it available
    clickedPosition = "!!"
    if (pygame.mouse.get_pressed()[0] == False):
      self.leftClickLocked = False
    # LEFT CLICKED
    if (self.leftClickLocked == False):
      if pygame.mouse.get_pressed()[0] == True:
        coordPosition = pygame.mouse.get_pos()
        clickedPosition = self.coordsToBoardPosition(
            coordPosition, boardObj)
        self.leftClickLocked = True
    # IF CLICKED SOMEWHERE
    if clickedPosition != "!!":
      # CHECK IF IT'S THE FIRST CLICK
      if self.firstClicked == "!!":
        # SET THE FIRST CLICK TO CLICKED POSITION
        self.firstClicked = clickedPosition
      else:
        # ITS SECOND CLICK THEREFORE SET THAT
        self.secondClicked = clickedPosition

    # DID THEY CLICK ON AN EMPTY POSITION?
    if (self.firstClicked != "!!"):
      pieceToMoveObj = self.getPieceObjAtPos(self.firstClicked, boardObj)
      if (pieceToMoveObj == -1):
        self.firstClicked = "!!"
        self.secondClicked = "!!"
    
        
    # MOVE PIECE IF BOTH FIRST AND SECOND IS CLICKED
    if (self.firstClicked != "!!") and (self.secondClicked != "!!"):
      pieceToMoveObj = self.getPieceObjAtPos(self.firstClicked, boardObj)
    #   # is there a piece on this position?
      if (pieceToMoveObj == -1):
        self.firstClicked = "!!"
        self.secondClicked = "!!"
      else:
        pieceToMoveObj.tryMovingPiece(self.secondClicked, boardObj)
      self.firstClicked = "!!"
      self.secondClicked = "!!"

  def getPieceObjAtPos(self, position, boardObj):
    boardObjectList = boardObj.boardObjectList
    for piece in boardObjectList:
      if (piece.position.lower() == position.lower()) and (piece.taken == False):
        return piece
    print("THERE IS NO OBJECT AT POSITION (2):" + position)
    return -1

  def ifClickedPutMovesOnBoard(self, boardObj):
    # is a piece clicked
      if self.firstClicked != "!!":
        # allow the board to draw and set the position which's object needs to be drawn
        boardObj.selectedPiece = self.firstClicked
        boardObj.DoIDrawMoves = True
      else:
      # A piece isn't clicked so dont draw
        boardObj.selectedPiece = "!!"
        boardObj.DoIDrawMoves = False

  def drawTextForScreen(self):
    drawText("firstClicked:" + self.firstClicked, 450, 50, 40, BLACK)
    drawText("secondClicked:" + self.secondClicked, 450, 150, 40, BLACK)

  def undoLastMove(self, boardObj):
    # Get the last move that occured in list
    # get the piece object at the position
    # change the position to the previous position
    # if a piece was taken, set it's "taken" to false
    # remove the last move in the list

    # if list not empty
    if len(allPieceMoveList) != 0:
      # get last item
      lastMoveValues = allPieceMoveList[len(allPieceMoveList)-1]
      
      # get piece that was moved to position
      for piece in boardObj.boardObjectList:
        if (piece.pieceNum == lastMoveValues[0]):
          lastPieceToMove = piece

      # change last Piece's position to previous position
      lastPieceToMove.position = lastMoveValues[1]
      lastPieceToMove.numOfMoves -= 1
      lastPieceToMove.moveListUpdated = False

      # did the last piece take something?
      if lastMoveValues[3] != 0:
        # something was taken so revive it
        for piece in boardObj.boardObjectList:
          if (piece.pieceNum == lastMoveValues[3]):
            takenPiece = piece
        # revive taken piece
        takenPiece.taken = False


        # ERROR WITH NUMBER 
      # remove the last item in list
      allPieceMoveList.remove(lastMoveValues)

      # make board updated
      boardObj.boardPositionIsUpToDate = False
          
          
  def isPrintBoardButtonClicked(self, boardObj):
    if (pygame.mouse.get_pressed()[0] == False):
      self.leftClickLocked = False
    # LEFT CLICKED
    if (self.leftClickLocked == False):
      if pygame.mouse.get_pressed()[0] == True:
        coordPosition = pygame.mouse.get_pos()
        # IS CLICK INSIDE BOX
        print(coordPosition)
        if (coordPosition[0] > self.printBoardButtonX) and (coordPosition[0] < self.printBoardButtonX + self.printBoardButtonWidth):
          if (coordPosition[1] > self.printBoardButtonY) and (coordPosition[1] < self.printBoardButtonY + self.printBoardButtonHeight):
            printBoard(boardObj.boardPosition)


  
  def isBackButtonClicked(self, boardObj):
    if (pygame.mouse.get_pressed()[0] == False):
      self.leftClickLocked = False
    # LEFT CLICKED
    if (self.leftClickLocked == False):
      if pygame.mouse.get_pressed()[0] == True:
        coordPosition = pygame.mouse.get_pos()
        # IS CLICK INSIDE BOX
        print(coordPosition)
        if (coordPosition[0] > self.backButtonX) and (coordPosition[0] < self.backButtonX + self.backButtonWidth):
          if (coordPosition[1] > self.backButtonY) and (coordPosition[1] < self.backButtonY + self.backButtonHeight):
            self.undoLastMove(boardObj)
  
  def drawBackButton(self):
    textX = self.backButtonX + 10
    textY = self.backButtonY + 17
    pygame.draw.rect(window, (GREEN), (self.backButtonX, self.backButtonY, self.backButtonWidth, self.backButtonHeight))
    drawText("BACK", textX, textY, self.backButtonTextSize, BLACK)

  def drawPrintBoardButton(self):
    textX = self.printBoardButtonX + 10
    textY = self.printBoardButtonY + 17
    pygame.draw.rect(window, (GREEN), (self.printBoardButtonX, self.printBoardButtonY, self.printBoardButtonWidth, self.printBoardButtonHeight))
    drawText("PRINT BOARD", textX, textY, self.printBoardButtonTextSize, BLACK)

  def coordsToBoardPosition(self, coords, boardObj):
    xCoord = coords[0]
    xCoord -= boardObj.x
    xNumber = xCoord // (boardObj.widthOfBoard / 8)

    letterList = ["A", "B", "C", "D", "E", "F", "G", "H"]
    if (len(letterList) > int(xNumber) and xNumber >= 0):
      xLetter = letterList[int(xNumber)]
    else:
      xLetter = "!"

    yCoord = coords[1]
    yCoord -= boardObj.y
    yNumber = yCoord // (boardObj.heightOfBoard / 8)
    yNumber = 8 - yNumber
    if (yNumber > 8 or yNumber <= 0):
      yLetter = "!"
    else:
      yLetter = str(int(yNumber))


    if (xLetter == "!" or yLetter == "!"):
      print("Clicked off board")
      return "!!"
    else:
      letterPosition = xLetter + yLetter
      return letterPosition


boardPosition = [[10, 9, 8, 11, 12, 8, 9, 10], [7, 7, 7, 7, 0, 7, 7, 7],
                 [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1], [4, 3, 2, 5, 6, 2, 3, 4]]

#allPieceMoveList=[[22, 'f2', 'f4', 0], [12, 'd7', 'd5', 0], [20, 'd2', 'd4', 0], [11, 'c7', 'c5', 0], [20, 'd4', 'c5', 11], [2, 'b8', 'd7', 0], [28, 'd1', 'd5', 12], [13, 'e7', 'e6', 0], [28, 'd5', 'd4', 0], [6, 'f8', 'c5', 20], [28, 'd4', 'g7', 15], [4, 'd8', 'h4', 0], [23, 'g2', 'g3', 0], [4, 'h4', 'h6', 0], [28, 'g7', 'h8', 8], [2, 'd7', 'f6', 0], [18, 'b2', 'b3', 0], [6, 'c5', 'f8', 0], [22, 'f4', 'f5', 0], [6, 'f8', 'g7', 0], [27, 'c1', 'h6', 4], [6, 'g7', 'h8', 28], [27, 'h6', 'g5', 0], [2, 'f6', 'e4', 0], [31, 'g1', 'f3', 0], [6, 'h8', 'a1', 25], [21, 'e2', 'e3', 0], [6, 'a1', 'c3', 0], [26, 'b1', 'c3', 6], [2, 'e4', 'c3', 26], [30, 'f1', 'g2', 0], [2, 'c3', 'a2', 17], [31, 'f3', 'd4', 0], [2, 'a2', 'c1', 0], [29, 'e1', 'd2', 0], [2, 'c1', 'a2', 0], [19, 'c2', 'c3', 0], [13, 'e6', 'f5', 22], [32, 'h1', 'a1', 0], [14, 'f7', 'f6', 0], [30, 'g2', 'd5', 0], [2, 'a2', 'c3', 19], [29, 'd2', 'c3', 2], [14, 'f6', 'g5', 27], [30, 'd5', 'g8', 7], [10, 'b7', 'b6', 0], [31, 'd4', 'c6', 0], [3, 'c8', 'd7', 0], [30, 'g8', 'd5', 0], [1, 'a8', 'c8', 0], [32, 'a1', 'a7', 9], [3, 'd7', 'c6', 31], [30, 'd5', 'c6', 3], [1, 'c8', 'c6', 30]]


def running():

  # RUN ONCE VARIABLES
  # pieceNum:
  # /  A  B  C  D  E  F  G  H
  # 8  1  2  3  4  5  6  7  8
  # 7  9 10 11 12 13 14 15 16
  # 6
  # 5
  # 4
  # 3
  # 2 17 18 19 20 21 22 23 24
  # 1 25 26 27 28 29 30 31 32

  # 0 = None
  # 1 = PawnWhite
  # 2 = BishopWhite
  # 3 = KnightWhite
  # 4 = CastleWhite
  # 5 = QueenWhite
  # 6 = KingWhite
  # 7 = PawnBlack
  # 8 = BishopBlack
  # 9 = KnightBlack
  # 10 = CastleBlack
  # 11 = QueenBlack
  # 12 = KingBlack

  piece_CastleAB = Piece("CastleAB", 1, 10, "a8")
  piece_KnightBB = Piece("KnightBB", 2, 9, "b8")
  piece_BishopCB = Piece("BishopCB", 3, 8, "c8")
  piece_QueenDB = Piece("QueenDB", 4, 11, "d8")
  piece_KingEB = Piece("KingEB", 5, 12, "e8")
  piece_BishopGB = Piece("BishopGB", 6, 8, "f8")
  piece_KnightFB = Piece("KnightFB", 7, 9, "g8")
  piece_CastleHB = Piece("CastleHB", 8, 10, "h8")

  piece_PawnAB = Piece("PawnAB", 9, 7, "a7")
  piece_PawnBB = Piece("PawnBB", 10, 7, "b7")
  piece_PawnCB = Piece("PawnCB", 11, 7, "c7")
  piece_PawnDB = Piece("PawnDB", 12, 7, "d7")
  piece_PawnEB = Piece("PawnEB", 13, 7, "e7")
  piece_PawnFB = Piece("PawnFB", 14, 7, "f7")
  piece_PawnGB = Piece("PawnGB", 15, 7, "g7")
  piece_PawnHB = Piece("PawnHB", 16, 7, "h7")

  piece_CastleAW = Piece("CastleAW", 25, 4, "a1")
  piece_KnightBW = Piece("KnightBW", 26, 3, "b1")
  piece_BishopCW = Piece("BishopCW", 27, 2, "c1")
  piece_QueenDW = Piece("QueenDW", 28, 5, "d1")
  piece_KingEW = Piece("KingEW", 29, 6, "e1")
  piece_BishopGW = Piece("BishopGW", 30, 2, "f1")
  piece_KnightFW = Piece("KnightFW", 31, 3, "g1")
  piece_CastleHW = Piece("CastleHW", 32, 4, "h1")

  piece_PawnAW = Piece("PawnAW", 17, 1, "a2")
  piece_PawnBW = Piece("PawnBW", 18, 1, "b2")
  piece_PawnCW = Piece("PawnCW", 19, 1, "c2")
  piece_PawnDW = Piece("PawnDW", 20, 1, "d2")
  piece_PawnEW = Piece("PawnEW", 21, 1, "e2")
  piece_PawnFW = Piece("PawnFW", 22, 1, "f2")
  piece_PawnGW = Piece("PawnGW", 23, 1, "g2")
  piece_PawnHW = Piece("PawnHW", 24, 1, "h2")

  boardGame = Board(10, 10, 400, 400)
  boardObjects = [
      piece_CastleAB, piece_KnightBB, piece_BishopCB, piece_QueenDB,
      piece_KingEB, piece_BishopGB, piece_KnightFB, piece_CastleHB,
      piece_PawnAB, piece_PawnBB, piece_PawnCB, piece_PawnDB, piece_PawnEB,
      piece_PawnFB, piece_PawnGB, piece_PawnHB, piece_CastleAW,
      piece_KnightBW, piece_BishopCW, piece_QueenDW, piece_KingEW,
      piece_BishopGW, piece_KnightFW, piece_CastleHW, piece_PawnAW,
      piece_PawnBW, piece_PawnCW, piece_PawnDW, piece_PawnEW, piece_PawnFW,
      piece_PawnGW, piece_PawnHW
  ]
  boardGame.setBoardPosition(boardObjects)
  run = True
  mouseObj = Mouse()

  piece_PawnBW.doMoveList(boardGame, [[22, 'f2', 'f4', 0], [12, 'd7', 'd5', 0], [20, 'd2', 'd4', 0], [11, 'c7', 'c5', 0], [20, 'd4', 'c5', 11], [2, 'b8', 'd7', 0], [28, 'd1', 'd5', 12], [13, 'e7', 'e6', 0], [28, 'd5', 'd4', 0], [6, 'f8', 'c5', 20], [28, 'd4', 'g7', 15], [4, 'd8', 'h4', 0], [23, 'g2', 'g3', 0], [4, 'h4', 'h6', 0], [28, 'g7', 'h8', 8], [2, 'd7', 'f6', 0], [18, 'b2', 'b3', 0], [6, 'c5', 'f8', 0], [22, 'f4', 'f5', 0], [6, 'f8', 'g7', 0], [27, 'c1', 'h6', 4], [6, 'g7', 'h8', 28], [27, 'h6', 'g5', 0], [2, 'f6', 'e4', 0], [31, 'g1', 'f3', 0], [6, 'h8', 'a1', 25], [21, 'e2', 'e3', 0], [6, 'a1', 'c3', 0], [26, 'b1', 'c3', 6], [2, 'e4', 'c3', 26], [30, 'f1', 'g2', 0], [2, 'c3', 'a2', 17], [31, 'f3', 'd4', 0], [2, 'a2', 'c1', 0], [29, 'e1', 'd2', 0], [2, 'c1', 'a2', 0], [19, 'c2', 'c3', 0], [13, 'e6', 'f5', 22], [32, 'h1', 'a1', 0], [14, 'f7', 'f6', 0], [30, 'g2', 'd5', 0], [2, 'a2', 'c3', 19], [29, 'd2', 'c3', 2], [14, 'f6', 'g5', 27], [30, 'd5', 'g8', 7], [10, 'b7', 'b6', 0], [31, 'd4', 'c6', 0], [3, 'c8', 'd7', 0], [30, 'g8', 'd5', 0], [1, 'a8', 'c8', 0], [32, 'a1', 'a7', 9], [3, 'd7', 'c6', 31]])

  
  while run:
    for event in pygame.event.get():
      
      # QUITTING
      if event.type == pygame.QUIT:
        run = False    

      # PROGRAM

      # UPDATE ORDER:
      # UPDATE BOARD POSITION
      # UPDATE MOVE LIST
      # UPDATE MOUSE OBJ
      if (boardGame.boardPositionIsUpToDate == True):
        allPiecesUpdated = True
        for piece in boardObjects:
          if (piece.moveListUpdated == False):
            allPiecesUpdated = False
      
        if not (allPiecesUpdated):
          for piece in boardObjects:
            piece.update(boardGame)
        else:
          mouseObj.update(boardGame)
      else:
        boardGame.update()
      # DRAW ORDER: Background, board, letters, piece moves (brown circle), pieces
      drawBackGround()
      mouseObj.drawTextForScreen()
      mouseObj.drawBackButton()
      mouseObj.drawPrintBoardButton()
      boardGame.drawBoard()
      boardGame.drawAllMoves()
      boardGame.drawAllBoardPieces()
      boardGame.drawLetters()
      #print(f"{allPieceMoveList=}")

      
      pygame.display.flip()

running()
