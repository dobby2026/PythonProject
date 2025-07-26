# ============================================================================
# 🎮 6단계: PNG 애니메이션 시스템
# ============================================================================

import pygame
import random
import math
import sys
import platform
import os
import glob  # 🆕 파일 패턴 검색용
import re  # 🆕 정규표현식용

# ============================================================================
# ✨ 6단계에서 새로 추가된 내용들
# - images 폴더 자동 생성 및 관리
# - PNG 프레임 파일 자동 검색 시스템
# - PNG 프레임 애니메이션 클래스
# - 이미지 관리자 클래스
# - 캐릭터별 개별 애니메이션 속도 설정
# - 배경 이미지 지원
# - 이미지 로드 실패 시 기본 그래픽 백업
# ============================================================================

pygame.init()

# 기본 설정 (5단계와 동일)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
MAP_WIDTH = 4000
MAP_HEIGHT = 3000
FPS = 60

# 색상 정의 (5단계와 동일)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
GOLD = (255, 215, 0)
DARK_BLUE = (25, 25, 112)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)

# 🆕 이미지 폴더 설정
IMAGES_FOLDER = "images"


# ============================================================================
# 🆕 images 폴더 관리
# ============================================================================
def ensure_images_folder():
    """🆕 images 폴더가 존재하지 않으면 자동으로 생성"""
    if not os.path.exists(IMAGES_FOLDER):
        os.makedirs(IMAGES_FOLDER)
        print(f"✓ {IMAGES_FOLDER} 폴더가 생성되었습니다.")
        print("📁 이 폴더에 다음 이미지들을 넣으면 애니메이션이 적용됩니다:")
        print("   - grim_reaper_frame_0001.png, grim_reaper_frame_0002.png, ...")
        print("   - evil_spirit_normal_1.png, evil_spirit_normal_2.png, ...")
        print("   - evil_spirit_strong.png")
        print("   - evil_spirit_boss.png")
        print("   - background.png")
    else:
        print(f"✓ {IMAGES_FOLDER} 폴더를 발견했습니다.")


# ============================================================================
# 한글 폰트 시스템 (5단계와 동일)
# ============================================================================
def get_korean_font(size):
    system = platform.system()

    if system == "Windows":
        font_candidates = [
            "C:/Windows/Fonts/malgun.ttf",
            "C:/Windows/Fonts/gulim.ttc",
            "C:/Windows/Fonts/batang.ttc",
        ]
    elif system == "Darwin":  # Mac
        font_candidates = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    else:  # Linux
        font_candidates = [
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]

    for font_path in font_candidates:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except pygame.error:
                continue

    korean_fonts = ["malgun", "gulim", "batang", "nanumgothic"]
    for font_name in korean_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            test_surface = font.render("한글", True, (255, 255, 255))
            if test_surface.get_width() > 0:
                return font
        except pygame.error:
            continue

    print("⚠️  한글 폰트를 찾을 수 없습니다. 기본 폰트 사용")
    return pygame.font.Font(None, size)


