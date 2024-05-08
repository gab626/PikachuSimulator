import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')

from scipy.optimize import curve_fit

def main():
    
    r1 = 820.77 # dati apparato sperimentale
    r2 = 2692
    r3 = 10012
    c1 = 101.8E-9
    l1 = 47.25E-3
    v0 = 5
    c2 = 30E-9 # c2 ed l2 inventati sul momento per disegnare il doppio notch
    l2 = 20E-3
    rgen = 50 # aggiunti per confronto tra ampiezze con resistenze interne
    rl = 120.41

    def vr(f, r, l, c): # funzione ampiezza notch singolo
        w = 2 * np.pi * f
        y = w**2 * l * c - 1
        arg = w * l / r / y
        A = (1 + arg**2)**(-1/2)
        return v0 * A

    def phi(f, r, l, c): # funzione differenza di fase notch singolo
        w = 2 * np.pi * f
        arg = l * w / r / (w**2 * l * c - 1)
        return np.arctan(arg)

    def duenotch(f, r, l1, c1, l2, c2): # funzione ampiezza doppio notch
        w = 2 * np.pi * f
        y1 = 1 - w**2 * l1 * c1
        y2 = 1 - w**2 * l2 * c2
        num = w * (l1 * y2 + l2 * y1)
        den = r * y1 * y2
        A = (1 + (num / den)**2)**(-1/2)
        return v0 * A

    def realnotch(f, r, l, c):
        w = 2 * np.pi * f
        y = 1 - w**2 * l * c
        rtot = r + rgen
        smallnum = 2 * rl * rtot + rl**2 + (w * l)**2
        smallden = y**2 + (w * rl * c)**2
        num = rtot**2 + (smallnum / smallden)
        A = (num / (r**2))**(-1/2)
        return v0 * A

    def realphi(f, r, l, c):
        w = 2 * np.pi * f
        y = 1 - w**2 * l * c
        rtot = r + rgen
        num = w * (rl**2 * c - y * l)
        den = rl + rtot * (y**2 + (rl * w * c)**2)
        return np.arctan(num / den)

    x = np.linspace(100, 4500, 1000) # creazione array di x e y tramite le funzioni per plottare su grafici
    y1 = vr(x, r1, l1, c1)
    y2 = vr(x, r2, l1, c1)
    y3 = vr(x, r3, l1, c1)
    p1 = phi(x, r1, l1, c1)
    p2 = phi(x, r2, l1, c1)
    p3 = phi(x, r3, l1, c1)
    xx = np.linspace(100, 11000, 1000)
    n1 = duenotch(xx, r1, l1, c1, l2, c2)
    n2 = duenotch(xx, r2, l1, c1, l2, c2)
    n3 = duenotch(xx, r3, l1, c1, l2, c2)
    m1 = realnotch(x, r1, l1, c1)
    m2 = realnotch(x, r2, l1, c1)
    m3 = realnotch(x, r3, l1, c1)
    t1 = realphi(x, r1, l1, c1)
    t2 = realphi(x, r2, l1, c1)
    t3 = realphi(x, r3, l1, c1)
    
    plt.figure() # grafici ampiezza notch singolo
    plt.plot(x, y1, color='red', label='R1 (ideal)')
    plt.plot(x, y2, color='blue', label='R2 (ideal)')
    plt.plot(x, y3, color='green', label='R3 (ideal)')
    plt.xlim(100, 4500)
    plt.ylim(0, 6)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("ampiezza (V)", fontsize=20.0)
    plt.title("Ampiezze caso ideale", fontsize=30.0, fontname='sans-serif')
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0) 
    plt.grid(True)

    plt.figure() # grafici differenza di fase notch singolo
    plt.plot(x, p1, color='red', label='R1 (ideal)')
    plt.plot(x, p2, color='blue', label='R2 (ideal)')
    plt.plot(x, p3, color='green', label='R3 (ideal)')
    plt.xlim(100, 4500)
    plt.ylim(-2, 2)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("differenza di fase (rad)", fontsize=20.0)
    plt.title("Funzione phi = fase Vr - fase Vg", fontsize=30.0, fontname='sans-serif')
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0) 
    plt.grid(True)

    plt.figure() # grafici ampiezza doppio notch
    plt.plot(xx, n1, color='red', label='R1')
    plt.plot(xx, n2, color='blue', label='R2')
    plt.plot(xx, n3, color='green', label='R3')
    plt.xlim(100, 11000)
    plt.ylim(0, 6)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("ampiezza", fontsize=20.0)
    plt.title("Funzione duenotch", fontsize=30.0, fontname='sans-serif')
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0) 
    plt.grid(True)

    plt.figure() # grafici ampiezza reale (aggiungendo gli effetti di Rgen e Rinduttanza)
    plt.plot(x, m1, color='red', label='R1 (real)')
    plt.plot(x, m2, color='blue', label='R2 (real)')
    plt.plot(x, m3, color='green', label='R3 (real)')
    plt.xlim(100, 4500)
    plt.ylim(0, 6)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("ampiezza (V)", fontsize=20.0)
    plt.title("Ampiezze caso reale", fontsize=30.0, fontname='sans-serif')
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0) 
    plt.grid(True)

    plt.figure() # grafici differenza di fase reale (aggiungendo gli effetti di Rgen e Rinduttanza)
    plt.plot(x, t1, color='red', label='R1 (real)')
    plt.plot(x, t2, color='blue', label='R2 (real)')
    plt.plot(x, t3, color='green', label='R3 (real)')
    plt.xlim(100, 4500)
    plt.ylim(-1, 1)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("differenza di fase (rad)", fontsize=20.0)
    plt.title("Funzione phi = fase Vr - fase Vg", fontsize=30.0, fontname='sans-serif')
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0) 
    plt.grid(True)

    plt.show() # apre le canvas con i grafici

if __name__ == "__main__":
    main()