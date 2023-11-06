import pygame
import numpy as np
import time
import requests, json
import threading
import queue
import websocket
import time
import tkinter as tk
import re
import ast





current_player=1

BOARD_SIZE = 15
board = np.zeros([BOARD_SIZE, BOARD_SIZE], dtype=str)
memory = [None]
online_board=0
WIDTH, HEIGHT = 1000, 1000# 두 값이 일치한다는 전제조건 하에 코드를 작성함
STONE_SIZE = int(WIDTH / BOARD_SIZE-(WIDTH / BOARD_SIZE)/10)
blank = (WIDTH-STONE_SIZE*(BOARD_SIZE+1))/2 # 여백 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (160, 90, 40)
GOLD = (255,215,0)
RED = (255,0,0)
GREEN=(191,255,0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("오목 게임")
font = pygame.font.SysFont("arial",30,True,True)


def draw_board():
    global memory
    for i in range(BOARD_SIZE-1):
        for j in range(BOARD_SIZE-1):
              # 그리드 그리기
            pygame.draw.rect(screen, BLACK, ((j+1)*STONE_SIZE+blank, (i+1)*STONE_SIZE+blank, STONE_SIZE, STONE_SIZE), 2)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == '1':
                # 플레이어 1의 돌 그리기 (검은색 돌)
                stone_x = j*STONE_SIZE+STONE_SIZE//2 + blank+STONE_SIZE/2
                stone_y = i*STONE_SIZE+STONE_SIZE//2 + blank+STONE_SIZE/2
                pygame.draw.circle(screen, BLACK, (stone_x, stone_y), STONE_SIZE//2-2)
            elif board[i][j] == '2':
                # 플레이어 2의 돌 그리기 (흰색 돌)
                stone_x = j*STONE_SIZE+STONE_SIZE//2 + blank+STONE_SIZE/2
                stone_y = i*STONE_SIZE+STONE_SIZE//2 + blank+STONE_SIZE/2
                pygame.draw.circle(screen, WHITE, (stone_x, stone_y), STONE_SIZE//2-2)
            elif board[i][j] == 'w':
                # 이긴 돌 표시 (금색 돌)
                stone_x = j*STONE_SIZE+STONE_SIZE//2 + blank+STONE_SIZE/2
                stone_y = i*STONE_SIZE+STONE_SIZE//2 + blank+STONE_SIZE/2
                pygame.draw.circle(screen, GOLD, (stone_x, stone_y), STONE_SIZE//2-2)
            elif board[i][j] == 'P':
                stone_x = j*STONE_SIZE+STONE_SIZE//2 + blank+STONE_SIZE/2
                stone_y = i*STONE_SIZE+STONE_SIZE//2 + blank+STONE_SIZE/2
                pygame.draw.circle(screen, RED, (stone_x, stone_y), STONE_SIZE//2-2,2)
            elif board[i][j] == 'x':
                # 금지된 영역 표시 (빨간 선)
                  
                line_x1 = j*STONE_SIZE + blank+STONE_SIZE/2
                line_y1 = i*STONE_SIZE + blank+STONE_SIZE/2
                line_x2 = (j+1)*STONE_SIZE + blank+STONE_SIZE/2
                line_y2 = (i+1)*STONE_SIZE + blank+STONE_SIZE/2
                pygame.draw.line(screen, RED, (line_x1, line_y1), (line_x2, line_y2), 5)
                line_x3 = (j+1)*STONE_SIZE + blank+STONE_SIZE/2
                line_y3 = i*STONE_SIZE + blank+STONE_SIZE/2
                line_x4 = j*STONE_SIZE + blank+STONE_SIZE/2
                line_y4 = (i+1)*STONE_SIZE + blank+STONE_SIZE/2
                pygame.draw.line(screen, RED, (line_x3, line_y3), (line_x4, line_y4), 5)
    
    if memory[0]!=None:
        stone_x = memory[1]*STONE_SIZE+STONE_SIZE//2 + blank+STONE_SIZE/2
        stone_y = memory[0]*STONE_SIZE+STONE_SIZE//2 + blank+STONE_SIZE/2
        pygame.draw.circle(screen,GREEN,(stone_x, stone_y), STONE_SIZE//8)





            
                
   
    

def rule(player):
    if player ==1:
         pass
     
def cross():
    for i in range(BOARD_SIZE-4):
        for j in range(4, BOARD_SIZE):
            if board[i][j] != "" and \
            board[i][j] == board[i+1][j-1] and \
            board[i+1][j-1] == board[i+2][j-2] and \
            board[i+2][j-2] == board[i+3][j-3] and \
            board[i+3][j-3] == board[i+4][j-4] and \
            board[i][j]!= "P"   :

                board[i][j] = "w"
                board[i+1][j-1] = "w"
                board[i+2][j-2] = "w"
                board[i+3][j-3] = "w"
                board[i+4][j-4] = "w"
                print('역대각선 yes!')
                return True

    for i in range(4, BOARD_SIZE):
        for j in range(4, BOARD_SIZE):
            if board[i][j] != "" and \
            board[i][j] == board[i-1][j-1] and \
            board[i-1][j-1] == board[i-2][j-2] and \
            board[i-2][j-2] == board[i-3][j-3] and \
            board[i-3][j-3] == board[i-4][j-4] and \
            board[i][j]!= "P"   :
                board[i][j] = "w"
                board[i-1][j-1] = "w"
                board[i-2][j-2] = "w"
                board[i-3][j-3] = "w"
                board[i-4][j-4] = "w"







                print('정대각선yes!')
                return True

    for i in range(BOARD_SIZE):
        for j in range( BOARD_SIZE-4):
            if board[i][j]!= "" and \
            board[i][j] == board[i][j+1] and \
            board[i][j+1] == board[i][j+2] and \
            board[i][j+2] == board[i][j+3] and \
            board[i][j+3] == board[i][j+4] and \
            board[i][j]!= "P"   :
                board[i][j] = "w"
                board[i][j+1] = "w"
                board[i][j+2] = "w"
                board[i][j+3] = "w"
                board[i][j+4] = "w"
                print('가로yes!')
                return True
    for j in range(BOARD_SIZE):
        for i in range( BOARD_SIZE-4):
            if board[i][j]!= "" and \
            board[i][j] == board[i+1][j] and \
            board[i+1][j] == board[i+2][j] and \
            board[i+2][j] == board[i+3][j] and \
            board[i+3][j] == board[i+4][j] and \
            board[i][j]!= "P"   :
                board[i][j] = "w"
                board[i+1][j] = "w"
                board[i+2][j] = "w"
                board[i+3][j] = "w"
                board[i+4][j] = "w"






                print('세로yes!')
        
        
        
                return True
            

#버튼 위치 담당(y 좌표)
base=100
base2=300
base3=-300

game = False
menu = 0
Turn = False


def gamestart():
    global game
    print("게임 시작")
    game=True


def main_buttion(value):
    global menu
    print("버튼 클릭",value)
    menu=value




    # WebSocket 연결 열기



    # 연결 반환
    
 
online_mode=False


thread=False

ws=0

def data_receive():
    global thread
    thread=True
    
    
    
    try:
        global ws 
        url = f'ws://127.0.0.1:3000'
        ws = websocket.create_connection(url)
    except:
        print('오프라인 모드')
        thread=False
    while True:
        global online_board,online_mode,game,board
        data = ws.recv()
        print(data)
        # 받은 데이터 처리
        
        
        
        
        if data=='매칭':
            online_mode=True
            game=True
            print('매칭')

      
    
        elif online_mode and game:
            try:
                if cross():
                    print("플레이어 {} 승리!".format(current_player))
                    win = current_player
                    
                data=data[1:]
                
                data = re.sub(r'\[|\]', '', data)
                result = data.split(",")
                
                
                    
                print('b',result)
                board[int(result[1])][int(result[2])]=result[0]
                
                
                
            except:
                pass

            
            
            
           

            
                
            
                # print(q.get())
            
       

data3={
#   'headers':'matching',
  'id':'ysj',
'headers':'matching'

}

button_width, button_height = 400, 100

button_x, button_y = (WIDTH - button_width) // 2, (HEIGHT - button_height) // 2
# Font settings
font = pygame.font.Font(None, 72)
font2 = pygame.font.Font(None, 160)
button_text = font.render("game start", True, WHITE)
text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2+100))
button_text2 = font.render("multiplay", True, WHITE)
text_rect2 = button_text2.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2+200 ))  # Adjusted y-position
button_text4 = font2.render("THE Oooomok", True, WHITE)
text_rect4 = button_text4.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2 -180))