# ============================================================================
# 🆕 PNG 프레임 파일 검색 시스템
# ============================================================================
def find_frame_files(filename_base):
    """🆕 주어진 파일명 기준으로 images 폴더에서 모든 프레임 파일을 찾기"""
    frame_files = []

    # 🆕 다양한 파일명 패턴 지원
    patterns = [
        os.path.join(IMAGES_FOLDER, f"{filename_base}_frame_*.png"),  # filename_frame_001.png
        os.path.join(IMAGES_FOLDER, f"{filename_base}_*.png"),  # filename_1.png
        os.path.join(IMAGES_FOLDER, f"{filename_base}*.png"),  # filename1.png
    ]

    all_candidates = []

    # 🆕 각 패턴별로 파일 검색
    for pattern_idx, pattern in enumerate(patterns):
        files = glob.glob(pattern)

        for file in files:
            basename = os.path.basename(file)

            # 🆕 패턴별로 프레임 번호 추출
            if pattern_idx == 0:  # _frame_ 패턴
                match = re.search(rf"{re.escape(filename_base)}_frame_(\d+)\.png$", basename)
            elif pattern_idx == 1:  # _ 패턴
                if "_frame_" not in basename:
                    match = re.search(rf"{re.escape(filename_base)}_(\d+)\.png$", basename)
                else:
                    continue
            else:  # 직접 패턴
                if "_frame_" not in basename and f"{filename_base}_" not in basename:
                    match = re.search(rf"{re.escape(filename_base)}(\d+)\.png$", basename)
                else:
                    continue

            if match:
                frame_num = int(match.group(1))
                all_candidates.append((frame_num, file, pattern_idx))

    # 🆕 프레임 번호순으로 정렬
    all_candidates.sort(key=lambda x: x[0])

    if all_candidates:
        # 🆕 가장 많은 파일을 가진 패턴 선택
        pattern_counts = {}
        for _, _, pattern_idx in all_candidates:
            pattern_counts[pattern_idx] = pattern_counts.get(pattern_idx, 0) + 1

        best_pattern = max(pattern_counts.keys(), key=lambda p: pattern_counts[p])
        selected_files = [(num, file) for num, file, pattern_idx in all_candidates if pattern_idx == best_pattern]
        frame_files = [file for _, file in selected_files]

        if frame_files:
            print(f"✓ {filename_base}: {len(frame_files)}개 프레임 파일 발견")

    return frame_files


# ============================================================================
# 🆕 PNG 프레임 애니메이션 클래스
# ============================================================================
class PngFrameAnimation:
    """🆕 PNG 파일들로 프레임 애니메이션을 만드는 클래스"""

    def __init__(self, frame_files, frame_duration=700, width=None, height=None):
        """
        🆕 PNG 프레임 애니메이션 초기화

        Args:
            frame_files: PNG 파일 경로들의 리스트
            frame_duration: 각 프레임의 지속시간 (밀리초)
            width, height: 목표 이미지 크기
        """
        self.frames = []  # pygame Surface 객체들
        self.frame_durations = []  # 각 프레임의 지속시간
        self.current_frame = 0  # 현재 프레임 인덱스
        self.frame_timer = 0  # 프레임 타이머
        self.total_frames = 0  # 총 프레임 수

        if isinstance(frame_duration, (list, tuple)):
            self.default_duration = frame_duration
        else:
            self.default_duration = frame_duration

        self.load_png_frames(frame_files, width, height)

    def load_png_frames(self, frame_files, width, height):
        """🆕 PNG 파일들을 로드하여 pygame Surface로 변환"""
        for i, file_path in enumerate(frame_files):
            if os.path.exists(file_path):
                try:
                    # pygame으로 PNG 로드
                    pygame_surface = pygame.image.load(file_path).convert_alpha()
                    if width and height:
                        pygame_surface = pygame.transform.scale(pygame_surface, (width, height))

                    self.frames.append(pygame_surface)

                    # 🆕 프레임별 지속시간 설정
                    if isinstance(self.default_duration, (list, tuple)):
                        if i < len(self.default_duration):
                            duration = self.default_duration[i]
                        else:
                            duration = self.default_duration[-1]
                    else:
                        duration = self.default_duration

                    self.frame_durations.append(duration)

                except Exception as e:
                    print(f"✗ {file_path} 프레임 로드 실패: {e}")

        self.total_frames = len(self.frames)
        if self.total_frames > 0:
            print(f"✓ PNG 애니메이션 생성 완료: {self.total_frames}개 프레임")

    def update(self, dt):
        """🆕 애니메이션 프레임 업데이트"""
        if self.total_frames > 1:
            self.frame_timer += dt * 1000  # 초를 밀리초로 변환

            current_duration = self.frame_durations[self.current_frame] if self.frame_durations else 700

            if self.frame_timer >= current_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % self.total_frames

    def get_current_frame(self):
        """🆕 현재 표시해야 할 프레임 반환"""
        if self.frames:
            return self.frames[self.current_frame]
        return None

    def has_frames(self):
        """🆕 프레임이 있는지 확인"""
        return len(self.frames) > 0


