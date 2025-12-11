from reportlab.platypus import Image
from reportlab.lib.units import cm
import matplotlib.pyplot as plt
from src.config import IMAGES_DIR


#IMAGENS
class InsertImage():
    def __init__(self):
        pass

    def contar_inversores(self):
        pass
    
    def imagem_diagrama(self):    
        imagem1_caminho = f'{IMAGES_DIR}/diagramasolar.png'
        img1 = Image(imagem1_caminho, width=10*cm, height=7*cm)
        return img1

    def imagem_aviso(self):
        imagem2_caminho =f'{IMAGES_DIR}/aviso.png'
        img2 = Image(imagem2_caminho, width=18*cm, height=15*cm)
        return img2
    
    def imagem_assinatura(self):
        imagem3_caminho = f'{IMAGES_DIR}/ASSINATURA.png'
        img3 = Image(imagem3_caminho, width=15*cm, height=4*cm)
        return img3
    
    @staticmethod
    def render_equation_to_image(equation, filename):
        fig = plt.figure(figsize=(3, 1))
        plt.text(0.5, 0.5, rf"{equation}", fontsize=20, ha='center', va='center')
        plt.axis('off')
        plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, dpi=200)
        plt.close()

    def insert_equation(self, equation, story, img_filename):
        self.render_equation_to_image(equation, img_filename)
        img = Image(img_filename)
        img.drawHeight = 50
        img.drawWidth = 250
        story.append(img)

    def insert_equation_current(self, equation: list, story, img_filename):
        for sistema in range(len(equation)):
            caminho =  f"{sistema}" + img_filename 
            self.render_equation_to_image(equation[sistema], caminho)
            img = Image(caminho)
            img.drawHeight = 50
            img.drawWidth = 250
            story.append(img)