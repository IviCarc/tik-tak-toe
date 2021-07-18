import pygame
import random
from pygame import draw
from pygame.constants import KEYDOWN
import pygame.gfxdraw
pygame.init()

class Game:
    def __init__(self):
        
        running = True
        while running:
            pos = pygame.mouse.get_pos()

            # Sets the display and draw the table
            self.screen_width, self.screen_height = 1024, 800
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Tik Tak Toe")
            self.lines_color = (255, 255, 255)
            self.text_color = (0,0,0)

            # Sets font
            self.font = pygame.font.SysFont("Century Gothic", 60)
            width, height = self.screen_width/2, self.screen_height/2
            pos_width, pos_height = self.screen_width/3, self.screen_height/3
            # Sets all positions or buttons, first element on the array is the rectangle, te second is it's value on the game
            self.positions = {
                "pos0": [pygame.Rect(0, 0, pos_width, pos_height), 0],
                "pos1": [pygame.Rect(pos_width, 0, pos_width, pos_height), 1],
                "pos2": [pygame.Rect(pos_width*2, 0, pos_width, pos_height), 2],
                "pos3": [pygame.Rect(0, pos_height, pos_width, pos_height), 3],
                "pos4": [pygame.Rect(pos_width, pos_height, pos_width, pos_height), 4],
                "pos5": [pygame.Rect(pos_width * 2, pos_height, pos_width, pos_height), 5],
                "pos6": [pygame.Rect(0, pos_height*2, pos_width, pos_height), 6],
                "pos7": [pygame.Rect(pos_width, pos_height*2,pos_width, pos_height), 7],
                "pos8": [pygame.Rect(pos_width * 2, pos_height*2, pos_width, pos_height), 8]
            }

            # Creates title
            title_text = "Select the mode you wanna play"
            title_width, title_height = self.font.size(title_text)
            self.draw_text(title_text, self.font, self.lines_color, self.screen, width - title_width / 2, height - 200)

            # Creates PvP option
            pvp_rect = pygame.Rect(self.screen_width / 8, self.screen_height / 2.3, 250, 125)
            if pvp_rect.collidepoint(pos): #Add a hover
                pygame.draw.rect(self.screen, (155,155,155), pvp_rect)
            else:
                pygame.draw.rect(self.screen, self.lines_color, pvp_rect)
            pvp_width, pvp_height = self.font.size("PVP")
            self.draw_text("PVP", self.font, self.text_color, self.screen, pvp_rect.centerx - pvp_width / 2, pvp_rect.centery - pvp_height /2)

            # Creates pvIa option
            pv_ia_rect = pygame.Rect((self.screen_width / 8) * 5, self.screen_height / 2.3, 250, 125)
            if pv_ia_rect.collidepoint(pos): # Add a hover    
                pygame.draw.rect(self.screen, (155,155,155), pv_ia_rect)
            else:
                pygame.draw.rect(self.screen, self.lines_color, pv_ia_rect)
            pv_ia_width, pv_ia_height = self.font.size("IA")
            self.draw_text("IA", self.font, self.text_color, self.screen, pv_ia_rect.centerx - pv_ia_width / 2, pv_ia_rect.centery - pv_ia_height / 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pvp_rect.collidepoint(pos):
                        self.pvp()
                    if pv_ia_rect.collidepoint(pos):
                        self.pvIA()
            
            pygame.display.update()
        
    def pvp(self):
        # # Create the main array
        self.game = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.screen.fill((0,0,0))
        self.draw_line()
       
        # 0 is player 1, 1 is player 2

        win = False  # While win is false, the game will be expecting click events
        turn = True  # Sets the turn, if True it's players one turn
        running = True
        count = 0  # Set a count variable, it represents how many turns have passed since the game started
        restart_btn = None  # When the game is finished, these two variables
        return_btn = None   # will represent each one a btn
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not win:
                        for k, v in self.positions.items():
                            if v[0].collidepoint(pos):
                                if self.game[v[1]] != 0 and self.game[v[1]] != 1:
                                    self.draw_fig(v[0].center, turn)
                                    if turn: self.game[v[1]] = 0
                                    else: self.game[v[1]] = 1
                                    turn = not turn
                                    count += 1
                    else:
                        if restart_btn.collidepoint(pos):
                            self.screen.fill((0,0,0))
                            self.pvp()
                        elif return_btn.collidepoint(pos):
                            running = False
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if self.check_win() and not win:
                win = True
                if turn: text = "PLAYER TWO WINS!!"
                else: text = "PLAYER ONE WINS!!"
                width, height = self.font.size(text)
                self.draw_text(text, self.font, self.text_color, self.screen,
                               self.screen_width / 2 - width / 2, self.screen_height / 2 - 200, True)
                restart_btn, return_btn = self.end_btns()
            #Checks for a tie
            if count == len(self.game) and not win:
                text = "TIE"
                width, height = self.font.size(text)
                self.draw_text(text, self.font, self.text_color, self.screen,
                               self.screen_width / 2 - width / 2, self.screen_height / 2 - 200, True)
                restart_btn, return_btn = self.end_btns()
                win = True
            # Add a hover
            if win:
                pos = pygame.mouse.get_pos()
                if restart_btn.collidepoint(pos):
                    self.end_btns(res_hover=True)
                elif return_btn.collidepoint(pos):
                    self.end_btns(rtrn_hover=True)
                else:
                    self.end_btns()
            pygame.display.update()

    def pvIA(self):
        # # Create the main array
        self.game = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.screen.fill((0, 0, 0))
        self.draw_line()

        # 0 is player 1, 1 is IA  
        win = False  # While win is false, the game will be expecting click events
        running = True
        turn = True
        count = 0  # Set a count variable, it represents how many turns have passed since the game started
        restart_btn = None  # When the game is finished, these two variables
        return_btn = None   # will represent each one a btn
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not win:
                        for k, v in self.positions.items():
                            if v[0].collidepoint(pos):
                                if self.game[v[1]] != 0 and self.game[v[1]] != 1:
                                    self.draw_fig(v[0].center, turn)
                                    turn = not turn
                                    self.game[v[1]] = 0
                                    count += 1
                    else:
                        if restart_btn.collidepoint(pos):
                            self.screen.fill((0, 0, 0))
                            self.pvIA()
                        elif return_btn.collidepoint(pos):
                            running = False
                        pos = pygame.mouse.get_pos()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            if self.check_win() and not win:
                win = True
                text = "YOU WIN"
                width, height = self.font.size(text)
                self.draw_text(text, self.font, self.text_color, self.screen,
                               self.screen_width / 2 - width / 2, self.screen_height / 2 - 200, True)
                restart_btn, return_btn= self.end_btns()
            #Checks for a tie
            if count == len(self.game) and not win:
                win = True
                text = "TIE"
                width, height = self.font.size(text)
                self.draw_text(text, self.font, self.text_color, self.screen,
                               self.screen_width / 2 - width / 2, self.screen_height / 2 - 200, True)
                restart_btn, return_btn = self.end_btns()

            # IA moves
            if turn == False and not win:
                while True:
                    movementIA = random.randrange(9)
                    if self.game[movementIA] != 0 and self.game[movementIA] != 1:
                        print (movementIA)
                        print(self.game[movementIA])
                        self.game[movementIA] = 1
                        for k, v in self.positions.items():
                            if v[1] == movementIA:
                                self.draw_fig(v[0].center, turn)
                        count += 1
                        turn = not turn
                        break
                if self.check_win() and not win:
                    win = True
                    text = "COMPUTER WINS"
                    width, height = self.font.size(text)
                    self.draw_text(text, self.font, self.lines_color, self.screen,
                                   self.screen_width / 2 - width / 2, self.screen_height / 2 - 200, True)
                    restart_btn, return_btn = self.end_btns()
            # Add a hover
            if win:
                pos = pygame.mouse.get_pos()
                if restart_btn.collidepoint(pos):
                    self.end_btns(res_hover=True)
                elif return_btn.collidepoint(pos):
                    self.end_btns(rtrn_hover=True)
                else:
                    self.end_btns()
            pygame.display.update()

    def check_win(self):  # This function checks if somebody wins, it doesn't recognices what player did win
        if self.game[0] == self.game[1] and self.game[0] == self.game[2] or self.game[3] == self.game[4] and self.game[3] == self.game[5] or self.game[6] == self.game[7] and self.game[6] == self.game[8]:
            return True
        elif self.game[0] == self.game[4] and self.game[0] == self.game[8] or self.game[2] == self.game[4] and self.game[2] == self.game[6] or self.game[6] == self.game[7] and self.game[6] == self.game[8]:
            return True
        elif self.game[0] == self.game[3] and self.game[0] == self.game[6] or self.game[1] == self.game[4] and self.game[1] == self.game[7] or self.game[2] == self.game[5] and self.game[2] == self.game[8]:
            return True

    def draw_line(self):
        for x in range(self.screen_width):
        # Horizontal lines
            pygame.draw.line(self.screen, self.lines_color, (0, self.screen_height/3), (x, self.screen_height/3), 2)
            pygame.draw.line(self.screen, self.lines_color, (0, self.screen_height / 3 * 2), (x, self.screen_height/3 * 2), 2)
            # Vertical lines
            pygame.draw.line(self.screen, self.lines_color, (self.screen_width / 3, 0), (self.screen_width / 3, x), 2)
            pygame.draw.line(self.screen, self.lines_color, (self.screen_width / 3 * 2, 0), (self.screen_width / 3 * 2, x), 2)
            pygame.display.flip()

    def draw_fig(self, pos, turn):
        if turn:
            xpos = pos[0] - 40
            ypos = pos[1] - 40
            for x in range(80):
                pygame.time.Clock().tick(450)    
                pygame.draw.line(self.screen, self.lines_color, (xpos, ypos), (xpos + x, ypos+x), 5)
                pygame.draw.line(self.screen, self.lines_color, (xpos+80, ypos), ((xpos+80)-x, ypos+x), 5)
                pygame.display.flip()
        else:
            for x in range(360):
                pygame.time.Clock().tick(600)
                pygame.gfxdraw.arc(self.screen, pos[0], pos[1], 50, 0, x, (255, 255, 255))
                pygame.gfxdraw.arc(self.screen, pos[0], pos[1], 51, 0, x, (255, 255, 255))
                pygame.gfxdraw.arc(self.screen, pos[0], pos[1], 52, 0, x, (255, 255, 255))
                pygame.display.flip()

    def draw_text(self, text, font, color, surface, x, y, background = False):
        if background:
            textobj = font.render(text, True, color, self.lines_color)
        else:
            textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    def end_btns(self, res_hover = None, rtrn_hover = None):
        # Set a different font
        font = pygame.font.SysFont("Century Gothic", 40)
        # Creates restart button
        res_rect = pygame.Rect(self.screen_width / 8,self.screen_height / 2.3, 250, 125)
        res_fig = None
        if res_hover == True:
            res_fig = pygame.draw.rect(self.screen, (150,150,150), res_rect)
        else:
            res_fig = pygame.draw.rect(self.screen, self.lines_color, res_rect)
        res_text = "Restart"
        res_width, res_height = self.font.size(res_text)
        self.draw_text(res_text, self.font, self.text_color, self.screen, res_rect.centerx - res_width / 2, res_rect.centery - res_height / 2)
        # Creates return button
        rtrn_rect = pygame.Rect((self.screen_width / 8)*5, self.screen_height / 2.3, 250, 125)
        if rtrn_hover:
            rtrn_fig = pygame.draw.rect(self.screen, (150,150,150), rtrn_rect)
        else:
            rtrn_fig = pygame.draw.rect(self.screen, self.lines_color, rtrn_rect)
        rtrn_text = "Return"
        rtrn_width, rtrn_height = self.font.size(rtrn_text)
        self.draw_text(rtrn_text, self.font, self.text_color, self.screen,
                       rtrn_rect.centerx - rtrn_width / 2, rtrn_rect.centery - rtrn_height / 2)
        return res_rect, rtrn_rect
tateti = Game()
