import time
import board
import busio
import digitalio

from pathlib import Path
from PIL import Image
from adafruit_rgb_display import st7789


class LCD:
    def __init__(self):
        # SPI 통신 설정
        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI)

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

    # 이미지 출력
    def show(self, image):
        image = image.convert("RGB").resize((240, 240))
        self.display.image(image)

    # 하드웨어 자원 정리
    def cleanup(self):
        self.bl.value = False
        self.cs.deinit()
        self.dc.deinit()
        self.rst.deinit()
        self.bl.deinit()
        self.spi.deinit()


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