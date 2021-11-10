# SIR-Model
SIR & SEIR Model for a math exam.

# Description

### SIR.py
Implémentation du modèle SIR en python grace a solve_ivp.

### SEIR.py
Implémentation du modèle SEIR en python avec un solver utilisant la méthode d'euler explicite.

### SEIR (solve_ivp).py
Implémentation du modèle SEIR en python avec solve_ivp.

### SEIRV.py
Implémentation d'un modèle fait maison qui ajoute les personnes vaccinées au modèle.

### SEIGVM.py
Implémentation d'un modèle fait maison qui ajoute les personnes Mortes de la maladie au modèle.

# The Maths
![SEIR Model](https://raw.githubusercontent.com/ozeliurs-MaximeBilly/SIR-Model/main/content/SEIR.jpg)

# Inspiration
[CNRS: Modelisation d'une epidemie](https://images.math.cnrs.fr/Modelisation-d-une-epidemie.html)

[Wiki: SIR model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model)

[Wiki: SEIR model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SEIR_model)

# The Help needed
[scipy.integrate.odeint](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html)

[methode d'euler](https://www.f-legrand.fr/scidoc/docimg/numerique/euler/euler/euler.html)

[scipy.integrate.solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html#scipy.integrate.solve_ivp)

# TODO
- [x] SIR
- [x] SEIR
- [x] Autres Modèles
- [x] Moteur de résolution avec méthode d'euleur explicite (a gauche)
- [ ] Moteur de résolution avec méthode d'euleur explicite (a droite)
- [ ] Moteur de résolution avec méthode d'euleur explicite (a moyenne)
- [X] Simulation SIR
- [X] Simulation SEIR
- [X] Expliquer le moteur
- [X] Conclusion

# Gifs
## Mortalité = Natalité
![IMG](https://github.com/ozeliurs-MaximeBilly/SIR-Model/blob/main/gifs/Mort%3DNat.gif)
## Mortalité = 0%
![IMG](https://github.com/ozeliurs-MaximeBilly/SIR-Model/blob/main/gifs/Mort%3D0.gif)
## Natalité = 0%
![IMG](https://github.com/ozeliurs-MaximeBilly/SIR-Model/blob/main/gifs/Nat%3D0.gif)
