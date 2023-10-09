import pygame
import sys
from random import choice, randint
pygame.font.init()
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()
pygame.display.set_caption('PingPong-2p')
game_active = False
f3 = False
txt_msg_flag = ()
txt_gravity = 0
border_surf = pygame.Surface((35, HEIGHT - 76))
border_surf.fill('red')
border_surf.set_alpha(25)
border_center = ((0, 76), (WIDTH - border_surf.get_width(), 76))
border_rect = border_surf.get_rect()


score_font = pygame.font.SysFont('Garamond', WIDTH // 4)
win_font = pygame.font.SysFont('Garamond', int(WIDTH // 35))
rules_font = pygame.font.SysFont('Garamond', int(WIDTH // 37.5))
fps_font = pygame.font.SysFont('Garamond', WIDTH // 48)
dot_multi = [0, 1, 2, 3]
dot_index = 0

def scoreRenderAndFPS():
    player1_score_surf = score_font.render(f'{player1.score}', False, (255, 255, 255))
    player1_score_surf.set_alpha(25)
    screen.blit(player1_score_surf, (WIDTH / 4 - player1_score_surf.get_width() / 2, (HEIGHT + 75) / 2 - player1_score_surf.get_height() / 2))

    player2_score_surf = score_font.render(f'{player2.score}', False, (255, 255, 255))
    player2_score_surf.set_alpha(25)
    screen.blit(player2_score_surf, (WIDTH - WIDTH / 4 - player2_score_surf.get_width() / 2, (HEIGHT + 75) / 2 - player2_score_surf.get_height() / 2))

    player1_wins_surf = win_font.render(f'PLAYER 1 WINS: {player1.wins}', False, (255, 255, 255))
    player1_wins_rect = player1_wins_surf.get_rect(center=(WIDTH / 4, 75 / 2))
    screen.blit(player1_wins_surf, player1_wins_rect)
    player2_wins_surf = win_font.render(f'PLAYER 2 WINS: {player2.wins}', False, (255, 255, 255))
    player2_wins_rect = player2_wins_surf.get_rect(center=(WIDTH - WIDTH / 4, 75 / 2))
    screen.blit(player2_wins_surf, player2_wins_rect)









class Panel:
    def __init__(self, center):
        self.up_flag = True
        self.down_flag = True
        self.speed = HEIGHT / 60
        self.surf = pygame.surface.Surface((2 * WIDTH / 100, 15 * HEIGHT/100))
        self.surf.fill(0x5e77a9)
        self.rect = self.surf.get_rect(center=center)
        self.score = 0
        self.wins = 0



player1 = Panel((75, HEIGHT/2))
player2 = Panel((WIDTH - 75, HEIGHT/2))

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH / 40, WIDTH / 40, WIDTH / 40, WIDTH / 40)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.start_dir = choice([-1, 1])
        self.speedx = WIDTH / 150 * self.start_dir
        self.speedy = HEIGHT / 150 * self.start_dir
        self.move = False
        self.live_time = 0
        self.set_timer = True

    def ball_logic(self):
        global txt_msg_flag
        if self.move:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.left <= 15:
                player2.score += 1
                pygame.mixer.Sound.play(plus_score)
                txt_msg_flag = (win_font.render('PLAYER2 +1', False, (125, 255, 125)), [randint(WIDTH - WIDTH // 2 + WIDTH // 8, WIDTH - WIDTH // 8), randint(WIDTH // 8, HEIGHT)])
                self.rect.center = (WIDTH / 2, HEIGHT / 2)
                self.speedx *= -1
                self.live_time = pygame.time.get_ticks()
                self.set_timer = True

            if self.rect.right >= WIDTH - 15:
                player1.score += 1
                pygame.mixer.Sound.play(plus_score)
                txt_msg_flag = (win_font.render('PLAYER1 +1', False, (125, 255, 125)), [randint(150, WIDTH // 2 - WIDTH // 8), randint(WIDTH // 8, HEIGHT)])
                self.rect.center = (WIDTH / 2, HEIGHT / 2)
                self.speedx *= -1
                self.live_time = pygame.time.get_ticks()
                self.set_timer = True

            if self.rect.colliderect(player1) and self.speedx < 0:
                if abs(self.rect.left - player1.rect.right) <= player1.surf.get_width():
                    pygame.mixer.Sound.play(ballhit_sound)
                    self.speedx *= -1
                    self.speedx += 1
                    if player1.down_flag:
                        self.rect.y += abs(self.speedy) * 5
                        self.speedy += 0.3
                    if player1.up_flag:
                        self.rect.y -= abs(self.speedy) * 5
                        self.speedy += 0.3

                elif abs(self.rect.bottom - player1.rect.top) < 10 and self.speedy > 0:
                    self.speedy *= -1
                elif abs(self.rect.top - player1.rect.bottom) < 10 and self.speedy < 0:
                    self.speedy *= -1

            if self.rect.colliderect(player2) and self.speedx > 0:
                pygame.mixer.Sound.play(ballhit_sound)
                if abs(self.rect.right - player2.rect.left) < player2.surf.get_width():
                    self.speedx *= -1
                    self.speedx += -1
                    if player2.down_flag:
                        self.rect.y += abs(self.speedy) * 5
                        self.speedy += 0.3
                    if player2.up_flag:
                        self.rect.y -= abs(self.speedy) * 5
                        self.speedy += 0.3
                elif abs(self.rect.bottom - player2.rect.top) < 10 and self.speedy > 0:
                    self.speedy *= -1
                    self.speedy += -0.5
                elif abs(self.rect.top - player2.rect.bottom) < 10 and self.speedy < 0:
                    self.speedy *= -1
                    self.speedy += 0.5

            if self.rect.top <= 75:
                pygame.mixer.Sound.play(ballwallhit)
                self.speedy *= -1
                self.rect.top = 75 + self.speedy + 5
            if self.rect.bottom >= HEIGHT:
                pygame.mixer.Sound.play(ballwallhit)
                self.speedy *= -1
                self.rect.bottom = HEIGHT - self.speedy - 5

        self.timer()

    def timer(self):
        if self.set_timer:
            if (pygame.time.get_ticks() - self.live_time) / 1000 > 1.5:
                self.move = True
                self.set_timer = False
                self.speedx = self.speedx / 1.5 * -1
                self.speedy = self.speedy / 1.5 * -1

                if abs(self.speedx) < WIDTH / 150:
                    self.speedx = WIDTH / 150 * (self.speedx / abs(self.speedx)) * -1
                if abs(self.speedy) < HEIGHT / 150:
                    self.speedy = HEIGHT / 150 * (self.speedy / abs(self.speedy)) * -1
            else:
                self.move = False





ball = Ball()
bg_music = pygame.mixer.music.load('Recources/PingPongBg_music.ogg')
ballhit_sound = pygame.mixer.Sound('Recources/BallHitSound.ogg')
ballwallhit = pygame.mixer.Sound('Recources/WallHitSound.ogg')
plus_score = pygame.mixer.Sound('Recources/plusScore.ogg')
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for eve in pygame.event.get():
        if eve.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if eve.type == pygame.KEYUP:
            if eve.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if not game_active:
                game_active = True
                ball.live_time = pygame.time.get_ticks()
            if eve.key == pygame.K_F3:
                if f3 == False:
                    f3 = True
                else: f3 = False

    if game_active:
        keys = pygame.key.get_pressed()

        #  Player 1 controls :
        if keys[pygame.K_w] and player1.up_flag:
            player1.rect.y -= player1.speed
            player1.down_flag = False
        else: player1.down_flag = True

        if keys[pygame.K_s] and player1.down_flag:
            player1.rect.y += player1.speed
            player1.up_flag = False
        else: player1.up_flag = True

        if player1.rect.bottom >= HEIGHT:
            player1.rect.bottom = HEIGHT
        if player1.rect.top <= 75:
            player1.rect.top = 75

        #  Player 2 controls :
        if keys[pygame.K_UP] and player2.up_flag:
            player2.rect.y -= player2.speed
            player2.down_flag = False
        else:
            player2.down_flag = True

        if keys[pygame.K_DOWN] and player2.down_flag:
            player2.rect.y += player2.speed
            player2.up_flag = False
        else: player2.up_flag = True

        if player2.rect.bottom >= HEIGHT:
            player2.rect.bottom = HEIGHT
        if player2.rect.top <= 75:
            player2.rect.top = 75

        #  Winning logic :
        if player1.score == 5:
            player1.wins += 1
            txt_msg_flag = (win_font.render('PLAYER1 +1', False, (125, 255, 125)), [randint(150, WIDTH // 2 - WIDTH // 8), randint(HEIGHT // 12.8, HEIGHT)])
            player1.score = 0
            player2.score = 0
            pygame.mixer.Sound.play(plus_score)

        elif player2.score == 5:
            player2.wins += 1
            txt_msg_flag = (win_font.render('PLAYER2 WINS +1', False, (125, 255, 125)), [randint(WIDTH - WIDTH // 2 + WIDTH // 8, WIDTH - WIDTH // 8), randint(HEIGHT // 12.8, HEIGHT)])
            player1.score = 0
            player2.score = 0
            pygame.mixer.Sound.play(plus_score)


        screen.fill(0x121212)

        #  Borders :
        pygame.draw.line(screen, 0x006400, (0, 75), (WIDTH, 75))
        pygame.draw.line(screen, 0x006400, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
        pygame.draw.line(screen, 0x006400, (0, 0), (0, 75))
        pygame.draw.line(screen, 0x006400, (WIDTH - 1, 0), (WIDTH - 1, 75))
        screen.blit(border_surf, border_center[0])
        screen.blit(border_surf, border_center[1])




        #  Texts :
        scoreRenderAndFPS()
        if len(txt_msg_flag) > 0:
            screen.blit(txt_msg_flag[0], txt_msg_flag[1])
            txt_msg_flag[1][1] -= txt_gravity
            txt_gravity += 0.5
            if txt_msg_flag[1][1] < 0:
                txt_gravity = 0
                txt_msg_flag = ()


        #  Playable :
        ball.ball_logic()

        screen.blit(player1.surf, player1.rect)
        screen.blit(player2.surf, player2.rect)
        pygame.draw.ellipse(screen, 0x8da3cd, ball.rect)
        if f3:
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (255, 0, 0), ball.rect, 1)
            pygame.draw.rect(screen, (255, 0, 0), player1.rect, 1)
            pygame.draw.rect(screen, (255, 0, 0), player2.rect, 1)
            screen.blit(win_font.render(str((pygame.time.get_ticks() - ball.live_time) / 1000), False, (0, 125, 0)), (WIDTH / 2, HEIGHT / 2))
        fps = fps_font.render(f'FPS: {clock.get_fps():.0f}', False, (0, 255, 0))
        fps.set_alpha(50)
        screen.blit(fps, (1, 0))

    else:
        screen.fill(0x121212)
        dot_index += 0.1
        if dot_index > 4:
            dot_index = 0
        rules_surf1 = rules_font.render("A game by Itay Shinderman.", False, 0xFFD700)
        rules_surf2 = rules_font.render("Use 'ws' to move player1 and the arrow keys for player2 (F3 for more details).", False, 0xFFD700)
        rules_surf3 = rules_font.render("PRESS ANY BUTTON (except Esc)" + "." * dot_multi[int(dot_index)], False, 0xFFD700)
        screen.blit(rules_surf1, (25, 25))
        screen.blit(rules_surf2, (25, 90))
        screen.blit(rules_surf3, (25, 160))

    pygame.display.update()


'''
18/02/23
By: Itay Shinderman
Music: pixabay
Help tools: Community version IDE PyCharm
Version: 1.0.0
For: Mentoring
'''

