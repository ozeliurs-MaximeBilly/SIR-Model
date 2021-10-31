import random
import time
from math import sqrt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

# Configuration de l'affichage de matplotlib
# matplotlib.use('Qt5Agg')  # A utiliser sur Linux
matplotlib.use('TkAgg')  # A utiliser sur Windows


# Populations initiales
N0 = 300  # Population
E0 = 0  # Nombre initial de personnes infectées non-infectieuses
I0 = 10  # Nombre initial de personnes infectées infectieuses
R0 = 0  # Nombre initial de personnes retirées
S0 = N0 - (I0 + R0 + E0)  # Nombre initial de personnes Saines

# Longeur du tableau de jeu
X_LEN = 100
Y_LEN = 100

THR = 2  # Contamination area
INCUBATION_TIME = 30
GAMMA = 0.03

list_of_ppl = []
history = []

fig, ax = plt.subplots()
ax.set_autoscale_on(False)



def gen_ppl():
    lst = []
    for _ in range(S0):
        lst.append({"x": random.random() * X_LEN, "y": random.random() * Y_LEN,
                    "x_vect": random.random() - 0.5, "y_vect": random.random() - 0.5,
                    "S": True, "E": False, "I": False, "R": False, "incubation": INCUBATION_TIME})

    for _ in range(E0):
        lst.append({"x": random.random() * X_LEN, "y": random.random() * Y_LEN,
                    "x_vect": random.random() - 0.5, "y_vect": random.random() - 0.5,
                    "S": False, "E": True, "I": False, "R": False, "incubation": INCUBATION_TIME})

    for _ in range(I0):
        lst.append({"x": random.random() * X_LEN, "y": random.random() * Y_LEN,
                    "x_vect": random.random() - 0.5, "y_vect": random.random() - 0.5,
                    "S": False, "E": False, "I": True, "R": False, "incubation": INCUBATION_TIME})

    for _ in range(R0):
        lst.append({"x": random.random() * X_LEN, "y": random.random() * Y_LEN,
                    "x_vect": random.random() - 0.5, "y_vect": random.random() - 0.5,
                    "S": False, "E": False, "I": False, "R": True, "incubation": INCUBATION_TIME})

    return lst


def contaminate(lst):
    for ppl in lst:
        if ppl["I"]:
            for ppl2 in lst:
                if ppl2["S"] and sqrt( (ppl["x"]-ppl2["x"])**2 + (ppl["y"]-ppl2["y"])**2 ) <= THR:
                    ppl2["E"] = True
                    ppl2["S"] = False
    return lst


def incubate(lst):
    for ppl in lst:
        if ppl["E"]:
            ppl["incubation"] -= 1
            if ppl["incubation"] == 0:
                ppl["E"] = False
                ppl["I"] = True
    return lst


def get_rekt(lst):
    for ppl in lst:
        if ppl["I"]:
            if random.random() < GAMMA:
                ppl["I"] = False
                ppl["R"] = True
                ppl["x_vect"] = 0
                ppl["y_vect"] = 0
    return lst


def render(lst):
    ax.cla()
    ax.plot([0, X_LEN], [0,0], linewidth=1, color='black')
    ax.plot([X_LEN, X_LEN], [0, Y_LEN], linewidth=1, color='black')
    ax.plot([X_LEN, 0], [Y_LEN, Y_LEN], linewidth=1, color='black')
    ax.plot([0, 0], [Y_LEN, 0], linewidth=1, color='black')
    for ppl in lst:
        if ppl["S"]:
            ax.scatter(ppl["x"], ppl["y"], color="blue")
        elif ppl["E"]:
            ax.scatter(ppl["x"], ppl["y"], color="yellow")
        elif ppl["I"]:
            ax.scatter(ppl["x"], ppl["y"], color="red")
        elif ppl["R"]:
            ax.scatter(ppl["x"], ppl["y"], color="grey")
        else:
            ax.scatter(ppl["x"], ppl["y"], color="black")


def update(x):
    global history
    global list_of_ppl

    history.append([x,
                    len([x for x in list_of_ppl if x["S"]]),
                    len([x for x in list_of_ppl if x["E"]]),
                    len([x for x in list_of_ppl if x["I"]]),
                    len([x for x in list_of_ppl if x["R"]])])

    for ppl in list_of_ppl:
        ppl["x"] += ppl["x_vect"]
        ppl["y"] += ppl["y_vect"]
        if ppl["x"] < 0 or ppl["x"] > X_LEN:
            ppl["x_vect"] = -ppl["x_vect"]
        if ppl["y"] < 0 or ppl["y"] > Y_LEN:
            ppl["y_vect"] = -ppl["y_vect"]

    list_of_ppl = contaminate(list_of_ppl)
    list_of_ppl = incubate(list_of_ppl)
    list_of_ppl = get_rekt(list_of_ppl)

    render(list_of_ppl)


def make_frame(x):
    update(x)
    return mplfig_to_npimage(fig)


def bouboules_without_render(duration, fps):
    for i in range(duration*fps):
        print(f"\r{i}/{duration * fps} ~{round(i / (duration * fps) * 100, 1)} %", end="")
        i = i/fps
        update(i)


def main(ren):
    global list_of_ppl
    list_of_ppl = gen_ppl()
    render(list_of_ppl)
    if ren == 0:
        t = time.perf_counter()
        ani = FuncAnimation(fig, update, interval=10)
        print(f"The simulation + render took {time.perf_counter()-t} s.")
        plt.show()
    elif ren == 1:
        animation = VideoClip(make_frame, duration=40)
        animation.write_gif("output.gif", fps=20)
    elif ren == 2:
        t = time.perf_counter()
        bouboules_without_render(40,20)
        print(f"The simulation took {time.perf_counter() - t} s.")


if __name__ == "__main__":
    main(2)

    days = [x[0] for x in history]
    S = [x[1] for x in history]
    E = [x[2] for x in history]
    I = [x[3] for x in history]
    R = [x[4] for x in history]

    plt.subplot(2, 1, 1)
    plt.bar(days, R, color='grey', label='R')
    plt.bar(days, I, color='red', bottom=R, label='I')
    plt.bar(days, E, color='yellow', bottom=[I[i]+R[i] for i in range(len(I))], label='E')
    plt.bar(days, S, color='blue', bottom=[E[i]+I[i]+R[i] for i in range(len(I))], label='S')

    plt.legend()
    plt.show()