# ============================================================================
# 🆕 이미지 관리자 클래스
# ============================================================================
class ImageManager:
    """🆕 게임의 모든 이미지와 애니메이션을 관리하는 클래스"""

    def __init__(self):
        self.images = {}  # 정적 이미지들 (현재 프레임)
        self.png_animations = {}  # PNG 프레임 애니메이션들
        self.animation_configs = {}  # 애니메이션별 설정
        self.load_images()

    def setup_animation_configs(self):
        """🆕 각 캐릭터별 애니메이션 설정 정의"""
        self.animation_configs = {
            'grim_reaper': {
                'frame_duration': 500,  # 저승사자: 500ms 간격 (안정적)
                'description': '저승사자 (500ms 간격)'
            },
            'evil_spirit_normal': {
                'frame_duration': 300,  # 일반 악귀: 300ms 간격 (빠름)
                'description': '일반 악귀 (300ms 간격)'
            },
            'evil_spirit_strong': {
                'frame_duration': 400,  # 강한 악귀: 400ms 간격 (보통)
                'description': '강한 악귀 (400ms 간격)'
            },
            'evil_spirit_boss': {
                'frame_duration': [800, 400, 600],  # 보스: 가변 간격 (특별한 패턴)
                'description': '보스 악귀 (가변 간격)'
            },
            'background': {
                'frame_duration': 2000,  # 배경: 2초 간격 (매우 느림)
                'description': '배경 (2000ms 간격)'
            },
        }

    def load_images(self):
        """🆕 모든 게임 이미지 로드"""
        self.setup_animation_configs()

        # 🆕 로드할 이미지들 정의
        image_files = {
            'grim_reaper': 'grim_reaper',
            'evil_spirit_normal': 'evil_spirit_normal',
            'evil_spirit_strong': 'evil_spirit_strong',
            'evil_spirit_boss': 'evil_spirit_boss',
            'background': 'background',
        }

        # 🆕 각 이미지의 목표 크기 설정
        size_map = {
            'grim_reaper': (30, 30),
            'evil_spirit_normal': (20, 20),
            'evil_spirit_strong': (25, 25),
            'evil_spirit_boss': (40, 40),
            'background': (MAP_WIDTH, MAP_HEIGHT),  # 배경은 맵 전체 크기
        }

        # 🆕 각 이미지에 대해 로드 시도
        for key, filename_base in image_files.items():
            loaded = False
            width, height = size_map.get(key, (60, 60))

            # 애니메이션 설정 가져오기
            config = self.animation_configs.get(key, {'frame_duration': 700})
            frame_duration = config['frame_duration']

            # 🆕 1단계: PNG 프레임 파일들 검색
            frame_files = find_frame_files(filename_base)

            if len(frame_files) >= 1:
                try:
                    png_animation = PngFrameAnimation(frame_files, frame_duration=frame_duration,
                                                      width=width, height=height)
                    if png_animation.has_frames():
                        self.png_animations[key] = png_animation
                        self.images[key] = png_animation.get_current_frame()
                        loaded = True
                        print(f"  ✓ {config.get('description', '기본 애니메이션')}")
                except Exception as e:
                    print(f"✗ {filename_base} PNG 애니메이션 생성 오류: {e}")

            # 🆕 2단계: 단일 PNG 파일 시도
            if not loaded:
                png_filename = os.path.join(IMAGES_FOLDER, f"{filename_base}.png")
                if os.path.exists(png_filename):
                    try:
                        surface = pygame.image.load(png_filename).convert_alpha()
                        surface = pygame.transform.scale(surface, (width, height))
                        self.images[key] = surface
                        print(f"✓ {png_filename} 정적 PNG 로드 성공")
                        loaded = True
                    except Exception as e:
                        print(f"✗ {png_filename} PNG 로드 실패: {e}")

            # 🆕 3단계: 로드 실패 시 None (기본 그래픽 사용)
            if not loaded:
                self.images[key] = None
                print(f"✗ {key} 이미지를 찾을 수 없습니다 - 기본 그래픽 사용")

    def update_animations(self, dt):
        """🆕 모든 애니메이션 업데이트"""
        for key, animation in self.png_animations.items():
            animation.update(dt)
            # 현재 프레임으로 정적 이미지 업데이트
            self.images[key] = animation.get_current_frame()

    def get_image(self, key):
        """🆕 지정된 키의 이미지 반환"""
        return self.images.get(key)

    def scale_image(self, key, size):
        """🆕 이미지를 지정된 크기로 스케일링"""
        image = self.get_image(key)
        if image:
            return pygame.transform.scale(image, (size, size))
        return None


