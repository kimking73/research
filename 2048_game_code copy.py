# build 2048 in python using pygame!!
import pygame
import random
import copy
import time
from evaluation_4x4 import cal
from evauation_by_move import cal_by_around
pygame.init()
evaluate=0
up_avg=0
down_avg=0
left_avg=0
rigfht_avg=0
# initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = False
init_count = 0
direction = ''
score = 0
# file = open('high_score', 'r')
# init_high = int(file.readline())
# file.close()
# high_score = init_high


# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# take your turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board


# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    # high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    # screen.blit(high_score_text, (10, 450))
    pass


# draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


def find_evaluation():
    evaluate,D = cal(board_values)
    z = copy.deepcopy(board_values)
    up,down,left,right = cal_by_around(z)  
    
    value_random = [[],[],[],[]]
    random_1 = 2
    random_2 = 4
    
    for i in range(0,4):
        for j in range(0,4):
            if up[i][j] == 0:
                up[i][j] = random_1
                value,D = cal(up)
                value_random[0].append(value)
                up[i][j] = 0
            if down[i][j] == 0:
                down[i][j] = random_1
                value,D = cal(down)
                value_random[1].append(value)
                down[i][j] = 0
            if left[i][j] == 0:
                left[i][j] = random_1
                value,D = cal(up)
                value_random[2].append(value)
                left[i][j] = 0
            if right[i][j] == 0:
                right[i][j] = random_1
                value,D = cal(right)
                value_random[3].append(value)
                right[i][j] = 0
    count = [0,0,0,0]  
    for i in range(0,4):
        for j in range(0,4):
            if up[i][j] == 0:
                count[0] += 1
                up[i][j] = random_2
                value,D = cal(up)
                value_random[0].append(value)
                up[i][j] = 0
            if down[i][j] == 0:
                count[1] += 1
                down[i][j] = random_2
                value,D = cal(down)
                value_random[1].append(value)
                down[i][j] = 0
            if left[i][j] == 0:
                count[2] += 1
                left[i][j] = random_2
                value,D = cal(up)
                value_random[2].append(value)
                left[i][j] = 0
            if right[i][j] == 0:
                count[3] += 1
                right[i][j] = random_2
                value,D = cal(right)
                value_random[3].append(value)
                right[i][j] = 0
    
    # print(count)
    # print(value_random)
    up_avg = sum(value_random[0])/count[0]
    down_avg = sum(value_random[1])/count[1]
    left_avg = sum(value_random[2])/count[2]
    rigfht_avg = sum(value_random[3])/count[3]
    # print(up_avg)

    return evaluate,up_avg,down_avg,left_avg,rigfht_avg


def blit(evaluate,up,down,left,right):

    text_eval = font.render(str(evaluate),True,'black')
    text_up = font.render(str(up),True,'black')
    text_down = font.render(str(down),True,'black')
    text_left = font.render(str(left),True,'black')
    text_right = font.render(str(right),True,'black') 
    screen.blit(text_eval, (150, 410))
    screen.blit(text_up, (10, 440))
    screen.blit(text_down, (70, 440))
    screen.blit(text_left, (130, 440))
    screen.blit(text_right, (190, 440))
count = 0
# main game loop
run = True
while run:
    evaluate=0
    up_avg=0
    down_avg=0
    left_avg=0
    rigfht_avg=0
    highest = [0,0]
    #print('------------------------------------------------------')
    # print(board_values) # 판의 숫자들이 저장되어 있다.
    first =board_values
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if count < 1:
        board_values, game_over = new_pieces(board_values)
        board_values, game_over = new_pieces(board_values)
        count +=1
    evaluate,up_avg,down_avg,left_avg,rigfht_avg = find_evaluation()
    evaluate_divided = int(evaluate/100)
    up_avg_divided=int(up_avg/100)
    down_avg_divided = int(down_avg/100)
    left_avg_divided = int(left_avg/100)
    right_avg_divided = int(rigfht_avg/100)
    divided_list = [up_avg_divided,down_avg_divided,left_avg_divided,right_avg_divided]
    highest = [up_avg_divided,0]
    for index,value in enumerate (divided_list) :
        if value > highest[0]:
            highest[0] = value
            highest[1] = index
    print(highest)
    if highest[1] == 0:
        direction = 'UP'
    if highest[1] == 1:
        direction = 'DOWN'
    if highest[1] == 2:
        direction = 'LEFT'
    if highest[1] == 3:
        direction = 'RIGHT'

    print(direction)


    evaluate,up_avg,down_avg,left_avg,rigfht_avg = find_evaluation()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    direction = 'UP'
                    evaluate,up_avg,down_avg,left_avg,rigfht_avg = find_evaluation()
                elif event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                    evaluate,up_avg,down_avg,left_avg,rigfht_avg = find_evaluation()
                elif event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                    evaluate,up_avg,down_avg,left_avg,rigfht_avg = find_evaluation()
                elif event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'
                    evaluate,up_avg,down_avg,left_avg,rigfht_avg = find_evaluation()

                if game_over:
                    quit()
                    if event.key == pygame.K_RETURN:
                        board_values = [[0 for _ in range(4)] for _ in range(4)]
                        spawn_new = True
                        init_count = 0
                        score = 0
                        direction = ''
                        game_over = False
                        

    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        draw_over()

    # time.sleep(0.05)
    if spawn_new: # init_count : 시작 때 2개를 기본값으로 주기 위하여 존개
        # print('-----')
        # print('before : ',board_values[0])
        # print('before : ',board_values[1])
        # print('before : ',board_values[2])
        # print('before : ',board_values[3])
        # print('-----')
        board_values, game_over = new_pieces(board_values)
        # print('after : ',board_values[0])
        # print('after : ',board_values[1])
        # print('after : ',board_values[2])
        # print('after : ',board_values[3])
        # print('-----')
        spawn_new = False
    

    # if score > high_score:
    #     high_score = score


    # print(up_avg_divided)
    divided_list = [up_avg_divided,down_avg_divided,left_avg_divided,right_avg_divided]
    blit(evaluate_divided,up_avg_divided,down_avg_divided,left_avg_divided,right_avg_divided)
    



    
    end =board_values
    if first != end:
        print("error")
    pygame.display.flip()
    # print('final : ',board_values[0])
    # print('final : ',board_values[1])
    # print('final : ',board_values[2])
    # print('final : ',board_values[3])
    # print(direction)
pygame.quit()