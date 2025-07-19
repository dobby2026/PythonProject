import pygame
import random
import sys
from enum import Enum, auto
from dataclasses import dataclass

"""
Pygame Lotto Slot Machine Game
==============================
Features:
- 5 Reels with spinning symbols (numbers 1-45 like Korean Lotto, plus special symbols: BONUS, WILD, FREE)
- Adjustable bet per spin
- Virtual credits & payout table
- Win conditions based on horizontal line (center) + bonus combinations
- Wild symbol substitutes any number for sequence / set matches
- Bonus: triggers mini lotto draw (pick 6 numbers, generate winning numbers, pays for matches)
- Free Spin symbol: 3+ gives free spins
- Smooth spinning animation with easing & staggered stop
- Sound effects (placeholder beeps) using pygame.mixer (safe if file absent – uses generated tones)
- Simple persistent high score (session only)
- FPS independent timing using delta time
Controls:
  SPACE : Spin (if not spinning)
  UP/DOWN : Change bet
  B : Toggle Fast Mode
  L : Trigger manual Lotto mini-game (if you have a ticket prepared)
  ESC : Quit
  F : Toggle Fullscreen
  M : Mute sounds
  R : Reset credits

Reel Mechanics:
- Each reel scrolls symbol sprites vertically. A reel stops after its individual spin time.
- Result is taken from center row of each reel.
- Payout checks patterns: matching numbers (3,4,5 of a kind), sequential run of numbers (3+), specials.

Bonus Mini Lotto:
- If BONUS symbol appears anywhere in result, you receive one Lotto Ticket (auto stored until used).
- Press L to play mini lotto if you have a ticket and not currently in spin.
- Game chooses 6 unique random numbers (1-45) as player's pick and separate 6 winning numbers + 1 bonus number.
- Matches pay according to count.

This is a teaching / demo code: clarity prioritized over micro-optimization.
"""

# --------------------------- Configuration ---------------------------
WIDTH, HEIGHT = 960, 540
FPS = 60
REEL_COUNT = 5
SYMBOL_SIZE = 96
VISIBLE_ROWS = 3
REEL_SPIN_TIME_BASE = 1.2  # seconds for first reel
REEL_SPIN_TIME_INCREMENT = 0.35  # added per reel for stagger
FAST_MODE_FACTOR = 0.4
FONT_NAME = 'arial'
START_CREDITS = 1000
MIN_BET = 10
MAX_BET = 200
BET_STEP = 10
FREE_SPINS_AWARD = 5

NUMBER_SYMBOLS = list(range(1, 46))  # 1..45
SPECIALS = ['WILD', 'BONUS', 'FREE']
ALL_SYMBOLS = NUMBER_SYMBOLS + SPECIALS

# Payout settings
PAYOUT_MATCH = {  # n-of-a-kind (numbers only or WILD substitute)
    3: 50,
    4: 150,
    5: 500,
}
PAYOUT_SEQUENCE_PER_LENGTH = 60  # sequence length * this
PAYOUT_FREE_SPINS = 0  # free spins just awarded, not direct credit
PAYOUT_WILDS_ALL = 300  # all wilds

# Lotto mini game payouts for matches (like a simplified table)
LOTTO_PAYOUTS = {
    3: 100,
    4: 400,
    5: 2000,
    6: 10000,
}
BONUS_MATCH_PAYOUT = 3000  # 5 matches + bonus number (approx mimic)

# Colors
WHITE = (240, 240, 240)
BLACK = (15, 15, 18)
GRAY = (80, 80, 90)
GREEN = (60, 180, 90)
RED = (230, 70, 70)
YELLOW = (250, 218, 94)
BLUE = (90, 140, 240)
PURPLE = (160, 100, 210)
ORANGE = (240, 150, 60)

# --------------------------- Game States ---------------------------
class GameState(Enum):
    READY = auto()
    SPINNING = auto()
    MINI_LOTTO = auto()
    RESULT = auto()

@dataclass
class Reel:
    symbols: list
    offset: float = 0.0
    spinning: bool = False
    spin_time: float = 0.0
    time_accum: float = 0.0
    result_index: int = 0  # index in symbols that is at center after spin

# --------------------------- Utility Functions ---------------------------

