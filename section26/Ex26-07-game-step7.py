# ============================================================================
# 🎮 7단계: 최종완성 - 저승사자 뱀서라이크
# ============================================================================

import pygame
import random
import math
import sys
import platform
import os
import glob
import re

# ============================================================================
# ✨ 7단계에서 새로 추가된 최종 기능들
# - 레벨업 시스템 + 경험치 바
# - 전역 스킬 (천상화염진) + 쿨다운 시스템
# - 3종류 적 타입 (normal, strong, boss) + 차등 능력치
# - 웨이브 시스템 + 시간에 따른 난이도 증가
# - GIF 애니메이션 지원 (선택적)
# - 완전한 UI (경험치, 스킬, 레벨, 웨이브)
# - 성능 최적화 + 카메라 가시성 체크
# - 향상된 게임플레이 메커니즘
# ============================================================================

pygame.init()

# 기본 설정 (6단계와 동일)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
MAP_WIDTH = 4000
MAP_HEIGHT = 3000
FPS = 60

# 색상 정의 (6단계 + 추가)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
GOLD = (255, 215, 0)
DARK_BLUE = (25, 25, 112)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)  # 🆕 보스용
ORANGE = (255, 165, 0)  # 🆕 강한 적용

# 🆕 이미지 폴더 설정
IMAGES_FOLDER = "images"

# 🆕 GIF 지원 체크 (선택적)
try:
    from PIL import Image, ImageSequence

    GIF_SUPPORT = True
    print("✓ GIF 지원 활성화됨 (PIL 사용)")
except ImportError:
    GIF_SUPPORT = False
    print("✗ PIL 라이브러리 없음 - PNG 애니메이션만 지원")


# ============================================================================
# images 폴더 관리 (6단계와 동일)
# ============================================================================
def ensure_images_folder():
    if not os.path.exists(IMAGES_FOLDER):
        os.makedirs(IMAGES_FOLDER)
        print(f"✓ {IMAGES_FOLDER} 폴더가 생성되었습니다.")
        print("📁 이 폴더에 다음 이미지들을 넣으면 애니메이션이 적용됩니다:")
        print("   - grim_reaper_frame_0001.png, grim_reaper_frame_0002.png, ...")
        print("   - evil_spirit_normal_1.png, evil_spirit_normal_2.png, ...")
        print("   - evil_spirit_strong_1.png, evil_spirit_strong_2.png, ...")
        print("   - evil_spirit_boss_1.png, evil_spirit_boss_2.png, ...")
        print("   - background_frame_0001.png, background_frame_0002.png, ...")
        print("   - attack_effect_1.png, attack_effect_2.png, ...")
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
    elif system == "Darwin":
        font_candidates = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    else:
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
# PNG 프레임 파일 검색 시스템 (6단계와 동일)
# ============================================================================
def find_frame_files(filename_base):
    frame_files = []
    patterns = [
        os.path.join(IMAGES_FOLDER, f"{filename_base}_frame_*.png"),
        os.path.join(IMAGES_FOLDER, f"{filename_base}_*.png"),
        os.path.join(IMAGES_FOLDER, f"{filename_base}*.png"),
    ]

    all_candidates = []

    for pattern_idx, pattern in enumerate(patterns):
        files = glob.glob(pattern)

        for file in files:
            basename = os.path.basename(file)

            if pattern_idx == 0:
                match = re.search(rf"{re.escape(filename_base)}_frame_(\d+)\.png$", basename)
            elif pattern_idx == 1:
                if "_frame_" not in basename:
                    match = re.search(rf"{re.escape(filename_base)}_(\d+)\.png$", basename)
                else:
                    continue
            else:
                if "_frame_" not in basename and f"{filename_base}_" not in basename:
                    match = re.search(rf"{re.escape(filename_base)}(\d+)\.png$", basename)
                else:
                    continue

            if match:
                frame_num = int(match.group(1))
                all_candidates.append((frame_num, file, pattern_idx))

    all_candidates.sort(key=lambda x: x[0])

    if all_candidates:
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
# 🆕 GIF 애니메이션 클래스 (선택적)
# ============================================================================
class GifAnimation:
    def __init__(self, gif_path, width, height):
        self.frames = []
        self.frame_durations = []
        self.current_frame = 0
        self.frame_timer = 0
        self.total_frames = 0

        if GIF_SUPPORT:
            self.load_gif(gif_path, width, height)

    def load_gif(self, gif_path, width, height):
        try:
            pil_image = Image.open(gif_path)
            for frame in ImageSequence.Iterator(pil_image):
                frame = frame.convert('RGBA')
                frame = frame.resize((width, height), Image.Resampling.LANCZOS)

                mode = frame.mode
                size = frame.size
                raw = frame.tobytes()
                pygame_surface = pygame.image.fromstring(raw, size, mode)
                self.frames.append(pygame_surface)

                duration = frame.info.get('duration', 100)
                self.frame_durations.append(duration)

            self.total_frames = len(self.frames)
            print(f"✓ GIF 로드 성공: {self.total_frames}프레임")
        except Exception as e:
            print(f"✗ GIF 로드 실패: {e}")

    def update(self, dt):
        if self.total_frames > 1:
            self.frame_timer += dt * 1000
            current_duration = self.frame_durations[self.current_frame] if self.frame_durations else 100
            if self.frame_timer >= current_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % self.total_frames

    def get_current_frame(self):
        if self.frames:
            return self.frames[self.current_frame]
        return None

    def has_frames(self):
        return len(self.frames) > 0


