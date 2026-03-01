from PIL import Image, ImageDraw, ImageFont
import random
import uuid
from pathlib import Path
import os

class CatGenerator:
    def __init__(self, static_dir: Path):
        self.static_dir = static_dir
        
        # Различные цвета для котов
        self.cat_colors = [
            ("#FFB6C1", "#FF69B4"),  # Розовый
            ("#87CEEB", "#4682B4"),  # Голубой
            ("#98FB98", "#32CD32"),  # Зеленый
            ("#FFD700", "#DAA520"),  # Золотой
            ("#DDA0DD", "#DA70D6"),  # Фиолетовый
            ("#F0E68C", "#BDB76B"),  # Хаки
            ("#FFA07A", "#FF4500"),  # Оранжевый
            ("#E0FFFF", "#40E0D0"),  # Бирюзовый
        ]
        
        # Формы котов
        self.cat_shapes = ["circle", "square", "triangle"]
        
    def generate_random_cat(self, text="Мяу!"):
        """Генерирует случайное изображение кота"""
        
        # Создаем изображение
        img_size = 400
        image = Image.new('RGB', (img_size, img_size), 'white')
        draw = ImageDraw.Draw(image)
        
        # Выбираем случайный цвет
        bg_color, fg_color = random.choice(self.cat_colors)
        
        # Рисуем фон
        draw.rectangle([0, 0, img_size, img_size], fill=bg_color)
        
        # Рисуем голову кота
        head_size = 200
        head_x = (img_size - head_size) // 2
        head_y = (img_size - head_size) // 2 - 30
        
        # Рисуем голову
        draw.ellipse(
            [head_x, head_y, head_x + head_size, head_y + head_size], 
            fill=fg_color, 
            outline='black', 
            width=3
        )
        
        # Уши
        ear_size = 40
        # Левое ухо
        draw.polygon([
            (head_x + 40, head_y + 20),
            (head_x + 20, head_y - 20),
            (head_x + 70, head_y + 20)
        ], fill=fg_color, outline='black', width=3)
        
        # Правое ухо
        draw.polygon([
            (head_x + head_size - 40, head_y + 20),
            (head_x + head_size - 20, head_y - 20),
            (head_x + head_size - 70, head_y + 20)
        ], fill=fg_color, outline='black', width=3)
        
        # Глаза
        eye_size = 20
        eye_y = head_y + 70
        
        # Левый глаз
        draw.ellipse(
            [head_x + 60, eye_y, head_x + 60 + eye_size, eye_y + eye_size], 
            fill='white', 
            outline='black', 
            width=2
        )
        draw.ellipse(
            [head_x + 70, eye_y + 5, head_x + 70 + 5, eye_y + 10], 
            fill='black'
        )
        
        # Правый глаз
        draw.ellipse(
            [head_x + head_size - 80, eye_y, head_x + head_size - 80 + eye_size, eye_y + eye_size], 
            fill='white', 
            outline='black', 
            width=2
        )
        draw.ellipse(
            [head_x + head_size - 70, eye_y + 5, head_x + head_size - 70 + 5, eye_y + 10], 
            fill='black'
        )
        
        # Нос
        draw.polygon([
            (head_x + 100, head_y + 100),
            (head_x + 90, head_y + 110),
            (head_x + 110, head_y + 110)
        ], fill='pink', outline='black', width=1)
        
        # Рот
        draw.arc(
            [head_x + 90, head_y + 110, head_x + 110, head_y + 130], 
            start=0, end=180, fill='black', width=2
        )
        
        # Усы
        whisker_y = head_y + 110
        for i in range(3):
            offset = i * 10
            # Левые усы
            draw.line(
                [head_x + 80, whisker_y + offset, head_x + 20, whisker_y + offset - 10], 
                fill='black', width=2
            )
            # Правые усы
            draw.line(
                [head_x + head_size - 80, whisker_y + offset, head_x + head_size - 20, whisker_y + offset - 10], 
                fill='black', width=2
            )
        
        # Добавляем текст
        try:
            # Пытаемся загрузить шрифт побольше
            font_size = 30
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Если шрифт не найден, используем дефолтный
            font = ImageFont.load_default()
        
        # Текст под головой
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (img_size - text_width) // 2
        text_y = head_y + head_size + 20
        
        # Рисуем белый фон под текст
        draw.rectangle(
            [text_x - 5, text_y - 5, text_x + text_width + 5, text_y + 30],
            fill='white',
            outline='black',
            width=2
        )
        
        # Добавляем текст
        draw.text((text_x, text_y), text, fill='black', font=font)
        
        # Сохраняем изображение
        cat_id = str(uuid.uuid4())[:8]
        image_path = self.static_dir / f"{cat_id}.png"
        image.save(image_path)
        
        return cat_id