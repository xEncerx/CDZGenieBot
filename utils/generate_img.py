from typing import Union
from aiogram.types import InputFile
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from io import BytesIO
import markups as nav
from config.bot_data import bot

font_dir = os.path.join(os.getcwd(), 'Fonts')
skelet = os.path.join(os.getcwd(), 'Skelets')

class GenerateImg:
    def __init__(self, test_name: str, client_name: str,  answer: list = None, time: Union[datetime, str] = None):
        if time is None:
            self.time = datetime.now().strftime("%H:%M")
        else: self.time = time
        if answer is None:
            self.answer = [10, 0]
            self.probability = 100
        else:
            self.answer = list(map(int, answer))
            self.probability = round(self.answer[0]/(self.answer[0] + self.answer[1])*100)
        self.correct_answer = f"{self.answer[0]} ({self.probability}%)"
        self.incorrect_answer = f"{self.answer[1]} ({100 - self.probability}%)"
        self.client_name = client_name
        self.test_name = test_name
        self.probability_font = ImageFont.truetype(os.path.join(font_dir, "Roboto.ttf"), 47)

    def generate_chart(self, output_size: Union[tuple, list] = (350, 350)) -> Image:
        size = (1080, 1080)
        center = (540, 540)
        radius = 524
        image = Image.new('RGBA', size, (255, 255, 255, 255))
        draw = ImageDraw.Draw(image)
        start_end_angle = int(360 * (self.answer[1] / (self.answer[0] + self.answer[1])))
        if start_end_angle == 0:
            draw.ellipse([(center[0] - radius, center[1] - radius), (center[0] + radius, center[1] + radius)],
                         outline="#6dd16b", width=240)
        else:
            draw.pieslice([(center[0] - radius, center[1] - radius), (center[0] + radius, center[1] + radius)],
                          start_end_angle, 0, fill="#6dd16b", width=56)
            draw.pieslice([(center[0] - radius, center[1] - radius), (center[0] + radius, center[1] + radius)], 360,
                          start_end_angle, fill="#ff8b57", width=56)
        draw.ellipse([(center[0] - 312, center[1] - 312), (center[0] + 312, center[1] + 312)], fill="white")
        draw.ellipse([(center[0] - 300, center[1] - 300), (center[0] + 300, center[1] + 300)], outline="#e5e5e5",
                     width=6)
        return image.resize(output_size)

    def windows_img(self, save_path):
        number_font = ImageFont.truetype(os.path.join(font_dir, 'Roboto Light.ttf'), 21)
        windows_test_name_font = ImageFont.truetype(os.path.join(font_dir, 'Roboto.ttf'), 15)
        with Image.open(os.path.join(skelet, 'Windows_skelet.png')) as image:
            draw = ImageDraw.Draw(image)
            draw.text((170, 230), self.client_name, fill="#262626", font=windows_test_name_font)
            draw.text((1667, 10), self.client_name, fill="#000000", font=windows_test_name_font)
            draw.text((170, 250), self.test_name, fill="#262626", font=windows_test_name_font)
            draw.text((1130, 505), self.correct_answer, fill="#393939", font=number_font)
            draw.text((1154, 552), self.incorrect_answer, fill="#393939", font=number_font)
            w_image, _ = image.size
            _, _, prob_text, _ = draw.textbbox((0, 0), f"{self.probability}/100", font=self.probability_font)
            draw.text(((w_image - prob_text) / 2 + 705, 395), f"{self.probability}/100", fill="#252526", font=self.probability_font)
            chart = self.generate_chart(output_size=(275, 275))
            image.paste(chart, (420, 405))
            image.save(save_path, "PNG")

    def android_img(self, save_path, text_wrap: Union[str, int] = None):
        android_time_font = ImageFont.truetype(os.path.join(font_dir, 'Roboto Medium.ttf'), 19)
        android_test_name_font = ImageFont.truetype(os.path.join(font_dir, 'Roboto.ttf'), 25)
        with Image.open(os.path.join(skelet, 'Android_skelet.png')) as image:
            draw = ImageDraw.Draw(image)
            draw.text((510, 14), self.time, fill="#8b8b8b", font=android_time_font)
            w_image, _ = image.size
            d_text = [self.client_name] + textwrap.wrap(self.test_name, width=(int(text_wrap) if text_wrap is not None else 47))
            _, _, text_width, _ = draw.textbbox((0, 0), "\n".join(d_text), font=android_test_name_font)
            _, _, prob_text, _ = draw.textbbox((0, 0), f"{self.probability}/100", font=self.probability_font)
            draw.text(((w_image - prob_text) / 2 + 95, 920), f"{self.probability}/100", fill="#252526", font=self.probability_font)
            for index, text in enumerate(d_text):
                draw.text(((w_image-text_width)/2, 205+index*37), text, fill="#262626", font=android_test_name_font)
            chart = self.generate_chart()
            chart_w, _ = chart.size
            image_w, _ = image.size
            image.paste(chart, ((image_w-chart_w)//2, 425))
            image.save(save_path, "PNG")

    def iphone_img(self, save_path, text_wrap: Union[str, int] = None):
        iphone_time_font = ImageFont.truetype(os.path.join(font_dir, "SFProText-Semibold.ttf"), 22)
        iphone_name_font = ImageFont.truetype(os.path.join(font_dir, "Roboto.ttf"), 23)
        iphone_number_font = ImageFont.truetype(os.path.join(font_dir, "Roboto Light.ttf"), 24)
        with Image.open(os.path.join(skelet, "Iphone_skelet.png")) as image:
            draw = ImageDraw.Draw(image)
            draw.text((43, 22), self.time, fill="#fdfdfd", font=iphone_time_font)
            draw.text((340, 985), self.correct_answer, fill="#1b1d20", font=iphone_number_font)
            draw.text((365, 1045), self.incorrect_answer, fill="#1b1d20", font=iphone_number_font)
            w_image, _ = image.size
            d_text = [self.client_name] + textwrap.wrap(self.test_name, width=(int(text_wrap) if text_wrap is not None else 55))
            _, _, prob_text, _ = draw.textbbox((0, 0), f"{self.probability}/100", font=self.probability_font)
            _, _, text_width, _ = draw.textbbox((0, 0), "\n".join(d_text), font=iphone_name_font)
            draw.text(((w_image - prob_text) / 2 + 95, 861), f"{self.probability}/100", fill="#252526", font=self.probability_font)
            for index, text in enumerate(d_text):
                draw.text(((w_image - text_width) / 2, 205+index*37), text, fill="#262626", font=iphone_name_font)
            chart = self.generate_chart(output_size=(320, 320))
            chart_w, _ = chart.size
            image_w, _ = image.size
            image.paste(chart, ((image_w - chart_w) // 2, 415))
            image.save(save_path, "PNG")

async def aio_create_img(user_id: int, cdz_name: str, client_name: str, time: str, answer: str, system: str, text_wrap: int):
    img = GenerateImg(test_name=cdz_name, client_name=client_name, time=time, answer=answer)
    with BytesIO() as image_buffer:
        if system == "windows":
            img.windows_img(image_buffer)
        elif system == "android":
            img.android_img(image_buffer, text_wrap)
        elif system == "iphone":
            img.iphone_img(image_buffer, text_wrap)
        image_buffer.seek(0)
        await bot.send_document(user_id, document=InputFile(image_buffer, filename="image.png"),
                                caption="Ваше изображение 👆",
                                reply_markup=nav.main_menu)