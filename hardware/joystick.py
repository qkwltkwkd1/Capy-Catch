import time
import board
import digitalio


# 조이스틱 및 버튼 GPIO 핀 설정
PINS = {
    "UP": board.D17,
    "DOWN": board.D22,
    "LEFT": board.D27,
    "RIGHT": board.D23,
    "CENTER": board.D4,
    "A": board.D5,
    "B": board.D6
}


class Joystick:
    def __init__(self):
        # 입력 핀을 저장할 딕셔너리
        self.buttons = {}

        # 각 GPIO 핀을 입력 모드로 설정
        try:
            for name, pin in PINS.items():
                button = digitalio.DigitalInOut(pin)
                self.buttons[name] = button

                button.direction = digitalio.Direction.INPUT
                button.pull = digitalio.Pull.UP

        except Exception:
            self.cleanup()
            raise

    # 현재 눌린 버튼 확인
    def read(self):
        pressed = []

        for name, button in self.buttons.items():
            if not button.value:
                pressed.append(name)

        return pressed

    # GPIO 자원 정리
    def cleanup(self):
        for button in self.buttons.values():
            button.deinit()

        self.buttons.clear()


# 조이스틱 및 버튼 입력 테스트
if __name__ == "__main__":
    joystick = Joystick()

    try:
        previous = []

        while True:
            pressed = joystick.read()

            # 입력 상태가 변경되었을 때만 출력
            if pressed != previous:
                if pressed:
                    print("입력:", pressed)

                previous = pressed

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("입력 테스트 종료")

    finally:
        joystick.cleanup()