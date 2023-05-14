#este codigo sirve para leer el archivo json y nos debuelve los vectores
import json
def extraexy(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    # Extract x and y coordinates into separate lists
    x = [pos['x'] for pos in data['positions']]
    y = [pos['y'] for pos in data['positions']]

    return x,y