# ============================================================================
# PNG 프레임 애니메이션 클래스 (6단계 확장)
# ============================================================================
class PngFrameAnimation:
    def __init__(self, frame_files, frame_duration=700, width=None, height=None):
        self.frames = []
        self.frame_durations = []
        self.current_frame = 0
        self.frame_timer = 0
        self.total_frames = 0

        if isinstance(frame_duration, (list, tuple)):
            self.default_duration = frame_duration
        else:
            self.default_duration = frame_duration

        self.load_png_frames(frame_files, width, height)

    def load_png_frames(self, frame_files, width, height):
        for i, file_path in enumerate(frame_files):
            if os.path.exists(file_path):
                try:
                    if GIF_SUPPORT:
                        # PIL을 사용한 고품질 로드
                        pil_image = Image.open(file_path).convert('RGBA')
                        if width and height:
                            pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)

                        mode = pil_image.mode
                        size = pil_image.size
                        raw = pil_image.tobytes()
                        pygame_surface = pygame.image.fromstring(raw, size, mode)
                    else:
                        # pygame 직접 로드
                        pygame_surface = pygame.image.load(file_path).convert_alpha()
                        if width and height:
                            pygame_surface = pygame.transform.scale(pygame_surface, (width, height))

                    self.frames.append(pygame_surface)

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
        if self.total_frames > 1:
            self.frame_timer += dt * 1000
            current_duration = self.frame_durations[self.current_frame] if self.frame_durations else 700
            if self.frame_timer >= current_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % self.total_frames

    def get_current_frame(self):
        if self.frames:
            return self.frames[self.current_frame]
        return None

    def has_frames(self):
        return len(self.frames) > 0


