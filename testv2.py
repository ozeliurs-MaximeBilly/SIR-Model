import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.widgets import Slider

# Configuration de l'affichage de matplotlib
matplotlib.use('TkAgg')


# --- FONCTIONS ---
# Equations differentielles du modèle SEIR
def SEIR(t_max, dt, alpha, beta, gamma, micro, mu, N, S0, E0, I0, R0):
    t = 0
    S, E, I, R = S0, E0, I0, R0
    Sl, El, Il, Rl, Tl = ([], [], [], [], [])

    while t < t_max:
        S = -beta*S*I + mu*N + micro*S
        E = beta*S*I - alpha*E - micro*E
        I = alpha*E - (gamma+micro)*I
        R = gamma*I - micro*R

        Sl.append(S)
        plt.scatter(t, S)
        El.append(E)
        Il.append(I)
        Rl.append(R)
        Tl.append(t)
        t += dt

    return Sl, El, Il, Rl


# --- PARAMETRES INITIAUX ---
N = 1000        # Population
E0 = 0          # Nombre initial de personnes infectées non-infectieuses
I0 = 5          # Nombre initial de personnes infectées infectieuses
R0 = 0          # Nombre initial de personnes retirées
S0 = N - (I0 + R0 + E0) # Nombre initial de personnes Saines


# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
init_alpha = 0.75     # Taux d'incubation (0-1)
init_beta = 0.8     # Taux de transmission (0-1)
init_gamma = 0.05     # Taux de guérison (0-1)
init_micro = 0.01     # Taux de mortalité (0-1)
init_mu = 0.009    # Taux de natalité (0-0.5)


# Résolution des équations différentielles avec les paramètres Initiaux
S, E, I, R = SEIR(160, 0.1, init_alpha, init_beta, init_gamma, init_micro, init_mu, N, S0, E0, I0, R0)

plt.show()
