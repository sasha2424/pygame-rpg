import numpy as np


V = "aeiouy"
C = "bcdfghjklmnpqrstvwxz"

V = "aeo"
C = "kfnhprtkfnhprtkfnhprtbcdklmsp"

def rand_letter(L):
    n = np.random.randint(len(L))
    return L[n]

def rand_sylable():
    r = ""
    if np.random.rand() < .1:
        r += rand_letter(V)
    if np.random.rand() < .9:
        r += rand_letter(C)
    if np.random.rand() < .1:
        r += rand_letter(C)
    if np.random.rand() < .5:
        r += rand_letter(V)
    return r

def name_gen():
    r = ""
    for i in range(np.random.randint(3,5)):
        r += rand_sylable()
    return r
