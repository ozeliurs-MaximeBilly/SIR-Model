import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.widgets import Slider, Button

# Configuration de l'affichage de matplotlib
# matplotlib.use('Qt5Agg') # A utiliser sur Linux
matplotlib.use('TkAgg') # A utiliser sur Windows

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Total population, N.
N = 1000
# Initial number of infected and recovered individuals, I0 and R0.
I0, R0 = 1, 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
init_beta, init_gamma = 0.5, 1./10
# A grid of time points (in days)
t = np.linspace(0, 160, 160)

# Initial conditions vector
y0 = S0, I0, R0

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

ret = odeint(deriv, y0, t, args=(N, init_beta, init_gamma))
S, I, R = ret.T

line1, = plt.plot(S, label="Susceptible")
line2, = plt.plot(I, label="Infected")
line3, = plt.plot(R, label="Recovered with Immunity")

ax.set_xlabel('Time [s]')

ax.margins(x=0)
ax.legend()

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.1, bottom=0.5, top=1)

# Make a horizontal slider to control the frequency.
beta_slider = Slider(
    ax = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='β (Transmission)',
    valmin=0,
    valmax=1,
    valinit=init_beta,
    color="purple"
)

# Make a horizontal slider to control the frequency.
gamma_slider = Slider(
    ax = plt.axes([0.1, 0.06, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='γ (Guérison)',
    valmin=0,
    valmax=1,
    valinit=init_gamma,
    color="green"
)

# The function to be called anytime a slider's value changes
def update(val):
    ret = odeint(deriv, y0, t, args=(N, beta_slider.val, gamma_slider.val))
    S, I, R = ret.T
    line1.set_ydata(S)
    line2.set_ydata(I)
    line3.set_ydata(R)
    fig.canvas.draw_idle()


# register the update function with each slider
beta_slider.on_changed(update)
gamma_slider.on_changed(update)

plt.show()
