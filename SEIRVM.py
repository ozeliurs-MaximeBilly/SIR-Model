#!/usr/bin/env python3

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.widgets import Slider

# Configuration de l'affichage de matplotlib
matplotlib.use('Qt5Agg')
#matplotlib.use('TkAgg')


# --- Fonctions ---
# Equations differentielles du modèle SEIR
def deriv(_t, y, alpha, beta, gamma, micro, nu, tv, mv):
    """
    Methode regroupant les équations differentielles du modèle SEIR.
    """
    S, E, I, R, V, M= y
    dSdt = -beta * S * I + nu * (S + E + I + R + V) - micro * S - tv*S
    dEdt = beta * S * I - alpha * E - micro * E + beta*R
    dIdt = alpha * E - ((gamma + micro) * I) - mv*I
    dRdt = gamma * I  - micro * R  - tv*R -beta*R
    dVdt = tv*S + tv*R - micro*V
    dMdt = mv *I
    return dSdt, dEdt, dIdt, dRdt, dVdt, dMdt


# The function to be called anytime a slider's value changes
def update(_x):
    """
    Méthode appelée a chaque changement des sliders. Recalcule les courbes et les affiche.
    """
    solution = solve_ivp(fun=deriv, t_span=(0, SIM_TIME), t_eval=t, dense_output=True, y0=(S0, E0, I0, R0, V0, M0), method='DOP853',
                         args=(alpha_slider.val, beta_slider.val, gamma_slider.val, micro_slider.val, nu_slider.val, tv_slider.val, mv_slider.val))
    S, E, I, R, V, M = solution.y
    line1.set_ydata(S)
    line2.set_ydata(I)
    line3.set_ydata(R)
    line4.set_ydata(E)
    line5.set_ydata(V)
    N = [S[i] + E[i] + I[i] + R[i] +V[i] for i in range(len(S))]
    line6.set_ydata(N)
    line7.set_ydata(M)
    fig.canvas.draw_idle()


# --- Paramètres Initiaux ---
SIM_TIME = 50  # Simulation time
SIM_PRECISION = 250  # Samples per day

N0 = 1000  # Population
E0 = 0  # Nombre initial de personnes infectées non-infectieuses
I0 = 5  # Nombre initial de personnes infectées infectieuses
R0 = 0  # Nombre initial de personnes retirées
V0 = 0  # Nombre initial de personnes vacinnées
M0 = 0  # Nombre initial de personnes mortes
S0 = N0 - (I0 + R0 + E0)  # Nombre initial de personnes Saines

# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
INIT_ALPHA = 0.75  # Taux d'incubation (0-1)
INIT_BETA = 0.1  # Taux de transmission (0-1)
INIT_GAMMA = 0.05  # Taux de guérison (0-1)
INIT_MICRO = 0.01  # Taux de mortalité (0-1)
INIT_NU = 0.01  # Taux de natalité (0-0.5)
INIT_TV = 0.1
INIT_MV = 0.1

# Une grille de points de temps (en jours)
t = np.linspace(0, SIM_TIME, SIM_TIME * SIM_PRECISION)

# Creation & Configuration d'un subplot pour l'affichage des courbes d'evolution
fig, ax = plt.subplots()
ax.margins(x=0)
ax.autoscale(True)

# Résolution des équations différentielles avec les paramètres Initiaux
ret = solve_ivp(fun=deriv, t_span=(0, SIM_TIME), t_eval=t, dense_output=True, y0=(S0, E0, I0, R0, V0, M0), method='DOP853',
                args=(INIT_ALPHA, INIT_BETA, INIT_GAMMA, INIT_MICRO, INIT_NU, INIT_TV, INIT_MV))
S, E, I, R, V, M= ret.y

# Ajout des courbes d'évolution avec leurs labels
line1, = plt.plot(S, label="Susceptible")
line2, = plt.plot(I, label="Infected")
line3, = plt.plot(R, label="Recovered with Immunity")
line4, = plt.plot(E, label="Exposed")
line5, = plt.plot(V, label= "Vaccinated")
N = [S[i] + E[i] + I[i] + R[i] + V[i] for i in range(len(S))]
line6, = plt.plot(N, label="Population")
line7, = plt.plot(M, label="morts")
# Ajustement des tracés principaux pour faire de la place aux sliders
plt.subplots_adjust(left=0.1, bottom=0.4)
ax.set_xlabel('Time [days]')
ax.legend()

# Slider Horizontal alpha
alpha_slider = Slider(
    ax=plt.axes([0.1, 0.25, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='alpha (Incubation)',
    valmin=0,
    valmax=1,
    valinit=INIT_ALPHA,
    color="grey"
)

# Slider Horizontal beta
beta_slider = Slider(
    ax=plt.axes([0.1, 0.20, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='β (Transmission)',
    valmin=0,
    valmax=0.05,
    valinit=INIT_BETA,
    color="red"
)

# Slider Horizontal gamma
gamma_slider = Slider(
    ax=plt.axes([0.1, 0.15, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='γ (Guérison)',
    valmin=0,
    valmax=1,
    valinit=INIT_GAMMA,
    color="green"
)

# Slider Horizontal micro
micro_slider = Slider(
    ax=plt.axes([0.1, 0.10, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='μ (Mortalité)',
    valmin=0,
    valmax=0.013,
    valinit=INIT_MICRO,
    color="black"
)

# Slider Horizontal nu
nu_slider = Slider(
    ax=plt.axes([0.1, 0.05, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='ν (Natalité)',
    valmin=0,
    valmax=0.013,
    valinit=INIT_NU,
    color="white"
)

tv_slider = Slider(
    ax=plt.axes([0.1, 0.30, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='tv (vaccination)',
    valmin=0,
    valmax=0.13,
    valinit=INIT_TV,
    color="brown"
)

mv_slider = Slider(
    ax=plt.axes([0.1, 0.00, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='mv (mortalite du virus)',
    valmin=0,
    valmax=0.13,
    valinit=INIT_TV,
    color="brown"
)
# register the update function with each slider
alpha_slider.on_changed(update)
beta_slider.on_changed(update)
gamma_slider.on_changed(update)
micro_slider.on_changed(update)
nu_slider.on_changed(update)
tv_slider.on_changed(update)
mv_slider.on_changed(update)
plt.show()