def create_reel_symbols():
    # Weighted: numbers more frequent than specials
    base_numbers = NUMBER_SYMBOLS * 2  # double frequency
    specials = SPECIALS * 4  # repeat specials for visibility
    pool = base_numbers + specials
    random.shuffle(pool)
    return pool

# Text rendering helper with border

def render_text(surface, text, size, color, x, y, center=False, shadow=True):
    font = pygame.font.SysFont(FONT_NAME, size)
    txt = font.render(str(text), True, color)
    if shadow:
        sh = font.render(str(text), True, (0,0,0))
        if center:
            rect = txt.get_rect(center=(x+2, y+2))
            surface.blit(sh, rect)
        else:
            surface.blit(sh, (x+2, y+2))
    if center:
        rect = txt.get_rect(center=(x, y))
        surface.blit(txt, rect)
    else:
        surface.blit(txt, (x, y))


# --------------------------- Core Game Class ---------------------------
class SlotMachine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Lotto Slot Machine')
        self.clock = pygame.time.Clock()
        self.state = GameState.READY
        self.fast_mode = False
        self.muted = False
        self.credits = START_CREDITS
        self.bet = MIN_BET
        self.free_spins = 0
        self.lotto_tickets = 0
        self.last_win = 0
        self.high_credits = START_CREDITS
        self.reels = [Reel(create_reel_symbols()) for _ in range(REEL_COUNT)]
        self.symbol_surfaces = {}
        self.build_symbol_surfaces()
        self.result_symbols = []
        self.mini_lotto_data = None
        self.sounds = {}
        self.build_sounds()

    def build_symbol_surfaces(self):
        font = pygame.font.SysFont(FONT_NAME, 42, bold=True)
        for sym in ALL_SYMBOLS:
            surf = pygame.Surface((SYMBOL_SIZE, SYMBOL_SIZE))
            # background color based on type
            if isinstance(sym, int):
                color = BLUE if sym <= 15 else GREEN if sym <= 30 else ORANGE
            else:
                color = PURPLE if sym == 'WILD' else YELLOW if sym == 'BONUS' else RED
            surf.fill((25,25,30))
            pygame.draw.rect(surf, color, surf.get_rect(), border_radius=14)
            txt = font.render(str(sym), True, WHITE)
            rect = txt.get_rect(center=(SYMBOL_SIZE//2, SYMBOL_SIZE//2))
            surf.blit(txt, rect)
            self.symbol_surfaces[sym] = surf

    def build_sounds(self):
        try:
            pygame.mixer.init()
            # Generate simple beep sounds
            self.sounds['spin'] = self.generate_tone(440, 0.08)
            self.sounds['stop'] = self.generate_tone(330, 0.08)
            self.sounds['win'] = self.generate_tone(880, 0.25)
            self.sounds['bonus'] = self.generate_tone(523, 0.3)
        except Exception:
            self.muted = True

    def generate_tone(self, freq, duration):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        volume = 64
        for i in range(n_samples):
            t = i / sample_rate
            val = int(volume * (1 if (int(freq * t * 2) % 2 == 0) else -1)) + 128  # square wave
            buf.append(val & 0xFF)
        sound = pygame.mixer.Sound(buffer=bytes(buf))
        return sound

    # ----------------------- Game Loop -------------------
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

    # ----------------------- Event Handling --------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_SPACE and self.state == GameState.READY:
                    self.start_spin()
                if event.key == pygame.K_UP:
                    self.bet = min(MAX_BET, self.bet + BET_STEP)
                if event.key == pygame.K_DOWN:
                    self.bet = max(MIN_BET, self.bet - BET_STEP)
                if event.key == pygame.K_b:
                    self.fast_mode = not self.fast_mode
                if event.key == pygame.K_m:
                    self.muted = not self.muted
                if event.key == pygame.K_r:
                    self.reset()
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                if event.key == pygame.K_l and self.state == GameState.READY and self.lotto_tickets > 0:
                    self.start_mini_lotto()

    # ----------------------- Spin Logic ------------------
    def start_spin(self):
        if self.free_spins > 0:
            self.free_spins -= 1
        else:
            if self.credits < self.bet:
                return
            self.credits -= self.bet
        self.state = GameState.SPINNING
        base = REEL_SPIN_TIME_BASE
        for i, reel in enumerate(self.reels):
            reel.spinning = True
            reel.spin_time = base + i * REEL_SPIN_TIME_INCREMENT
            if self.fast_mode:
                reel.spin_time *= FAST_MODE_FACTOR
            reel.time_accum = 0
        self.result_symbols = []
        self.last_win = 0
        self.play_sound('spin')

    def update(self, dt):
        if self.state == GameState.SPINNING:
            self.update_spinning(dt)
        elif self.state == GameState.MINI_LOTTO:
            self.update_mini_lotto(dt)
        # READY & RESULT no continuous logic

    def update_spinning(self, dt):
        all_stopped = True
        speed = 14 if self.fast_mode else 10
        for reel in self.reels:
            if reel.spinning:
                reel.time_accum += dt
                reel.offset += speed * dt * SYMBOL_SIZE
                if reel.offset >= SYMBOL_SIZE:
                    reel.offset -= SYMBOL_SIZE
                    reel.symbols.append(reel.symbols.pop(0))  # rotate
                if reel.time_accum >= reel.spin_time:
                    reel.spinning = False
                    reel.offset = 0
                    reel.result_index = 1  # center row after rotation
                    self.play_sound('stop')
            if reel.spinning:
                all_stopped = False
        if all_stopped:
            # collect results
            self.result_symbols = [reel.symbols[reel.result_index] for reel in self.reels]
            self.evaluate_spin()
            self.state = GameState.RESULT

    # ----------------------- Evaluation ------------------
    def evaluate_spin(self):
        result = self.result_symbols
        numbers = [s for s in result if isinstance(s, int) or s == 'WILD']
        specials = [s for s in result if isinstance(s, str)]
        win = 0
        # All wilds
        if len(result) == 5 and all(s == 'WILD' for s in result):
            win += PAYOUT_WILDS_ALL
        # of-a-kind (treat WILD as any matching number) - use frequency counts
        # Approach: try each number candidate by replacing WILD with that number
        base_numbers = [s for s in result if isinstance(s, int)]
        wild_count = result.count('WILD')
        from collections import Counter
        counts = Counter(base_numbers)
        # Try enhancing counts with wilds for best payout
        for num in list(counts.keys()) + ([None] if not base_numbers else []):
            c = counts[num] if num is not None else 0
            total = c + wild_count
            if total in PAYOUT_MATCH:
                win = max(win, PAYOUT_MATCH[total])
        # Sequential run detection (numbers only, substituting WILD flexibly) simplified:
        nums_sorted = sorted([n for n in result if isinstance(n, int)])
        if nums_sorted:
            best_seq = self.longest_consecutive(nums_sorted)
            if best_seq >= 3:
                win = max(win, best_seq * PAYOUT_SEQUENCE_PER_LENGTH)
        # Specials
        free_count = result.count('FREE')
        if free_count >= 3:
            self.free_spins += FREE_SPINS_AWARD
        bonus_count = result.count('BONUS')
        if bonus_count >= 1:
            self.lotto_tickets += bonus_count
            self.play_sound('bonus')
        if win > 0:
            win *= max(1, self.bet // MIN_BET)
            self.credits += win
            self.play_sound('win')
        self.last_win = win
        self.high_credits = max(self.high_credits, self.credits)

    def longest_consecutive(self, arr):
        # Standard longest consecutive sequence length
        s = set(arr)
        longest = 0
        for x in s:
            if x - 1 not in s:
                cur = x
                length = 1
                while cur + 1 in s:
                    cur += 1
                    length += 1
                longest = max(longest, length)
        return longest

    # ----------------------- Mini Lotto ------------------
    def start_mini_lotto(self):
        self.lotto_tickets -= 1
        self.state = GameState.MINI_LOTTO
        player_numbers = sorted(random.sample(range(1,46), 6))
        winning_numbers = sorted(random.sample(range(1,46), 7))  # last is bonus
        bonus_number = winning_numbers[-1]
        main_winning = winning_numbers[:-1]
        matches = len(set(player_numbers) & set(main_winning))
        bonus_hit = bonus_number in player_numbers
        payout = 0
        if matches == 5 and bonus_hit:
            payout = BONUS_MATCH_PAYOUT
        elif matches in LOTTO_PAYOUTS:
            payout = LOTTO_PAYOUTS[matches]
        self.credits += payout
        self.last_win = payout
        self.high_credits = max(self.high_credits, self.credits)
        self.mini_lotto_data = {
            'player': player_numbers,
            'winning': main_winning,
            'bonus': bonus_number,
            'matches': matches,
            'bonus_hit': bonus_hit,
            'payout': payout
        }
        # Immediately finish (display for a short time with update)
        self.mini_timer = 2.5

    def update_mini_lotto(self, dt):
        self.mini_timer -= dt
        if self.mini_timer <= 0:
            self.state = GameState.READY

    # ----------------------- Drawing ---------------------
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_reels()
        self.draw_ui()
        if self.state == GameState.MINI_LOTTO and self.mini_lotto_data:
            self.draw_mini_lotto_overlay()
        pygame.display.flip()

    def draw_reels(self):
        total_width = REEL_COUNT * SYMBOL_SIZE
        start_x = (WIDTH - total_width) // 2
        start_y = (HEIGHT - VISIBLE_ROWS * SYMBOL_SIZE) // 2
        for idx, reel in enumerate(self.reels):
            x = start_x + idx * SYMBOL_SIZE
            # draw 4 symbols to cover scrolling
            for row in range(VISIBLE_ROWS + 1):
                sym_index = (row) % len(reel.symbols)
                sym = reel.symbols[sym_index]
                y = start_y + row * SYMBOL_SIZE - reel.offset
                self.screen.blit(self.symbol_surfaces[sym], (x, y))
            # frame
            pygame.draw.rect(self.screen, GRAY, (x, start_y, SYMBOL_SIZE, SYMBOL_SIZE*VISIBLE_ROWS), 2, border_radius=8)
        # highlight center line
        cy = start_y + SYMBOL_SIZE
        pygame.draw.rect(self.screen, (250,250,250), (start_x-6, cy-4, total_width+12, SYMBOL_SIZE+8), 2, border_radius=10)

    def draw_ui(self):
        render_text(self.screen, f'Credits: {self.credits}', 28, WHITE, 20, 15)
        render_text(self.screen, f'Bet: {self.bet}', 28, YELLOW, 20, 50)
        render_text(self.screen, f'High: {self.high_credits}', 24, BLUE, 20, 85)
        render_text(self.screen, f'Free Spins: {self.free_spins}', 24, ORANGE, 20, 115)
        render_text(self.screen, f'Tickets: {self.lotto_tickets}', 24, PURPLE, 20, 145)
        if self.last_win > 0:
            render_text(self.screen, f'Won: {self.last_win}', 34, GREEN, WIDTH-200, 20)
        if self.state == GameState.READY:
            render_text(self.screen, 'SPACE=Spin  UP/DOWN=Bet  B=Fast  L=MiniLotto  M=Mute  R=Reset', 20, WHITE, WIDTH//2, HEIGHT-30, center=True)
        if self.state == GameState.SPINNING:
            render_text(self.screen, 'Spinning...', 32, WHITE, WIDTH//2, 30, center=True)
        if self.state == GameState.RESULT and self.last_win == 0:
            render_text(self.screen, 'No Win', 32, RED, WIDTH//2, 30, center=True)

    def draw_mini_lotto_overlay(self):
        data = self.mini_lotto_data
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay, (0,0))
        render_text(self.screen, 'MINI LOTTO RESULT', 40, YELLOW, WIDTH//2, 80, center=True)
        render_text(self.screen, f'Player: {data['player']}', 28, WHITE, WIDTH//2, 140, center=True)
        render_text(self.screen, f'Winning: {data['winning']} + Bonus {data['bonus']}', 28, ORANGE, WIDTH//2, 180, center=True)
        render_text(self.screen, f'Matches: {data['matches']}  BonusHit: {data['bonus_hit']}', 28, WHITE, WIDTH//2, 220, center=True)
        render_text(self.screen, f'Payout: {data['payout']}', 34, GREEN if data['payout']>0 else RED, WIDTH//2, 270, center=True)
        render_text(self.screen, 'Closing...', 24, GRAY, WIDTH//2, 320, center=True)

    # ----------------------- Helpers ---------------------
    def play_sound(self, key):
        if self.muted: return
        s = self.sounds.get(key)
        if s: s.play()

    def reset(self):
        self.credits = START_CREDITS
        self.bet = MIN_BET
        self.free_spins = 0
        self.lotto_tickets = 0
        self.last_win = 0
        self.state = GameState.READY

# --------------------------- Main Entry -----------------------------
if __name__ == '__main__':
    game = SlotMachine()
    game.run()
