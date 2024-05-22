import numpy as np

f1_amp = 2265.98
f2_amp = 2294.08
f3_amp = 2337.65
f1_phi = 2255.3
f2_phi = 2281.96
f3_phi = 2336.54

freq = [f1_amp, f2_amp, f3_amp, f1_phi, f2_phi, f3_phi]
mean = np.mean(freq)
devstd = np.std(freq)
semi = (f3_amp - f1_phi) / 2

print("Media: ", mean)
print("Deviazione standard: ", devstd)
print("Semidispersione massima: ", semi)