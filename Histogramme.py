import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def histogrammes(image_originale_path, image_dechiffree_path):
    # Charger les images
    img_orig = cv2.imread(image_originale_path)
    img_dechiffree = cv2.imread(image_dechiffree_path)
    
    # Séparer les canaux de couleur des deux images
    b_orig, g_orig, r_orig = cv2.split(img_orig)
    b_dechiffree, g_dechiffree, r_dechiffree = cv2.split(img_dechiffree)

    
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