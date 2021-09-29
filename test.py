import matplotlib.pyplot as plt

k=11
m=0.1
x=0.05
v=0
t=0
dt=0.01

courbe = []
time = []

while t<2:
    a=-k*x/m
    v=v+a*dt
    x=x+v*dt
    courbe.append(x)
    time.append(t)
    print(t,x)
    t=t+dt

plt.scatter(time, courbe)
plt.show()