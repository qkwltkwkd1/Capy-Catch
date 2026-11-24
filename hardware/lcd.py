import time
import board
import busio
import digitalio

from pathlib import Path
from PIL import Image
from adafruit_rgb_display import st7789


class LCD:
    def __init__(self):
        # 초기화된 자원 관리
        self.spi = None
        self.cs = None
        self.dc = None
        self.rst = None
        self.bl = None

        try:
            # SPI 통신 설정
            self.spi = busio.SPI(
                board.SCK,
                MOSI=board.MOSI
            )

            # GPIO 핀 설정
            self.cs = digitalio.DigitalInOut(board.CE0)
            self.dc = digitalio.DigitalInOut(board.D25)
            self.rst = digitalio.DigitalInOut(board.D24)

            # 백라이트 설정
            self.bl = digitalio.DigitalInOut(board.D26)
            self.bl.switch_to_output(value=True)

            # LCD 초기화
            self.display = st7789.ST7789(
                self.spi,
                cs=self.cs,
                dc=self.dc,
                rst=self.rst,
                width=240,
                height=240,
                rotation=180,
                y_offset=80,
                baudrate=24000000
            )

        except BaseException:
            self.cleanup()
            raise

    # 이미지 출력
    def show(self, image):
        image = image.convert("RGB").resize((240, 240))
        self.display.image(image)

    # 하드웨어 자원 정리
    def cleanup(self):
        # 백라이트 끄기
        if self.bl is not None:
            try:
                self.bl.value = False
            except Exception as e:
                print(f"백라이트 종료 오류: {e}")

        # 초기화된 자원만 정리
        for resource in (
            self.bl,
            self.rst,
            self.dc,
            self.cs,
            self.spi
        ):
            if resource is not None:
                try:
                    resource.deinit()
                except Exception as e:
                    print(f"자원 정리 오류: {e}")


# 배경 이미지 출력 테스트
if __name__ == "__main__":
    lcd = LCD()

    background_dir = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "backgrounds"
    )

    try:
        for path in sorted(background_dir.iterdir()):
            if path.suffix.lower() in (".jpeg", ".jpg", ".png"):
                print(f"이미지 출력: {path.name}")

                with Image.open(path) as image:
                    lcd.show(image)

                time.sleep(3)

    finally:
        lcd.cleanup()