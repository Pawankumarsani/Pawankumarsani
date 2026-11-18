import sys
import io
import cv2
import numpy as np
from PIL import Image
from rembg import remove

input_path = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
output_path = "source-prepped.png"

with open(input_path, "rb") as f:
    fg_bytes = remove(f.read())

fg = Image.open(io.BytesIO(fg_bytes)).convert("RGBA")
white_bg = Image.new("RGBA", fg.size, (255, 255, 255, 255))
composited = Image.alpha_composite(white_bg, fg).convert("L")

img_np = np.array(composited)
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
enhanced = clahe.apply(img_np)

cv2.imwrite(output_path, enhanced)
print(f"Saved {output_path}")
