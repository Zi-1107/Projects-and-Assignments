from linear_transformation import translation, refelct_axis, enlargment, rotation

def read_file(filename = r"C:\Users\ACER\Desktop\VS Code\PGM\PGM transformation\cat1.pgm" ):
    
    with open(filename, "r") as myfile:
        lines = myfile.readlines()

        width, height = lines[1].split()
        width = int(width)
        height = int(height)
        max_b = int(lines[2])

    dit = []
    ph = []
    for line in lines[3:]:
        line = line.split()
        for x in line:
            if len(ph) >= width:
                dit.append(ph)
                ph = []
            ph.append(int(x))
    if len(ph) >= width:
                dit.append(ph)
                ph = []

    return dit, width, height, max_b

def convert_list_to_dict(picture:list):
    dic = {}
    for i, row in enumerate(picture):
        for j, col in enumerate(row):
            dic[(i, j)] = col
    return dic

def reflection(dic:dict, height:int, width:int, axis="x"):
    coords = list(dic.keys())
    greyscale = list(dic.values())
    
    new_coords = refelct_axis(coords, f"{axis}")

    new_dic = {}
    if axis == "x":
        for index, val in enumerate(new_coords):
            new_dic[(val[0], val[1]+height -1)] = greyscale[index]
    else:
        for index, val in enumerate(new_coords):
            new_dic[(val[0] + width - 1, val[1])] = greyscale[index]

    return new_dic
    
def convert_dict_to_list(dic:dict):
    screen = []

    coordi = list(dic.keys())
    x_coord = [coordi[0] for coordi in coordi]
    y_coord = [coordi[1] for coordi in coordi]
    max_x = max(x_coord) 
    max_y = max(y_coord)

    for y_c in range(max_x + 1):
        row = []
        for x_c in range(max_y + 1):
            row.append(0)
        screen.append(row)

    for coor, greyscale in dic.items():
        x , y = coor
        screen[x][y] = greyscale
        
    return screen, max_x+2, max_y+2

def convert_to_pgm(screen, width, height, max_b):
    with open("result.pgm", 'w') as file:
        
        file.write("P2\n")
        file.write(f"{width} {height}\n")
        file.write(f" {max_b}\n")
        
        for row in screen:
            temp = " ".join([str(num) for num in row])
            temp += "\n"
            file.write(temp)

def enlarge(dic:dict, scale=2):
    coords = list(dic.keys())
    greyscale = list(dic.values())

    new_coords = enlargment(coords, scale, scale)

    new_dic = {}
    for index, val in enumerate(new_coords):
        new_dic[(val[0]), val[1]] = greyscale[index]

        for x_add in range(scale):
            for y_add in range(scale):
                new_dic[(val[0]+x_add), val[1]+y_add] = greyscale[index]

    return new_dic

def rotate(dic:dict, angle:int = 180):
    coords = list(dic.keys())
    greyscale = list(dic.values())
    
    new_coords = rotation(coords, angle)
    new_coords = [(round(x), round(y)) for x, y in new_coords]

    x_coord = [coords[0] for coords in new_coords]
    y_coord = [coords[1] for coords in new_coords]
    min_x = min(x_coord)
    min_y = min(y_coord)

    new_coords = [(x if min_x >= 0 else x - min_x, y if min_y >= 0 else y - min_y) for x, y in coords]

    new_dic = {}
    for index, val in enumerate(new_coords):
        new_dic[(val[0], val[1])] = greyscale[index]

    return new_dic


picture, width_og, height_og, max_b = read_file()
og_coord = convert_list_to_dict(picture)
new_coord = rotate(og_coord, 45)
# new_coord = enlarge(og_coord, 5)
# new_coord = reflection(og_coord, height_og, width_og, "y")

screen, width, height = convert_dict_to_list(new_coord)
convert_to_pgm(screen, width, height, max_b)