from typing import List
import PySimpleGUI as sg
import os
import random
# sg.theme('graygraygray')
def generate(filename):
    with open(filename, "r") as myfile:
        lines = myfile.readlines()
    numbers = []
    for line in lines:
        numbers.append(line.split(sep="\n", maxsplit=1)[0])
    rows = numbers
#----
    col = []
    col_n = len(numbers[0])
    for i in range(col_n):
        x = []
        for y in numbers:
            x.append(y[i])
        col.append(x)
    return(rows, col)

def generate_reference(filename):
    reference = {}
    with open(filename, "r") as myfile:
        lines = myfile.readlines()
        for r, x in enumerate(lines):
            for c, y in enumerate(x):
                if y == "0":
                    reference[(r, c)] = False
                else:
                    reference[(r, c)] = True

    print(reference)
    return(reference)

def generate_indicatior(numbers:List[int]):
    row = []
    for n in numbers:
        ind = []
        for x in n:
            x = int(x)
            if x == 0:
                ind.append(0)
            else:
                if len(ind) == 0:
                    ind.append(1)
                else:
                    if ind[-1] == 0:
                        ind.append(1)
                    else:
                        ind[-1] += 1
        ind = [x for x in ind if x > 0]
        row.append(ind)

    return(row)

def game_ui():

    mid = [[sg.Button(key="start", button_text="Start"), sg.Button(key="reset", button_text="Reset"), sg.Button(key="exit", button_text="Exit")],
           [sg.Text(key="lives", text="Lives :", pad=((1, 1), (1, 1))), sg.Text(key="lives_n", text= 3 * "\u2764\uFE0F"),
           sg.Button(key="X", button_text="   X   ", pad=((2, 2), (2, 2))), sg.Button(key="Box", button_color = "green", 
            button_text="   \u2588   ", pad=((2, 2), (2, 2)))]]

    top = [
        [sg.Text("Select Size", text_color="black", size=(12, None))],
        [sg.Radio("5 x 5", group_id="boxes", text_color="black",  default= False, key='33', enable_events=True), 
            sg.Radio("10 x 10", group_id="boxes", text_color="black",  default= False, key='1818', enable_events=True),
            sg.Radio("15 x 15", group_id="boxes", text_color="black",  default= False, key='2727', enable_events=True), 
            sg.Radio("Random", group_id="boxes", text_color="black", default=True , key="rrandom", enable_events=True)]]

    bottom = []
    toplist = []
    toplist.append(sg.Button(key=(-1, "ColN"), button_text=" ", disabled=True, button_color="white", 
            size=(10, 7), pad=((0.5, 0.5), (0.5, 0.5))))
    for x in range(15):
            toplist.append(sg.Button(key=(x, "ColN"), button_text=" ", disabled=True, button_color="white", 
            size=(3, 7), pad=((0.5, 0.5), (0.5, 0.5))))
    bottom.append(toplist)
    
    for x in range(15):
        rowlist = []
        rowlist.append(sg.pin(sg.Button(key=(x, "rowN"), button_text=" ", disabled=True, button_color="white", 
        size=(10, None), pad=((0.5, 0.5), (0.5, 0.5)))))
        for y in range(15):
            rowlist.append(sg.Button(key=(x, y), size=(3, None), pad=((0.5, 0.5), (0.5, 0.5))))
        bottom.append(rowlist)

    layout = [top, mid, [sg.HSep()], bottom]

    return layout
        
