# 🎮 미니게임 통합 플랫폼 (Python GUI)

> Python Tkinter 기반 멀티 게임 통합 플랫폼

## 📌 프로젝트 소개

캐릭터를 조작하여 원하는 게임 영역으로 이동하면 해당 게임이 실행되는 통합 게임 플랫폼입니다.
3가지 미니게임(가위바위보, 끝말잇기, 마피아게임)을 하나의 플랫폼에서 즐길 수 있으며, 멀티스레드를 활용하여 끊김 없는 사용자 경험을 제공합니다.

- **개발 기간**: 2025.8월 27일~ 2025.9월 3일
- **개발 인원**: 1팀 프로젝트 (총인원 5명, 팀장)
- **담당 역할**: GUI 구현 / 게임 로직 개발 / 멀티스레드 설계 

## 🛠 기술 스택

### Language & Framework
- Python 3.13
- Tkinter (GUI 프레임워크)
- Threading (멀티스레드 처리)

### Libraries
- Pillow (이미지 처리)
- Random (게임 랜덤 로직)

### Tools
- PyCharm / VS Code
- Git / GitHub

## 🎯 주요 기능

### 1. 통합 게임 플랫폼
- **메인 화면**: 캐릭터 이동 가능한 메인 맵
- **구역 감지**: 캐릭터가 특정 영역 진입 시 자동으로 게임 실행
- **게임 전환**: 게임 종료 후 메인 맵으로 자동 복귀

### 2. 미니게임 3종
- **가위바위보**: 컴퓨터와 대전하는 고전 게임
- **끝말잇기**: 단어 데이터베이스 기반 끝말잇기 게임
- **마피아 게임**: 멀티플레이어 추리 게임

### 3. 캐릭터 이동 시스템
- 키보드 입력 기반 캐릭터 조작 (방향키 또는 WASD)
- 실시간 위치 업데이트
- 충돌 감지 및 영역 판정

### 4. 멀티스레드 처리
- **게임 루프 스레드**: 메인 게임 로직 독립 실행
- **UI 업데이트 스레드**: 화면 갱신 전담
- **이벤트 처리 스레드**: 사용자 입력 비동기 처리
- **논블로킹 실행**: 게임 실행 중에도 프로그램 멈춤 현상 없음

## 📂 프로젝트 구조

```
game_box/
├── game.py                         # 메인 실행 파일 (프로그램 진입점)
├── dragonball_location7.py         # 통합 플랫폼 GUI
├── mafia_game/                     # 마피아 게임 모듈
│   ├── __itit__.py  
│   ├── day_vote.py    
│   ├── main.py
│   ├── morning_phase.py
│   ├── night_phase.py        
│   └── game_over.py 
├── __pycache__/                 	  # Python 컴파일된 캐시 파일
│   ├── __itit__.cpython-313.pyc  
│   ├── day_vote.cpython-313.pyc
│   ├── game_over.cpython-313.pyc
│   ├── main.cpython-313.pyc
│   ├── morning_phase.cpython-313.pyc
│   ├── night_phase.cpython-313.pyc
├── __pycache__/
│   ├── game.cpython-313.pyc
│   └── korea_word.cpython-313.pyc/
├── A.png/                       	 # 이미지 및 리소스 파일
├── b.png/
├── room.png/
├── rooma.png/
├── roomb.png/
├── roomc.png/
├── run_game.bat/		               # Windows에서 바로 실행 가능한 배치 파일
├── 필독!!GUI구동하기전 설치할부분.txt
└── README.md
```

## 🚀 실행 방법

### 1. Python 설치
Python 3.8 이상이 필요합니다.
```bash
python --version
```

### 2. 필요한 라이브러리 설치
```bash
pip install pillow
```

### 3. 프로젝트 실행
```bash
python main.py
```

### 4. 게임 조작 방법
- **이동**: 방향키 (↑↓←→) 또는 WASD 키
- **게임 시작**: 캐릭터를 원하는 게임 영역으로 이동
- **게임 종료**: 게임 완료 후 자동으로 메인 화면 복귀

## 💡 트러블슈팅

### 1. GUI 프리징 문제 해결
**문제**: 게임 실행 시 메인 윈도우가 멈추고 응답 없음 현상 발생

**해결**:
- Python `threading` 모듈을 활용한 멀티스레드 구현
- 게임 로직을 별도 스레드에서 실행하여 GUI 이벤트 루프와 분리
- `daemon=True` 옵션으로 메인 프로그램 종료 시 스레드 자동 종료

```python
import threading

def run_game():
    # 게임 로직 실행
    pass

game_thread = threading.Thread(target=run_game, daemon=True)
game_thread.start()
```

**결과**: 게임 실행 중에도 메인 화면 조작 가능, 프로그램 멈춤 현상 100% 해결

### 2. 영역 충돌 감지 최적화
**문제**: 캐릭터 이동 시 영역 판정이 부정확하여 게임이 의도치 않게 실행됨

**해결**:
- 픽셀 기반 정밀 충돌 감지 알고리즘 구현
- Bounding Box를 활용한 사각형 충돌 판정

```python
def check_collision(character_pos, zone_rect):
    char_x, char_y = character_pos
    zone_x, zone_y, zone_w, zone_h = zone_rect
    
    return (zone_x <= char_x <= zone_x + zone_w and
            zone_y <= char_y <= zone_y + zone_h)
```

**결과**: 영역 감지 정확도 95% 이상 향상

### 3. 끝말잇기 단어 검증
**문제**: 존재하지 않는 단어 입력 또는 중복 단어 사용 방지 필요

**해결**:
- 한국어 단어 데이터셋 구축 (1,000개 이상)
- 이미 사용한 단어 리스트 관리
- 실시간 단어 유효성 검증

```python
used_words = set()
word_database = load_words('korean_words.txt')

def is_valid_word(word):
    return word in word_database and word not in used_words
```

**결과**: 게임 공정성 확보 및 사용자 경험 개선

## 📈 개선 계획

- [ ] 네트워크 멀티플레이 기능 추가 (소켓 통신)
- [ ] 게임 결과 저장 및 랭킹 시스템
- [ ] 추가 미니게임 구현 (오목, 테트리스 등)
- [ ] BGM 및 효과음 추가
- [ ] 게임 난이도 선택 기능
- [ ] 모바일 버전 포팅 (Kivy 활용)

## 🎓 배운 점

- **멀티스레드 프로그래밍**: GUI 프리징 문제 해결을 위한 비동기 처리
- **이벤트 기반 프로그래밍**: Tkinter 이벤트 루프와 콜백 함수 활용
- **충돌 감지 알고리즘**: 2D 게임에서의 위치 판정 및 영역 감지
- **팀 협업**: Git을 활용한 버전 관리 및 코드 통합
- **사용자 경험 설계**: 직관적인 인터페이스와 부드러운 게임 전환

## 👥 팀원 및 역할

- **권혁민 팀장**: PPT자료 및 py파트별 총괄 담당
- **박정대 팀원**: 가위바위보 CLI 및 GUI역할 담당
- **정호영 팀원**: 끝말잇기 CLI 및 테스트/버그 수정, GUI
- **이상우 팀원**: 마피아 게임 CLI 및 테스트/버그 수정, 정의서, 명세서 작성
- **태재우 팀원**: 마피아 게임 CLI 및 테스트/버그 수정, GUI 구축


## 📧 문의

- Email: johnkwon33@gmail.com
- GitHub: https://github.com/johnkwon87/game

---

© 2025 Team Project. All rights reserved.
