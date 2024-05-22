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
    dl = 0.4725E-3
    dc = 1.018E-9

    def phase(f, r, l, c, m, rl):
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
    
    def deltaf(l, c, dl, dc):
        a = dl / (2 * np.sqrt(c * l**3))
        b = dc / (2 * np.sqrt(l * c**3))
        return (a + b)

    f = 1 / np.sqrt(l * c) / 2 / np.pi
    # q1 = r1 * c * 2 * np.pi * f
    # q2 = r2 * c * 2 * np.pi * f
    # q3 = r3 * c * 2 * np.pi * f
    # print("Q1: ", q1)
    # print("Q2: ", q2)
    # print("Q3: ", q3)

    x1,y1,yerr1 = np.loadtxt("r1_phi.txt", unpack=True)
    x2,y2,yerr2 = np.loadtxt("r2_phi.txt", unpack=True)
    x3,y3,yerr3 = np.loadtxt("r3_phi.txt", unpack=True)

    P1 = [r1, l, c, m, rl] # parametri liberi per i fit
    P2 = [r2, l, c, m, rl]
    P3 = [r3, l, c, m, rl]
    popt1, pcov1 = curve_fit(phase, x1, y1, p0=P1, sigma=yerr1,
                             bounds=([r1 - 80, l - 5E-3, c - 1E-8, m - 1E-6, rl - 15], [r1 + 80, l + 5E-3, c + 1E-8, m + 2E-6, rl + 15]), maxfev=50000) # fit
    popt2, pcov2 = curve_fit(phase, x2, y2, p0=P2, sigma=yerr2,
                             bounds=([r2 - 270, l - 5E-3, c - 1E-8, m - 1E-6, rl - 15], [r2 + 270, l + 5E-3, c + 1E-5, m + 2E-6, rl + 15]), maxfev=50000)
    popt3, pcov3 = curve_fit(phase, x3, y3, p0=P3, sigma=yerr3,
                             bounds=([r3 - 1000, l - 5E-3, c - 1E-8, m - 1E-6, rl - 15], [r3 + 1000, l + 5E-3, c + 1E-5, m + 2E-6, rl + 15]), maxfev=50000)

    rcs1 = rcs(x1, y1, yerr1, popt1)
    rcs2 = rcs(x2, y2, yerr2, popt2)
    rcs3 = rcs(x3, y3, yerr3, popt3)
    print("\nR1: ", popt1[0], " ± ", np.sqrt(pcov1[0,0]), "\nL: ", popt1[1], " ± ", np.sqrt(pcov1[1,1]),
          "\nC: ", popt1[2], " ± ", np.sqrt(pcov1[2,2]), "\nm: ", popt1[3], " ± ", np.sqrt(pcov1[3,3]),
          "\nRl: ", popt1[4]," ± ", np.sqrt(pcov1[4,4]), "\nX2 / ndf: ", rcs1, "\n")
    print("\nR2: ", popt2[0], " ± ", np.sqrt(pcov2[0,0]), "\nL: ", popt2[1], " ± ", np.sqrt(pcov2[1,1]),
          "\nC: ", popt2[2], " ± ", np.sqrt(pcov2[2,2]), "\nm: ", popt2[3], " ± ", np.sqrt(pcov2[3,3]),
          "\nRl: ", popt2[4]," ± ", np.sqrt(pcov2[4,4]), "\nX2 / ndf: ", rcs2, "\n")
    print("\nR3: ", popt3[0], " ± ", np.sqrt(pcov3[0,0]), "\nL: ", popt3[1], " ± ", np.sqrt(pcov3[1,1]),
          "\nC: ", popt3[2], " ± ", np.sqrt(pcov3[2,2]), "\nm: ", popt3[3], " ± ", np.sqrt(pcov3[3,3]),
          "\nRl: ", popt3[4]," ± ", np.sqrt(pcov3[4,4]), "\nX2 / ndf: ", rcs3, "\n\n")
    
    f1 = 1 / (2 * np.pi * np.sqrt(popt1[1] * popt1[2]))
    f2 = 1 / (2 * np.pi * np.sqrt(popt2[1] * popt2[2]))
    f3 = 1 / (2 * np.pi * np.sqrt(popt3[1] * popt3[2]))
    print("FREQ NOTCH ASPETTATA: ", f , " ± ", deltaf(l, c, dl, dc) )
    print("FREQ NOTCH DA FIT SENZA INCERTEZZE")
    print("Da fit di R1: ", f1)
    print("Da fit di R2: ", f2)
    print("Da fit di R3: ", f3)
    
    plt.figure()
    plt.errorbar(x1,y1,yerr=yerr1, linestyle= 'None', color = 'orange')
    plt.plot(x1,y1, '.', label = "dati sperimentali R1", color = 'orange', markersize=7.0)
    plt.plot(x1, phase(x1, *popt1), color = 'red', label = "R1 fit")
    plt.xlim(100, 4500)
    plt.ylim(-1, 1)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("fase (rad)", fontsize=20.0)
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0)
    plt.grid(True)

    plt.figure()
    plt.errorbar(x2,y2,yerr=yerr2, linestyle= 'None', color = 'teal')
    plt.plot(x2,y2, '.', label = "dati sperimentali R2", color = 'teal', markersize=7.0)
    plt.plot(x2, phase(x2, *popt2), color = 'blue', label = "R2 fit")
    plt.xlim(100, 4500)
    plt.ylim(-0.6, 0.6)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("fase (rad)", fontsize=20.0)
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0)
    plt.grid(True)

    plt.figure()
    plt.errorbar(x3,y3,yerr=yerr3, linestyle= 'None', color = 'yellowgreen')
    plt.plot(x3,y3, '.', label = "dati sperimentali R3", color = 'yellowgreen', markersize=7.0)
    plt.plot(x3, phase(x3, *popt3), color = 'green', label = "R3 fit")
    plt.xlim(100, 4500)
    plt.ylim(-0.3, 0.3)
    plt.xlabel("frequenza (Hz)", fontsize=20.0)
    plt.ylabel("fase (rad)", fontsize=20.0)
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0)
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()