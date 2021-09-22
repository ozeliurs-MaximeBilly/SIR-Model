import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.widgets import Slider

# The SIR model differential equations.
def deriv(y, t, N, alpha, beta, gamma, micro, mu):
    S, E, I, R, N = y
    dSdt = micro*N - micro*S - (beta*I*S)/N
    dEdt = (beta*I*S)/N - (micro+alpha)*E
    dIdt = alpha*E - (gamma+micro)*I
    dRdt = gamma*I - micro*R
    dNdt = N+(mu*N)-(micro*N)
    return dSdt, dEdt, dIdt, dRdt, dNdt

def solve(t):
    pass

# Total population, N.
N = 861635
# Initial number of infected and recovered individuals, I0 and R0.
I0 = 0
R0 = 0
E0 = 1
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0 - E0

# Starting necessary parameters for model
init_alpha = 0.75     # 0-1 incubation
init_beta = 0.8     #0-1 taux de transmission
init_gamma = 0.05     #0-1 guérison
init_micro = 0.01     #0-1 mortalité
init_mu = 0.009    #0-0.5 natalité

# A grid of time points (in days)
t = np.linspace(0, 365, 365)

# Initial conditions vector
y0 = S0, E0, I0, R0, N

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

ret = odeint(deriv, y0, t, args=(N, init_alpha, init_beta, init_gamma, init_micro, init_mu))
S, E, I, R, N = ret.T

Pop = []
Pop = [ Pop.append(N*init_micro**i) for i in range(len(S))]

line1, = plt.plot(S, label="Susceptible")
line2, = plt.plot(I, label="Infectious")
line3, = plt.plot(R, label="Recovered with Immunity")
line4, = plt.plot(E, label="Exposed")
line5, = plt.plot(N, label="Population")


ax.set_xlabel('Time [days]')
ax.legend()

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
    color=[52/255, 152/255, 219/255, 1]
)

# Make a horizontal slider to control the frequency.
beta_slider = Slider(
    ax = plt.axes([0.1, 0.20, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='β (Transmission)',
    valmin=0,
    valmax=1,
    valinit=init_beta,
    color=[231/255, 76/255, 60/255, 1]
)

# Make a horizontal slider to control the frequency.
gamma_slider = Slider(
    ax = plt.axes([0.1, 0.15, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='γ (Guérison)',
    valmin=0,
    valmax=1,
    valinit=init_gamma,
    color=[46/255, 204/255, 113/255, 1]
)

# Make a horizontal slider to control the frequency.
micro_slider = Slider(
    ax = plt.axes([0.1, 0.10, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='micro (Mortalité)',
    valmin=0,
    valmax=1,
    valinit=init_micro,
    color=[155/255, 89/255, 182/255, 1]
)

# Make a horizontal slider to control the frequency.
mu_slider = Slider(
    ax = plt.axes([0.1, 0.05, 0.8, 0.03], facecolor="lightgoldenrodyellow"),
    label='mu (Natalité)',
    valmin=0,
    valmax=0.5,
    valinit=init_mu,
    color=[243/255, 156/255, 18/255, 1]
)

# The function to be called anytime a slider's value changes
def update(val):
    ret = odeint(deriv, y0, t, args=(N, alpha_slider.val, beta_slider.val, gamma_slider.val, micro_slider.val, mu_slider.val))
    S, E, I, R, N = ret.T
    line1.set_ydata(S)
    line2.set_ydata(I)
    line3.set_ydata(R)
    line4.set_ydata(E)
    line5.set_ydata(N)
    fig.canvas.draw_idle()


# register the update function with each slider
alpha_slider.on_changed(update)
beta_slider.on_changed(update)
gamma_slider.on_changed(update)
micro_slider.on_changed(update)
mu_slider.on_changed(update)

plt.show()
