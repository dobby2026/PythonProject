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