# ============================================================================
# 카메라 클래스 (5단계와 동일)
# ============================================================================
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.smoothing = 0.1

    def update(self, target_x, target_y):
        self.target_x = target_x - WINDOW_WIDTH // 2
        self.target_y = target_y - WINDOW_HEIGHT // 2
        self.target_x = max(0, min(MAP_WIDTH - WINDOW_WIDTH, self.target_x))
        self.target_y = max(0, min(MAP_HEIGHT - WINDOW_HEIGHT, self.target_y))
        self.x += (self.target_x - self.x) * self.smoothing
        self.y += (self.target_y - self.y) * self.smoothing

    def apply(self, x, y):
        return (x - self.x, y - self.y)


# ============================================================================
# 플레이어 클래스 (이미지 시스템 추가)
# ============================================================================
class GrimReaper:
    def __init__(self, x, y, image_manager):
        # 기존 속성들
        self.x = x
        self.y = y
        self.size = 30
        self.speed = 200
        self.hp = 100
        self.max_hp = 100
        self.attack_damage = 25
        self.attack_range = 80
        self.attack_cooldown = 0
        self.attack_speed = 30
        self.attacking = False
        self.attack_animation_timer = 0

        # 🆕 이미지 관리
        self.image_manager = image_manager
        self.image = self.image_manager.scale_image('grim_reaper', self.size * 2)

    def update(self, dt, keys):
        # 기존 업데이트 로직 (5단계와 동일)
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed * dt

        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.x += dx
        self.y += dy
        self.x = max(self.size, min(MAP_WIDTH - self.size, self.x))
        self.y = max(self.size, min(MAP_HEIGHT - self.size, self.y))

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.attack_animation_timer > 0:
            self.attack_animation_timer -= dt
            if self.attack_animation_timer <= 0:
                self.attacking = False

        # 🆕 이미지 업데이트 (애니메이션 반영)
        self.image = self.image_manager.scale_image('grim_reaper', self.size * 2)

    def attack(self, enemies):
        if self.attack_cooldown <= 0:
            closest_enemy = None
            closest_distance = float('inf')

            for enemy in enemies:
                distance = math.sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
                if distance <= self.attack_range and distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = enemy

            if closest_enemy:
                closest_enemy.take_damage(self.attack_damage)
                self.attack_cooldown = self.attack_speed
                self.attacking = True
                self.attack_animation_timer = 0.3
                return True
        return False

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            return True
        return False

    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply(self.x, self.y)

        # 공격 범위 표시 (기존과 동일)
        if not self.attacking:
            attack_surface = pygame.Surface((self.attack_range * 2, self.attack_range * 2))
            attack_surface.set_alpha(20)
            pygame.draw.circle(attack_surface, GOLD, (self.attack_range, self.attack_range), self.attack_range)
            screen.blit(attack_surface, (screen_x - self.attack_range, screen_y - self.attack_range))

        if self.attacking:
            attack_surface = pygame.Surface((self.attack_range * 2, self.attack_range * 2))
            attack_surface.set_alpha(100)
            pygame.draw.circle(attack_surface, GOLD, (self.attack_range, self.attack_range), self.attack_range)
            screen.blit(attack_surface, (screen_x - self.attack_range, screen_y - self.attack_range))

        # 🆕 플레이어 그리기 (이미지 or 기본 그래픽)
        if self.image:
            # 이미지가 있는 경우
            image_rect = self.image.get_rect()
            image_rect.center = (int(screen_x), int(screen_y))
            screen.blit(self.image, image_rect)
        else:
            # 이미지가 없는 경우 기본 그래픽
            pygame.draw.circle(screen, DARK_BLUE, (int(screen_x), int(screen_y)), self.size)
            pygame.draw.circle(screen, GOLD, (int(screen_x), int(screen_y)), self.size - 3)
            pygame.draw.circle(screen, BLACK, (int(screen_x), int(screen_y)), self.size, 2)
            pygame.draw.circle(screen, GOLD, (int(screen_x - 4), int(screen_y - 2)), 2)
            pygame.draw.circle(screen, RED, (int(screen_x + 4), int(screen_y - 2)), 2)


