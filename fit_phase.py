import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')

from scipy.optimize import curve_fit

def main():

    r1 = 820.77 # dati apparato sperimentale
    r2 = 2692
    r3 = 10012
    c = 101.8E-9
    l = 47.25E-3
    rgen = 50
    rl = 120.41
    m = 1.36E-5

    def phase(f, r, l, c, rgen, rl, m):
        w = 2 * np.pi * f
        y = 1 - w**2 * l * c
        rtot = r + rgen
        num = w * (rl**2 * c - y * l)
        den = rl + rtot * (y**2 + (rl * w * c)**2)
        return np.arctan(num / den) + m*f
    
    def rcs(x, y , yerr, popt):
        residuals = y - phase(x, *popt)
        chi_squared = np.sum(((residuals/yerr)**2))
        ndof = len(x) - len(popt)
        return chi_squared / ndof

    f1 = 1 / np.sqrt(l * c) / 2 / np.pi # calcolo frequenze di notch e fattori di qualità
    q1 = r1 * c * 2 * np.pi * f1
    q2 = r2 * c * 2 * np.pi * f1
    q3 = r3 * c * 2 * np.pi * f1
    print("FREQ NOTCH 1: ", f1) # stampa a schermo frequenze di notch e fattori di qualità
    print("Q1: ", q1)
    print("Q2: ", q2)
    print("Q3: ", q3)

    x1,y1,yerr1 = np.loadtxt("r1_phi.txt", unpack=True)
    x2,y2,yerr2 = np.loadtxt("r2_phi.txt", unpack=True)
#     x3,y3,yerr3 = np.loadtxt("r3_phi.txt", unpack=True)

    P1 = [r1, l, c, rgen, rl, m] # parametri liberi per i fit
    P2 = [r2, l, c, rgen, rl, m]
    P3 = [r3, l, c, rgen, rl, m]
    popt1, pcov1 = curve_fit(phase, x1, y1, p0=P1, sigma=yerr1, maxfev=50000) # fit
    popt2, pcov2 = curve_fit(phase, x2, y2, p0=P2, sigma=yerr2, maxfev=50000)
#     popt3, pcov3 = curve_fit(phase, x3, y3, p0=P3, sigma=yerr3, maxfev=50000)

    print("\nR1: ", popt1[0], "\nL: ", popt1[1], "\nC: ", popt1[2],
          "\nRgen: ", popt1[3], "\nRl: ", popt1[4], "\nm: ", popt1[5],
           "\nX2 / ndf: ", rcs(x1, y1, yerr1, popt1), "\n\n") # stampa parametri dal fit (senza errori)
    print("\nR2: ", popt2[0], "\nL: ", popt2[1], "\nC: ", popt2[2],
          "\nRgen: ", popt2[3], "\nRl: ", popt2[4], "\nm: ", popt2[5],
           "\nX2 / ndf: ", rcs(x2, y2, yerr2, popt2), "\n\n")
#     print("\nR3: ", popt3[0], "\nL: ", popt3[1], "\nC: ", popt3[2],
      #     "\nRgen: ", popt3[3], "\nRl: ", popt3[4], "\nm: ", popt3[5], "\n\n")
    
    plt.figure()
    plt.errorbar(x1,y1,yerr=yerr1, linestyle= 'None', color = 'orange')
    plt.plot(x1,y1, '.', label = "dati sperimentali R1", color = 'orange', markersize=7.0)
    plt.plot(x1, phase(x1, *popt1), color = 'red', label = "R1 fit")
    plt.xlim(100, 4500)
    plt.ylim(-1.25, 1.25)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("fase (rad)", fontsize=20.0)
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0)
    plt.grid(True)

    plt.figure()
    plt.errorbar(x2,y2,yerr=yerr2, linestyle= 'None', color = 'teal')
    plt.plot(x2,y2, '.', label = "dati sperimentali R2", color = 'teal', markersize=7.0)
    plt.plot(x2, phase(x2, *popt2), color = 'blue', label = "R2 fit")
    plt.xlim(100, 4500)
    plt.ylim(-1, 1)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("fase (rad)", fontsize=20.0)
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0)
    plt.grid(True)

#     plt.figure()
#     plt.errorbar(x3,y3,yerr=yerr3, linestyle= 'None', color = 'orange')
#     plt.plot(x3,y3, '.', label = "dati sperimentali R3", color = 'orange', markersize=7.0)
#     plt.plot(x3, phase(x3, *popt3), color = 'green', label = "R3 fit")
#     plt.xlim(100, 4500)
#     plt.ylim(-1, 1)
#     plt.xlabel("frequenza (Hz)", fontsize=20.0)
#     plt.ylabel("fase (rad)", fontsize=20.0)
#     plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0)
#     plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()