import pygame
import sys
import threading
from random import randint
from pathlib import Path

# -------------------------------------------------------
# 설정값 (절대 경로로 고정)
# -------------------------------------------------------
BASE_PATH = Path(r"D:\game")
MAP_FILE = BASE_PATH / "A.png"     # 배경 맵 이미지 파일
GOKU_FILE = BASE_PATH / "b.png"    # 손오공 아이콘 파일
ROOM_FILE = BASE_PATH / "room.png" # 게임방 아이콘 파일

SPEED = 280
RUN_MULT = 1.8
START_POS = "center"   # "center" 또는 "bottom_center"

# room.png 위치 (위에서 약 4cm ≈ 150px 내려서 배치)
ROOM_SIZE = (120, 100)
ROOM_POS = (30, 180)


# -------------------------------------------------------
# 터미널(콘솔)에서 동작하는 아주 간단한 미니게임
# -------------------------------------------------------
def terminal_minigame():
  
            print("테스트")


def main():
    pygame.init()
    pygame.display.set_caption("Map 이동 데모 (A.png + b.png + room.png)")

    # ---------------------------------------------------
    # 맵 로드 및 화면 초기화
    # ---------------------------------------------------
    map_img_raw = pygame.image.load(str(MAP_FILE))
    map_w, map_h = map_img_raw.get_width(), map_img_raw.get_height()
    screen = pygame.display.set_mode((map_w, map_h))
    map_img = map_img_raw.convert()

    # ---------------------------------------------------
    # 손오공 로드
    # ---------------------------------------------------
    goku_img_raw = pygame.image.load(str(GOKU_FILE)).convert_alpha()
    target_h = max(32, int(map_h * 0.10))  # 맵 높이의 10%
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

    # ---------------------------------------------------
    # 게임방(room.png) 로드
    # ---------------------------------------------------
    room_img_raw = pygame.image.load(str(ROOM_FILE)).convert_alpha()
    room_img = pygame.transform.smoothscale(room_img_raw, ROOM_SIZE)
    room_rect = room_img.get_rect()
    room_rect.topleft = ROOM_POS

    # 문 앞 충돌 영역(집 하단 중앙 부분)
    door_rect = pygame.Rect(
        room_rect.centerx - 20,
        room_rect.bottom - 15,
        40,
        15
    )

    # ---------------------------------------------------
    # 메인 루프
    # ---------------------------------------------------
    clock = pygame.time.Clock()
    running = True
    mini_thread = None

    print("프로그램 시작: 손오공을 화살표/WASD로 움직이세요. room.png 앞에 닿으면 터미널에서 게임 시작!")

    while running:
        dt = clock.tick(120) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # 이동 처리
        keys = pygame.key.get_pressed()
        mul = RUN_MULT if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 1.0
        vx = vy = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx -= SPEED * mul
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx += SPEED * mul
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vy -= SPEED * mul
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vy += SPEED * mul

        goku_rect.x += int(vx * dt)
        goku_rect.y += int(vy * dt)
        goku_rect.clamp_ip(screen.get_rect())

        # 손오공이 문 앞에 닿으면 터미널 미니게임을 스레드로 실행
        if goku_rect.colliderect(door_rect):
            if mini_thread is None or not mini_thread.is_alive():
                print("\n[알림] 손오공이 room.png 앞에 도착했습니다. 터미널에서 미니게임이 시작됩니다!")
                mini_thread = threading.Thread(target=terminal_minigame, daemon=True)
                mini_thread.start()

        # 화면 그리기
        screen.blit(map_img, (0, 0))
        screen.blit(room_img, room_rect)
        # pygame.draw.rect(screen, (255, 0, 0), door_rect, 1)  # 충돌 영역 확인용
        screen.blit(goku_img, goku_rect)
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
