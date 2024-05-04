import os
import numpy as np
import cv2
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog as Filedialog
from math import log2
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import structural_similarity as ssim
import imagBmpManage
import ImageCompressionCryptageDecryptage

from tkinter import messagebox

def choixImage():
    global filepathTxt
    file = Filedialog.askopenfile(title="Choisir l'image")
    filepathTxt.set(file.name)
    
def compressImage():
    global imgOriginalLabel
    global imgCompressedLabel

    ImageCompressionCryptageDecryptage.compressImage(filepathTxt.get())

    imgOrig = Image.open(filepathTxt.get())
    imgOrig = imgOrig.resize((165, 165))
    imgOrig = ImageTk.PhotoImage(imgOrig)
    imgOriginalLabel.configure(image=imgOrig)
    imgOriginalLabel.image = imgOrig

    imgComp = Image.open('compressed.jpg')
    imgComp = imgComp.resize((165, 165))
    imgComp = ImageTk.PhotoImage(imgComp)
    imgCompressedLabel.configure(image=imgComp)
    imgCompressedLabel.image = imgComp

    originalSize = os.path.getsize(filepathTxt.get()) / 1000.0
    compressedSize = os.path.getsize('compressed.jpg') / 1000.0

    imgOriginalLabel.configure(text=str(originalSize) + "ko",compound='top')
    imgCompressedLabel.configure(compound='top',text=str(compressedSize) + "ko")    

def calculate_entropy(image_path):
    # Ouvrir l'image à partir du chemin de fichier
    img = Image.open(image_path)
    
    # Calculer l'entropie de l'image
    histogram = img.histogram()
    total_pixels = sum(histogram)
    entropy = 0
    for count in histogram:
        probability = count / total_pixels
        if probability > 0:
            entropy -= probability * log2(probability)
    return entropy

def correlation_coefficient(image1_path, image2_path):
    # Charger les images en couleur
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    
    # Redimensionner les images pour qu'elles aient les mêmes dimensions si nécessaire
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    # Diviser les images en canaux de couleur
    img1_red, img1_green, img1_blue = cv2.split(img1)
    img2_red, img2_green, img2_blue = cv2.split(img2)
    
    # Calculer les coefficients de corrélation pour chaque paire de canaux de couleur
    correlation_red = np.corrcoef(img1_red.flatten(), img2_red.flatten())[0, 1]
    correlation_green = np.corrcoef(img1_green.flatten(), img2_green.flatten())[0, 1]
    correlation_blue = np.corrcoef(img1_blue.flatten(), img2_blue.flatten())[0, 1]
    
    return correlation_red, correlation_green, correlation_blue

def chiffrerImage():
    global imgClairLabel
    global imgChiffreLabel
    img = Image.open('compressed.jpg')
    img.save("temp.bmp")
    bmp = imagBmpManage.BmpManager('temp.bmp',key.get()) #image + pass
    bmp.encrypt()
    imgOrig = Image.open('temp.bmp')
    imgOrig = imgOrig.resize((165, 165))
    imgOrig = ImageTk.PhotoImage(imgOrig)
    imgClairLabel.configure(image=imgOrig)
    imgClairLabel.image = imgOrig

    imgChiff= Image.open('img_enc.bmp')
    imgChiff = imgChiff.resize((165, 165))
    imgChiff = ImageTk.PhotoImage(imgChiff)
    imgChiffreLabel.configure(image=imgChiff)
    imgChiffreLabel.image = imgChiff


def afficher_histogrammes_tkinter(image_originale_path, image_dechiffree_path):
    # Charger les images
    img_orig = cv2.imread(image_originale_path)
    img_dechiffree = cv2.imread(image_dechiffree_path)
    
    # Séparer les canaux de couleur des deux images
    b_orig, g_orig, r_orig = cv2.split(img_orig)
    b_dechiffree, g_dechiffree, r_dechiffree = cv2.split(img_dechiffree)
    
    # Créer une nouvelle fenêtre Tkinter
    fenetre_histogrammes = tk.Toplevel()
    fenetre_histogrammes.title("Histogrammes")
    
    # Créer une figure Matplotlib
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
    
    # Afficher les histogrammes pour chaque canal de couleur
    for i, (color, channel_orig, channel_dechiffree) in enumerate(zip(['Blue', 'Green', 'Red'], [b_orig, g_orig, r_orig], [b_dechiffree, g_dechiffree, r_dechiffree])):
        # Histogramme de l'image originale
        hist_orig, bins = np.histogram(channel_orig.ravel(), bins=256, range=(0, 256))
        axes[i].plot(hist_orig, color='blue', alpha=0.5, label='Original')
        
        # Histogramme de l'image déchiffrée
        hist_dechiffree, _ = np.histogram(channel_dechiffree.ravel(), bins=256, range=(0, 256))
        axes[i].plot(hist_dechiffree, color='red', alpha=0.5, label='Decrypted')
        
        # Ajouter des légendes et titres
        axes[i].set_title(f'{color} Channel')
        axes[i].legend()
        
    # Afficher les histogrammes
    plt.tight_layout()
    
    # Incorporer la figure Matplotlib dans la fenêtre Tkinter
    canvas = FigureCanvasTkAgg(fig, master=fenetre_histogrammes)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



