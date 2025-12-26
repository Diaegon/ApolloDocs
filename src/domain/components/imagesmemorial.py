from io import BytesIO

import matplotlib.pyplot as plt
from reportlab.lib.units import cm
from reportlab.platypus import Image

from src.config import IMAGES_DIR


# IMAGENS
class InsertImage:
    @staticmethod
    def imagem_diagrama():
        imagem1_caminho = f"{IMAGES_DIR}/diagramasolar.png"
        img1 = Image(imagem1_caminho, width=10 * cm, height=7 * cm)
        return img1

    @staticmethod
    def imagem_aviso():
        imagem2_caminho = f"{IMAGES_DIR}/aviso.png"
        img2 = Image(imagem2_caminho, width=18 * cm, height=15 * cm)
        return img2

    @staticmethod
    def imagem_assinatura():
        imagem3_caminho = f"{IMAGES_DIR}/ASSINATURA.png"
        img3 = Image(imagem3_caminho, width=15 * cm, height=4 * cm)
        return img3

    @staticmethod
    def render_equation_to_image(equation):
        buffer = BytesIO()
        plt.figure(figsize=(3, 1))
        plt.text(0.5, 0.5, rf"{equation}", fontsize=20, ha='center', va='center')
        plt.axis('off')
        plt.savefig(buffer, bbox_inches='tight', pad_inches=0.1, dpi=200)
        plt.close()
        buffer.seek(0)
        return buffer

    def insert_equation(self, equation, story):
        buffer = self.render_equation_to_image(equation)
        img = Image(buffer)
        img.drawHeight = 50
        img.drawWidth = 250
        story.append(img)

    def insert_equation_current(self, equation: list, story):
        for sistema in range(len(equation)):
            buffer = self.render_equation_to_image(equation[sistema])
            img = Image(buffer)
            img.drawHeight = 50
            img.drawWidth = 250
            story.append(img)
