"""
Ex26-01-game-step1.py

1단계: 기본 환경 + 움직이는 플레이어

pip install pygame
"""

import pygame
import sys

pygame.init()

# 게임 기본 설정
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
DARK_BLUE = (25, 25, 112)
GRAY = (50, 50, 50)


# ======================================================
# 플레이어 클래스 (저승사자)
# ======================================================
class GrimReaper:

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
        self.x = max(self.size, min(WINDOW_WIDTH - self.size, self.x))
        self.y = max(self.size, min(WINDOW_HEIGHT - self.size, self.y))

    def draw(self, screen):
        """ 저승사자 그리기 """

        # 본체 (파란색 원)
        pygame.draw.circle(screen, DARK_BLUE, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), self.size - 3)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size, 2)

        # 눈
        pygame.draw.circle(screen, GOLD, (int(self.x - 4), int(self.y - 2)), 2)
        pygame.draw.circle(screen, WHITE, (int(self.x + 4), int(self.y - 2)), 2)


# ======================================================
# 게임 메인 클래스
# ======================================================
class Game:
    def __init__(self):
        """ 게임 초기화 """
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("1단계: 움직이는 플레이어")
        self.clock = pygame.time.Clock()

        # 플레이어를 화면 중앙에 생성
        self.player = GrimReaper(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

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
                # ESC 키를 눌렀는지 확인
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self, dt):
        """ 게임 로직 업데이트
            캐릭터 이동, 충돌 검사, 점수 계산 등 모든 게임 계산
        """
        # 키를 계속 누르고 있는지 실시간으로 체크
        keys = pygame.key.get_pressed()

        # 플레이어 객체에게 시간 간격(dt)과 키 상태를 전달해서 업데이트
        # dt = 이전 프레임으로부터 경과된 시간 (초 단위)
        # keys = 현재 눌려있는 키들의 상태 (True/False 배열)
        self.player.update(dt, keys)

    def draw(self):
        """ 화면 그리기 """

        # 화면 전체 GRAY 색으로 채워서 이전 프레임의 잔상을 지움
        self.screen.fill(GRAY)

        # 플레이어 캐릭터 화면에 그리기
        self.player.draw(self.screen)

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
