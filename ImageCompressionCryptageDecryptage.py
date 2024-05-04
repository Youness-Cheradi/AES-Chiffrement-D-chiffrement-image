import numpy
import pywt
import utils as util
from PIL import Image, ImageEnhance

def getCoeffecients(image):
    (width, height) = image.size
    image = image.copy()

    matrice_r = numpy.empty((width,height))
    matrice_g = numpy.empty((width,height))
    matrice_b = numpy.empty((width,height))

    for i in range(width):
        for j in range(height):
            (r,g,b) = image.getpixel((i,j))
            matrice_r[i,j] = r
            matrice_g[i,j] = g
            matrice_b[i,j] = b

    '''L'ondelette de Haar, ou fonction de Rademacher, est une ondelette créée par 
    Alfréd Haar en 19091. On considère que c'est la première ondelette connue. 
    Il s'agit d'une fonction constante par morceaux, ce qui en fait l'ondelette la 
    plus simple à comprendre et à implémenter. L'ondelette de Haar peut être généralisée 
    par ce qu'on appelle le système de Haar.'''

    coeffecientsR = pywt.dwt2(matrice_r,'haar')
    coeffecientsG = pywt.dwt2(matrice_g,'haar')
    coeffecientsB = pywt.dwt2(matrice_b,'haar')

    return (coeffecientsR,coeffecientsG,coeffecientsB)

def coefToImage(coeffecients):
    (coeffecientsR,coeffecientsG,coeffecientsB) = coeffecients
    coeffArray = numpy.array((coeffecientsR,coeffecientsG,coeffecientsB),dtype=object)

    (width,height) =  (len(coeffecientsR[0]), len(coeffecientsR[0][0]))

    cARed = numpy.array(coeffecientsR[0])
    cHRed = numpy.array(coeffecientsR[1][0])
    cVRed = numpy.array(coeffecientsR[1][1])
    cDRed = numpy.array(coeffecientsR[1][2])
    # Channel Green
    cAGreen = numpy.array(coeffecientsG[0])
    cHGreen = numpy.array(coeffecientsG[1][0])
    cVGreen = numpy.array(coeffecientsG[1][1])
    cDGreen = numpy.array(coeffecientsG[1][2])
    # Channel Blue
    cABlue = numpy.array(coeffecientsB[0])
    cHBlue = numpy.array(coeffecientsB[1][0])
    cVBlue = numpy.array(coeffecientsB[1][1])
    cDBlue = numpy.array(coeffecientsB[1][2])

    cAMaxRed = util.max_ndarray(cARed)
    cAMaxGreen = util.max_ndarray(cAGreen)
    cAMaxBlue = util.max_ndarray(cABlue)

    # cHMaxRed = util.max_ndarray(cHRed)
    # cHMaxGreen = util.max_ndarray(cHGreen)
    # cHMaxBlue = util.max_ndarray(cHBlue)
    #
    # cVMaxRed = util.max_ndarray(cVRed)
    # cVMaxGreen = util.max_ndarray(cVGreen)
    # cVMaxBlue = util.max_ndarray(cVBlue)
    #
    # cDMaxRed = util.max_ndarray(cDRed)
    # cDMaxGreen = util.max_ndarray(cDGreen)
    # cDMaxBlue = util.max_ndarray(cDBlue)

    # Image object init
    dwt_img = Image.new('RGB', (width, height), (0, 0, 20))
    '''
    The image formed from the low frequnecy of the images which contains the main content of the image
    '''
    for i in range(width):
        for j in range(height):
            R = cARed[i][j]
            R = (R / cAMaxRed) * 100.0
            G = cAGreen[i][j]
            G = (G / cAMaxGreen) * 100.0
            B = cABlue[i][j]
            B = (B / cAMaxBlue) * 100.0
            new_value = (int(R), int(G), int(B))
            dwt_img.putpixel((i, j), new_value)
    return dwt_img

def compressImage(imageFile):
    img = util.load_img(imageFile)
    coeff = getCoeffecients(img)
    compressedImg = coefToImage(coeff)

    enhancer = ImageEnhance.Brightness(compressedImg)
    compressedImg = enhancer.enhance(2.58)

    compressedImg.save("compressed.jpg")