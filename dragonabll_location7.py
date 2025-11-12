
import pygame
import sys
import threading
import time
import random
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from random import randint, choice

API_KEY = "267281338A8C7B83636DD8BC6660150F"
BASE_URL = "https://krdict.korean.go.kr/api/search"

# -------------------------------------------------------
# 설정값 (d:/game 하위 파일 경로)
# -------------------------------------------------------
MAP_FILE   = "d:/game/A.png"       # 배경 맵 이미지 파일
GOKU_FILE  = "d:/game/b.png"       # 손오공 아이콘 파일
ROOMa_FILE = "d:/game/rooma.png"   # 게임방 A 아이콘 파일
ROOMb_FILE = "d:/game/roomb.png"   # 게임방 B 아이콘 파일
ROOMc_FILE = "d:/game/roomc.png"   # 게임방 C 아이콘 파일

SPEED = 280
RUN_MULT = 1.8
START_POS = "center"  # "center" or "bottom_center"

# -------------------------------------------------------
# 집(방) 크기/위치
# (1cm ≈ 37px 가정)
# - B: (210,180) → (395, 69)
# - C: (585,900) → (770,826)
# -------------------------------------------------------
ROOMa_SIZE = (120, 100)
ROOMa_POS  = (30,  180)

ROOMb_SIZE = (120, 100)
ROOMb_POS  = (395, 69)

ROOMc_SIZE = (140, 110)
ROOMc_POS  = (770, 826)

# -------------------------------------------------------
# 콘솔 미니게임들
# -------------------------------------------------------
def game1_number_guess():
    print("가위 바위 보 게임")

    # 0 -> "가위", 1 -> "바위", 2 -> "보"
    choices = ["가위", "바위", "보"]
    win_conditions = {("가위", "보"), ("바위", "가위"), ("보", "바위")}

    while True:
        print("\n무엇을 내시겠어요?")
        print(" 1. 가위")
        print(" 2. 바위")
        print(" 3. 보")
        print(" 0. 나가기")

        user_input = input("번호 입력: ").strip()

        if user_input == "0":
            print("집에서 나갑니다.\n")
            return

        if user_input not in ("1", "2", "3"):
            print("잘못 입력했습니다. 1, 2, 3, 0 중에서 선택하세요.")
            continue

        user_idx = int(user_input) - 1
        user_choice = choices[user_idx]
        comp_choice = random.choice(choices)

        print(f"당신: {user_choice} | 컴퓨터: {comp_choice}")

        if user_choice == comp_choice:
            print("결과: 무승부!\n")
        elif (user_choice, comp_choice) in win_conditions:
            print("결과: 당신이 이겼습니다!\n")
        else:
            print("결과: 컴퓨터가 이겼습니다!\n")


def game2_rps():
    # 끝말잇기 실행
    play_game()


# 두음 법칙 대응 맵
INITIAL_SOUND_RULE = {
    "ㄹ": ["ㄴ", "ㄹ", "ㅇ"],
    "ㄴ": ["ㄴ", "ㅇ"],
    "ㅁ": ["ㅁ"],
    "ㅇ": ["ㅇ"],
    "ㄱ": ["ㄱ"],
    "ㄷ": ["ㄷ"],
    "ㅂ": ["ㅂ"],
    "ㅅ": ["ㅅ"],
    "ㅈ": ["ㅈ"],
    "ㅊ": ["ㅊ"],
    "ㅋ": ["ㅋ"],
    "ㅌ": ["ㅌ"],
    "ㅍ": ["ㅍ"],
    "ㅎ": ["ㅎ"],
}

def adjust_initial_sound(char):
    """두음 법칙 적용"""
    return INITIAL_SOUND_RULE.get(char, [char])

def get_three_syllable_nouns(start_char, num=50):
    """start_char로 시작하는 3음절 명사 단어만 가져오기"""
    query_params = {
        "key": API_KEY,
        "q": start_char,
        "part": "word",
        "sort": "popular",
        "num": num
    }
    url = BASE_URL + "?" + urllib.parse.urlencode(query_params)
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
    except Exception as e:
        print("⚠️ API 요청 실패", e)
        return []

    root = ET.fromstring(data)
    words = []
    for item in root.findall("item"):
        word = item.find("word").text
        pos = item.find("pos").text if item.find("pos") is not None else ""
        if word and len(word) == 3 and ("명사" in pos or "N" in pos):
            # 두음 법칙 대응
            for adj in adjust_initial_sound(word[0]):
                if adj == start_char:
                    words.append(word)
    return words

