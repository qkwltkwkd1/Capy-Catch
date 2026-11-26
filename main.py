import time

from hardware.lcd import LCD
from hardware.joystick import Joystick
from game.renderer import Renderer

def main():
    # 렌더러 초기화
    renderer = Renderer()

    # LCD 초기화
    lcd = LCD()

    try:
        # 조이스틱 초기화
        joystick = Joystick()

        try:
            # 처음 선택된 테마
            selected_theme = 0

            # 이전 버튼 입력 상태
            previous = []

            # 시작 화면 표시
            lcd.show(renderer.draw_menu(selected_theme))

            print("CAPY-CATCH 시작!")

            while True:
                # 현재 눌린 버튼 확인
                pressed = joystick.read()

                # 새롭게 눌린 버튼만 저장
                new_pressed = []

                for button in pressed:
                    if button not in previous:
                        new_pressed.append(button)

                # 이동하기 전의 테마 번호 저장
                old_theme = selected_theme

                # 위쪽 이동
                if "UP" in new_pressed:
                    if selected_theme >= 2:
                        selected_theme -= 2

                # 아래쪽 이동
                elif "DOWN" in new_pressed:
                    if selected_theme < 2:
                        selected_theme += 2

                # 왼쪽 이동
                elif "LEFT" in new_pressed:
                    if selected_theme % 2 == 1:
                        selected_theme -= 1

                # 오른쪽 이동
                elif "RIGHT" in new_pressed:
                    if selected_theme % 2 == 0:
                        selected_theme += 1

                # 테마가 변경됐을 때 화면 갱신
                if old_theme != selected_theme:
                    image = renderer.draw_menu(selected_theme)
                    lcd.show(image)

                # 선택 버튼 눌림
                if "A" in new_pressed:
                    image = renderer.draw_background(selected_theme)
                    lcd.show(image)
                    print(f"선택된 테마: {selected_theme}")
                    break

                # 현재 입력 상태 저장
                previous = pressed

                # 50ms 간격으로 입력 확인
                time.sleep(0.05)

            # 선택한 배경 유지
            while True:
                time.sleep(0.1)

        finally:
            joystick.cleanup()

    except KeyboardInterrupt:
        print("게임 종료")

    finally:
        lcd.cleanup()

if __name__ == "__main__":
    main()