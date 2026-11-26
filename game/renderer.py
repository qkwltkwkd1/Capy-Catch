from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from game.config import SIZE, THEMES

# 프로젝트 최상위 폴더 경로
ROOT = Path(__file__).resolve().parent.parent

# 배경 이미지 폴터 경로
BACKGROUND_DIR = ROOT / "assets" / "backgrounds"

# 글꼴 파일 경로
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

class Renderer:
    def __init__(self):
        # 배경 이미지 저장 
        self.backgrounds = []

        # 테마 미리보기 이미지 저장 
        self.previews = []

        # 글꼴 설정
        self.title_font = ImageFont.truetype(FONT_PATH, 22)
        self.text_font = ImageFont.truetype(FONT_PATH, 12)
        self.theme_font = ImageFont.truetype(FONT_PATH, 10)

        # 배경 이미지 불러오기
        self.load_backgrounds()

    # 배경 이미지 불러오기 
    def load_backgrounds(self):
        for theme in THEMES:
            filename = theme["filename"]
            path = BACKGROUND_DIR / filename

            with Image.open(path) as source:
                image = source.convert("RGB")

            # LCD에 출력할 배경 이미지
            background = image.resize((SIZE, SIZE))
            self.backgrounds.append(background)

            # 메뉴에서 사용할 작은 미리보기 이미지
            preview = image.resize((93, 40))
            self.previews.append(preview)

    # 텍스트 가운데 정렬 
    def draw_text(self, draw, text, x, y, font, color):
        draw.text(
            (x, y),
            text,
            font=font,
            fill=color,
            anchor="mm"  # 가운데 정렬
        )

    # 시작 및 테마 선택 화면
    def draw_menu(self, selected_theme):
        # 현재 선택된 테마를 배경으로 사용
        image = self.backgrounds[selected_theme].copy()

        # 이미지 위에 그림 그릴 객체 생성 
        draw = ImageDraw.Draw(image)

        # 시작 화면 패널
        draw.rounded_rectangle(
            (8, 8, 232, 232),
            radius=14,
            fill="#fff7e7"
        )

        # 게임 제목
        self.draw_text(
            draw, 
            "CAPY-CATCH!",
            120, 25,
            self.title_font,
            "#644936"
        )

        # 테마 선택 안내 문구
        self.draw_text(
            draw,
            "CHOOSE YOUR THEME",
            120, 46,
            self.text_font,
            "#96765d"
        )

        # 테마 4개 2x2 형태로 배치
        for i in range(len(THEMES)):
            row = i // 2
            col = i % 2

            x = 19 + col * 105
            y = 63 + row * 67

            # 선택한 테마는 주황색 테두리
            if i == selected_theme:
                border_color = "#c5823e"
                border_width = 3
                card_color = "#ffe3a4"

            # 선택하지 않은 테마
            else:
                border_color = "#e8ddc9"
                border_width = 1
                card_color = "#e8ddc9"

            # 테마 선택 카드
            draw.rounded_rectangle(
                (x - 3, y - 3, x + 96, y + 60),
                radius=7,
                fill=card_color,
                outline=border_color,
                width=border_width
            )

            # 테마 미리보기 이미지
            image.paste(self.previews[i], (x, y))

            # 테마 이름 표시
            self.draw_text(
                draw,
                THEMES[i]["name"],
                x + 46, y + 50,
                self.theme_font,
                "#694b36"
            )

        # 조작 안내
        self.draw_text(
            draw,
            "JOYSTICK: CHOOSE  A: START",
            120, 214,
            self.text_font,
            "#694b36"
        )

        return image

    # 선택한 배경 이미지 반환 
    def draw_background(self, selected_theme):
        return self.backgrounds[selected_theme].copy()