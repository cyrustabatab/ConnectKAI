import pygame,sys,random
from pprint import pprint
import time

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption("CONNECT K")

SQUARE_SIZE = 100
ROWS,COLS = 6,7
BOARD_HEIGHT,BOARD_WIDTH = SQUARE_SIZE * ROWS,SQUARE_SIZE * COLS
GAP = 200
SCREEN_WIDTH,SCREEN_HEIGHT = BOARD_WIDTH + GAP ,BOARD_HEIGHT + GAP
FPS = 60
BLACK = (0,) * 3
WHITE = (255,) * 3
RED = (255,0,0)
TRANSPARENT_RED = (255,0,0,128)
YELLOW = (255,255,0)
TRANSPARENT_YELLOW = (255,255,0,128)
BLUE = (30,144,255)
GREEN = (0,255,0)
BGCOLOR = (144,248,144)





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


class Menu:

    menu_font = pygame.font.SysFont("calibri",60)
    def __init__(self,screen_width=800,screen_height=800):

        self.screen = pygame.display.set_mode((screen_width,screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_text = self.menu_font.render("CONNECT K",True,BLACK)
        top_gap = 50
        self.title_text_rect = self.title_text.get_rect(center=(screen_width//2,top_gap + self.title_text.get_height()//2 ))
        button_width = 350
        button_height = button_width//2
        buttons_x = screen_width//2 - button_width//2
        self.two_player_button = Button(buttons_x,self.title_text_rect.bottom + top_gap,"TWO PLAYER",self.menu_font,button_width,button_height)
        self.computer_button = Button(buttons_x,self.title_text_rect.bottom + 2 * top_gap + button_height,"COMPUTER",self.menu_font,button_width,button_height)
        self.buttons = pygame.sprite.Group(self.two_player_button,self.computer_button)
        self._menu()
    
    

    def _gravity_or_no_gravity_screen(self):

        gap = 100
        button_height = (self.screen_height - gap * 3)//2
        button_width = button_height * 2
        buttons_x= self.screen_width//2 - button_width//2
        gravity_button = Button(buttons_x,gap,"GRAVITY",self.menu_font,button_width,button_height)
        no_gravity_button = Button(buttons_x,self.screen_height - gap - button_height,"NO GRAVITY",self.menu_font,button_width,button_height)

        buttons = pygame.sprite.Group()

        buttons.add(gravity_button,no_gravity_button)



        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()

                    for i,button in enumerate(buttons):
                        if button.is_clicked_on(point):
                            if i == 0:
                                return True
                            else:
                                return False
                            


                


            point = pygame.mouse.get_pos() 
            buttons.update(point)


            self.screen.fill(BGCOLOR)
            buttons.draw(self.screen)
            pygame.display.update()







    def _standard_or_custom_screen(self):
        

        
        gap = 100
        button_height = (self.screen_height - gap * 3)//2
        button_width = button_height * 2
        buttons_x= self.screen_width//2 - button_width//2
        standard_button = Button(buttons_x,gap,"STANDARD",self.menu_font,button_width,button_height)
        custom_button = Button(buttons_x,self.screen_height - gap - button_height,"CUSTOM",self.menu_font,button_width,button_height)

        buttons = pygame.sprite.Group(standard_button,custom_button)



        default_values = (4,6,7)
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()

                    for i,button in enumerate(buttons):
                        if button.is_clicked_on(point):
                            if i == 0:
                                return default_values
                            else:
                                result= self._custom_screen()
                                return result


            
            point = pygame.mouse.get_pos()
            buttons.update(point)

            self.screen.fill(BGCOLOR)
            buttons.draw(self.screen)


            pygame.display.update()




    def _custom_screen(self):


        title_text = self.menu_font.render("CUSTOM GAME",True,BLACK)
        top_gap = 50
        title_text_rect = title_text.get_rect(center=(self.screen_width//2,top_gap + title_text.get_height()//2 ))

        cursor_index = 0
        texts = [f'K: 4|','ROWS: 6','COLS: 7']


        lengths = [len(text) - 1 for text in texts]

        lengths[0] -= 1
        
        button_width = 350
        button_height = button_width//2
        buttons_x =  self.screen_width//2  - button_width//2
        play_again_button = Button(buttons_x,self.screen_height - 50 - button_height,"START GAME",self.menu_font,button_width,button_height)

        

        button = pygame.sprite.GroupSingle(play_again_button)



        

        def render_and_draw_texts():


            left_gap = 50
            for i,text in enumerate(texts):
                text = self.menu_font.render(text,True,BLACK)
                self.screen.blit(text,(left_gap,title_text_rect.bottom + top_gap + (top_gap + text.get_height()) * i))



        
        def get_values():

            
            values = []
            for text in texts:
                index = text.index(' ')
                last = text[-1]
                value = text[index:] if last != '|' else text[index:-1]
                values.append(value)

            return values







        flickering_event = pygame.USEREVENT + 10

        pygame.time.set_timer(flickering_event,200)

        
        invalid_text = None
        invalid_font = pygame.font.SysFont("calibri",40)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    
                    last = texts[cursor_index][-1]
                    if pygame.K_0 <= event.key <= pygame.K_9:
                        value = chr(event.key)
                        last = texts[cursor_index][-1]
                        if last != '|':
                            texts[cursor_index] += value 
                        else:
                            texts[cursor_index] = texts[cursor_index][:-1] + value + '|'
                    elif event.key == pygame.K_BACKSPACE:
                        last = texts[cursor_index][-1]
                        length = len(texts[cursor_index]) - (1 if last == '|' else 0)
                        if length != lengths[cursor_index]:
                            index = -2 if texts[cursor_index][-1] == '|' else -1
                            texts[cursor_index] = texts[cursor_index][:index]
                    elif event.key == pygame.K_RETURN:
                        if cursor_index < 2:
                            if last == '|':
                                texts[cursor_index] = texts[cursor_index][:-1]
                            cursor_index += 1
                    elif event.key == pygame.K_UP:

                        if cursor_index > 0:
                            if last == '|':
                                texts[cursor_index] = texts[cursor_index][:-1]
                            cursor_index -= 1
                    elif event.key == pygame.K_DOWN:

                        if cursor_index < 2:
                            if last == '|':
                                texts[cursor_index] = texts[cursor_index][:-1]
                            cursor_index += 1
                elif event.type == flickering_event:
                    last = texts[cursor_index][-1]
                    if last == '|':
                        texts[cursor_index] = texts[cursor_index][:-1]
                    else:
                        texts[cursor_index] += '|'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()

                    if button.sprite.is_clicked_on(point): 
                        values = get_values()
                        k,rows,cols = values
                        valid = True
                        if any(value == ' ' for value in values):
                            invalid_text = invalid_font.render("No Empty Values!",True,BLACK)  
                            invalid_start = time.time()
                        else:
                            values = list(map(int,values))
                            if any(value < 3 for value in values):
                                invalid_text = invalid_font.render("K, ROWS, and COLS Must All Be At Least 3!",True,BLACK)  
                                invalid_start = time.time()
                            else:
                                return values


                            
            if invalid_text:  
                current_time = time.time()
                if current_time - invalid_start >= 1:
                    invalid_text = None






              
            point = pygame.mouse.get_pos() 
            button.update(point)
            

            self.screen.fill(BGCOLOR)
            button.draw(self.screen)
            self.screen.blit(title_text,title_text_rect)
            render_and_draw_texts()

            if invalid_text:
                self.screen.blit(invalid_text,(self.screen_width//2 - invalid_text.get_width()//2,self.screen_height - 100 - button_height - invalid_text.get_height()))


            pygame.display.update()
            clock.tick(FPS)









    
    def _menu(self):



        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    for i,button in enumerate(self.buttons):
                        if button.is_clicked_on(point):
                            if i == 0:
                                gravity = self._gravity_or_no_gravity_screen()
                                k,rows,cols = self._standard_or_custom_screen()
                                square_size = BOARD_HEIGHT//rows
                                connect_k = ConnectK(rows,cols,k,square_size,gravity=gravity)
                                #self._custom_screen()
                                pygame.display.set_caption("Connect K")
                                pygame.display.set_mode((self.screen_width,self.screen_height))



            

            point = pygame.mouse.get_pos()
            self.buttons.update(point)
            
            self.screen.fill(BGCOLOR)

            self.screen.blit(self.title_text,self.title_text_rect)
            self.buttons.draw(self.screen)
            pygame.display.update()

class ConnectK:

    font = pygame.font.SysFont("calibri",40)
    column_full_sound = pygame.mixer.Sound("wrong.wav")
    pop_sound = pygame.mixer.Sound("pop_sound.wav")
    def __init__(self,rows=6,cols=7,k=4,square_size=100,gap=200,gravity=True):
        self.rows = rows
        self.cols = cols
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.square_size = square_size
        self.turn = random.choice(('R','Y'))
        self.k = k
        s = 'NO GRAVITY' if not gravity else 'GRAVITY'
        pygame.display.set_caption(f"CONNECT {str(k)} {s}")
        self.color = RED if self.turn == 'R' else YELLOW
        self.red_turn_text = self.font.render("RED'S TURN!",True,RED)
        self.yellow_turn_text = self.font.render("YELLOW'S TURN!",True,YELLOW)
        self.turn_text = self.red_turn_text if self.turn == 'R' else self.yellow_turn_text
        self.board_height,self.board_width = self.square_size *rows,self.square_size * cols
        self.gravity = gravity
        self.gap = gap 
        self.turns = 0
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

        center_y = self.square_size//2






        

        pop_sound_event  = pygame.USEREVENT + 2
        pygame.time.set_timer(pop_sound_event,100)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pop_sound_event:
                    self.pop_sound.play()
            
            
            current_y += speed
            if current_y >= target_y:
                break
                    
            










            

            self.screen.fill(BGCOLOR)
            self._draw_board()
            pygame.draw.circle(self.screen,self.color,(col * self.square_size + self.square_size//2,current_y - self.square_size//2),self.square_size//2)

            pygame.display.update()
            clock.tick(FPS)


        pygame.time.set_timer(pop_sound_event,0)


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
            if up_count == self.k:
                print('up')
                return True,self.turn,winners
            current_row -= 1

        

        current_row = row + 1

        down_count = 1
        
        winners = {(row,col)}
        while current_row < len(board) and board[current_row][col] == turn:
            down_count += 1
            winners.add((current_row,col))
            if down_count == self.k:
                print('down')
                return True,self.turn,winners


            current_row += 1

        if down_count + up_count  - 1>= self.k:
            winners = {(i,col) for i in range(current_row -1,current_row -5,-1)}
            return True,turn,winners
        
        # check rows

        current_col = col - 1
        left_count = 1
        winners = {(row,col)} 
        while current_col >= 0 and board[row][current_col] == turn:
            left_count += 1
            winners.add((row,current_col))
            if left_count == self.k:
                print('left')
                return True,turn,winners
            current_col -= 1
        

        current_col = col + 1
        right_count = 1
        winners = {(row,col)}
        while current_col < len(board[0]) and board[row][current_col] == turn:
            right_count += 1
            winners.add((row,current_col))
            if right_count == self.k:
                print('right')
                return True,turn,winners
            
            current_col += 1


        if left_count + right_count - 1 >= self.k:        
            winners = {(row,i) for i in range(current_col - 1,current_col - 5,-1)}
            return True,turn,winners

        

        up_left_count = 1
        current_row = row - 1
        current_col = col - 1
        winners = {(row,col)}
        while current_row >= 0 and current_col >= 0 and board[current_row][current_col] == turn:
            up_left_count += 1
            winners.add((current_row,current_col))
            if up_left_count == self.k:
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
            if down_right_count == self.k:
                return True,turn,winners

            current_row += 1
            current_col += 1


        if up_left_count + down_right_count - 1 >= self.k:
            winners = {(current_row - 1 - i,current_col - 1 - i) for i in range(self.k)}
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
            winners = {(current_row + 1 + i,current_col - 1 - i) for i in range(self.k)}
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
        self.turns = 0
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if not invalid and event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    
                    if not self.game_over:

                        x,y = point
                    
                        if x <= self.board_width:
                            col = x//self.square_size
                            if self.gravity:
                                row = self._place_piece(col)
                            else:
                                if y >= self.gap:
                                    row = (y - self.gap)//self.square_size
                                    if self.board[row][col] is None:
                                        self.board[row][col] = self.turn
                                    else:
                                        row = None
                                else:
                                    row = None
                            if row is not None:
                                game_over,_,winning_squares = self._check_game_over(self.board,row,col)
                                if game_over:
                                    winner,color = ('RED',RED) if self.turn == 'R' else ('YELLOW',YELLOW)
                                    self.winner_text= self.font.render(f"{winner} WINS!",True,color)
                                    self.game_over= True
                                self.turns += 1
                                if not self.game_over and self.turns == self.rows * self.cols:
                                    self.winner_text = self.font.render(f"TIE!",True,BLACK)
                                    self.game_over = True
                                self._switch_turns()
                            elif self.gravity:
                                self.column_full_sound.play()
                                self.invalid = True
                                invalid_start_time = time.time()

                    else:

                        for i,button in enumerate(buttons):
                            if button.is_clicked_on(point):
                                if i == 0:
                                    winning_squares = None
                                    self._reset()
                                else:
                                    return


            
            
            if self.invalid:
                current_time = time.time()

                if current_time - invalid_start_time >= 1:
                    self.invalid = False


            
            point = pygame.mouse.get_pos()
            x,y = point


            
            self.screen.fill(BGCOLOR)
            

            if not self.game_over and self.gravity:
                    
                if x <= self.board_width:
                    col = x//self.square_size
                    
                    pygame.draw.circle(self.screen,self.color,(col * self.square_size + self.square_size//2,self.gap - self.square_size//2),self.square_size//2)




            else:
                buttons.update(point)
                buttons.draw(self.screen)
                
            
            
            self._draw_board(winning_squares)

            if not self.gravity:
                if x <= self.board_width and y >= self.gap:
                    col = x//self.square_size
                    row = (y - self.gap) //self.square_size
                    if self.board[row][col] is None:
                        transparent_surface = pygame.Surface((self.square_size,self.square_size),pygame.SRCALPHA)
                        color = TRANSPARENT_YELLOW if self.color == YELLOW else TRANSPARENT_RED
                        pygame.draw.circle(transparent_surface,color,(self.square_size//2,self.square_size//2),self.square_size//2)
                        self.screen.blit(transparent_surface,(col * self.square_size,self.gap + row * self.square_size))
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
    

    menu = Menu()


        
    
