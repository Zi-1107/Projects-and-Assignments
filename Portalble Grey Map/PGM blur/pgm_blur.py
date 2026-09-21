def read_file(filename = r"C:\Users\ACER\Desktop\VS Code\PGM\PGM blur\cat1.pgm" ):
    
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

def convert_to_pgm(screen, width, height, max_b):
    with open("result.pgm", 'w') as file:
        
        file.write("P2\n")
        file.write(f"{width} {height}\n")
        file.write(f" {max_b}\n")
        
        for row in screen:
            temp = " ".join([str(num) for num in row])
            temp += "\n"
            file.write(temp)

def boxes(box_size, coord:tuple, pic:list):
    x , y = coord
    summ = 0
    count = 0
    for i in range(int(-((box_size -1)/2)), int((box_size -1)/2)+1):
        for j in range(int(-((box_size -1)/2)), int((box_size -1)/2)+1):
            if x + i < 0 or y + j < 0:
                continue
            if x + i >= len(pic) or y + j >= len(pic[0]):
                continue
            else:
                summ += pic[x + i][y + j]
                count += 1

    average = int(summ / count)
    return average

def blur(pic:list, width, height):
    box_size = int(input("?"))

    new_pic = []

    for i in range(len(pic)):
        placeholder = []
        for j in range(len(pic[0])):
                average = boxes(box_size, (i, j), pic)   
                placeholder.append(average)
        new_pic.append(placeholder)

    return new_pic

pic , width, height, max_b = read_file()
new_pic = blur(pic, width, height)
convert_to_pgm(new_pic, width, height, max_b)