def window(layout, ref):
    lives = 3
    tool = ("\u2588" , True)
    radio = "random"
    window = (sg.Window('nonogram', layout=layout, resizable=True, finalize=True))
    window.Maximize()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'exit':
            break
        if event == "33":
            radio = "5x5"
            print(radio)
        if event == "1818":
            radio =  "10x10"
            print(radio)
        if event == "2727":
            radio =  "15x15"
            print(radio)
        if event == "rrandom":
            radio = "random"
            print(radio)
        if event == "start":
            if radio == "5x5":
                file = random.choice(os.listdir(r"C:\Users\ACER\Desktop\VS Code\nonogram5"))
                file = "nonogram\\" + file
                print(file)
                (x, y) = generate(file)
                row = generate_indicatior(x)
                col = generate_indicatior(y)
                layout = game_ui()
                ref = generate_reference(file)
                for x in range(15):
                    for y in range(15):
                        if x in range(len(row)) and y in range(len(col)):
                                window[(x, y)].update(disabled=False, visible=True, text="", button_color = "#062121")
                        else:
                            window[(x, y)].update(disabled=True, visible=False, text="", button_color = "#062121")

                for x in range(15):
                    if x in range(len(row)):
                        window[(x, "rowN")].update(visible=True, text=row[x])
                    else:
                        window[(x, "rowN")].update(visible=False, text=" ")
                for x in range(15):
                    if x in range(len(col)):
                        window[(x, "ColN")].update(visible=True, text='\n'.join(str(z) for z in col[x]))
                    else:
                        window[(x, "ColN")].update(visible=False, text=" ")
                        # xxx
                lives = 3
                window["lives_n"].update(lives * "\u2764\uFE0F")
            if radio == "10x10":
                file = random.choice(os.listdir(r"C:\Users\ACER\Desktop\VS Code\nonogram10"))
                file = "nonogram\\" + file
                print(file)
                (x, y) = generate(file)
                row = generate_indicatior(x)
                col = generate_indicatior(y)
                layout = game_ui()
                ref = generate_reference(file)
                for x in range(15):
                    for y in range(15):
                        if x in range(len(row)) and y in range(len(col)):
                                window[(x, y)].update(disabled=False, visible=True, text="", button_color = "#062121")
                        else:
                            window[(x, y)].update(disabled=True, visible=False, text="", button_color = "#062121")

                for x in range(15):
                    if x in range(len(row)):
                        window[(x, "rowN")].update(visible=True, text=row[x])
                    else:
                        window[(x, "rowN")].update(visible=False, text=" ")
                for x in range(15):
                    if x in range(len(col)):
                        window[(x, "ColN")].update(visible=True, text='\n'.join(str(z) for z in col[x]))
                    else:
                        window[(x, "ColN")].update(visible=False, text=" ")
                        # xxx
                lives = 3
                window["lives_n"].update(lives * "\u2764\uFE0F")
            if radio == "15x15":
                file = random.choice(os.listdir(r"C:\Users\ACER\Desktop\VS Code\nonogram15"))
                file = "nonogram\\" + file
                print(file)
                (x, y) = generate(file)
                row = generate_indicatior(x)
                col = generate_indicatior(y)
                layout = game_ui()
                ref = generate_reference(file)
                for x in range(15):
                    for y in range(15):
                        if x in range(len(row)) and y in range(len(col)):
                                window[(x, y)].update(disabled=False, visible=True, text="", button_color = "#062121")
                        else:
                            window[(x, y)].update(disabled=True, visible=False, text="", button_color = "#062121")

                for x in range(15):
                    if x in range(len(row)):
                        window[(x, "rowN")].update(visible=True, text=row[x])
                    else:
                        window[(x, "rowN")].update(visible=False, text=" ")
                for x in range(15):
                    if x in range(len(col)):
                        window[(x, "ColN")].update(visible=True, text='\n'.join(str(z) for z in col[x]))
                    else:
                        window[(x, "ColN")].update(visible=False, text=" ")
                        # xxx
                lives = 3
                window["lives_n"].update(lives * "\u2764\uFE0F")
            elif radio == "random":
                file = random.choice(os.listdir(r"C:\Users\ACER\Desktop\VS Code\nonogram"))
                file = "nonogram\\" + file
                print(file)
                (x, y) = generate(file)
                row = generate_indicatior(x)
                col = generate_indicatior(y)
                layout = game_ui()
                ref = generate_reference(file)
                for x in range(15):
                    for y in range(15):
                        if x in range(len(row)) and y in range(len(col)):
                                window[(x, y)].update(disabled=False, visible=True, text="", button_color = "#062121")
                        else:
                            window[(x, y)].update(disabled=True, visible=False, text="", button_color = "#062121")

                for x in range(15):
                    if x in range(len(row)):
                        window[(x, "rowN")].update(visible=True, text=row[x])
                    else:
                        window[(x, "rowN")].update(visible=False, text=" ")
                for x in range(15):
                    if x in range(len(col)):
                        window[(x, "ColN")].update(visible=True, text='\n'.join(str(z) for z in col[x]))
                    else:
                        window[(x, "ColN")].update(visible=False, text=" ")
                        # xxx
                lives = 3
                window["lives_n"].update(lives * "\u2764\uFE0F")
        if event == "X":
            window[event].update(button_color = "green")
            tool = ("X", False)
            window["Box"].update(button_color = "#062121")
        if event == "Box":
            window[event].update(button_color = "green")
            tool = ("\u2588" , True)
            window["X"].update(button_color = "#062121")
        if isinstance(event, tuple):
            window[event].update(text=tool[0])
            r = event[0]
            c = event[1]
            if ref[(r, c)] == tool[1]:
                window[event].update(text = tool[0], disabled = True)
            else:
                lives -=1
                window["lives_n"].update(lives * "\u2764\uFE0F")
                window[event].update(button_color = "red", disabled = True)
            if lives == 0:
                sg.popup_annoying("u died")
                for x in range(15):
                    for y in range(15):
                        if x in range(len(row)) and y in range(len(col)):
                            window[(x, y)].update(disabled=True)
        if event == "reset":
            x, y = 15, 15
            lives = 3
            window["lives_n"].update(lives * "\u2764\uFE0F")
            for x in range(15):
                    for y in range(15):
                        if x in range(len(row)) and y in range(len(col)):
                                window[(x, y)].update(disabled=False, visible=True, text="", button_color = "#062121")
                        else:
                            window[(x, y)].update(disabled=True, visible=False, text="", button_color = "#062121")
    window.close()

if __name__ == "__main__":
   (x, y) = generate("nonogram\\pic1_5_5.txt")
   row = generate_indicatior(x)
   col = generate_indicatior(y) 
   layout = game_ui()
   ref = generate_reference("nonogram\\pic1_5_5.txt")
   window(layout, ref)
   