# ============================================================================
# 🆕 이미지 관리자 클래스 (확장됨)
# ============================================================================
class ImageManager:
    def __init__(self):
        self.images = {}
        self.animations = {}  # 🆕 GIF 애니메이션
        self.png_animations = {}
        self.animation_configs = {}
        self.load_images()

    def setup_animation_configs(self):
        """🆕 확장된 애니메이션 설정"""
        self.animation_configs = {
            'grim_reaper': {
                'frame_duration': 500,
                'description': '저승사자 (500ms 간격)'
            },
            'evil_spirit_normal': {
                'frame_duration': 300,
                'description': '일반 악귀 (300ms 간격)'
            },
            'evil_spirit_strong': {
                'frame_duration': 400,
                'description': '강한 악귀 (400ms 간격)'
            },
            'evil_spirit_boss': {
                'frame_duration': [800, 400, 600],  # 🆕 가변 간격
                'description': '보스 악귀 (가변 간격)'
            },
            'background': {
                'frame_duration': 2000,
                'description': '배경 (2000ms 간격)'
            },
            'attack_effect': {  # 🆕 공격 이펙트
                'frame_duration': 100,
                'description': '공격 이펙트 (100ms 간격)'
            }
        }

    def load_images(self):
        self.setup_animation_configs()

        image_files = {
            'grim_reaper': 'grim_reaper',
            'evil_spirit_normal': 'evil_spirit_normal',
            'evil_spirit_strong': 'evil_spirit_strong',
            'evil_spirit_boss': 'evil_spirit_boss',
            'background': 'background',
            'attack_effect': 'attack_effect',  # 🆕 공격 이펙트
        }

        size_map = {
            'grim_reaper': (30, 30),
            'evil_spirit_normal': (20, 20),
            'evil_spirit_strong': (25, 25),
            'evil_spirit_boss': (40, 40),
            'background': (MAP_WIDTH, MAP_HEIGHT),
            'attack_effect': (160, 160),  # 🆕 공격 이펙트 크기
        }

        for key, filename_base in image_files.items():
            loaded = False
            width, height = size_map.get(key, (60, 60))

            config = self.animation_configs.get(key, {'frame_duration': 700})
            frame_duration = config['frame_duration']

            # 1단계: PNG 프레임 파일들
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

            # 🆕 2단계: GIF 파일 시도
            if not loaded:
                gif_filename = os.path.join(IMAGES_FOLDER, f"{filename_base}.gif")
                if GIF_SUPPORT and os.path.exists(gif_filename):
                    try:
                        animation = GifAnimation(gif_filename, width, height)
                        if animation.has_frames():
                            self.animations[key] = animation
                            self.images[key] = animation.get_current_frame()
                            print(f"✓ {gif_filename} GIF 애니메이션 로드 성공")
                            loaded = True
                    except Exception as e:
                        print(f"✗ {gif_filename} GIF 로드 오류: {e}")

            # 3단계: 단일 PNG 파일
            if not loaded:
                png_filename = os.path.join(IMAGES_FOLDER, f"{filename_base}.png")
                if os.path.exists(png_filename):
                    try:
                        if GIF_SUPPORT:
                            pil_image = Image.open(png_filename).convert('RGBA')
                            pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
                            mode = pil_image.mode
                            size = pil_image.size
                            raw = pil_image.tobytes()
                            surface = pygame.image.fromstring(raw, size, mode)
                        else:
                            surface = pygame.image.load(png_filename).convert_alpha()
                            surface = pygame.transform.scale(surface, (width, height))

                        self.images[key] = surface
                        print(f"✓ {png_filename} 정적 PNG 로드 성공")
                        loaded = True
                    except Exception as e:
                        print(f"✗ {png_filename} PNG 로드 실패: {e}")

            if not loaded:
                self.images[key] = None
                print(f"✗ {key} 이미지를 찾을 수 없습니다 - 기본 그래픽 사용")

    def update_animations(self, dt):
        """🆕 PNG + GIF 애니메이션 업데이트"""
        for key, animation in self.png_animations.items():
            animation.update(dt)
            self.images[key] = animation.get_current_frame()

        for key, animation in self.animations.items():
            animation.update(dt)
            self.images[key] = animation.get_current_frame()

    def get_image(self, key):
        return self.images.get(key)

    def scale_image(self, key, size):
        image = self.get_image(key)
        if image:
            return pygame.transform.scale(image, (size, size))
        return None


# ============================================================================
# 🆕 카메라 클래스 (향상됨)
# ============================================================================
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
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

    def is_visible(self, x, y, size=50):
        """🆕 객체가 화면에 보이는지 확인 (성능 최적화)"""
        screen_x, screen_y = self.apply(x, y)
        return (-size <= screen_x <= WINDOW_WIDTH + size and
                -size <= screen_y <= WINDOW_HEIGHT + size)


