import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')

from scipy.optimize import curve_fit

def main(): # dati apparato sperimentale
    
    r1 = 820.77
    r2 = 2692
    r3 = 10012
    c = 101.8E-9
    l = 47.25E-3
    v0 = 5

    def vr(f, r, l, c):
        w = 2 * np.pi * f
        y = w**2 * l * c - 1
        arg = w * l / r / y
        A = (1 + arg**2)**(-1/2)
        phi = np.arctan(arg)
        return v0 * A * np.cos(phi) # funzione fit per ddp

    def phi(f, r, l, c):
        w = 2 * np.pi * f
        arg = l * w / r / (w**2 * l * c - 1)
        return np.arctan(arg)

    f0 = 1 / np.sqrt(l * c) / 2 / np.pi
    q1 = r1 * c * 2 * np.pi * f0
    q2 = r2 * c * 2 * np.pi * f0
    q3 = r3 * c * 2 * np.pi * f0

    print("frequenza di notch: ", f0)
    print("Q1: ", q1)
    print("Q2: ", q2)
    print("Q3: ", q3)

    x = np.linspace(100, 4500, 1000)
    y1 = vr(x, r1, l, c)
    y2 = vr(x, r2, l, c)
    y3 = vr(x, r3, l, c)
    p1 = phi(x, r1, l, c)
    p2 = phi(x, r2, l, c)
    p3 = phi(x, r3, l, c)
    
    plt.figure()
    plt.plot(x, y1, color='red', label='R1')
    plt.plot(x, y2, color='blue', label='R2')
    plt.plot(x, y3, color='green', label='R3')
    plt.xlim(100, 4500)
    plt.ylim(0, 6)
    plt.xlabel("Frequenza (1/s)", fontsize=20.0)
    plt.ylabel("Ddp misurata (V)", fontsize=20.0)
    plt.title("Funzione Vr", fontsize=30.0, fontname='sans-serif')
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0) 
    plt.grid(True)

    plt.figure()
    plt.plot(x, p1, color='red', label='R1')
    plt.plot(x, p2, color='blue', label='R2')
    plt.plot(x, p3, color='green', label='R3')
    plt.xlim(100, 4500)
    plt.ylim(-2, 2)
    plt.xlabel("Frequenza (1/s)", fontsize=20.0)
    plt.ylabel("Differenza di fase (rad)", fontsize=20.0)
    plt.title("Funzione phi = fase Vr - fase Vg", fontsize=30.0, fontname='sans-serif')
    plt.legend(loc='upper left', fontsize=14.0, markerscale=2.0) 
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main()