# ============================================================================
# 적 클래스 (이미지 시스템 추가)
# ============================================================================
class EvilSpirit:
    def __init__(self, x, y, spirit_type="normal", image_manager=None):
        # 기존 속성들
        self.x = x
        self.y = y
        self.spirit_type = spirit_type
        self.alive = True
        self.image_manager = image_manager

        # 타입별 스탯 설정
        if spirit_type == "boss":
            self.size = 20
            self.speed = 30
            self.hp = 150
            self.max_hp = 150
            self.damage = 25
            self.image_key = 'evil_spirit_boss'
        elif spirit_type == "strong":
            self.size = 12
            self.speed = 45
            self.hp = 60
            self.max_hp = 60
            self.damage = 15
            self.image_key = 'evil_spirit_strong'
        else:  # normal
            self.size = 10
            self.speed = 60
            self.hp = 30
            self.max_hp = 30
            self.damage = 10
            self.image_key = 'evil_spirit_normal'

        # 🆕 이미지 로드
        self.image = self.image_manager.scale_image(self.image_key, self.size * 2) if self.image_manager else None

    def update(self, dt, player):
        if not self.alive:
            return

        # 기존 추적 AI
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt

        # 🆕 이미지 업데이트 (애니메이션 반영)
        if self.image_manager:
            self.image = self.image_manager.scale_image(self.image_key, self.size * 2)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def draw(self, screen, camera):
        if not self.alive:
            return

        screen_x, screen_y = camera.apply(self.x, self.y)

        if -30 <= screen_x <= WINDOW_WIDTH + 30 and -30 <= screen_y <= WINDOW_HEIGHT + 30:
            # 🆕 적 그리기 (이미지 or 기본 그래픽)
            if self.image:
                # 이미지가 있는 경우
                image_rect = self.image.get_rect()
                image_rect.center = (int(screen_x), int(screen_y))
                screen.blit(self.image, image_rect)
            else:
                # 이미지가 없는 경우 기본 그래픽
                colors = {"normal": RED, "strong": (255, 165, 0), "boss": (128, 0, 128)}
                color = colors.get(self.spirit_type, RED)
                pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), self.size)
                pygame.draw.circle(screen, BLACK, (int(screen_x), int(screen_y)), self.size, 1)
                pygame.draw.circle(screen, WHITE, (int(screen_x - 3), int(screen_y - 2)), 1)
                pygame.draw.circle(screen, WHITE, (int(screen_x + 3), int(screen_y - 2)), 1)

            # HP 바 (기존과 동일)
            bar_width = self.size * 2
            bar_height = 3
            bar_x = screen_x - bar_width // 2
            bar_y = screen_y - self.size - 8

            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            current_hp_width = (self.hp / self.max_hp) * bar_width
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_hp_width, bar_height))
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)