# ============================================================================
# 🆕 저승사자 클래스 (완전판)
# ============================================================================
class GrimReaper:
    def __init__(self, x, y, image_manager):
        # 기본 속성
        self.x = x
        self.y = y
        self.size = 15
        self.speed = 200

        # 🆕 HP 및 레벨 시스템
        self.hp = 100
        self.max_hp = 100
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100

        # 공격 시스템
        self.attack_damage = 25
        self.attack_range = 80
        self.attack_cooldown = 0
        self.attack_speed = 30
        self.attacking = False
        self.attack_animation_timer = 0

        # 🆕 전역 스킬 시스템 (천상화염진)
        self.ultimate_skill_cooldown = 0
        self.ultimate_skill_max_cooldown = 600  # 10초 (60fps)
        self.ultimate_skill_active = False
        self.ultimate_skill_timer = 0
        self.ultimate_skill_duration = 180  # 3초
        self.ultimate_skill_damage = 100
        self.ultimate_skill_range = 200

        # 이미지 관리
        self.image_manager = image_manager
        self.image = self.image_manager.scale_image('grim_reaper', self.size * 2)
        self.attack_effect_image = self.image_manager.scale_image('attack_effect', self.attack_range * 2)

    def update(self, dt, keys):
        # 이동 처리 (전역 스킬 중 속도 감소)
        speed_modifier = 0.3 if self.ultimate_skill_active else 1.0

        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed * dt * speed_modifier
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed * dt * speed_modifier
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed * dt * speed_modifier
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed * dt * speed_modifier

        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.x += dx
        self.y += dy
        self.x = max(self.size, min(MAP_WIDTH - self.size, self.x))
        self.y = max(self.size, min(MAP_HEIGHT - self.size, self.y))

        # 🆕 전역 스킬 입력 처리
        if keys[pygame.K_SPACE] and self.ultimate_skill_cooldown <= 0 and not self.ultimate_skill_active:
            self.activate_ultimate_skill()

        # 타이머 업데이트
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.attack_animation_timer > 0:
            self.attack_animation_timer -= dt
            if self.attack_animation_timer <= 0:
                self.attacking = False

        # 🆕 전역 스킬 시스템 업데이트
        if self.ultimate_skill_cooldown > 0:
            self.ultimate_skill_cooldown -= 1

        if self.ultimate_skill_active:
            self.ultimate_skill_timer -= 1
            if self.ultimate_skill_timer <= 0:
                self.ultimate_skill_active = False

        # 이미지 업데이트
        self.image = self.image_manager.scale_image('grim_reaper', self.size * 2)

    def activate_ultimate_skill(self):
        """🆕 전역 스킬 활성화"""
        self.ultimate_skill_active = True
        self.ultimate_skill_timer = self.ultimate_skill_duration
        self.ultimate_skill_cooldown = self.ultimate_skill_max_cooldown

    def ultimate_skill_attack(self, enemies):
        """🆕 전역 스킬로 범위 내 모든 적 공격"""
        if not self.ultimate_skill_active:
            return 0

        damaged_enemies = 0
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
            if distance <= self.ultimate_skill_range:
                damage_modifier = max(0.5, 1 - (distance / self.ultimate_skill_range) * 0.5)
                final_damage = int(self.ultimate_skill_damage * damage_modifier)
                enemy.take_damage(final_damage)
                damaged_enemies += 1

        return damaged_enemies

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

    def gain_exp(self, amount):
        """🆕 경험치 획득 및 레벨업"""
        self.exp += amount
        if self.exp >= self.exp_to_next:
            self.level_up()

    def level_up(self):
        """🆕 레벨업 처리"""
        self.level += 1
        self.exp = 0
        self.exp_to_next = int(self.exp_to_next * 1.2)

        # 레벨업 보상
        self.attack_damage += 5
        self.max_hp += 10
        self.hp = self.max_hp  # HP 완전 회복

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            return True
        return False

    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply(self.x, self.y)

        if not camera.is_visible(self.x, self.y, self.ultimate_skill_range):
            return

        # 🆕 전역 스킬 이펙트
        if self.ultimate_skill_active:
            progress = 1 - (self.ultimate_skill_timer / self.ultimate_skill_duration)

            # 3단계 파동 효과
            for i in range(3):
                wave_progress = max(0, min(1, progress * 3 - i))
                if wave_progress > 0:
                    wave_radius = int(wave_progress * self.ultimate_skill_range)
                    wave_alpha = int(100 * (1 - wave_progress))

                    wave_surface = pygame.Surface((wave_radius * 2, wave_radius * 2))
                    wave_surface.set_alpha(wave_alpha)
                    pygame.draw.circle(wave_surface, (135, 206, 235), (wave_radius, wave_radius), wave_radius)
                    screen.blit(wave_surface, (screen_x - wave_radius, screen_y - wave_radius))

            # 중앙 에너지 구체
            energy_size = int(20 * (0.5 + 0.5 * math.sin(progress * math.pi * 4)))
            energy_surface = pygame.Surface((energy_size * 2, energy_size * 2))
            energy_surface.set_alpha(150)
            pygame.draw.circle(energy_surface, (135, 206, 235), (energy_size, energy_size), energy_size)
            screen.blit(energy_surface, (screen_x - energy_size, screen_y - energy_size))

            # 회전하는 에너지 입자들
            for i in range(8):
                angle = (progress * 360 * 2 + i * 45) % 360
                particle_x = screen_x + math.cos(math.radians(angle)) * 40
                particle_y = screen_y + math.sin(math.radians(angle)) * 40
                particle_color = (135, 206, 235) if i % 2 == 0 else (65, 105, 225)
                pygame.draw.circle(screen, particle_color, (int(particle_x), int(particle_y)), 3)

            # 스킬 범위 표시
            pygame.draw.circle(screen, (135, 206, 235), (int(screen_x), int(screen_y)), self.ultimate_skill_range, 2)

        # 일반 공격 이펙트
        if self.attacking and self.attack_effect_image:
            effect_rect = self.attack_effect_image.get_rect()
            effect_rect.center = (int(screen_x), int(screen_y))
            effect_surface = self.attack_effect_image.copy()
            alpha = int(255 * (self.attack_animation_timer / 0.3))
            effect_surface.set_alpha(alpha)
            screen.blit(effect_surface, effect_rect)
        elif self.attacking:
            attack_surface = pygame.Surface((self.attack_range * 2, self.attack_range * 2))
            attack_surface.set_alpha(100)
            pygame.draw.circle(attack_surface, GOLD, (self.attack_range, self.attack_range), self.attack_range)
            screen.blit(attack_surface, (screen_x - self.attack_range, screen_y - self.attack_range))

        # 공격 범위 표시
        if not self.attacking and not self.ultimate_skill_active:
            attack_surface = pygame.Surface((self.attack_range * 2, self.attack_range * 2))
            attack_surface.set_alpha(20)
            pygame.draw.circle(attack_surface, GOLD, (self.attack_range, self.attack_range), self.attack_range)
            screen.blit(attack_surface, (screen_x - self.attack_range, screen_y - self.attack_range))

        # 플레이어 본체
        if self.image:
            image_rect = self.image.get_rect()
            image_rect.center = (int(screen_x), int(screen_y))

            # 전역 스킬 중 글로우 효과
            if self.ultimate_skill_active:
                glow_image = pygame.transform.scale(self.image, (self.size * 3, self.size * 3))
                glow_rect = glow_image.get_rect()
                glow_rect.center = image_rect.center
                glow_surface = glow_image.copy()
                glow_surface.set_alpha(50)
                screen.blit(glow_surface, glow_rect)

            screen.blit(self.image, image_rect)
        else:
            # 기본 그래픽
            current_size = self.size + (5 if self.ultimate_skill_active else 0)
            pygame.draw.circle(screen, DARK_BLUE, (int(screen_x), int(screen_y)), current_size)
            pygame.draw.circle(screen, GOLD, (int(screen_x), int(screen_y)), current_size - 3)
            pygame.draw.circle(screen, BLACK, (int(screen_x), int(screen_y)), current_size, 2)

            left_eye_color = GOLD if not self.ultimate_skill_active else (255, 255, 0)
            right_eye_color = RED if not self.ultimate_skill_active else (255, 0, 0)
            pygame.draw.circle(screen, left_eye_color, (int(screen_x - 4), int(screen_y - 2)), 2)
            pygame.draw.circle(screen, right_eye_color, (int(screen_x + 4), int(screen_y - 2)), 2)


