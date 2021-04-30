import pygame,sys,random
from pprint import pprint
import time

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption("CONNECT 4")

SQUARE_SIZE = 100
ROWS,COLS = 6,7
BOARD_HEIGHT,BOARD_WIDTH = SQUARE_SIZE * ROWS,SQUARE_SIZE * COLS
GAP = 200
SCREEN_WIDTH,SCREEN_HEIGHT = BOARD_WIDTH + GAP ,BOARD_HEIGHT + GAP
FPS = 60
BLACK = (0,) * 3
WHITE = (255,) * 3
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (30,144,255)
GREEN = (0,255,0)




class Button(pygame.sprite.Sprite):


    def __init__(self,x,y,text,font,width,height,button_color=RED,text_color=BLACK):
        super().__init__()
        self.original_surface = pygame.Surface((width,height))
        self.original_surface.fill(button_color)
        text =font.render(text,True,text_color)
        self.original_surface.blit(text,(self.original_surface.get_width()//2 - text.get_width()//2,self.original_surface.get_height()//2 - text.get_height()//2))
        self.original_rect = self.original_surface.get_rect(topleft=(x,y))

        self.expanded_surface = pygame.Surface((width + 10,height + 10))
        self.expanded_surface.fill(button_color)
        self.expanded_surface.blit(text,(self.expanded_surface.get_width()//2 - text.get_width()//2,self.expanded_surface.get_height()//2 - text.get_height()//2))
        self.expanded_surface_rect = self.expanded_surface.get_rect(center=self.original_rect.center)

        self.image = self.original_surface
        self.rect = self.original_rect
        self.hovered_on = False
    
    
    def update(self,point):
        
        collision = self.original_rect.collidepoint(point)
        if self.hovered_on and not collision:
            self.image = self.original_surface
            self.rect = self.original_rect
            self.hovered_on = not self.hovered_on
        elif not self.hovered_on and collision:
            self.image = self.expanded_surface
            self.rect = self.expanded_surface_rect
            self.hovered_on = not self.hovered_on

    
    def is_clicked_on(self,point):

        return self.rect.collidepoint(point)


class ConnectK:

    font = pygame.font.SysFont("calibri",40)
    def __init__(self,rows=6,cols=7,k=4,square_size=100,gap=200):
        self.rows = rows
        self.cols = cols
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.square_size = square_size
        self.turn = random.choice(('R','Y'))
        self.k = k
        self.color = RED if self.turn == 'R' else YELLOW
        self.red_turn_text = self.font.render("RED'S TURN!",True,RED)
        self.yellow_turn_text = self.font.render("YELLOW'S TURN!",True,YELLOW)
        self.turn_text = self.red_turn_text if self.turn == 'R' else self.yellow_turn_text
        self.board_height,self.board_width = self.square_size *rows,self.square_size * cols
        self.gap = gap 
        self.invalid = False
        self.invalid_text = self.font.render("COLUMN FULL!",True,BLACK)
        self.screen_width,self.screen_height = self.board_width + gap ,self.board_height + gap
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.game_over = False
        self._play_game()

    
    
    def _draw_board(self,winners=None):



        for row in range(self.rows):
            for col in range(self.cols):
                if winners and (row,col) in winners:
                    square_color = GREEN
                else:
                    square_color = BLUE
                pygame.draw.rect(self.screen,square_color,(col * self.square_size,self.gap + row * self.square_size,self.square_size,self.square_size))
                if self.board[row][col]:
                    if self.board[row][col] == 'R':

                        color = RED
                    elif self.board[row][col] == 'Y':
                        color = YELLOW
                else:
                    color = WHITE

                pygame.draw.circle(self.screen,color,(col * self.square_size + self.square_size//2,self.gap + row * self.square_size + self.square_size//2),self.square_size//2)
                pygame.draw.rect(self.screen,BLACK,(col * self.square_size,self.gap + row * self.square_size,self.square_size,self.square_size),1)




    
    def _play_animation(self,row,col):

        speed = 20

        target_y = self.gap + (row + 1) * self.square_size

        current_y = self.gap


        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            
            current_y += speed
            if current_y >= target_y:
                break

            

            self.screen.fill(WHITE)
            self._draw_board()
            pygame.draw.circle(self.screen,self.color,(col * self.square_size + self.square_size//2,current_y - self.square_size//2),self.square_size//2)

            pygame.display.update()
            clock.tick(FPS)





    def _check_game_over(self,board,row,col):
        # pass in board for future use in AI class that will inherit from this class


        # check vertical
        
        turn = board[row][col]

        current_row = row - 1
        
        up_count = 1

        winners = {(row,col)}

        while current_row >= 0 and board[current_row][col] == turn:
            up_count += 1
            winners.add((current_row,col))
            if up_count == 4:
                print('up')
                return True,self.turn
            current_row -= 1

        

        current_row = row + 1

        down_count = 1
        
        winners = {(row,col)}
        while current_row < len(board) and board[current_row][col] == turn:
            down_count += 1
            winners.add((current_row,col))
            if down_count == 4:
                print('down')
                return True,self.turn,winners


            current_row += 1

        if down_count + up_count  - 1>= 4:
            winners = {(i,col) for i in range(current_row -1,current_row -5,-1)}
            return True,turn,winners
        
        # check rows

        current_col = col - 1
        left_count = 1
        winners = {(row,col)} 
        while current_col >= 0 and board[row][current_col] == turn:
            left_count += 1
            winners.add((row,current_col))
            if left_count == 4:
                print('left')
                return True,turn,winners
            current_col -= 1
        

        current_col = col + 1
        right_count = 1
        winners = {(row,col)}
        while current_col < len(board[0]) and board[row][current_col] == turn:
            right_count += 1
            winners.add((row,current_col))
            if right_count == 4:
                print('right')
                return True,turn,winners
            
            current_col += 1


        if left_count + right_count - 1 >= 4:        
            winners = {(row,i) for i in range(current_col - 1,current_col - 5,-1)}
            return True,turn,winners

        

        up_left_count = 1
        current_row = row - 1
        current_col = col - 1
        winners = {(row,col)}
        while current_row >= 0 and current_col >= 0 and board[current_row][current_col] == turn:
            up_left_count += 1
            winners.add((current_row,current_col))
            if up_left_count == 4:
                return True,turn,winners
            current_row -= 1
            current_col -= 1


        down_right_count = 1

        current_row = row + 1
        current_col = col + 1
        winners = {(row,col)}
        while current_row < len(board) and current_col < len(board[0]) and board[current_row][current_col] == turn:
            down_right_count += 1
            winners.add((current_row,current_col))
            if down_right_count == 4:
                return True,turn,winners

            current_row += 1
            current_col += 1


        if up_left_count + down_right_count - 1 >= self.k:
            winners = {(current_row - 1 - i,current_col - 1 - i) for i in range(4)}
            return True,turn,winners



        down_left_count = 1

        current_row = row + 1
        current_col = col - 1
        
        winners = {(row,col)}
        while current_row < len(board) and current_col >= 0 and board[current_row][current_col] == turn:
            down_left_count += 1
            winners.add((current_row,current_col))
            if down_left_count == self.k:
                return True,turn,winners
            current_row += 1
            current_col -= 1

        up_right_count = 1
        current_row = row - 1
        current_col = col + 1
        
        winners = {(row,col)}
        while current_row >= 0 and current_col < len(board[0]) and board[current_row][current_col] == turn:
            up_right_count += 1
            winners.add((current_row,current_col))
            if up_right_count == self.k:
                return True,turn,winners

            current_row -= 1
            current_col += 1


        if down_left_count  + up_right_count - 1 >= self.k:
            winners = {(current_row + 1 + i,current_col - 1 - i) for i in range(4)}
            return True,turn,winners








        return False,None,None



        


    def _place_piece(self,col):



        row = self.rows - 1

        while row >= 0 and self.board[row][col] is not None:
            row -= 1

        if row >= 0:
            self._play_animation(row,col)
            self.board[row][col] = self.turn
            return row
    
    def _reset(self):

        self.game_over = False
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)] 
        self.turn = random.choice(('R','Y'))
        self.color = RED if self.turn == 'R' else YELLOW
        self.turn_text = self.red_turn_text if self.turn == 'R' else self.yellow_turn_text

    def _play_game(self):

        
        buttons = pygame.sprite.Group()
        
        button_width = 150
        button_height = button_width/2
        
        buttons_x = self.board_width + (self.screen_width - self.board_width)//2 - button_width//2
        button_font = pygame.font.SysFont("calibri",30)

        play_again_button = Button(buttons_x,self.gap + 50,"PLAY AGAIN",button_font,button_width,button_height)
        menu_button = Button(buttons_x,self.gap + 100 + button_height,"MENU",button_font,button_width,button_height)
        buttons.add(play_again_button,menu_button)

        winning_squares = None
        invalid = False
        while True:
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not invalid and event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    
                    if not self.game_over:
                        x,_ = point

                        if x <= self.board_width:
                            col = x//self.square_size
                            row = self._place_piece(col)
                            if row is not None:
                                game_over,_,winning_squares = self._check_game_over(self.board,row,col)
                                if game_over:
                                    winner,color = ('RED',RED) if self.turn == 'R' else ('YELLOW',YELLOW)
                                    self.winner_text= self.font.render(f"{winner} WINS!",True,color)
                                    self.game_over= True

                                self._switch_turns()
                            else:
                                self.invalid = True
                                invalid_start_time = time.time()

                    else:

                        for i,button in enumerate(buttons):
                            if button.is_clicked_on(point):
                                if i == 0:
                                    winning_squares = None
                                    self._reset()


            
            
            if self.invalid:
                current_time = time.time()

                if current_time - invalid_start_time >= 1:
                    self.invalid = False


            
            point = pygame.mouse.get_pos()


            
            self.screen.fill(WHITE)
            

            if not self.game_over:
                x,_ = point
                
                if x <= self.board_width:
                    col = x//self.square_size
                    pygame.draw.circle(self.screen,self.color,(col * self.square_size + self.square_size//2,self.gap - self.square_size//2),self.square_size//2)
            else:
                buttons.update(point)
                buttons.draw(self.screen)
                
            
            
            self._draw_board(winning_squares)
            self._draw_text()

            pygame.display.update()
            clock.tick(FPS)
    
    def _draw_text(self):


        text = self.invalid_text if self.invalid else self.turn_text if not self.game_over else self.winner_text 
        self.screen.blit(text,(self.board_width//2 - text.get_width()//2,50))


    
    def _switch_turns(self):

        if self.turn == 'R':
            self.turn ='Y'
            self.color = YELLOW
            self.turn_text = self.yellow_turn_text
        else:
            self.turn = 'R'
            self.color = RED
            self.turn_text = self.red_turn_text



if __name__ == "__main__":
    

    connect_4 = ConnectK()


        
    
