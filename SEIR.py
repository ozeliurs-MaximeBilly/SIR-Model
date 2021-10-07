import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.widgets import Slider

# Configuration de l'affichage de matplotlib
matplotlib.use('Qt5Agg')


## Fonctions
# Equations differentielles du modèle SEIR
def deriv(t, y, alpha, beta, gamma, micro, mu):
    S, E, I, R = y
    dSdt = -beta*S*I + mu*(S+E+I+R) + micro*S
    dEdt = beta*S*I - alpha*E - micro*E
    dIdt = alpha*E - (gamma+micro)*I
    dRdt = gamma*I - micro*R
    return dSdt, dEdt, dIdt, dRdt


# The function to be called anytime a slider's value changes
def update(val):
    ret = solve_ivp(fun=deriv, t_span=(0, Sim_Time), t_eval=t, dense_output=True, y0=(S0, E0, I0, R0), method='DOP853', args=(alpha_slider.val, beta_slider.val, gamma_slider.val, micro_slider.val, mu_slider.val))
    S, E, I, R = ret.y
    line1.set_ydata(S)
    line2.set_ydata(I)
    line3.set_ydata(R)
    line4.set_ydata(E)
    N = [S[i]+E[i]+I[i]+R[i] for i in range(len(S))]
    line5.set_ydata(N)
    fig.canvas.draw_idle()


## Paramètres Initiaux
Sim_Time = 100   # Simulation time
Sim_Precision = 100 # Samples per day

N0 = 1000        # Population
E0 = 0          # Nombre initial de personnes infectées non-infectieuses
I0 = 5          # Nombre initial de personnes infectées infectieuses
R0 = 0          # Nombre initial de personnes retirées
S0 = N0 - (I0 + R0 + E0) # Nombre initial de personnes Saines


# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
init_alpha = 0.75     # Taux d'incubation (0-1)
init_beta = 0.1     # Taux de transmission (0-1)
init_gamma = 0.05     # Taux de guérison (0-1)
init_micro = 0.2     # Taux de mortalité (0-1)
init_mu = 0.2    # Taux de natalité (0-0.5)

# Une grille de points de temps (en jours)
t = np.linspace(0, Sim_Time, Sim_Time*Sim_Precision)

# Creation & Configuration d'un subplot pour l'affichage des courbes d'evolution
fig, ax = plt.subplots()
ax.margins(x=0)
ax.autoscale(True)

# Résolution des équations différentielles avec les paramètres Initiaux
ret = solve_ivp(fun=deriv, t_span=(0, Sim_Time), t_eval=t, dense_output=True, y0=(S0, E0, I0, R0), method='DOP853', args=(init_alpha, init_beta, init_gamma, init_micro, init_mu))
S, E, I, R = ret.y

# Ajout des courbes d'évolution avec leurs labels
line1, = plt.plot(S, label="Susceptible")
line2, = plt.plot(I, label="Infected")
line3, = plt.plot(R, label="Recovered with Immunity")
line4, = plt.plot(E, label="Exposed")
N = [S[i]+E[i]+I[i]+R[i] for i in range(len(S))]
line5, = plt.plot(N, label="Population")

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
    color="grey"
)

# Slider Horizontal beta
beta_slider = Slider(
    ax = plt.axes([0.1, 0.20, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='β (Transmission)',
    valmin=0,
    valmax=0.05,
    valinit=init_beta,
    color="red"
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
    label='μ (Mortalité)',
    valmin=0,
    valmax=0.2,
    valinit=init_micro,
    color="black"
)

# Slider Horizontal mu
mu_slider = Slider(
    ax = plt.axes([0.1, 0.05, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='ν (Natalité)',
    valmin=0,
    valmax=0.5,
    valinit=init_mu,
    color="white"
)


# register the update function with each slider
alpha_slider.on_changed(update)
beta_slider.on_changed(update)
gamma_slider.on_changed(update)
micro_slider.on_changed(update)
mu_slider.on_changed(update)

plt.show()
