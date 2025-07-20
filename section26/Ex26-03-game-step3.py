"""
Ex26-02-game-step2.py

3단계: 카메라 시스템

pip install pygame
"""

import pygame
import sys
import math
import random


pygame.init()

# 게임 기본 설정
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
# 큰 맵 크기
MAP_WIDTH = 4000
MAP_HEIGHT = 3000
FPS = 60

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
GOLD = (255, 215, 0)
DARK_BLUE = (25, 25, 112)
GRAY = (50, 50, 50)


# ======================================================
# 플레이어 클래스 (저승사자)
# ======================================================
class GrimReaper:
    """
    저승사자(플레이어) 클래스
    - 키보드 입력으로 움직임
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 15
        self.speed = 200

    def update(self, dt, keys):
        """ 플레이어 업데이트 (이동처리) """
        dx = dy = 0

        # 키 입력 처리
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed * dt

        # 대각선 이동 시 속도 조정
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        # 위치 업데이트
        self.x += dx
        self.y += dy

        # 화면 경계 제한
        self.x = max(self.size, min(MAP_WIDTH - self.size, self.x))
        self.y = max(self.size, min(MAP_HEIGHT - self.size, self.y))

    def draw(self, screen, camera):
        """ 저승사자 그리기 """

        # 월드 좌표를 화면 좌표로 변환
        screen_x, screen_y = camera.apply(self.x, self.y)

        # 본체 (파란색 원)
        pygame.draw.circle(screen, DARK_BLUE, (int(screen_x), int(screen_y)), self.size)
        pygame.draw.circle(screen, GOLD, (int(screen_x), int(screen_y)), self.size - 3)
        pygame.draw.circle(screen, BLACK, (int(screen_x), int(screen_y)), self.size, 2)

        # 눈
        pygame.draw.circle(screen, BLACK, (int(screen_x - 4), int(screen_y - 2)), 2)  # 왼쪽 눈
        pygame.draw.circle(screen, WHITE, (int(screen_x + 4), int(screen_y - 2)), 2)
        # 오른쪽 눈


# ======================================================
# 적 클래스 (악귀) - 플레이어를 추적하는 적
# ======================================================
class EvilSpirit:
    """
    악귀(적) 클래스
    - 플레이어를 자동으로 추적함
    """

    def __init__(self, x, y):
        """ 악귀 초기화 """

        self.x = x
        self.y = y
        self.size = 10
        self.speed = 60
        self.alive = True   # 생존상태

    def update(self, dt, player):
        """
        악귀 업데이트 - 플레이어 추적 AI
        """

        # 죽은 적은 움직이지 않음
        if not self.alive:
            return

        # 플레이어 방향 벡터 계산
        dx = player.x - self.x # 플레이어까지의 x 거리
        dy = player.y - self.y # 플레이어까지의 y 거리

        # 피타고라스 정리로 플레이어 까지의 직선 거리 계산
        distance = math.sqrt(dx * dx + dy * dy)

        # 거리가 0이 아닐 때만 이동
        if distance > 0:
            
            # 방향 백터를 단위 벡터로 정규화
            dx /= distance  # dx를 거리로 나누어 -1~1 사이 값으로 만듬
            dy /= distance  # dy를 거리로 나누어 -1~1 사이 값으로 만듬

            # 정규화된 방향 벡터에 속도와 시간을 곱해서 실제 이동
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt


    def draw(self, screen, camera):
        """ 악귀를 화면에 그리기 """

        # 죽은 적은 그리지 않음
        if not self.alive:
            return
        
        # 월드 좌표를 화면 좌표로 변환
        screen_x, screen_y = camera.apply(self.x, self.y)


        # 화면에 보이지 않으면 그리지 않음 (성능 최적화)
        if -20 <= screen_x <= WINDOW_WIDTH + 20 and -20 <= screen_y <= WINDOW_HEIGHT + 20:
            # 빨간색 원으로 적 본체 그리기
            pygame.draw.circle(screen, RED, (int(screen_x), int(screen_y)), self.size)
            pygame.draw.circle(screen, BLACK, (int(screen_x), int(screen_y)), self.size, 1)

            # 적의 눈 그리기
            pygame.draw.circle(screen, WHITE, (int(screen_x - 3), int(screen_y - 2)), 1)
            pygame.draw.circle(screen, WHITE, (int(screen_x + 3), int(screen_y - 2)), 1)

# ======================================================
# 카메라 클래스
# ======================================================
class Camera:
    def __init__(self):
        """ 카메라 초기화 """
        self.x = 0  # 현재 카메라 위치 x
        self.y = 0  # 현재 카메라 위치 y
        self.target_x = 0 # 목표 위치 x
        self.target_y = 0 # 목표 위치 y
        self.smoothing = 0.1    # 부드러운 이동 (0.1 = 부드럽게, 1.0 = 즉시)

    def update(self, target_x, target_y):
        """ 타겟(플레이어)을 따라 카메라 업데이트 """
        # 카메라가 타겟을 화면 중앙에 유지하도록 계산
        self.target_x = target_x - WINDOW_WIDTH // 2
        self.target_y = target_y - WINDOW_HEIGHT // 2

        # 맵 경계 제한 (카메라가 맵 밖으로 나가지 않게)
        self.target_x = max(0, min(MAP_WIDTH - WINDOW_WIDTH, self.target_x))
        self.target_y = max(0, min(MAP_HEIGHT - WINDOW_HEIGHT, self.target_y))

        # 부드러운 카메라 이동 (선형 보간)
        self.x += (self.target_x - self.x) * self.smoothing
        self.y += (self.target_y - self.y) * self.smoothing

    def apply(self, x, y):
        """ 월드 좌표를 화면 좌표로 변환 """
        return (x - self.x, y - self.y)


# ======================================================
# 게임 메인 클래스
# ======================================================
class Game:
    def __init__(self):
        """ 게임 초기화 """
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("3단계: 카메라 시스템(큰 맵)")
        self.clock = pygame.time.Clock()

        # 플레이어를 화면 중앙에 생성
        self.player = GrimReaper(MAP_WIDTH // 2, MAP_HEIGHT // 2)

        # 카메라 초기화
        self.camera = Camera()

        # 적 관리 관련 변수들
        self.enemies = []   # 현재 화면에 있는 모든 적들을 저장하는 리스트
        self.spawn_timer = 0    # 적 생성 타이머 (초 단위)
        self.spawn_rate = 1.0   # 적 생성 빈도 (1.0 = 1초마다 1마리)
        self.game_over = False  # 게임 오버 상태 플래그

    def spawn_enemy(self):
        """
        적 생성 - 화면 가장 자리에서 랜덤하게 생성

        화면 바깥쪽 4방향 중 하나를 랜덤 선택해서 적을 생성
        """

        # 플레이어 주변 원형 범위에서 생성
        angle = random.uniform(0, 2 * math.pi)
        distance = 300 + random.uniform(0, 200)

        x = self.player.x + math.cos(angle) * distance
        y = self.player.y + math.sin(angle) * distance
        
        # 맵 경계 안에 위치하도록 조정
        x = max(50, min(MAP_WIDTH - 50), x)
        y = max(50, min(MAP_HEIGHT - 50), y)

        # 생성된 위치에서 새 적 추가
        self.enemies.append(EvilSpirit(x, y))


    def handle_events(self):
        """ 이벤트 처리
            사용자 입력(마우스, 키보드, 창 닫기 등)을 감지하고 처리
        """
        # pygame.event.get()으로 발생한 모든 이벤트를 가져와서 하나씩 처리
        for event in pygame.event.get():
            # 창의 x(닫기) 버튼을 클릭했을 때 발생하는 이벤트
            if event.type == pygame.QUIT:
                return False  # 게임 종료 신호를 보냄
            # 키보드의 키를 눌렀을 때 발생하는 이벤트 (키를 누르는 순감만)
            elif event.type == pygame.KEYDOWN:
                if self.game_over: # 게임오버 상태일 때
                    if event.key == pygame.K_SPACE: # 스페이스바로 재시작
                        self.__init__() # 게임 객체를 다시 초기화 (재시작)
                    # ESC 키를 눌렀는지 확인
                    if event.key == pygame.K_ESCAPE:
                        return False
                else: # 게임 실행 중일 때
                    if event.key == pygame.K_ESCAPE:    # ESC로 종료
                        return False
        return True


    def update(self, dt):
        """ 게임 로직 업데이트
            캐릭터 이동, 충돌 검사, 점수 계산 등 모든 게임 계산
        """
        # 게임 오버시에는 업데이트 중단
        if self.game_over:
            return

        # 키를 계속 누르고 있는지 실시간으로 체크
        keys = pygame.key.get_pressed()

        # 플레이어 객체에게 시간 간격(dt)과 키 상태를 전달해서 업데이트
        # dt = 이전 프레임으로부터 경과된 시간 (초 단위)
        # keys = 현재 눌려있는 키들의 상태 (True/False 배열)
        self.player.update(dt, keys)

        # 카메라 업데이트 (플레이어 따라가기)
        self.camera.update(self.player.x, self.player.y)

        # 적 생성 타이머 업데이트
        self.spawn_timer += dt
        
        # 설정된 생성 주기가 되면 새 적 생성
        if self.spawn_timer >= 1.0 / self.spawn_rate:
            self.spawn_enemy() # 새 적 생성
            self.spawn_timer = 0 # 타이머 리셋

        # 모든 적들 업데이트 및 충돌 감지
        for enemy in self.enemies:
            # 각 적의 AI 업데이트 (플레이어 추적)
            enemy.update(dt, self.player)

            # 충돌 검사 - 플레이어와 적사이 거리 계산
            # 두 원(플레이어, 적)의 중심점 사이 거리를 구함

            distance_to_player = math.sqrt((enemy.x - self.player.x) ** 2 + (enemy.y - self.player.y) ** 2)
            # 너무 멀리 떨어진 적 제거 (성는 최적화)
            if distance_to_player > 800:
                self.enemies.remove(enemy)

            # 거리가 두 원의 반지름 합보다 작으면 충돌
            if distance_to_player < self.player.size + enemy.size:
                self.game_over = True

    def draw(self):
        """ 화면 그리기 """

        # 화면 전체 GRAY 색으로 채워서 이전 프레임의 잔상을 지움
        self.screen.fill(GRAY)

        # 격자 그리기(맵 크기 확인용)


        # 게임이 진행 중일 때만 게임 객체들 그릭
        if not self.game_over:
            # 모든 적들 그리기
            for enemy in self.enemies:
                enemy.draw(self.screen)

        # 플레이어 캐릭터 화면에 그리기
        self.player.draw(self.screen)

        # 게임 오버 화면 표시
        if self.game_over:
            # 큰 폰트로 "GAME OVER" 텍스트 생성
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("GAME OVER", True, RED) # 빨간색 텍스트

            # 작은 폰트로 재시작 안내 텍스트 생성
            restart_text = (pygame.font.Font(None, 36)
                            .render("Press SPACE to restart", True, WHITE))

            # 텍스트를 화면 중앙에 배치하기 위한 위치 계산
            go_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            re_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))

            # 텍스트를 화면에 그리기
            self.screen.blit(game_over_text, go_rect)
            self.screen.blit(restart_text, re_rect)

        # 지금까지 그린 것들 실제 화면에 표시
        pygame.display.flip()

    def run(self):
        """ 메인 게임 루프
            게임이 실행되는 동안 계속 반복되는 핵심 루프
        """
        running = True  # 게임 실생 상태를 나타내는 플래그 변수

        # 게임의 메인 루프 - 게임 종료될때 까지 무한반복
        while running:
            #  FPS(초당 프레임 수)를 60으로 제한하고, 이전 프레임으로부터 경과된 시간을 계산
            dt = self.clock.tick(FPS) / 1000.0  # 밀리초를 초로 변환
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


# 실행 코드
if __name__ == '__main__':
    game = Game()
    game.run()
