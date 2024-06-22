import numpy as np
import matplotlib.pyplot as plt

# Definicja funkcji
def f(x):
    return (1 + np.log(x)) / x

x = np.linspace(0.1, 5, 400)
y = f(x)

# Wykres funkcji
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='f(x) = (1 + ln(x)) / x')
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.axvline(1, color='r', linestyle='--', label='x = 1 (max lokalne)')
plt.axhline(1, color='g', linestyle='--', label='y = 1 (max lokalne)')
plt.legend()
plt.title('Wykres funkcji f(x) = (1 + ln(x)) / x')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.show()
