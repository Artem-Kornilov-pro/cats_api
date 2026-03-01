from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import random
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import uuid
import shutil
from pathlib import Path

from app.cat_generator import CatGenerator

app = FastAPI(title="Cat Randomizer API", description="API для случайных изображений котов")

# Создаем директорию для статических файлов, если её нет
STATIC_DIR = Path("app/static")
STATIC_DIR.mkdir(exist_ok=True)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Инициализируем генератор котов
cat_generator = CatGenerator(static_dir=STATIC_DIR)

# Цитаты для котов
CAT_QUOTES = [
    "Мяу!",
    "Дай поесть!",
    "Хочу спать...",
    "Поиграй со мной!",
    "Мур-мур-мур",
    "Кис-кис",
    "Люблю рыбку",
    "Царап-царап",
    "Мяу-мяу-мяу",
    "Мурлыка"
]

@app.get("/")
async def root():
    """Главная страница с информацией об API"""
    return {
        "message": "Cat Randomizer API 🐱",
        "endpoints": {
            "/": "Эта информация",
            "/random-cat": "Получить случайного кота (JSON с URL)",
            "/cat/image/random": "Получить случайное изображение кота",
            "/cat/image/{cat_id}": "Получить изображение по ID",
            "/cats": "Список всех доступных котов"
        }
    }

@app.get("/random-cat")
async def random_cat():
    """Возвращает URL случайного кота"""
    cat_id = cat_generator.generate_random_cat()
    return {
        "id": cat_id,
        "url": f"/cat/image/{cat_id}",
        "message": random.choice(CAT_QUOTES)
    }

@app.get("/cat/image/random")
async def get_random_cat_image():
    """Возвращает случайное изображение кота"""
    try:
        cat_id = cat_generator.generate_random_cat()
        image_path = STATIC_DIR / f"{cat_id}.png"
        
        if not image_path.exists():
            # Если изображение не создалось, пробуем еще раз
            cat_id = cat_generator.generate_random_cat("Meow")
            image_path = STATIC_DIR / f"{cat_id}.png"
        
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Cat image not found")
        
        # Читаем файл и возвращаем с правильными заголовками
        from fastapi.responses import FileResponse
        return FileResponse(
            path=image_path,
            media_type="image/png",
            headers={
                "X-Cat-ID": cat_id,
                "X-Cat-Message": "Meow",
                "Cache-Control": "no-cache"
            }
        )
    except Exception as e:
        print(f"Error in get_random_cat_image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cat/image/{cat_id}")
async def get_cat_image(cat_id: str):
    """Возвращает изображение кота по ID"""
    image_path = STATIC_DIR / f"{cat_id}.png"
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Cat not found")
    
    return FileResponse(
        image_path, 
        media_type="image/png",
        headers={"X-Cat-ID": cat_id}
    )

@app.get("/cats")
async def list_cats():
    """Список всех доступных котов"""
    cats = []
    for image_path in STATIC_DIR.glob("*.png"):
        cat_id = image_path.stem
        cats.append({
            "id": cat_id,
            "url": f"/cat/image/{cat_id}"
        })
    
    return {
        "total": len(cats),
        "cats": cats
    }

@app.post("/generate")
async def generate_new_cat(message: str = None):
    """Генерирует нового кота с опциональным сообщением"""
    if not message:
        message = random.choice(CAT_QUOTES)
    
    cat_id = cat_generator.generate_random_cat(text=message)
    
    return {
        "id": cat_id,
        "url": f"/cat/image/{cat_id}",
        "message": message
    }

@app.on_event("startup")
async def startup_event():
    """Создаем несколько котов при запуске"""
    print("Генерируем начальных котов...")
    for _ in range(5):
        cat_generator.generate_random_cat()
    print("Готово!")