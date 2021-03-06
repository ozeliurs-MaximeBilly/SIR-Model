import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Configuration de l'affichage de matplotlib
# matplotlib.use('Qt5Agg') # A utiliser sur Linux
matplotlib.use('TkAgg') # A utiliser sur Windows

# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
INIT_ALPHA = 0.75  # Taux d'incubation (0-1)
INIT_BETA = 0.8  # Taux de transmission (0-1)
INIT_GAMMA = 0.05  # Taux de guérison (0-1)
INIT_MICRO = 0.01  # Taux de mortalité (0-1)
INIT_NU = 0.009  # Taux de natalité (0-0.5)
INIT_EPSILON = 0.5  # Taux de vaccination (0-2)
INIT_DELTA = 0.2  # Taux de mortalité lié a la maladie (0-1)

# Populations initiales
N0 = 1000  # Population
E0 = 0  # Nombre initial de personnes infectées non-infectieuses
I0 = 5  # Nombre initial de personnes infectées infectieuses
G0 = 0  # Nombre initial de personnes guéris
S0 = N0 - (I0 + G0 + E0)  # Nombre initial de personnes Saines
V0 = 0  # Nombre initial de personnes vacinnées
M0 = 0  # Nombre initial de personnes mortes liées a la maladie

# Precision et durée de la simulation
SIM_PRECISION = 250
SIM_MULTIPLIER = 50


def solve(S0, E0, I0, G0, V0, M0, alpha, beta, gamma, micro, nu, epsilon, delta):
    S, E, I, G, V, M = [S0], [E0], [I0], [G0], [V0], [M0]
    h = 1/SIM_PRECISION
    for o in range(SIM_PRECISION*SIM_MULTIPLIER):
        St, Et, It, Gt, Vt, Mt = S[o-1], E[o-1], I[o-1], G[o-1], V[o-1], M[o-1]

        #Equations
        dSdt = -beta*St*It + nu*(St+Et+It+Gt+Vt) - micro*St - epsilon*St
        dEdt = beta*St*It - alpha*Et - micro*Et + beta*Gt
        dIdt = alpha*Et - gamma*It - micro*It - It*delta
        dGdt = gamma*It - micro*Gt - epsilon*Gt - beta*Gt
        dVdt = epsilon*St + epsilon*Gt - micro*Vt
        dMdt = It*delta

        S.append(St+h * dSdt)
        E.append(Et+h * dEdt)
        I.append(It+h * dIdt)
        G.append(Gt+h * dGdt)
        V.append(Vt+h * dVdt)
        M.append(Mt+h * dMdt)
    return S, E, I, G, V, M


# The function to be called anytime a slider's value changes
def update(_x):
    """
    Méthode appelée a chaque changement des sliders. Recalcule les courbes et les affiche.
    """
    S, E, I, G, V, M = solve(S0, E0, I0, G0, V0, M0, alpha_slider.val, beta_slider.val, gamma_slider.val, micro_slider.val, nu_slider.val, epsilon_slider.val, delta_slider.val)
    line1.set_ydata(S)
    line2.set_ydata(E)
    line3.set_ydata(I)
    line4.set_ydata(G)
    line5.set_ydata(V)
    line6.set_ydata(M)
    N = [S[i] + E[i] + I[i] + G[i] + V[i] for i in range(len(S))]
    line7.set_ydata(N)
    fig.canvas.draw_idle()


S, E, I, G, V, M = solve(S0, E0, I0, G0, V0, M0, INIT_ALPHA, INIT_BETA, INIT_GAMMA, INIT_MICRO, INIT_NU, INIT_EPSILON, INIT_DELTA)
N = [S[i] + E[i] + I[i] + G[i] + V[i] for i in range(len(S))]

fig, ax = plt.subplots()
ax.margins(x=0)

line1, = plt.plot(S, label="Healthy")
line2, = plt.plot(E, label="Exposed")
line3, = plt.plot(I, label="Infected")
line4, = plt.plot(G, label="Guéris")
line5, = plt.plot(V, label="Vaccinated")
line6, = plt.plot(M, label="Dead by Disease")
line7, = plt.plot(N, label="Population")

# Ajustement des tracés principaux pour faire de la place aux sliders
plt.subplots_adjust(left=0.1, bottom=0.5, top=1)
ax.set_xlabel('Time [days]')
ax.legend()

# Slider Horizontal alpha
alpha_slider = Slider(
    ax=plt.axes([0.1, 0.31, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='α (Incubation)',
    valmin=0,
    valmax=1,
    valinit=INIT_ALPHA,
    color="grey"
)

# Slider Horizontal beta
beta_slider = Slider(
    ax=plt.axes([0.1, 0.26, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='β (Transmission)',
    valmin=0,
    valmax=1,
    valinit=INIT_BETA,
    color="red"
)

# Slider Horizontal gamma
gamma_slider = Slider(
    ax=plt.axes([0.1, 0.21, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='γ (Guérison)',
    valmin=0,
    valmax=1,
    valinit=INIT_GAMMA,
    color="green"
)

# Slider Horizontal micro
micro_slider = Slider(
    ax=plt.axes([0.1, 0.16, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='μ (Mortalité)',
    valmin=0,
    valmax=1,
    valinit=INIT_MICRO,
    color="purple"
)

# Slider Horizontal nu
nu_slider = Slider(
    ax=plt.axes([0.1, 0.11, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='ν (Natalité)',
    valmin=0,
    valmax=0.5,
    valinit=INIT_NU,
    color="pink"
)

# Slider Horizontal epsilon
epsilon_slider = Slider(
    ax=plt.axes([0.1, 0.06, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='ϵ (Vaccination)',
    valmin=0,
    valmax=1,
    valinit=INIT_EPSILON,
    color="lightgreen"
)

delta_slider = Slider(
    ax=plt.axes([0.1, 0.01, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='δ (Mortalité Maladie)',
    valmin=0,
    valmax=1,
    valinit=INIT_DELTA,
    color="black"
)

# register the update function with each slider
alpha_slider.on_changed(update)
beta_slider.on_changed(update)
gamma_slider.on_changed(update)
micro_slider.on_changed(update)
nu_slider.on_changed(update)
epsilon_slider.on_changed(update)
delta_slider.on_changed(update)

plt.show()
