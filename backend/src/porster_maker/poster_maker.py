import io

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

from PIL.Image import Resampling

cur_dir = Path(__file__).resolve().parent
background_image_path = cur_dir / 'backgroung.png'
font_b = cur_dir / 'GraphikKinopoiskfamily' / 'Graphik Kinopoisk LC-Bold.otf'
font_r = cur_dir / 'GraphikKinopoiskfamily' / 'Graphik Kinopoisk LC-Regular.otf'
font_m = cur_dir / 'GraphikKinopoiskfamily' / 'Graphik Kinopoisk LC-Medium.otf'
font_ri = cur_dir / 'GraphikKinopoiskfamily' / 'Graphik Kinopoisk LC-Regular Italic.otf'

image_orig = Image.open(background_image_path)
font_b36 = ImageFont.truetype(str(font_b), 36)
font_m17 = ImageFont.truetype(str(font_m), 17)
font_r20 = ImageFont.truetype(str(font_r), 20)


def put_paragraph(draw, text, position, width, font, fill=(0, 0, 0), resplit=True):
    if not resplit:
        paragraph = text
    else:
        text = text.replace('\n', ' ').strip()
        words = text.split()[::-1]
        lines = [[]]
        while words:
            word = words.pop()
            last_line = lines[-1]
            if len(last_line) == 0 or draw.textlength(' '.join(last_line) + word, font=font) <= width:
                last_line.append(word)
            else:
                lines.append([word])
        paragraph = '\n'.join(' '.join(line) for line in lines)
    draw.multiline_text(position, paragraph, font=font, fill=fill)


def resize_and_crop(io_image: io.BytesIO, new_width, new_height):
    with Image.open(io_image) as img:
        img_width, img_height = img.size

        # Calculate target width and height ratios
        target_ratio = new_width / new_height
        img_ratio = img_width / img_height

        if img_ratio >= target_ratio:
            # Image is wider than needed, scale by height
            scale_height = new_height
            scale_width = int(img_width * (new_height / img_height))
            img = img.resize((scale_width, scale_height), Resampling.LANCZOS)

            # Calculate the coordinates to crop the center
            left = (scale_width - new_width) // 2
            top = 0
            right = left + new_width
            bottom = new_height
        else:
            # Image is taller than needed, scale by width
            scale_width = new_width
            scale_height = int(img_height * (new_width / img_width))
            img = img.resize((scale_width, scale_height), Resampling.LANCZOS)

            # Calculate the coordinates to crop the center
            left = 0
            top = (scale_height - new_height) // 2
            right = new_width
            bottom = top + new_height

        # Crop the image to the specified bounds
        return img.crop((left, top, right, bottom))


def make_poster(title: str, genres: str, tagline: str, name: str, review: str, actors: list[str], poster_image: io.BytesIO):
    image = image_orig.copy()
    draw = ImageDraw.Draw(image)
    put_paragraph(draw, title, (333, 92), 571, font_b36, (0, 0, 0), )
    put_paragraph(draw, genres, (501, 325), 401, font_m17, (0, 0, 0), )
    put_paragraph(draw, tagline, (501, 369), 401, font_m17, (166, 166, 166), )
    put_paragraph(draw, name, (501, 466), 401, font_m17, (0, 0, 0), )
    put_paragraph(draw, "\n\n".join(actors), (942, 200), 263, font_m17, (0, 0, 0), resplit=False)
    put_paragraph(draw, review, (24, 522), 867, font_r20, (0, 0, 0), )
    resized_image = resize_and_crop(poster_image, 270, 358)
    image.paste(resized_image, (22, 87))
    img_bytes_io = io.BytesIO()
    image.convert('RGB').save(img_bytes_io, format='JPEG')
    img_bytes_io.seek(0)
    return img_bytes_io

# make_poster(
#     'Анатомия огня (2024)',
#     'драма, криминал',
#     '«Когда тьма приходит в твой сарай, приходится вылезать из сеновала»',
#     'Сержео Шашлускони',
#     '''В маленьком городке на окраине Сибири, где зимы суровы и ночи длинны, каждый знает каждого. Жизнь течёт размеренно, пока не начинаются странные и загадочные пожары, уничтожающие сараи одного за другим. Главный герой, бывший пожарный инспектор Алексей, возвращается в родной город после личной трагедии, чтобы обнаружить, что его дом — следующая цель.''',
#     '',
# )
