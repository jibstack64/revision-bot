"Functions for generating revision card visuals."

# import required libraries
from PIL import Image, ImageDraw, ImageFont
import datetime

def generate(question: str, answer: str, identifier: str) -> str:
    "Generates a card with question, answer and identifier being displayed. Returns the path to the final image."
    
    ImageFont.load_default()
    image = Image.new("RGB", (700, 500), "white")
    draw = ImageDraw.Draw(image)
    draw.text((30, 30), question, stroke_width=10)
    draw.text((40, 40), answer, stroke_width=10)
    fn = f"temp/temp-{datetime.datetime.now().strftime('%H-%M-%S')}.png"
    image.save(fn)

    return fn
