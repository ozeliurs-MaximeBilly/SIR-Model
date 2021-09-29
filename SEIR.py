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
        # A revoir !!!!!
        S = -beta*S*I + mu*N + micro*S
        E = beta*S*I - alpha*E - micro*E
        I = alpha*E - (gamma+micro)*I
        R = gamma*I - micro*R

        Sl.append(S)
        El.append(E)
        Il.append(I)
        Rl.append(R)
        Tl.append(t)
        t += dt

    return Sl, El, Il, Rl


# The function to be called anytime a slider's value changes
def update(val):
    S, E, I, R = SEIR(160, 0.1, alpha_slider.val, beta_slider.val, gamma_slider.val, micro_slider.val, mu_slider.val, N, S0, E0, I0, R0)
    line1.set_ydata(S)
    line2.set_ydata(I)
    line3.set_ydata(R)
    line4.set_ydata(E)
    fig.canvas.draw_idle()


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

# Une grille de points de temps (en jours)
t = np.linspace(0, 50, 50)

# Creation & Configuration d'un subplot pour l'affichage des courbes d'evolution
fig, ax = plt.subplots()
ax.margins(x=0)

# Résolution des équations différentielles avec les paramètres Initiaux
S, E, I, R = SEIR(160, 0.1, init_alpha, init_beta, init_gamma, init_micro, init_mu, N, S0, E0, I0, R0)

# Ajout des courbes d'évolution avec leurs labels
line1, = plt.plot(S, label="Susceptible")
line2, = plt.plot(I, label="Infected")
line3, = plt.plot(R, label="Recovered with Immunity")
line4, = plt.plot(E, label="Exposed")

# Ajustement des tracés principaux pour faire de la place aux sliders
plt.subplots_adjust(left=0.1, bottom=0.4)
ax.set_xlabel('Time [days]')
ax.legend()

# Slider Horizontal alpha
alpha_slider = Slider(
    ax = plt.axes([0.1, 0.25, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='alpha (Incubation)',
    valmin=0,
    valmax=1,
    valinit=init_alpha,
    color="green"
)

# Slider Horizontal beta
beta_slider = Slider(
    ax = plt.axes([0.1, 0.20, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='β (Transmission)',
    valmin=0,
    valmax=1,
    valinit=init_beta,
    color="purple"
)

# Slider Horizontal gamma
gamma_slider = Slider(
    ax = plt.axes([0.1, 0.15, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='γ (Guérison)',
    valmin=0,
    valmax=1,
    valinit=init_gamma,
    color="green"
)

# Slider Horizontal micro
micro_slider = Slider(
    ax = plt.axes([0.1, 0.10, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='micro (Mortalité)',
    valmin=0,
    valmax=1,
    valinit=init_micro,
    color="green"
)

# Slider Horizontal mu
mu_slider = Slider(
    ax = plt.axes([0.1, 0.05, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='mu (Natalité)',
    valmin=0,
    valmax=0.5,
    valinit=init_mu,
    color="green"
)


# register the update function with each slider
alpha_slider.on_changed(update)
beta_slider.on_changed(update)
gamma_slider.on_changed(update)
micro_slider.on_changed(update)
mu_slider.on_changed(update)

plt.show()
