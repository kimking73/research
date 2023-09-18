n=3
board = []
for i in range(3):
  user_input = list(map(int,input().split()))
  board.append(user_input)

# board = [[2, 0, 0],
#          [2, 4, 0],
#          [32, 4, 2]]

connecting = [[0,0],[0,0,0],[0,0],[0,0,0],[0,0]] # 연결부위 리스트

A = 0
B = 0
C = 0
D = [0,0,0,0]

#A랑 B 점수 산출
for i in range(n):
  for j in range(n):
    if board[i][j] == 0:
      A += 1
    else:
      B += 1/board[i][j]

#상하좌우 탐색 함수
def find(lists, index:set):
    x, y = index
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    result = []
    for i in range(4):
      if x+dx[i] >=0 and y+dy[i] >=0 and x+dx[i]<3 and y+dy[i]<3: #테두리에 있는 친구들은 -1로  
        a = lists[x+dx[i]][y+dy[i]]
        result.append(a) # 테두리 아닌 값의 상하좌우를 저장
      else:
        result.append(-1) 
    return result

#C랑 D점수 산출
for i in range(n):
  for j in range(n):
    if board[i][j] != 0:
      for index, k in enumerate(find(board, (i,j))):
        print(k)
        # print(index,k)
        if k == -1: #테두리
            pass
        elif k == board[i][j] or k==0:#같거나 0 --> 움직일 수 있음
          match index:
            case 0: # 상
              connecting[2*i-1][j] = 1
              D[0]=1 #위 아래 좌 우 하나씩 검사
            case 1: # 하
              connecting[2*i+1][j] = 1
              D[1]=1 # 하로 움직일 수 있다!
            case 2: # 좌
              connecting[2*i][j-1] = 1
              D[2]=1
            case 3: # 우
              connecting[2*i][j] = 1
              D[3]=1
        elif k / board[i][j] == 2 or k / board[i][j] == 0.5:#나눈 값 2 또는 1/2 --> 비슷함(2)
          match index:
            case 0:
              connecting[2*i-1][j] = 2
            case 1:
              connecting[2*i+1][j] = 2
            case 2:
              connecting[2*i][j-1] = 2
            case 3:
              connecting[2*i][j] = 2


countConnecting = [data for inner_list in connecting for data in inner_list] # connecting을 1차원적으로 합친다.
C = countConnecting.count(2)#가치 비슷한 거 개수
Dscore=sum(D)
res = A*128 + B*4096 + C*256 + Dscore*256
print(res)
