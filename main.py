import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.widgets import Slider, Button


# The parametrized function to be plotted
def f(t, amplitude, frequency):
    return amplitude * np.sin(2 * np.pi * frequency * t)

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# The parametrized function to be plotted
def f(t, beta, gamma):
    # Total population, N.
    N = 1000
    # Initial number of infected and recovered individuals, I0 and R0.
    I0, R0 = 1, 0
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - R0
    
    
    
    return 

t = np.linspace(0, 160, 160)

# Define initial parameters
init_amplitude = 5
init_frequency = 3

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = plt.plot(t, f(t, init_amplitude, init_frequency), lw=2)
ax.set_xlabel('Time [s]')

ax.margins(x=0)

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
freq_slider = Slider(
    ax = plt.axes([0.25, 0.1, 0.55, 0.03], facecolor="red"),
    label='Beta',
    valmin=0,
    valmax=1,
    valinit=init_frequency,
)

# Make a horizontal slider to control the frequency.
amp_slider = Slider(
    ax = plt.axes([0.25, 0.06, 0.55, 0.03], facecolor="green"),
    label='Gamma',
    valmin=0,
    valmax=1,
    valinit=init_frequency,
)

# The function to be called anytime a slider's value changes
def update(val):
    
    
    
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    line.set_ydata(S)
    line.set_ydata(I)
    line.set_ydata(R)
    fig.canvas.draw_idle()


# register the update function with each slider
freq_slider.on_changed(update)
amp_slider.on_changed(update)

plt.show()


"""

fig, ax = plt.subplots()
line, = plt.plot(t, f(t, init_amplitude, init_frequency), lw=2)

def f(beta, gamma):
  ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
  ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
  ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')

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
beta, gamma = 0.5, 1./10
# A grid of time points (in days)
t = np.linspace(0, 160, 160)

# Initial conditions vector
y0 = S0, I0, R0

# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

# Plot the data on three separate curves for S(t), I(t) and R(t)
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)

f(beta, gamma)

ax.set_xlabel('Time /days')
ax.set_ylabel('Number (1000s)')
ax.set_ylim(0,1.2)

ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')

legend = ax.legend()
legend.get_frame().set_alpha(0.5)

plt.show()
"""
