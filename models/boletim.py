import cv2
import pytesseract
from PIL import Image

def extrair_notas(imagem_boletim):
    """
    Extrai as notas de um boletim escolar a partir de uma imagem.

    Args:
        imagem_boletim (str): Caminho para a imagem do boletim.

    Returns:
        dict: Dicionário com as notas extraídas, onde as chaves são os nomes
              das disciplinas e os valores são as notas.
    """

    # Carrega a imagem do boletim
    imagem = cv2.imread(imagem_boletim)

    # Converte a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplica limiarização para melhorar o contraste
    _, imagem_limiar = cv2.threshold(imagem_cinza, 127, 255, cv2.THRESH_BINARY)

    # Configura o Tesseract para reconhecer o idioma português
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Substitua pelo caminho para o Tesseract
    pytesseract.pytesseract.set_lang('por')

    # Realiza o OCR na imagem para extrair o texto
    texto = pytesseract.image_to_string(Image.fromarray(imagem_limiar))

    # Processa o texto para extrair as notas
    notas = {}
    linhas = texto.split('\n')
    for linha in linhas:
        partes = linha.split(':')
        if len(partes) == 2:
            disciplina = partes[0].strip()
            nota = partes[1].strip()
            try:
                nota_float = float(nota)
                notas[disciplina] = nota_float
            except ValueError:
                pass  # Ignora linhas que não representam notas

    return notas

# Exemplo de uso
imagem_boletim = 'caminho/para/boletim.jpg'  # Substitua pelo caminho da imagem
notas_extraidas = extrair_notas(imagem_boletim)
print(notas_extraidas) 