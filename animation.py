import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

# Configuration de l'affichage de matplotlib
# matplotlib.use('Qt5Agg') # A utiliser sur Linux
matplotlib.use('TkAgg')  # A utiliser sur Windows

# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
INIT_ALPHA = 0.75  # Taux d'incubation (0-1)
INIT_BETA = 0.8  # Taux de transmission (0-1)
INIT_GAMMA = 0.05  # Taux de guérison (0-1)
INIT_MICRO = 0.01  # Taux de mortalité (0-1)
INIT_NU = 0.009  # Taux de natalité (0-0.5)

# Populations initiales
N0 = 1000  # Population
E0 = 0  # Nombre initial de personnes infectées non-infectieuses
I0 = 5  # Nombre initial de personnes infectées infectieuses
R0 = 0  # Nombre initial de personnes retirées
S0 = N0 - (I0 + R0 + E0)  # Nombre initial de personnes Saines

# Precision et durée de la simulation
SIM_PRECISION = 1000
SIM_MULTIPLIER = 2


def solve(S0, E0, I0, R0, alpha, beta, gamma, micro, nu):
    S, E, I, R = [S0], [E0], [I0], [R0]
    h = 1 / SIM_PRECISION
    for o in range(SIM_PRECISION * SIM_MULTIPLIER):
        St, Et, It, Rt = S[o - 1], E[o - 1], I[o - 1], R[o - 1]

        # Equations
        dSdt = -beta * St * It + nu * (St + Et + It + Rt) - micro * St
        dEdt = beta * St * It - alpha * Et - micro * Et
        dIdt = alpha * Et - gamma * It - micro * It
        dRdt = gamma * It - micro * Rt

        S.append(St + h * dSdt)
        E.append(Et + h * dEdt)
        I.append(It + h * dIdt)
        R.append(Rt + h * dRdt)
    return S, E, I, R


def init():
    return ln,


# The function to be called anytime a slider's value changes
def update(x):
    """
    Méthode appelée a chaque changement des sliders. Recalcule les courbes et les affiche.
    """
    if x<1:
        a, b, g, m, n = INIT_ALPHA, INIT_BETA, INIT_GAMMA, INIT_MICRO, x
    elif 1 <= x < 2:
        x -= 1
        a, b, g, m, n = INIT_ALPHA, INIT_BETA, INIT_GAMMA, x, INIT_NU
    elif 2 <= x < 3:
        x -= 2
        a, b, g, m, n = INIT_ALPHA, INIT_BETA, x, INIT_MICRO, INIT_NU
    elif 3 <= x < 4:
        x -= 3
        a, b, g, m, n = INIT_ALPHA, x, INIT_GAMMA, INIT_MICRO, INIT_NU
    else:
        x -= 4
        a, b, g, m, n = x, INIT_BETA, INIT_GAMMA, INIT_MICRO, INIT_NU
    S, E, I, R = solve(S0, E0, I0, R0, a, b, g, m, n)
    line1.set_ydata(S)
    line2.set_ydata(E)
    line3.set_ydata(I)
    line4.set_ydata(R)
    N = [S[i] + E[i] + I[i] + R[i] for i in range(len(S))]
    line5.set_ydata(N)
    alpha_slider.set_val(a)
    beta_slider.set_val(b)
    gamma_slider.set_val(g)
    micro_slider.set_val(m)
    nu_slider.set_val(n)
    fig.canvas.draw_idle()
    return ln,


def make_frame(x):
    update(x)
    return mplfig_to_npimage(fig)


S, E, I, R = solve(S0, E0, I0, R0, INIT_ALPHA, INIT_BETA, INIT_GAMMA, INIT_MICRO, INIT_NU)
N = [S[i] + E[i] + I[i] + R[i] for i in range(len(S))]

fig, ax = plt.subplots()
ax.margins(x=0)

line1, = plt.plot(S, label="Sains")
line2, = plt.plot(E, label="Exposed")
line3, = plt.plot(I, label="Infectes")
line4, = plt.plot(R, label="Recovered")
line5, = plt.plot(N, label="Population")
ln, = plt.plot(0)

# Ajustement des tracés principaux pour faire de la place aux sliders
plt.subplots_adjust(left=0.1, bottom=0.5, top=1)
ax.set_xlabel('Time [days]')
ax.legend()

# Slider Horizontal alpha
alpha_slider = Slider(
    ax=plt.axes([0.1, 0.25, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='α',
    valmin=0,
    valmax=1,
    valinit=INIT_ALPHA,
    color="grey"
)

# Slider Horizontal beta
beta_slider = Slider(
    ax=plt.axes([0.1, 0.20, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='β',
    valmin=0,
    valmax=1,
    valinit=INIT_BETA,
    color="red"
)

# Slider Horizontal gamma
gamma_slider = Slider(
    ax=plt.axes([0.1, 0.15, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='γ',
    valmin=0,
    valmax=1,
    valinit=INIT_GAMMA,
    color="green"
)

# Slider Horizontal micro
micro_slider = Slider(
    ax=plt.axes([0.1, 0.10, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='μ',
    valmin=0,
    valmax=2,
    valinit=INIT_MICRO,
    color="black"
)

# Slider Horizontal nu
nu_slider = Slider(
    ax=plt.axes([0.1, 0.05, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='ν',
    valmin=0,
    valmax=2,
    valinit=INIT_NU,
    color="pink"
)

# ani = FuncAnimation(fig, update, frames=[x/100 for x in range(0, 100)], init_func=init, blit=True)

animation = VideoClip(make_frame, duration=5)
animation.write_gif("output.gif", fps=20)
