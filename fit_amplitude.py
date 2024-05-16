import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')

from scipy.optimize import curve_fit

def main():

    r1 = 820.77 # dati apparato sperimentale
    r2 = 2692.
    r3 = 10012.
    c = 101.8E-9
    l = 47.25E-3
    v0 = 5.
    rgen = 50.
    rl = 120.41

    def amplitude(f, r, l, c, v0, rl, rgen):
        w = 2 * np.pi * f
        y = 1 - w**2 * l * c
        rtot = r + rgen
        smallnum = 2 * rl * rtot + rl**2 + (w * l)**2
        smallden = y**2 + (w * rl * c)**2
        num = rtot**2 + (smallnum / smallden)
        A = (num / (r**2))**(-1/2)
        return v0 * A

    def rcs(x, y , yerr, popt):
        residuals = y - amplitude(x, *popt)
        chi_squared = np.sum(((residuals/yerr)**2))
        ndof = len(x) - len(popt)
        return chi_squared / ndof

    f = 1 / np.sqrt(l * c) / 2 / np.pi # calcolo frequenze di notch e fattori di qualità
    q1 = r1 * c * 2 * np.pi * f
    q2 = r2 * c * 2 * np.pi * f
    q3 = r3 * c * 2 * np.pi * f
    print("FREQ NOTCH: ", f) # stampa a schermo frequenze di notch e fattori di qualità
    print("Q1: ", q1)
    print("Q2: ", q2)
    print("Q3: ", q3)

    x1,y1,yerr1 = np.loadtxt("r1_amp.txt", unpack=True)
    x2,y2,yerr2 = np.loadtxt("r2_amp.txt", unpack=True)
#     x3,y3,yerr3 = np.loadtxt("r3_amp.txt", unpack=True)

    P1 = [r1, l, c, v0, rl, rgen] # parametri liberi per i fit
    P2 = [r2, l, c, v0, rl, rgen]
    P3 = [r3, l, c, v0, rl, rgen]
    popt1, pcov1 = curve_fit(amplitude, x1, y1, p0=P1, sigma=yerr1,
                             bounds=([r1 - 200, l - 1E-2, c - 1E-5, v0 - 1, rl - 50, rgen - 20], [r1 + 200, l + 1E-2, c + 1E-5, v0 + 1, rl + 50, rgen + 20]), maxfev=50000) # fit
    popt2, pcov2 = curve_fit(amplitude, x2, y2, p0=P2, sigma=yerr2,
                             bounds=([r2 - 500, l - 1E-2, c - 1E-5, v0 - 1, rl - 50, rgen - 20], [r2 + 500, l + 1E-2, c + 1E-5, v0 + 1, rl + 50, rgen + 20]), maxfev=50000)
#     popt3, pcov3 = curve_fit(amplitude, x3, y3, p0=P3, sigma=yerr3, maxfev=50000)

    print("\nR1: ", popt1[0], "\nL: ", popt1[1], "\nC: ", popt1[2], "\nV0: ", popt1[3], "\nRl: ", popt1[4], "\nRgen: ", popt1[5],
           "\nX2 / ndf: ", rcs(x1, y1, yerr1, popt1), "\n\n") # stampa parametri dal fit (senza errori)
    print("\nR2: ", popt2[0], "\nL: ", popt2[1], "\nC: ", popt2[2], "\nV0: ", popt2[3], "\nRl: ", popt1[4], "\nRgen: ", popt1[5],
           "\nX2 / ndf: ", rcs(x2, y2, yerr2, popt2), "\n\n")
#     print("\nR3: ", popt3[0], "\nL: ", popt3[1], "\nC: ", popt3[2], "\nV0: ", popt3[3],
      #     "\nRgen: ", popt3[4], "\nRl: ", popt3[5], "\n\n")
    
    plt.figure()
    plt.errorbar(x1,y1,yerr=yerr1, linestyle= 'None', color = 'orange')
    plt.errorbar(x2,y2,yerr=yerr2, linestyle= 'None', color = 'teal')
#     plt.errorbar(x3,y3,yerr=yerr3, linestyle= 'None', color = 'yellowgreen')
    plt.plot(x1, y1, '.', label = "dati sperimentali R1", color = 'orange', markersize=7.0)
    plt.plot(x2, y2, '.', label = "dati sperimentali R2", color = 'teal', markersize=7.0)
#     plt.plot(x3, y3, '.', label = "dati sperimentali R3", color = 'yellowgreen', markersize=5.0)
    plt.plot(x1, amplitude(x1, *popt1), color = 'red', label = "R1 fit")
    plt.plot(x2, amplitude(x2, *popt2), color = 'blue', label = "R2 fit")
#     plt.plot(x3, amplitude(x3, *popt3), color = 'green', label = "R3 fit")
    plt.xlim(100, 4500)
    plt.ylim(0, 6)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("ampiezza (V)", fontsize=20.0)
    plt.legend(loc='lower left', fontsize=14.0, markerscale=2.0)
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()