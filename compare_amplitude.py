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
    rgen = 50
    rl = 120.41

    def amplitude(f, r, l, c):
        w = 2 * np.pi * f
        y = 1 - w**2 * l * c
        rtot = r + rgen
        smallnum = 2 * rl * rtot + rl**2 + (w * l)**2
        smallden = y**2 + (w * rl * c)**2
        num = rtot**2 + (smallnum / smallden)
        A = (num / (r**2))**(-1/2)
        return v0 * A

    f1 = 1 / np.sqrt(l1 * c1) / 2 / np.pi # calcolo frequenze di notch e fattori di qualità
    q1 = r1 * c1 * 2 * np.pi * f1
    q2 = r2 * c1 * 2 * np.pi * f1
    q3 = r3 * c1 * 2 * np.pi * f1
    print("FREQ NOTCH 1: ", f1) # stampa a schermo frequenze di notch e fattori di qualità
    print("Q1: ", q1)
    print("Q2: ", q2)
    print("Q3: ", q3)

    r1_amp = "r1_amp.txt" # esporta dati da file txt
    r2_amp = "r2_amp.txt"
    r3_amp = "r3_amp.txt"
    x1,y1 = np.loadtxt(r1_amp, unpack=True) # mancano ancora yerr
    x2,y2 = np.loadtxt(r2_amp, unpack=True)
    x3,y3 = np.loadtxt(r3_amp, unpack=True)

    x = np.linspace(100, 4500, 1000)
    t1 = amplitude(x, r1, l1, c1)
    t2 = amplitude(x, r2, l1, c1)
    t3 = amplitude(x, r3, l1, c1)


    plt.figure() # prossimamente aggiungere errorbars
    plt.plot(x1,y1, '.', label = "dati sperimentali R1", color = 'orange', markersize=5.0)
    plt.plot(x2,y2, '.', label = "dati sperimentali R2", color = 'orange', markersize=5.0)
    plt.plot(x3,y3, '.', label = "dati sperimentali R3", color = 'orange', markersize=5.0)
    plt.plot(x, t1, color='red', label='R1 (expected)')
    plt.plot(x, t2, color='blue', label='R2 (expected)')
    plt.plot(x, t3, color='green', label='R3 (expected)')
    plt.xlim(100, 4500)
    plt.ylim(0, 6)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("ampiezza (V)", fontsize=20.0)
    plt.title("Confronto tra ampiezze aspettate e sperimentali", fontsize=30.0, fontname='sans-serif')
    # plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0) # per ora non mostro la legenda
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()