# ============================================================================
# 게임 메인 클래스 (이미지 시스템 통합)
# ============================================================================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("6단계: PNG 애니메이션 시스템")
        self.clock = pygame.time.Clock()

        # 한글 폰트 설정 (5단계와 동일)
        try:
            self.font = get_korean_font(24)
            self.big_font = get_korean_font(48)
            print("✓ 한글 폰트 로드 성공")
        except Exception as e:
            print(f"⚠️  폰트 로드 실패: {e}")
            self.font = pygame.font.Font(None, 24)
            self.big_font = pygame.font.Font(None, 48)

        # 🆕 images 폴더 및 이미지 관리자 초기화
        ensure_images_folder()
        self.image_manager = ImageManager()
        self.background_image = self.image_manager.get_image('background')

        # 🆕 플레이어에 이미지 매니저 연결
        self.player = GrimReaper(MAP_WIDTH // 2, MAP_HEIGHT // 2, self.image_manager)
        self.camera = Camera()
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_rate = 1.5
        self.game_over = False
        self.game_time = 0
        self.score = 0

    def spawn_enemy(self):
        angle = random.uniform(0, 2 * math.pi)
        distance = 300 + random.uniform(0, 200)

        x = self.player.x + math.cos(angle) * distance
        y = self.player.y + math.sin(angle) * distance

        x = max(50, min(MAP_WIDTH - 50, x))
        y = max(50, min(MAP_HEIGHT - 50, y))

        # 🆕 시간에 따른 적 타입 결정
        rand = random.random()
        if self.game_time > 30 and rand < 0.05:
            enemy_type = "boss"
        elif self.game_time > 15 and rand < 0.2:
            enemy_type = "strong"
        else:
            enemy_type = "normal"

        # 🆕 적에 이미지 매니저 연결
        enemy = EvilSpirit(x, y, enemy_type, self.image_manager)
        self.enemies.append(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.__init__()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_ESCAPE:
                        return False
        return True

    def update(self, dt):
        if self.game_over:
            return

        # 🆕 애니메이션 업데이트
        self.image_manager.update_animations(dt)

        self.game_time += dt
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)
        self.camera.update(self.player.x, self.player.y)

        self.spawn_timer += dt
        if self.spawn_timer >= 1.0 / self.spawn_rate:
            self.spawn_enemy()
            self.spawn_timer = 0

        for enemy in self.enemies[:]:
            enemy.update(dt, self.player)

            distance_to_player = math.sqrt((enemy.x - self.player.x) ** 2 + (enemy.y - self.player.y) ** 2)
            if distance_to_player > 1000:
                self.enemies.remove(enemy)
                continue

            if distance_to_player < self.player.size + enemy.size:
                if self.player.take_damage(enemy.damage):
                    self.game_over = True
                enemy.alive = False

            if not enemy.alive:
                # 🆕 적 타입별 점수 차등 지급
                self.score += {"normal": 10, "strong": 20, "boss": 50}.get(enemy.spirit_type, 10)
                self.enemies.remove(enemy)

        self.player.attack(self.enemies)

    def draw(self):
        # 🆕 배경 이미지 그리기
        if self.background_image:
            # 배경이 맵 크기와 같은 경우
            if self.background_image.get_width() == MAP_WIDTH and self.background_image.get_height() == MAP_HEIGHT:
                bg_x, bg_y = self.camera.apply(0, 0)
                visible_rect = pygame.Rect(-bg_x, -bg_y, WINDOW_WIDTH, WINDOW_HEIGHT)
                visible_rect.clamp_ip(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))

                if visible_rect.width > 0 and visible_rect.height > 0:
                    bg_surface = self.background_image.subsurface(visible_rect)
                    screen_x = max(0, bg_x)
                    screen_y = max(0, bg_y)
                    self.screen.blit(bg_surface, (screen_x, screen_y))
            else:
                self.screen.blit(self.background_image, (0, 0))
        else:
            # 기본 배경 (격자)
            self.screen.fill(GRAY)

            grid_size = 100
            start_x = int(self.camera.x // grid_size) * grid_size
            start_y = int(self.camera.y // grid_size) * grid_size

            for x in range(start_x, start_x + WINDOW_WIDTH + grid_size, grid_size):
                screen_x, _ = self.camera.apply(x, 0)
                if 0 <= screen_x <= WINDOW_WIDTH:
                    pygame.draw.line(self.screen, (70, 70, 70), (screen_x, 0), (screen_x, WINDOW_HEIGHT))

            for y in range(start_y, start_y + WINDOW_HEIGHT + grid_size, grid_size):
                _, screen_y = self.camera.apply(0, y)
                if 0 <= screen_y <= WINDOW_HEIGHT:
                    pygame.draw.line(self.screen, (70, 70, 70), (0, screen_y), (WINDOW_WIDTH, screen_y))

        if not self.game_over:
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera)
            self.player.draw(self.screen, self.camera)

        # UI (5단계와 동일)
        hp_bar_width = 200
        hp_bar_height = 20
        hp_percentage = self.player.hp / self.player.max_hp

        pygame.draw.rect(self.screen, RED, (10, 10, hp_bar_width, hp_bar_height))
        pygame.draw.rect(self.screen, GREEN, (10, 10, hp_bar_width * hp_percentage, hp_bar_height))
        pygame.draw.rect(self.screen, WHITE, (10, 10, hp_bar_width, hp_bar_height), 2)

        hp_text = self.font.render(f"체력: {self.player.hp}/{self.player.max_hp}", True, WHITE)
        time_text = self.font.render(f"시간: {int(self.game_time)}초", True, WHITE)
        score_text = self.font.render(f"점수: {self.score}", True, WHITE)
        enemy_count_text = self.font.render(f"악귀: {len(self.enemies)}", True, WHITE)

        self.screen.blit(hp_text, (10, 40))
        self.screen.blit(time_text, (10, 70))
        self.screen.blit(score_text, (10, 100))
        self.screen.blit(enemy_count_text, (10, 130))

        # 🆕 애니메이션 상태 표시
        anim_text = self.font.render("🎬 PNG 애니메이션 적용됨!", True, (135, 206, 235))
        self.screen.blit(anim_text, (10, 160))

        # 미니맵 (5단계와 동일)
        minimap_size = 150
        minimap_x = WINDOW_WIDTH - minimap_size - 10
        minimap_y = 10

        pygame.draw.rect(self.screen, (30, 30, 30), (minimap_x, minimap_y, minimap_size, minimap_size))
        pygame.draw.rect(self.screen, WHITE, (minimap_x, minimap_y, minimap_size, minimap_size), 2)

        player_minimap_x = minimap_x + (self.player.x / MAP_WIDTH) * minimap_size
        player_minimap_y = minimap_y + (self.player.y / MAP_HEIGHT) * minimap_size
        pygame.draw.circle(self.screen, GOLD, (int(player_minimap_x), int(player_minimap_y)), 3)

        for enemy in self.enemies:
            enemy_minimap_x = minimap_x + (enemy.x / MAP_WIDTH) * minimap_size
            enemy_minimap_y = minimap_y + (enemy.y / MAP_HEIGHT) * minimap_size
            colors = {"normal": RED, "strong": (255, 165, 0), "boss": (128, 0, 128)}
            color = colors.get(enemy.spirit_type, RED)
            pygame.draw.circle(self.screen, color, (int(enemy_minimap_x), int(enemy_minimap_y)), 1)

        control_text = self.font.render("WASD/방향키: 이동 | ESC: 종료", True, WHITE)
        self.screen.blit(control_text, (10, WINDOW_HEIGHT - 30))

        # 게임 오버 화면 (5단계와 동일)
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.big_font.render("게임 종료!", True, RED)
            final_score_text = self.font.render(f"최종 점수: {self.score}", True, WHITE)
            final_time_text = self.font.render(f"생존 시간: {int(self.game_time)}초", True, WHITE)
            restart_text = self.font.render("스페이스바: 다시 시작 | ESC: 종료", True, WHITE)

            go_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
            fs_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            ft_rect = final_time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            rs_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))

            self.screen.blit(game_over_text, go_rect)
            self.screen.blit(final_score_text, fs_rect)
            self.screen.blit(final_time_text, ft_rect)
            self.screen.blit(restart_text, rs_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


# ============================================================================
# 메인 실행
# ============================================================================
if __name__ == "__main__":
    print("🎮 6단계: PNG 애니메이션 시스템이 추가되었습니다!")
    print("images 폴더에 PNG 프레임 파일을 넣으면 애니메이션이 적용됩니다.")
    print("📁 지원하는 파일 패턴:")
    print("   - grim_reaper_frame_0001.png, grim_reaper_frame_0002.png, ...")
    print("   - evil_spirit_normal_1.png, evil_spirit_normal_2.png, ...")
    print("   - evil_spirit_strong.png (단일 이미지)")
    print("   - background.png (배경 이미지)")
    print("🎬 이미지가 없어도 기본 그래픽으로 정상 작동합니다!")
    game = Game()
    game.run()