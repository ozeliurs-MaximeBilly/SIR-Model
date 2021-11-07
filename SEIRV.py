import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Configuration de l'affichage de matplotlib
# matplotlib.use('Qt5Agg')  # A utiliser sur Linux
matplotlib.use('TkAgg')  # A utiliser sur Windows

# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
INIT_ALPHA = 0.75  # Taux d'incubation (0-1)
INIT_BETA = 0.8  # Taux de transmission (0-1)
INIT_GAMMA = 0.05  # Taux de guérison (0-1)
INIT_MICRO = 0.01  # Taux de mortalité (0-1)
INIT_NU = 0.009  # Taux de natalité (0-0.5)
INIT_EPSILON = 0.5  # Taux de vaccination (0-2)

# Populations initiales
N0 = 1000  # Population
E0 = 0  # Nombre initial de personnes infectées non-infectieuses
I0 = 5  # Nombre initial de personnes infectées infectieuses
R0 = 0  # Nombre initial de personnes retirées
S0 = N0 - (I0 + R0 + E0)  # Nombre initial de personnes Saines
V0 = 0  # Nombre initial de personnes vacinnées

# Precision et durée de la simulation
SIM_PRECISION = 1000
SIM_MULTIPLIER = 2


def solve(S0, E0, I0, R0, V0, alpha, beta, gamma, micro, nu, epsilon):
    S, E, I, R, V = [S0], [E0], [I0], [R0], [V0]
    h = 1/SIM_PRECISION
    for o in range(SIM_PRECISION*SIM_MULTIPLIER):
        St, Et, It, Rt, Vt = S[o-1], E[o-1], I[o-1], R[o-1], V[o-1]

        # Equations
        dSdt = -beta*St*It + nu*(St+Et+It+Rt+Vt) - micro*St - epsilon*St
        dEdt = beta*St*It - alpha*Et - micro*Et
        dIdt = alpha*Et - gamma*It - micro*It
        dRdt = gamma*It - micro*Rt - epsilon*Rt
        dVdt = epsilon*St + epsilon*Rt - micro*Vt

        S.append(St+h * dSdt)
        E.append(Et+h * dEdt)
        I.append(It+h * dIdt)
        R.append(Rt+h * dRdt)
        V.append(Vt+h * dVdt)
    return S, E, I, R, V


# The function to be called anytime a slider's value changes
def update(_x):
    """
    Méthode appelée a chaque changement des sliders. Recalcule les courbes et les affiche.
    """
    S, E, I, R, V = solve(S0, E0, I0, R0, V0, alpha_slider.val, beta_slider.val, gamma_slider.val, micro_slider.val, nu_slider.val, epsilon_slider.val)
    line1.set_ydata(S)
    line2.set_ydata(E)
    line3.set_ydata(I)
    line4.set_ydata(R)
    line5.set_ydata(V)
    N = [S[i] + E[i] + I[i] + R[i] + V[i] for i in range(len(S))]
    line6.set_ydata(N)
    fig.canvas.draw_idle()


S, E, I, R, V = solve(S0, E0, I0, R0, V0, INIT_ALPHA, INIT_BETA, INIT_GAMMA, INIT_MICRO, INIT_NU, INIT_EPSILON)
N = [S[i] + E[i] + I[i] + R[i] + V[i] for i in range(len(S))]

fig, ax = plt.subplots()
ax.margins(x=0)

line1, = plt.plot(S, label="Sains")
line2, = plt.plot(E, label="Exposed")
line3, = plt.plot(I, label="Infectes")
line4, = plt.plot(R, label="Recovered")
line5, = plt.plot(V, label="Vaccinated")
line6, = plt.plot(N, label="Population")

# Ajustement des tracés principaux pour faire de la place aux sliders
plt.subplots_adjust(left=0.1, bottom=0.5, top=1)
ax.set_xlabel('Time [days]')
ax.legend()

# Slider Horizontal alpha
alpha_slider = Slider(
    ax=plt.axes([0.1, 0.25, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='α (Incubation)',
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
    valmax=1,
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
    valmax=1,
    valinit=INIT_MICRO,
    color="black"
)

# Slider Horizontal nu
nu_slider = Slider(
    ax=plt.axes([0.1, 0.05, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='ν (Natalité)',
    valmin=0,
    valmax=0.5,
    valinit=INIT_NU,
    color="pink"
)

# Slider Horizontal epsilon
epsilon_slider = Slider(
    ax=plt.axes([0.1, 0.30, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='ϵ (Vaccination)',
    valmin=0,
    valmax=1,
    valinit=INIT_EPSILON,
    color="lightgreen"
)

# register the update function with each slider
alpha_slider.on_changed(update)
beta_slider.on_changed(update)
gamma_slider.on_changed(update)
micro_slider.on_changed(update)
nu_slider.on_changed(update)
epsilon_slider.on_changed(update)

plt.show()