def is_valid_word(word):
    """해당 단어가 3음절 명사인지 API에서 확인"""
    if not word or len(word) != 3:
        return False
    query_params = {
        "key": API_KEY,
        "q": word,
        "part": "word",
        "sort": "popular",
        "num": 10
    }
    url = BASE_URL + "?" + urllib.parse.urlencode(query_params)
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
    except Exception as e:
        print("⚠️ API 요청 실패", e)
        return False

    root = ET.fromstring(data)
    for item in root.findall("item"):
        api_word = item.find("word").text
        pos = item.find("pos").text if item.find("pos") is not None else ""
        if api_word == word and ("명사" in pos or "N" in pos):
            return True
    return False

def input_with_timeout(prompt, timeout=10):
    result = [None]
    input_done = threading.Event()

    def inner():
        try:
            print(prompt, end="", flush=True)
            result[0] = input()
        except Exception:
            result[0] = None
        input_done.set()

    t = threading.Thread(target=inner)
    t.daemon = True
    t.start()

    sys.stdout.write(f"\n┌───────────────────────────────┐\n")
    sys.stdout.write(f"│ ⏳ 제한 시간 : {timeout:2d}초           │\n")
    sys.stdout.write(f"├───────────────────────────────┤\n")
    sys.stdout.flush()

    for remain in range(timeout, 0, -1):
        if input_done.is_set():
            break
        sys.stdout.write(f"\r│ ⏳ 남은 시간 : {remain:2d}초           │")
        sys.stdout.flush()
        time.sleep(1)

    print()
    if not input_done.is_set():
        print("\n└───────────────────────────────┘")
        print("⏰ Time Over!!!")
        return None
    print("└───────────────────────────────┘")
    return result[0]

def play_game():
    print("=== 끝말잇기 ===")
    print("3음절 단어 입력!!!")
    print("10초 내 입력!!!")
    print("게임 시작!\n")
    print("(언제든 q 입력으로 종료)")

    used_words = set()
    user_word = input_with_timeout("단어 입력 : ", 10)
    if user_word is None:
        return
    user_word = user_word.strip()

    # 추가: 첫 입력에서 q 종료
    if user_word.lower() == "q":
        print("게임을 종료합니다.")
        return

    while True:
        # 추가: 루프 진입 시 q 종료
        if user_word.lower() == "q":
            print("게임을 종료합니다.")
            return

        if len(user_word) != 3:
            print("⚠️ 3음절 단어만 입력하세요!")
            user_word = input_with_timeout("다시 입력 : ", 10)
            if user_word is None:
                break
            user_word = user_word.strip()
            continue

        if user_word in used_words:
            print("⚠️ 이미 사용한 단어입니다! 당신의 패배!")
            break

        if not is_valid_word(user_word):
            print(f"❌ '{user_word}'는(은) 사전에 없는 단어입니다! 당신의 패배!")
            break

        used_words.add(user_word)
        last_char = user_word[-1]

        candidates = [w for w in get_three_syllable_nouns(last_char) if w not in used_words]

        if not candidates:
            print(f"💥 '{last_char}'(으)로 시작하는 3음절 명사가 없습니다. 당신의 승리!")
            break

        computer_word = random.choice(candidates)
        if not is_valid_word(computer_word):
            print(f"🤖 컴퓨터가 '{computer_word}'를 냈지만, 사전에 없는 단어입니다. 당신의 승리!")
            break

        used_words.add(computer_word)
        time.sleep(1)
        print(f"🤖 컴퓨터 : {computer_word}")

        user_word = input_with_timeout("단어 입력 : ", 10)
        if user_word is None:
            break
        user_word = user_word.strip()

def game3_math_quiz():
    print("\n[게임3] 산수 퀴즈 3문제! (q 종료)")
    # 필요시 구현 추가