def makebutton(T,C,x,y,font): #글,색 x,y 좌표 ,배수 , 폰트 
    button_text = font.render(T, True, C)
    text_rect = button_text.get_rect(center=(button_x + button_width // 2-x, button_y + button_height // 2 +y))
    return button_text,text_rect





win=None


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
           
        
                    # Check if the mouse click is within the button area
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_pos = pygame.mouse.get_pos()
            if game==True:
                x, y = event.pos
                pos1=(x - blank-STONE_SIZE/2) / STONE_SIZE
                pos2=(y - blank-STONE_SIZE/2) / STONE_SIZE
                j, i = int((x - blank-STONE_SIZE/2) / STONE_SIZE), int((y - blank-STONE_SIZE/2) / STONE_SIZE)  # blank를 빼서 좌표를 보정
                print(i,j)
                print(pos1,pos2)
               

                if not i>BOARD_SIZE-1 and not j>BOARD_SIZE-1 and pos1>0 and pos2>0:
                    if online_mode:
                        ws.send(json.dumps({'x':i,'y':j}))
                        
                    elif board[i][j] == ""or board[i][j] == "P":
                        if Turn==True:
                           
                            if board[i][j] == "P":
                                
                                board[i][j] = current_player
                                memory=[i,j]
                                if cross():
                                    print("플레이어 {} 승리!".format(current_player))
                                    win = current_player
                        
                                current_player = 3 - current_player  # 1 -> 2, 2 -> 1
                                Turn=False
                            else:
                                Turn=False
                                print('위치 불일치')
                                for i in range(BOARD_SIZE):
                                    for j in range(BOARD_SIZE):
                                        if board[i, j] == 'P':
                                            board[i, j] = ''

                                
                        else:
                             board[i][j] = "P"
                             Turn=True
                            
                             
                        
                        
                    else:
                        print('돌이 있는 자리입니다')
                else:
                    print('범위 초과')
            else:
                if pygame.Rect((button_x, button_y+base, button_width, button_height)).collidepoint(mouse_pos):
                    if menu ==0:
                        main_buttion(1)
                    elif menu==1:
                        gamestart()
                    
                    
                elif pygame.Rect((button_x, button_y +base2, button_width, button_height)).collidepoint(mouse_pos) and not thread:
                    if menu == 0:
                        print("Multiplay button clicked!")
                        q = queue.Queue()
                        thread = threading.Thread(target=data_receive, args=())
                        thread.daemon = True
                        thread.start()
                    elif menu==1:
                        print('2')
                        
             
                  
                elif pygame.Rect((button_x-(button_width/2) , button_y +base3-(button_height/2), button_width*2, button_height*2)).collidepoint(mouse_pos) and menu==0:
                    print("THE Oooomok button clicked!")  
                elif pygame.Rect((button_x-(WIDTH-button_x)/2)+button_width/4, button_y+HEIGHT-(button_y*3), button_width/2, button_height).collidepoint(mouse_pos) and menu==1:
                    print("BACK")  
                    menu=0


      # 화면 업데이트
    if game==True:
        screen.fill(BROWN)
        draw_board()
        pygame.display.update()
        if win!=None:
            if win==1:
                win='BLACK'
            else:
                win='WHITE'
            button_text3 = font.render(str(win)+" is win!", True, WHITE)
            text_rect3 = button_text3.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2 ))  
            pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height))
            screen.blit(button_text3, text_rect3)
            pygame.display.update()
            time.sleep(3)
            board = np.zeros([BOARD_SIZE, BOARD_SIZE], dtype=str)
            game=False
            win=None
            menu=0
        
    elif menu==0: #메인 메뉴
        screen.fill(WHITE)
        # button_text = font.render("game start", True, WHITE)
        # text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2+100))
        # button_text2 = font.render("multiplay", True, WHITE)
        # text_rect2 = button_text2.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2+200 ))  # Adjusted y-position
        # button_text4 = font2.render("THE Oooomok", True, WHITE)
        # text_rect4 = button_text4.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2 -180))

        a,b=makebutton('game start',WHITE,0,base,font)
        c,d=makebutton('multiplay',WHITE,0,base2,font)
        e,f=makebutton('THE Oooomok',WHITE,0,base3,font2)







        
        pygame.draw.rect(screen, BLACK, (button_x, button_y+base, button_width, button_height))
        pygame.draw.rect(screen, BLACK, (button_x, button_y +base2, button_width, button_height))  
        pygame.draw.rect(screen, BLACK, (button_x-(button_width/2) , button_y +base3-(button_height/2), button_width*2, button_height*2))
        screen.blit(a, b)
        screen.blit(c, d)
        screen.blit(e, f)
        pygame.display.flip()
    elif menu==1: #game start 버튼 클릭시
        a,b=makebutton('SOLO MODE',WHITE,0,base,font) #글,색 x,y 좌표 , 폰트
        c,d=makebutton('AI MODE',WHITE,0,base2,font) #글,색 x,y 좌표 , 폰트
        e,f=makebutton('BACK',WHITE,((WIDTH-button_x)/2),HEIGHT-(button_y*3),font)
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (button_x, button_y+base, button_width, button_height))
        pygame.draw.rect(screen, BLACK, (button_x, button_y+base2, button_width, button_height)) 
        pygame.draw.rect(screen, BLACK, ((button_x-(WIDTH-button_x)/2)+button_width/4, button_y+HEIGHT-(button_y*3), button_width/2, button_height)) 
        screen.blit(a, b)
        screen.blit(c, d)
        screen.blit(e, f)
       
        
        pygame.display.flip()
    

cross()
time.sleep(2)
print(board)