# ============================================================================
# 🆕 악귀 클래스 (3종류 완전 구현)
# ============================================================================
class EvilSpirit:
    def __init__(self, x, y, spirit_type="normal", image_manager=None):
        self.x = x
        self.y = y
        self.spirit_type = spirit_type
        self.alive = True
        self.image_manager = image_manager

        # 🆕 타입별 완전한 스탯 차별화
        if spirit_type == "boss":
            self.size = 20
            self.hp = 150
            self.max_hp = 150
            self.speed = 30
            self.damage = 25
            self.exp_reward = 50
            self.color = PURPLE
            self.image_key = 'evil_spirit_boss'
        elif spirit_type == "strong":
            self.size = 12
            self.hp = 60
            self.max_hp = 60
            self.speed = 45
            self.damage = 15
            self.exp_reward = 20
            self.color = ORANGE
            self.image_key = 'evil_spirit_strong'
        else:  # normal
            self.size = 10
            self.hp = 30
            self.max_hp = 30
            self.speed = 60
            self.damage = 10
            self.exp_reward = 10
            self.color = RED
            self.image_key = 'evil_spirit_normal'

        self.image = self.image_manager.scale_image(self.image_key, self.size * 2) if self.image_manager else None

    def update(self, dt, player):
        if not self.alive:
            return

        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt

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

        if not camera.is_visible(self.x, self.y, self.size * 2):
            return

        # 악귀 본체
        if self.image:
            image_rect = self.image.get_rect()
            image_rect.center = (int(screen_x), int(screen_y))
            screen.blit(self.image, image_rect)
        else:
            pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.size)
            pygame.draw.circle(screen, BLACK, (int(screen_x), int(screen_y)), self.size, 1)

            eye_size = max(1, self.size // 5)
            eye_offset = max(2, self.size // 3)
            pygame.draw.circle(screen, WHITE, (int(screen_x - eye_offset), int(screen_y - eye_size)), eye_size)
            pygame.draw.circle(screen, WHITE, (int(screen_x + eye_offset), int(screen_y - eye_size)), eye_size)

        # HP 바
        bar_width = self.size * 2
        bar_height = 3
        bar_x = screen_x - bar_width // 2
        bar_y = screen_y - self.size - 8

        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        current_hp_width = (self.hp / self.max_hp) * bar_width
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_hp_width, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)


# ============================================================================
# 🆕 게임 메인 클래스 (최종완성)
# ============================================================================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("7단계: 최종완성 - 저승사자 뱀서라이크")
        self.clock = pygame.time.Clock()

        # 한글 폰트 설정
        try:
            self.font = get_korean_font(24)
            self.big_font = get_korean_font(48)
            print("✓ 한글 폰트 로드 성공")
        except Exception as e:
            print(f"⚠️  폰트 로드 실패: {e}")
            self.font = pygame.font.Font(None, 24)
            self.big_font = pygame.font.Font(None, 48)

        # 이미지 시스템 초기화
        ensure_images_folder()
        self.image_manager = ImageManager()
        self.background_image = self.image_manager.get_image('background')

        # 게임 상태 초기화
        self.reset_game()

    def reset_game(self):
        """🆕 게임 상태 초기화"""
        self.player = GrimReaper(MAP_WIDTH // 2, MAP_HEIGHT // 2, self.image_manager)
        self.camera = Camera()
        self.enemies = []
        self.game_time = 0
        self.spawn_timer = 0
        self.spawn_rate = 2.0
        self.game_over = False
        self.wave = 1  # 🆕 웨이브 시스템
        self.score = 0

    def spawn_enemy(self):
        """🆕 향상된 적 생성 시스템"""
        angle = random.uniform(0, 2 * math.pi)
        distance = 400 + random.uniform(0, 200)

        x = self.player.x + math.cos(angle) * distance
        y = self.player.y + math.sin(angle) * distance

        x = max(50, min(MAP_WIDTH - 50, x))
        y = max(50, min(MAP_HEIGHT - 50, y))

        # 🆕 시간에 따른 적 타입 결정 (더 정교함)
        rand = random.random()
        if self.game_time > 30 and rand < 0.05:  # 30초 후 5% 보스
            enemy_type = "boss"
        elif self.game_time > 15 and rand < 0.2:  # 15초 후 20% 강한 적
            enemy_type = "strong"
        else:
            enemy_type = "normal"

        self.enemies.append(EvilSpirit(x, y, enemy_type, self.image_manager))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_ESCAPE:
                        return False
        return True

    def update(self, dt):
        if self.game_over:
            return

        # 애니메이션 업데이트
        self.image_manager.update_animations(dt)

        # 카메라 업데이트
        self.camera.update(self.player.x, self.player.y)

        # 게임 시간 업데이트
        self.game_time += dt

        # 플레이어 업데이트
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)

        # 🆕 난이도 증가
        self.spawn_rate = min(8.0, 2.0 + self.game_time * 0.1)

        # 적 생성
        self.spawn_timer += dt
        if self.spawn_timer >= 1.0 / self.spawn_rate:
            self.spawn_enemy()
            self.spawn_timer = 0

        # 적 업데이트 및 관리
        for enemy in self.enemies[:]:
            # 성능 최적화: 너무 먼 적 제거
            distance_to_player = math.sqrt((enemy.x - self.player.x) ** 2 + (enemy.y - self.player.y) ** 2)
            if distance_to_player > 1000:
                self.enemies.remove(enemy)
                continue

            enemy.update(dt, self.player)

            # 충돌 검사
            if distance_to_player < self.player.size + enemy.size:
                if self.player.take_damage(enemy.damage):
                    self.game_over = True
                enemy.alive = False

            # 죽은 적 처리
            if not enemy.alive:
                self.player.gain_exp(enemy.exp_reward)
                self.score += enemy.exp_reward
                self.enemies.remove(enemy)

        # 공격 시스템
        self.player.attack(self.enemies)

        # 🆕 전역 스킬 시스템
        if self.player.ultimate_skill_active:
            damaged_count = self.player.ultimate_skill_attack(self.enemies)
            if damaged_count > 0:
                self.score += damaged_count * 5

        # 🆕 웨이브 계산
        self.wave = int(self.game_time // 30) + 1

    def draw(self):
        # 배경 그리기
        if self.background_image:
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
            # 기본 배경
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

        # 맵 경계 표시
        map_corners = [(0, 0), (MAP_WIDTH, 0), (MAP_WIDTH, MAP_HEIGHT), (0, MAP_HEIGHT)]
        screen_corners = [self.camera.apply(corner[0], corner[1]) for corner in map_corners]
        for i in range(len(screen_corners)):
            start = screen_corners[i]
            end = screen_corners[(i + 1) % len(screen_corners)]
            pygame.draw.line(self.screen, WHITE, start, end, 3)

        if not self.game_over:
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera)
            self.player.draw(self.screen, self.camera)

        # 🆕 완전한 UI 시스템
        # HP 바
        hp_bar_width = 200
        hp_bar_height = 20
        hp_percentage = self.player.hp / self.player.max_hp

        pygame.draw.rect(self.screen, RED, (10, 10, hp_bar_width, hp_bar_height))
        pygame.draw.rect(self.screen, GREEN, (10, 10, hp_bar_width * hp_percentage, hp_bar_height))
        pygame.draw.rect(self.screen, WHITE, (10, 10, hp_bar_width, hp_bar_height), 2)

        # 🆕 경험치 바
        exp_bar_width = 200
        exp_bar_height = 10
        exp_percentage = self.player.exp / self.player.exp_to_next

        pygame.draw.rect(self.screen, GRAY, (10, 35, exp_bar_width, exp_bar_height))
        pygame.draw.rect(self.screen, GOLD, (10, 35, exp_bar_width * exp_percentage, exp_bar_height))
        pygame.draw.rect(self.screen, WHITE, (10, 35, exp_bar_width, exp_bar_height), 2)

        # 🆕 전역 스킬 쿨다운 바
        skill_bar_width = 200
        skill_bar_height = 15

        if self.player.ultimate_skill_active:
            skill_percentage = self.player.ultimate_skill_timer / self.player.ultimate_skill_duration
            pygame.draw.rect(self.screen, (50, 50, 50), (10, 50, skill_bar_width, skill_bar_height))
            pygame.draw.rect(self.screen, (135, 206, 235),
                             (10, 50, skill_bar_width * skill_percentage, skill_bar_height))
            skill_text = self.font.render("천상화염진 발동중!", True, (135, 206, 235))
        elif self.player.ultimate_skill_cooldown > 0:
            skill_percentage = 1 - (self.player.ultimate_skill_cooldown / self.player.ultimate_skill_max_cooldown)
            pygame.draw.rect(self.screen, (50, 50, 50), (10, 50, skill_bar_width, skill_bar_height))
            pygame.draw.rect(self.screen, (100, 100, 100),
                             (10, 50, skill_bar_width * skill_percentage, skill_bar_height))
            remaining_seconds = int(self.player.ultimate_skill_cooldown / 60) + 1
            skill_text = self.font.render(f"천상화염진 쿨다운: {remaining_seconds}초", True, WHITE)
        else:
            pygame.draw.rect(self.screen, (50, 50, 50), (10, 50, skill_bar_width, skill_bar_height))
            pygame.draw.rect(self.screen, (135, 206, 235), (10, 50, skill_bar_width, skill_bar_height))
            skill_text = self.font.render("천상화염진 준비완료! (스페이스)", True, (135, 206, 235))

        pygame.draw.rect(self.screen, WHITE, (10, 50, skill_bar_width, skill_bar_height), 2)
        self.screen.blit(skill_text, (220, 50))

        # 🆕 게임 정보 텍스트
        level_text = self.font.render(f"레벨: {self.player.level}", True, WHITE)
        time_text = self.font.render(f"시간: {int(self.game_time)}초", True, WHITE)
        wave_text = self.font.render(f"웨이브: {self.wave}", True, WHITE)
        score_text = self.font.render(f"점수: {self.score}", True, WHITE)
        enemy_count_text = self.font.render(f"악귀: {len(self.enemies)}", True, WHITE)
        pos_text = self.font.render(f"위치: ({int(self.player.x)}, {int(self.player.y)})", True, WHITE)

        self.screen.blit(level_text, (10, 75))
        self.screen.blit(time_text, (10, 105))
        self.screen.blit(wave_text, (10, 135))
        self.screen.blit(score_text, (10, 165))
        self.screen.blit(enemy_count_text, (10, 195))
        self.screen.blit(pos_text, (10, 225))

        # 미니맵
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
            color = PURPLE if enemy.spirit_type == "boss" else ORANGE if enemy.spirit_type == "strong" else RED
            pygame.draw.circle(self.screen, color, (int(enemy_minimap_x), int(enemy_minimap_y)), 1)

        # 조작법 안내
        control_text = self.font.render("WASD/방향키: 이동 | 스페이스: 천상화염진 | ESC: 종료", True, WHITE)
        self.screen.blit(control_text, (10, WINDOW_HEIGHT - 30))

        # 🆕 향상된 게임 오버 화면
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.big_font.render("게임 종료!", True, RED)
            final_score_text = self.font.render(f"최종 점수: {self.score}", True, WHITE)
            final_time_text = self.font.render(f"생존 시간: {int(self.game_time)}초", True, WHITE)
            final_level_text = self.font.render(f"도달 레벨: {self.player.level}", True, WHITE)
            restart_text = self.font.render("스페이스바: 다시 시작 | ESC: 종료", True, WHITE)

            go_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
            fs_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            ft_rect = final_time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10))
            fl_rect = final_level_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            rs_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))

            self.screen.blit(game_over_text, go_rect)
            self.screen.blit(final_score_text, fs_rect)
            self.screen.blit(final_time_text, ft_rect)
            self.screen.blit(final_level_text, fl_rect)
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
    print("🎮 7단계: 최종완성 - 저승사자 뱀서라이크!")
    print()
    print("🌟 완성된 기능들:")
    print("✅ 레벨업 시스템 + 경험치 바")
    print("✅ 전역 스킬 (천상화염진) + 쿨다운 시스템")
    print("✅ 3종류 악귀 (일반/강화/보스) + 차등 능력치")
    print("✅ 웨이브 시스템 + 시간별 난이도 증가")
    print("✅ PNG + GIF 애니메이션 지원")
    print("✅ 완전한 UI (HP, EXP, 스킬, 미니맵)")
    print("✅ 성능 최적화 + 카메라 시스템")
    print("✅ 한글 폰트 지원")
    print()
    print("🎮 조작법:")
    print("- WASD/방향키: 이동")
    print("- 스페이스바: 천상화염진 (전역 스킬)")
    print("- ESC: 종료")
    print()
    print("📁 images 폴더에 애니메이션 파일을 넣으면 적용됩니다!")
    print("🚀 게임 시작!")

    game = Game()
    game.run()