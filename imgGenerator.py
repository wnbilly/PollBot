import numpy as np
from PIL import Image, ImageDraw, ImageFont
from perlin_noise import PerlinNoise
from matplotlib import pyplot as plt
import time
import random

def txt_to_img_perlin(txt="TEST", width = 128, height = 128, scale = 500.0) :

    # plus la valeur de scale est élevée, plus les motifs de bruit sont grands

    # Créer une nouvelle image de dimensions (width, height) et mode RGB
    img = Image.new("RGB", (width, height))

    # Générer une grille de bruit de Perlin pour chaque canal de couleur
    random.seed(time.time())
    noise_r = PerlinNoise(octaves=6, seed=random.randint(1, 1000))
    noise_g = PerlinNoise(octaves=6, seed=random.randint(1, 1000))
    noise_b = PerlinNoise(octaves=6, seed=random.randint(1, 1000))

    # Parcourir tous les pixels de l'image et générer une valeur de bruit pour chaque canal de couleur
    for x in range(width):
        for y in range(height):
            r = int(noise_r([x/scale, y/scale, 0.0]) * 127.0 + 128.0)
            g = int(noise_g([x/scale, y/scale, 0.5]) * 127.0 + 128.0)
            b = int(noise_b([x/scale, y/scale, 1.0]) * 127.0 + 128.0)
            img.putpixel((x, y), (r, g, b))

    draw = ImageDraw.Draw(img)

    black=(0,0,0)
    # Dtermine the text parameters
    font = ImageFont.truetype('/usr/share/fonts/truetype/tlwg/Purisa-Bold.ttf', size=16)
    draw.text(xy=(width//2, height//2), text=txt, anchor="mm", font=font, stroke_width=2, stroke_fill='black')

    plt.axis("off")
    plt.imshow(img)
    plt.show()

    # Enregistrer l'image
    img.save("perlin_noise.png")

    return img

txt_to_img_perlin(txt="TA MERE \nLA PUTE \nMATHIEU")