def afficherParametres(entropie,entropie_rec, psnr_value, mse_value, ssim_value, correlation,correlation_rec):
    # Créer une nouvelle fenêtre
    fenetre_parametres = Toplevel()
    fenetre_parametres.title("Resultat de traitement après déchiffrement")
    
    # Charger et afficher l'image déchiffrée
    img_dechiffree = Image.open('dec.bmp')
    img_dechiffree = img_dechiffree.resize((165, 165))
    img_dechiffree = ImageTk.PhotoImage(img_dechiffree)
    imgOriginalLabel = ttk.Label(fenetre_parametres, image=img_dechiffree)
    imgOriginalLabel.grid(row=2, column=2, pady=60)
    
    # Charger et afficher l'image original
    imgOrig = Image.open(filepathTxt.get())
    imgOrig = imgOrig.resize((165, 165))
    imgOrig = ImageTk.PhotoImage(imgOrig)
    imgOrigLabel = ttk.Label(fenetre_parametres, image=imgOrig)
    imgOrigLabel.grid(row=2, column=0, padx=60,pady=60, columnspan=2)
    
    # Ajouter des étiquettes pour afficher les paramètres
    ttk.Label(fenetre_parametres, text="Entropie d'image originale: " + str(entropie), foreground="#52be22", font=("Arial",10,"bold")).grid(row=3, pady=15,column=1, sticky='W')
    ttk.Label(fenetre_parametres, text="Coeff de corrélation: " + str(correlation), foreground="#0483f6", font=("Arial",10,"bold")).grid(row=3, padx=30,pady=15 ,column=2,sticky='W')
    
    ttk.Label(fenetre_parametres, text="Entropie d'image reconstruite: " + str(entropie_rec), foreground="#52be22", font=("Arial",10,"bold")).grid(row=4,pady=15,column=1, sticky='W')
    ttk.Label(fenetre_parametres, text="Coeff de corrélation: " + str(correlation_rec), foreground="#0483f6", font=("Arial",10,"bold")).grid(row=4,padx=30,pady=15, column=2,sticky='W')
    
    ttk.Label(fenetre_parametres, text="PSNR: " + str(psnr_value), foreground="red", font=("Arial",12,"bold")).grid(row=6, column=1,padx=30,pady=40, sticky='W')
    ttk.Label(fenetre_parametres, text="MSE: " + str(mse_value), foreground="#080358", font=("Arial",12,"bold")).grid(row=6, column=2,padx=30,pady=40,sticky='W')
    ttk.Label(fenetre_parametres, text="SSIM: " + str(ssim_value), foreground="#38761d", font=("Arial",12,"bold")).grid(row=6, column=2,padx=300,sticky='W')
    
    # Affecter les images aux labels
    imgOrigLabel.image = imgOrig
    imgOriginalLabel.image = img_dechiffree
    
    
    
    afficher_histogrammes_tkinter(filepathTxt.get(), 'dec.bmp')




