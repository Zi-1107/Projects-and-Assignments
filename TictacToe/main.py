import PySimpleGUI as sg
sg.theme('graygraygray')

def wcomb(row, col, connect):
    connect = connect
    win = []

    for i in range(row):
        for j in range(col - connect + 1):
            win.append({(i, j + k) for k in range(connect)})
    

    for j in range(col):
        for i in range(row - connect + 1):
            win.append({(i + k, j) for k in range(connect)})

    for i in range(row - connect + 1):
        for j in range(col - connect + 1):
            win.append({(i + k, j + k) for k in range(connect)})

    
    for i in range(row - connect + 1):
            for j in range(connect - 1, col):
                win.append({(i + k, j - k) for k in range(connect)})
            
    return(win)

class Player ():
    def __init__(self, sysmbol) -> None:
        self.sysmbol = sysmbol
        self.Is_win = False
        self.choice = set()

def main (row, col, connect):
    Player1 = Player("X")
    Player2 = Player("O")
    row = row
    col = col
    connect = connect
    wcombx = wcomb(row, col, connect)
    
    Avai_Choice = set()
    for i in range(row):
        for j in range(col):
            Avai_Choice.add((i,j))

    current_player = 0
    count = 1
    winner = 0
        
    while winner == 0:
        if count % 2 == 0:
            current_player = Player2
        else:
            current_player = Player1
        print(f"Player{current_player.sysmbol}'s Turn")
        row_in = int(input("ROw?"))
        col_in = int(input("Col?"))
        Avai_Choice.remove((row_in, col_in))
        current_player.choice.add((row_in, col_in))
        for x in wcombx:
            if x.issubset(current_player.choice) == True:
                winner = current_player.sysmbol
                print(f"Winner is Player{winner}")
                break
        count = count + 1
        if count > row * col and winner == 0:
            winner = "draw"
            print("It's a draw.")
            break

def generate (row, col, window:sg.Window):
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        if event == 'start':
            if values['33'] == True:
                row, col = (3, 3)
            elif values['1818'] == True:
                row, col = (18, 18)
            elif values['2727'] == True:
                row, col = (27, 27)
            
            for x in range(27):
                for y in range(27):
                    if x in range(row) and y in range(col):
                        window[(x, y)].update(disabled=False, visible=True, text="", button_color="white")
                    else:
                        window[(x, y)].update(disabled=True, visible=False, text="", button_color="white")

            # connect = window["connect"].get() = True
            connect_key = [x for x in window.key_dict if isinstance(x, str) and x[-1] == 'C' and values[x] == True]
            connect = int(connect_key[0][0] )
            win = wcomb(row, col, connect)
            Avai_Choice = set()
            for i in range(row):
                for j in range(col):
                    Avai_Choice.add((i,j))

            
            Player1 = Player("X")
            Player2 = Player("O")
            
            current_player = Player1
            count = 1
            winner = False
        if isinstance(event, tuple):
            window[event].update(text=current_player.sysmbol, disabled = True)
            current_player.choice.add(event)
            Avai_Choice.remove(event)
            for x in win:
                if x.issubset(current_player.choice):
                    winner = True
                    current_player.Is_win = True
                    combo = x
            if winner == True:
                for  i in combo:
                    window[i].update(button_color = "green")
                sg.popup(f'Player {current_player.sysmbol} wins!', title='Congratulations')
            else:
                if  len(Avai_Choice)==0:
                    sg.popup('It\'s a draw!',title="Draw")
                else:
                    count+=1
                    current_player = Player2 if count % 2 == 0 else Player1
                    
def b_window(row, col):
    topleft = [
        [sg.Text("Select Boxes", text_color="black", size=(12, None))],
        [sg.Radio("3 X 3", group_id="boxes", text_color="black",  default= True, key='33'), 
            sg.Radio("18 X 18", group_id="boxes", text_color="black",  default= False, key='1818'),
            sg.Radio("27 X 27", group_id="boxes", text_color="black",  default= False, key='2727')],
        [sg.HSep()],
        [sg.Text("Select Connect", text_color="black", size=(12, None))],
        [sg.Radio("3 in a row", group_id="connect", default= True, key='3C'),
            sg.Radio("4 in a row", group_id="connect", default= False, key='4C')]
    ]
    topright = [
        [sg.Button('GENERATE', key='start')],
    ]
    topleftcol = sg.Column(topleft)
    toprightcol = sg.Column(topright)
    toprow = [topleftcol,sg.VSep(), toprightcol]


    bottom = [sg.Element(key='out', type='')]
    for x in range(row):
        rowlist = []
        for y in range(col):
            rowlist.append(sg.Button(key=(x, y), size=(2, 1), pad=((0.1, 0.1), (0.1, 0.1))))
        bottom.append(rowlist)
        

    Layout = [toprow, [sg.HSep()], bottom]
    window = (sg.Window('tictactoe', layout=Layout, resizable=True))
    return(window)

if __name__ == "__main__":
    generate(3, 3, b_window(27, 27))