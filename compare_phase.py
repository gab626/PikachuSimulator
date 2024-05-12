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

    def phase(f, r, l, c):
        w = 2 * np.pi * f
        y = 1 - w**2 * l * c
        rtot = r + rgen
        num = w * (rl**2 * c - y * l)
        den = rl + rtot * (y**2 + (rl * w * c)**2)
        return np.arctan(num / den)

    f1 = 1 / np.sqrt(l1 * c1) / 2 / np.pi # calcolo frequenze di notch e fattori di qualità
    q1 = r1 * c1 * 2 * np.pi * f1
    q2 = r2 * c1 * 2 * np.pi * f1
    q3 = r3 * c1 * 2 * np.pi * f1
    print("FREQ NOTCH 1: ", f1) # stampa a schermo frequenze di notch e fattori di qualità
    print("Q1: ", q1)
    print("Q2: ", q2)
    print("Q3: ", q3)

    x1,y1,yerr1 = np.loadtxt("r1_phi.txt", unpack=True)
    x2,y2,yerr2 = np.loadtxt("r2_phi.txt", unpack=True)
    x3,y3,yerr3 = np.loadtxt("r3_phi.txt", unpack=True)

    x = np.linspace(100, 4500, 1000)
    t1 = phase(x, r1, l1, c1)
    t2 = phase(x, r2, l1, c1)
    t3 = phase(x, r3, l1, c1)

    plt.figure()
    plt.errorbar(x1,y1,yerr=yerr1, linestyle= 'None', color = 'orange')
    plt.plot(x1,y1, '.', label = "dati sperimentali R1", color = 'orange', markersize=5.0)
    plt.plot(x, t1, color='red', label='R1 (expected)')
    plt.xlim(100, 4500)
    plt.ylim(-1.25, 1.25)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("fase (rad)", fontsize=20.0)
    plt.title("Confronto tra fasi aspettate e sperimentali per R1", fontsize=30.0, fontname='sans-serif')
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0)
    plt.grid(True)

    plt.figure()
    plt.errorbar(x2,y2,yerr=yerr2, linestyle= 'None', color = 'orange')
    plt.plot(x2,y2, '.', label = "dati sperimentali R2", color = 'orange', markersize=5.0)
    plt.plot(x, t2, color='blue', label='R2 (expected)')
    plt.xlim(100, 4500)
    plt.ylim(-1, 1)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("fase (rad)", fontsize=20.0)
    plt.title("Confronto tra fasi aspettate e sperimentali per R2", fontsize=30.0, fontname='sans-serif')
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0)
    plt.grid(True)

    plt.figure()
    plt.errorbar(x3,y3,yerr=yerr3, linestyle= 'None', color = 'orange')
    plt.plot(x3,y3, '.', label = "dati sperimentali R3", color = 'orange', markersize=5.0)
    plt.plot(x, t3, color='green', label='R3 (expected)')
    plt.xlim(100, 4500)
    plt.ylim(-1, 1)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("fase (rad)", fontsize=20.0)
    plt.title("Confronto tra fasi aspettate e sperimentali per R3", fontsize=30.0, fontname='sans-serif')
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0)
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()