def imagen_random(lista_imagenes):
    from random import randrange
    return lista_imagenes[randrange(len(lista_imagenes))]

def color_aleatorio():
    from random import randint, randrange
    r = randrange(256)
    g = randrange(256)
    b = randrange(256)
    return (r, g, b)