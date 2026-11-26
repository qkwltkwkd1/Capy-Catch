import time

from hardware.lcd import LCD
from hardware.joystick import Joystick

from game.logic import GameLogic
from game.renderer import Renderer


def main():
    # 게임 로직 초기화
    logic = GameLogic()

    # 렌더러 초기화
    renderer = Renderer()

    # LCD 초기화
    lcd = LCD()

    try:
        # 조이스틱 초기화
        joystick = Joystick()

        try:
            # 이전 버튼 입력 상태
            previous = []

            # 시작 화면 출력
            lcd.show(renderer.draw_menu(logic.theme))

            print("CAPY-CATCH 시작!")

            while True:
                # 현재 시간 확인
                now = time.monotonic()

                # 현재 눌린 버튼 확인
                pressed = joystick.read()

                # 새롭게 눌린 버튼만 저장
                new_pressed = []

                for button in pressed:
                    if button not in previous:
                        new_pressed.append(button)

                # 현재 입력 상태 저장
                previous = pressed

                # 1. 테마 선택 화면
                if logic.state == "menu":
                    # 이동하기 전의 테마 번호
                    old_theme = logic.theme

                    # 위쪽 이동
                    if "UP" in new_pressed:
                        if logic.theme >= 2:
                            logic.theme -= 2

                    # 아래쪽 이동
                    elif "DOWN" in new_pressed:
                        if logic.theme < 2:
                            logic.theme += 2

                    # 왼쪽 이동
                    elif "LEFT" in new_pressed:
                        if logic.theme % 2 == 1:
                            logic.theme -= 1

                    # 오른쪽 이동
                    elif "RIGHT" in new_pressed:
                        if logic.theme % 2 == 0:
                            logic.theme += 1

                    # 테마가 변경되었을 때 화면 갱신
                    if old_theme != logic.theme:
                        image = renderer.draw_menu(
                            logic.theme
                        )

                        lcd.show(image)

                    # A 버튼으로 게임 시작
                    if "A" in new_pressed:
                        logic.start_game()

                        image = renderer.draw_game(logic)
                        lcd.show(image)

                        print("게임 시작!")

                # 2. 게임 진행 화면
                elif logic.state == "playing":
                    # 변경 전 게임 상태 저장
                    old_cursor = logic.cursor
                    old_score = logic.score
                    old_mole = logic.mole_position

                    # 조이스틱 방향 입력 처리
                    if "UP" in new_pressed:
                        logic.move_cursor("UP")

                    elif "DOWN" in new_pressed:
                        logic.move_cursor("DOWN")

                    elif "LEFT" in new_pressed:
                        logic.move_cursor("LEFT")

                    elif "RIGHT" in new_pressed:
                        logic.move_cursor("RIGHT")

                    # A 버튼으로 공격
                    if "A" in new_pressed:
                        logic.hit(now)

                    # 카피바라 등장 및 제거 처리
                    logic.update(now)

                    # 게임 상태가 변경되었는지 확인
                    if (
                        old_cursor != logic.cursor
                        or old_score != logic.score
                        or old_mole != logic.mole_position
                    ):
                        # 변경된 게임 화면 출력
                        image = renderer.draw_game(logic)
                        lcd.show(image)

                # 50ms 간격으로 입력 확인
                time.sleep(0.05)

        finally:
            joystick.cleanup()

    except KeyboardInterrupt:
        print("게임 종료")

    finally:
        lcd.cleanup()


if __name__ == "__main__":
    main()