# -------------------------------------------------------
# 메인
# -------------------------------------------------------
def main():
    pygame.init()
    pygame.display.set_caption("Map 이동 (A.png + b.png + rooma/b/c.png)")

    # 맵 로드 및 화면 초기화
    map_img_raw = pygame.image.load(MAP_FILE)
    map_w, map_h = map_img_raw.get_width(), map_img_raw.get_height()
    screen = pygame.display.set_mode((map_w, map_h))
    map_img = map_img_raw.convert()

    # 손오공 로드 + 스케일
    goku_img_raw = pygame.image.load(GOKU_FILE).convert_alpha()
    target_h = max(32, int(map_h * 0.10))
    scale_ratio = target_h / goku_img_raw.get_height()
    goku_img = pygame.transform.smoothscale(
        goku_img_raw,
        (int(goku_img_raw.get_width() * scale_ratio), target_h)
    )
    goku_rect = goku_img.get_rect()
    if START_POS == "bottom_center":
        goku_rect.midbottom = (map_w // 2, map_h - 10)
    else:
        goku_rect.center = (map_w // 2, map_h // 2)

    # 디버그: F1로 문(door) 사각형 표시 토글
    debug_doors = False

    # 방 세팅 (inside/started 상태 포함: 재입장 시 재실행)
    rooms = []

    def clamp_room_pos(rect):
        """room rect가 화면 밖으로 나가지 않도록 보정"""
        changed = False
        if rect.right > map_w:
            rect.x = max(0, map_w - rect.width)
            changed = True
        if rect.bottom > map_h:
            rect.y = max(0, map_h - rect.height)
            changed = True
        if rect.x < 0:
            rect.x = 0
            changed = True
        if rect.y < 0:
            rect.y = 0
            changed = True
        return changed

    def compute_door(rect):
        """rect 기준으로 문(집 하단 중앙) 충돌 박스 재계산"""
        return pygame.Rect(rect.centerx - 22, rect.bottom - 16, 44, 16)

    def add_room(img_path, size, pos, label, game_func):
        img = pygame.image.load(img_path).convert_alpha()
        img = pygame.transform.smoothscale(img, size)
        rect = img.get_rect()
        rect.topleft = pos

        # 화면 밖이면 안쪽으로 클램프
        changed = clamp_room_pos(rect)
        if changed:
            print(f"[주의] room{label}가 화면 밖이라 위치 보정 -> {rect.topleft}")

        door = compute_door(rect)

        rooms.append({
            "label": label,     # 'A','B','C'
            "img": img,
            "rect": rect,
            "door": door,
            "game": game_func,
            "inside": False,    # 현재 문 안에 있는가?
            "started": False    # 이번 입장 사이클에서 이미 게임 실행했는가?
        })

    add_room(ROOMa_FILE, ROOMa_SIZE, ROOMa_POS, 'A', game1_number_guess)
    add_room(ROOMb_FILE, ROOMb_SIZE, ROOMb_POS, 'B', game2_rps)
    add_room(ROOMc_FILE, ROOMc_SIZE, ROOMc_POS, 'C', game3_math_quiz)

    clock = pygame.time.Clock()
    running = True

    # 한 번에 하나의 게임만 돌도록 관리
    active_thread = None

    print("손오공을 화살표/WASD로 움직이세요.")
    print("roomA→게임1, roomB→게임2(끝말잇기, q로 종료), roomC→게임3")
    print("F1: 문(door) 박스 디버그 표시 토글")

    while running:
        dt = clock.tick(120) / 1000.0

        # 이벤트
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F1:
                    debug_doors = not debug_doors

        # 이동
        keys = pygame.key.get_pressed()
        mul = RUN_MULT if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else 1.0
        vx = vy = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: vx -= SPEED * mul
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: vx += SPEED * mul
        if keys[pygame.K_UP] or keys[pygame.K_w]: vy -= SPEED * mul
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: vy += SPEED * mul

        goku_rect.x += int(vx * dt)
        goku_rect.y += int(vy * dt)
        goku_rect.clamp_ip(screen.get_rect())

        # 각 방에 대해 "진입/이탈" 이벤트 감지
        for r in rooms:
            now_inside = goku_rect.colliderect(r["door"])

            # 1) 방 "진입" 이벤트
            if now_inside and not r["inside"]:
                if (active_thread is None) or (not active_thread.is_alive()):
                    if not r["started"]:
                        print(f"\n[알림] room{r['label']} 문 앞 진입 -> 해당 게임 시작!")
                        active_thread = threading.Thread(target=r["game"], daemon=True)
                        active_thread.start()
                        r["started"] = True
                r["inside"] = True

            # 2) 방 "이탈" 이벤트
            elif (not now_inside) and r["inside"]:
                r["inside"] = False
                r["started"] = False  # 다음에 다시 들어오면 재실행

        # 화면 그리기
        screen.blit(map_img, (0, 0))
        for r in rooms:
            screen.blit(r["img"], r["rect"])
            if debug_doors:
                pygame.draw.rect(screen, (255, 0, 0), r["door"], 1)
        screen.blit(goku_img, goku_rect)
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