def dechiffrerImage():
    global imgClairLabel
    global imgChiffreLabel
    bmp = imagBmpManage.BmpManager('img_enc.bmp', key.get())  # image + pass
    bmp.decrypt()
    imgOrig0 = Image.open('temp.bmp')
    imgOrig = Image.open('img_enc.bmp')
    imgOrig = imgOrig.resize((165, 165))
    imgOrig = ImageTk.PhotoImage(imgOrig)
    imgClairLabel.configure(image=imgOrig)
    imgClairLabel.image = imgOrig

    imgChiff = Image.open('dec.bmp')
    imgChiff = imgChiff.resize((165, 165))
    imgChiff = ImageTk.PhotoImage(imgChiff)
    imgChiffreLabel.configure(image=imgChiff)
    imgChiffreLabel.image = imgChiff

    # Calcul des mesures après le chiffrement
    img_original = cv2.imread(filepathTxt.get())
    img_encrypted = cv2.imread('dec.bmp')
    
    # Redimensionner les images pour qu'elles aient les mêmes dimensions
    img_original = cv2.resize(img_original, (img_encrypted.shape[1], img_encrypted.shape[0]))
    
    psnr_value = psnr(img_original, img_encrypted)
    #print("PSNR:", psnr_value)

    mse_value = mse(img_original, img_encrypted)
    #print("MSE:", mse_value)
    # Calcul de la similarité structurelle en spécifiant une taille de fenêtre appropriée
    min_dimension = min(img_original.shape[:3])
    win_size = min(min_dimension, 7)  # Assurez-vous que win_size est impair
    ssim_value = ssim(img_original, img_encrypted, win_size=win_size, multichannel=True)
    #print("SSIM:", ssim_value)
    
    correlation = correlation_coefficient(filepathTxt.get(), 'temp.bmp')
    correlation_rec = correlation_coefficient(filepathTxt.get(), 'dec.bmp')
    # print("Coefficient de corrélation:", correlation)
    
    entropie = calculate_entropy('temp.bmp') # suppose que 'img_enc.bmp' est l'image chiffrée
    entropie_rec = calculate_entropy('dec.bmp') # suppose que 'img_enc.bmp' est l'image chiffrée
   # print("Entropie:", entropie)

    # Afficher les paramètres dans une nouvelle fenêtre
    afficherParametres(entropie,entropie_rec, psnr_value, mse_value, ssim_value,correlation,correlation_rec)
   

'''///////////////////////////////////// Interface graphique par L'outil Tkinter ///////////////////////////////////'''

root = Tk()
s = ttk.Style()
root.geometry("1000x1000")

# Configuration du style pour le bouton
s.configure("Custom.TButton", bd =1,background="blue", foreground="black")
root.title("Cryptage et Décryptage d'Images")
s.configure('mRRed.TFrame', background='#F7F4F7')
root.geometry("1000x800")
frm = ttk.Frame(root, style='mRRed.TFrame')
root.configure(bg='#D1CCD1')
frm.grid()
'''logo'''
ttk.Label(frm, background='white',text="Le Chiffrement et Dechiffrement d'image",font=("Arial", 16,"underline","bold","italic")).grid(row=3, column=2,padx=30,pady=10, sticky='w')


#ouvrir image
ttk.Label(frm, text="Choisir une image: ", foreground="#541574", font="bold").grid(row=5, column=1,padx=20,sticky='W')
filepathTxt = StringVar()
Entry(frm, width=50, textvariable=filepathTxt,bd=1, relief=tk.SOLID, background="white",foreground="#D40C2F", font=("Arial",10,"normal")).grid(row=5, column=2)
ttk.Button(frm, text="choisir image", command=choixImage, style="Custom.TButton",width=18).grid(row=5, column=3, padx=5, sticky='w')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)




#compress
noimg = Image.open('noim.jpg')
noimg = ImageTk.PhotoImage(noimg)
ttk.Button(frm, text="Compresser image", command=compressImage,style="Custom.TButton",width=18).grid(row=6, column=3,pady=(150,0), sticky='w')

imgOriginalLabel = ttk.Label(frm,width=20, image=noimg,background='#fff')
imgCompressedLabel = ttk.Label(frm,width=20,image=noimg, background='#fff')
imgOriginalLabel.grid(row=8, column=2,pady=10, sticky='w')
imgCompressedLabel.grid(row=8, column=2, padx=(300, 0), sticky='w')


#chiffrement/déchiffrement 
key = StringVar()
ttk.Label(frm, text="Cle de chiffrement: ", foreground="#541574", font="bold").grid(row=6, column=1,padx=10,sticky='W')
Entry(frm, width=20, textvariable=key,bd=1, relief=tk.SOLID, background="white",foreground="#612361", font="italic").grid(row=6, column=2,padx=150)
key.set ("12345678qwertyui") #mot de passe par defaut


ttk.Button(frm, text="Chiffrer l'image", command=chiffrerImage,style="Custom.TButton",width=18).grid(row=8, column=3,pady=(120,0),sticky='w')
ttk.Button(frm, text="Déchiffrer l'image", command=dechiffrerImage,style="Custom.TButton",width=18).grid(row=9, column=3,pady=(120,0),sticky='w')

imgClairLabel = ttk.Label(frm, image=noimg, background='#fff')
imgChiffreLabel = ttk.Label(frm,image=noimg, background='#fff')
imgClairLabel.grid(row=9, column=2,pady=10, sticky='w')
imgChiffreLabel.grid(row=9, column=2,padx=(300, 0), sticky='w')





root.mainloop()
