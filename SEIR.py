import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.widgets import Slider

# The SIR model differential equations.
def deriv(y, t, N, alpha, beta, gamma, micro, nu):
    S, E, I, R = y
    dSdt = micro*N - micro*S - (beta*I*S)/N
    dEdt = (beta*I*S)/N - (micro+alpha)*E
    dIdt = alpha*E - (gamma+micro)*I
    dRdt = gamma*I - micro*R
    return dSdt, dEdt, dIdt, dRdt

# Total population, N.
N = 1000
# Initial number of infected and recovered individuals, I0 and R0.
I0 = 0
R0 = 0
E0 = 1
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0 - E0

# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
init_alpha = 0.75     # 0-1 incubation
init_beta = 0.8     #0-1 taux de transmission
init_gamma = 0.05     #0-1 guérison
init_micro = 0.01     #0-1 mortalité
init_mu = 0.009    #0-0.5 natalité

# A grid of time points (in days)
t = np.linspace(0, 160, 160)

# Initial conditions vector
y0 = S0, E0, I0, R0

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

ret = odeint(deriv, y0, t, args=(N, init_alpha, init_beta, init_gamma, init_micro, init_mu))
S, E, I, R = ret.T

line1, = plt.plot(S, label="Susceptible")

line2, = plt.plot(I, label="Infected")
line3, = plt.plot(R, label="Recovered with Immunity")
line4, = plt.plot(E, label="Exposed")


ax.set_xlabel('Time [days]')

ax.margins(x=0)

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.1, bottom=0.4)

# Make a horizontal slider to control the frequency.
alpha_slider = Slider(
    ax = plt.axes([0.1, 0.25, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='alpha (Incubation)',
    valmin=0,
    valmax=1,
    valinit=init_alpha,
    color="green"
)

# Make a horizontal slider to control the frequency.
beta_slider = Slider(
    ax = plt.axes([0.1, 0.20, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='β (Transmission)',
    valmin=0,
    valmax=1,
    valinit=init_beta,
    color="purple"
)

# Make a horizontal slider to control the frequency.
gamma_slider = Slider(
    ax = plt.axes([0.1, 0.15, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='γ (Guérison)',
    valmin=0,
    valmax=1,
    valinit=init_gamma,
    color="green"
)

# Make a horizontal slider to control the frequency.
micro_slider = Slider(
    ax = plt.axes([0.1, 0.10, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='micro (Mortalité)',
    valmin=0,
    valmax=1,
    valinit=init_micro,
    color="green"
)

# Make a horizontal slider to control the frequency.
mu_slider = Slider(
    ax = plt.axes([0.1, 0.05, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='mu (Natalité)',
    valmin=0,
    valmax=0.5,
    valinit=init_mu,
    color="green"
)

# The function to be called anytime a slider's value changes
def update(val):
    ret = odeint(deriv, y0, t, args=(N, alpha_slider.val, beta_slider.val, gamma_slider.val, micro_slider.val, mu_slider.val))
    S, E, I, R = ret.T
    line1.set_ydata(S)
    line2.set_ydata(I)
    line3.set_ydata(R)
    line4.set_ydata(E)
    fig.canvas.draw_idle()


# register the update function with each slider
alpha_slider.on_changed(update)
beta_slider.on_changed(update)
gamma_slider.on_changed(update)
micro_slider.on_changed(update)
mu_slider.on_changed(update)

plt.show()
