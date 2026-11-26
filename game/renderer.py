from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

from game.config import (
    SIZE,
    THEMES,
    GRID_SIZE,
    NORMAL_IMAGE
)

# 프로젝트 최상위 폴더 경로
ROOT = Path(__file__).resolve().parent.parent

# 배경 이미지 폴더 경로
BACKGROUND_DIR = ROOT / "assets" / "backgrounds"

# 캐릭터 이미지 폴더 경로
IMAGE_DIR = ROOT / "assets" / "images"

# 글꼴 파일 경로
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

class Renderer:
    def __init__(self):
        # 배경 이미지 저장
        self.backgrounds = []

        # 테마 미리보기 이미지 저장
        self.previews = []

        # 글꼴 설정
        self.title_font = self.load_font(22)
        self.text_font = self.load_font(12)
        self.theme_font = self.load_font(10)
        self.score_font = self.load_font(14)

        # 배경 이미지 불러오기
        self.load_backgrounds()

        # 일반 카피바라 이미지 불러오기
        self.load_character()

    # 글꼴 불러오기
    def load_font(self, size):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except OSError:
            print(f"글꼴 파일을 찾을 수 없습니다: {FONT_PATH}")
            return ImageFont.load_default(size=size)

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

    # 카피바라 이미지 불러오기
    def load_character(self):
        path = IMAGE_DIR / NORMAL_IMAGE

        with Image.open(path) as source:
            image = source.convert("RGBA")

        # 이미지 비율을 유지하면서 크기 조절
        self.capybara_image = ImageOps.contain(
            image,
            (76, 76)
        )

    # 기본 게임 화면 그리기
    def draw_game(self, logic):
        # 선택된 배경 이미지 가져오기
        image = self.backgrounds[logic.theme].copy()

        # 그림을 그릴 객체 생성
        draw = ImageDraw.Draw(image)

        # 1. 상단 점수 표시 영역
        draw.rounded_rectangle(
            (8, 8, SIZE - 8, 38),
            radius=8,
            fill="#fff7e7"
        )

        # 현재 레벨 표시
        self.draw_text(
            draw,
            "LEVEL 1",
            50, 23,
            self.text_font,
            "#644936"
        )

        # 현재 점수 표시
        self.draw_text(
            draw,
            f"SCORE: {logic.score}",
            175, 23,
            self.score_font,
            "#644936"
        )

        # 2. 게임판 크기 설정
        # 게임판 시작 위치
        board_x = 10
        board_y = 45

        # 게임판 전체 크기
        board_width = SIZE - 20
        board_height = 170

        # 구멍 하나가 차지하는 공간
        cell_width = board_width // GRID_SIZE
        cell_height = board_height // GRID_SIZE

        # 구멍 개수
        total_holes = GRID_SIZE * GRID_SIZE

        # 3. 구멍 그리기
        for i in range(total_holes):
            # 현재 구멍의 행과 열
            row = i // GRID_SIZE
            col = i % GRID_SIZE

            # 각 칸의 시작 위치
            x = board_x + col * cell_width
            y = board_y + row * cell_height

            # 각 칸의 중앙 좌표
            center_x = x + cell_width // 2
            center_y = y + cell_height // 2

            # 구멍의 중심을 조금 아래로 배치
            hole_y = center_y + 18

            # 구멍 크기
            hole_rx = 34
            hole_ry = 13

            # 구멍 바깥쪽 테두리
            draw.ellipse(
                (
                    center_x - hole_rx - 4,
                    hole_y - hole_ry - 3,
                    center_x + hole_rx + 4,
                    hole_y + hole_ry + 3
                ),
                fill="#d5bd92"
            )

            # 구멍 내부
            draw.ellipse(
                (
                    center_x - hole_rx,
                    hole_y - hole_ry,
                    center_x + hole_rx,
                    hole_y + hole_ry
                ),
                fill="#634735",
                outline="#9d7653",
                width=2
            )

            # 4. 카피바라 표시
            if i == logic.mole_position:
                character = self.capybara_image

                # 카피바라 이미지 가로, 세로 크기
                char_width = character.width
                char_height = character.height

                # 카피바라를 구멍 중앙 위에 배치
                char_x = center_x - char_width // 2
                char_y = hole_y - char_height + 17

                # 투명도를 유지하여 이미지 합성
                image.paste(
                    character,
                    (char_x, char_y),
                    character
                )

            # 5. 선택 커서 표시
            if i == logic.cursor:
                padding = 3

                draw.rounded_rectangle(
                    (
                        x + padding,
                        y + padding,
                        x + cell_width - padding,
                        y + cell_height - padding
                    ),
                    radius=8,
                    outline="#fff18a",
                    width=3
                )

        # 6. 하단 조작 안내
        draw.rounded_rectangle(
            (8, 218, SIZE - 8, 234),
            radius=5,
            fill="#fff7e7"
        )

        self.draw_text(
            draw,
            "JOYSTICK: MOVE  A: CATCH",
            SIZE // 2, 226,
            self.theme_font,
            "#644936"
        )

        return image