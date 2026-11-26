import random
import time

from game.config import (
    GRID_SIZE,
    MOLE_DURATION,
    SPAWN_DELAY,
    NORMAL_SCORE
)


class GameLogic:
    def __init__(self):
        # 처음 선택된 배경 테마
        self.theme = 0

        # 게임 상태
        self.state = "menu"

        # 현재 점수
        self.score = 0

        # 현재 커서 위치
        self.cursor = 0

        # 카피바라 위치: None이면 등장한 카피바라가 없음
        self.mole_position = None

        # 카피바라 등장 시간
        self.spawn_time = 0.0

        # 다음 카피바라 등장 예정 시간
        self.next_spawn_time = 0.0

    # 게임 시작
    def start_game(self):
        self.state = "playing"
        self.score = 0
        self.cursor = 0

        # 기존 카피바라 제거
        self.mole_position = None

        # 게임 시작 후 0.5초 뒤에 등장
        self.next_spawn_time = (
            time.monotonic() + SPAWN_DELAY
        )

    # 커서 이동
    def move_cursor(self, direction):
        # 현재 커서의 행과 열 계산
        row = self.cursor // GRID_SIZE
        col = self.cursor % GRID_SIZE

        # 위쪽 이동
        if direction == "UP":
            if row > 0:
                row -= 1

        # 아래쪽 이동
        elif direction == "DOWN":
            if row < GRID_SIZE - 1:
                row += 1

        # 왼쪽 이동
        elif direction == "LEFT":
            if col > 0:
                col -= 1

        # 오른쪽 이동
        elif direction == "RIGHT":
            if col < GRID_SIZE - 1:
                col += 1

        # 행과 열을 다시 커서 번호로 변환
        self.cursor = row * GRID_SIZE + col

    # 카피바라 등장
    def spawn_mole(self, now):
        # 전체 구멍 개수
        total_holes = GRID_SIZE * GRID_SIZE

        # 무작위 구멍 선택
        self.mole_position = random.randint(
            0, total_holes - 1
        )

        # 등장한 시간 저장
        self.spawn_time = now

    # 카피바라 제거
    def remove_mole(self, now):
        self.mole_position = None

        # 다음 카피바라 등장 시간 설정
        self.next_spawn_time = now + SPAWN_DELAY

    # 공격 판정
    def hit(self, now):
        # 등장한 카피바라가 없는 경우
        if self.mole_position is None:
            return

        # 이미 등장 유지시간이 지난 경우
        if now - self.spawn_time >= MOLE_DURATION:
            self.remove_mole(now)
            return

        # 커서와 카피바라 위치가 같은 경우
        if self.cursor == self.mole_position:
            self.score += NORMAL_SCORE

            # 잡은 카피바라 제거
            self.remove_mole(now)

            print(f"공격 성공! 현재 점수: {self.score}")

    # 게임 상태 갱신
    def update(self, now):
        # 게임 중이 아니면 실행하지 않음
        if self.state != "playing":
            return

        # 카피바라가 등장해 있는 경우
        if self.mole_position is not None:
            elapsed_time = now - self.spawn_time

            # 등장 유지시간이 지나면 제거
            if elapsed_time >= MOLE_DURATION:
                self.remove_mole(now)

        # 카피바라가 없는 경우
        else:
            # 다음 등장 시간이 되었는지 확인
            if now >= self.next_spawn_time:
                self.spawn_mole(now)