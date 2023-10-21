import copy
around_list = [
   [0,0,0,0],
   [0,0,0,0],
   [0,0,0,0],
   [0,0,0,0]
]

def find(lists, index:set):
    x, y = index
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    result = []
    for i in range(4):
      if x+dx[i] >=0 and y+dy[i] >=0 and x+dx[i]<4 and y+dy[i]<4: #테두리에 있는 친구들은 -1로  
        a = lists[x+dx[i]][y+dy[i]]
        result.append(a) # 테두리 아닌 값의 상하좌우를 저장
      else:
        result.append(-1) 
    return result

def make_around(board1):
   global around_list
   for i in range(4):
      for j in range(4):
         if board1[i][j] == 0:
            around_list[i][j]=-2
         if board1[i][j] != 0:
            around = find(board1, (i,j))
            around_list[i][j] = around


def left(board):
   for i in range(4):
      for j in range(4):
        if board[i][j] != 0:
            around = around_list[i][j]
            if around == -2:
               pass
            elif around[2] == -1:
                pass
            elif around[2] == board[i][j]:
               board[i][j-1] = around[2] * 2
               board[i][j] = 0
            else:
                  count = 0
                  for k in range(1,j+1):
                     if board[i][j-k] == 0:
                        count +=1
                  board[i][j-count] = board[i][j]
                  board[i][j] = 0
   return board

# def right(board):
#    for i in range(4):
#       for j in range(4):
#         if board[i][j] != 0:
#             around = around_list[i][j]
#             if around == -2:
#                pass
#             elif around[3] == -1:
#                 pass
#             elif around[3] == board[i][j]:
#                board[i][j+1] = around[3] * 2
#                board[i][j] = 0
#             elif  around[3] ==0:
#                board[i][j+1] = board[i][j]
#                board[i][j] = 0    
#             else:
#                   count = 0
#                   add = 1
#                   for k in range(i,3):
#                      if board[i][j+add] == 0:
#                         count +=1
#                         add +=1
#                   board[i][j-count] = board[i][j]
#                   board[i][j] = 0     

   # return board

def up(board):
   for i in range(4):
      for j in range(4):
        if board[i][j] != 0:
            around = around_list[i][j]
            if around == -2:
               pass
            elif around[0] == -1:
               pass
            elif around[0] == board[i][j]:
               board[i-1][j] = around[0] * 2
               board[i][j] = 0
            else:
                    count = 0
                    for k in range(1,i+1):
                        if board[i-k][j] == 0:
                            count +=1
                    board[i-count][j] = board[i][j]
                    board[i][j] = 0
   return board
# def down(board):
#    for i in range(4):
#       for j in range(4):
#         if board[i][j] != 0:
#             around = around_list[i][j]
#             if around == -2:
#                pass
#             elif around[1] == -1:
#                pass
#             elif around[1] == board[i][j]:
#                board[i+1][j] = around[1] * 2
#                board[i][j] = 0
#             elif around[1] == 0:
#                board[i+1][j] = board[i][j]
#                board[i][j] = 0
#    return board
# evaluation, D = cal()


def cal_by_around(board):

   board1 = copy.deepcopy(board)
   board2 = copy.deepcopy(board)
   board3 = copy.deepcopy(board)
   board4 = copy.deepcopy(board)

   make_around(board)

   left1 = left(board3)

   up1 =  up(board1)

   board_dublicate = copy.deepcopy(board2)
   board2[0] = board_dublicate[3]
   board2[1] = board_dublicate[2]
   board2[2] = board_dublicate[1]
   board2[3] = board_dublicate[0]
   make_around(board2)
   down1 =  up(board2)
   board_dublicate2 = copy.deepcopy(board2)
   board2[0] = board_dublicate2[3]
   board2[1] = board_dublicate2[2]
   board2[2] = board_dublicate2[1]
   board2[3] = board_dublicate2[0]


   for index,value in enumerate(board4):
      value.reverse()
      board4[index] = value
   make_around(board4)
   right_tem = left(board4)
   for index,value in enumerate(right_tem):
      value.reverse()
      board[index] = value
   right1 = right_tem
   return up1, down1, left1, right1


board = [
   [5,0,0,2],
   [0,0,2,0],
   [0,2,0,0],
   [2,0,4,0]
]
cal_by_around(board)