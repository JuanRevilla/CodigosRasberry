
import numpy as np
from mandaangulo import mandaAngulo

def muevebola(cx, cy, x, y, paso):
    # Movemos el valor de las posiciones anteriores
    errorx= x-cx
    errory= y-cy
    if(abs(errorx) & abs(errory) ==0):
        return paso+1
    mandaAngulo(errorx,errory)
    return paso