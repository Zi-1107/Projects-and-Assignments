import plotly.express as px
from matrix import matrix_multily_matrix as mxm
import math

arrow = [(-3, 0), (-2, 0), (-1, 0), (0,0), (1, 0), (2, 0), (3, 0), (4, 0), (1, 3), (1, -3), (2, 2), (2, -2), (3, 1), (3, -1)]
arrowx = [x[0] for x in arrow]
arrowy = [y[1] for y in arrow]


def translation(orgi, hori, vert):
    new = []

    for x, y in orgi:
        x_new, y_new = x+hori, y+vert
        new.append((x_new, y_new))

    return new

def refelct_axis(orgi, axis = "y"):
    factor_dict = {
        "y" : [[-1, 0], [0, 1]],
        "x" : [[1, 0], [0, -1]],
        "y=x" : [[0, 1], [1, 0]], 
        "y=-x" : [[0,-1], [-1, 0]]
    }
    factor = factor_dict[axis]
    orgi_matrix = [list(pts) for pts in orgi]
    img_matrix = mxm(orgi_matrix, factor)
    img_points = [tuple(pts) for pts in img_matrix]
    return img_points

def enlargment(orgi, factor:float = 2, factor2:float = 2):
    # factor = [[factor, 0], [0, factor]]
    factor2 = [[factor, 0], [0, factor2]]
    # enlargment is just identity matrix
    # factor 1 changes hori coor(x coor), factor 2 changes vert coor(y coor)
    orgi_matrix = [list(pts) for pts in orgi]
    img_matrix = mxm(orgi_matrix, factor2)
    img_points = [tuple(pts) for pts in img_matrix]
    return img_points

def rotation(orgi, angle:int = 0):
    angle = angle * math.pi/180
    orgi_matrix = [list(pts) for pts in orgi]
    factor = [[math.cos(angle), math.sin(angle)], [math.sin(angle)* -1 , math.cos(angle)]]
    img_matrix = mxm(orgi_matrix, factor)
    img_points = [tuple(pts) for pts in img_matrix]
    return img_points

def main():
   new_arrow = rotation(arrow, 45)
   arrowx = [x[0] for x in new_arrow]
   arrowy = [y[1] for y in new_arrow]
   fig = px.scatter(x = arrowx, y = arrowy)  
   fig.update_xaxes(showline=True, linewidth=2, linecolor="black")
   fig.update_yaxes(showline=True, linewidth=2, linecolor="black")
   fig.show()

if __name__ == "__main__":
    main()