import pygame as pg
import random 

pg.font.init()

s_width = 800
s_height = 700
p_width = 330	
p_height = 600
block_s = 30

game_x = (s_width - p_width) // 2
game_y = s_height - p_height

S = [['.....',
	  '......',
	  '..00..',
	  '.00...',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..00.',
	  '...0.',
	  '.....']]

Z = [['.....',
	  '.....',
	  '.00..',
	  '..00.',
	  '.....'],
	 ['.....',
	  '..0..',
	  '.00..',
	  '.0...',
	  '.....']]

I = [['.....',
	  '..0..',
	  '..0..',
	  '..0..',
	  '..0..'],
	 ['.....',
	  '0000.',
	  '.....',
	  '.....',
	  '.....']]

O = [['.....',
	  '.....',
	  '.00..',
	  '.00..',
	  '.....']]

J = [['.....',
	  '.0...',
	  '.000.',
	  '.....',
	  '.....'],
	 ['.....',
	  '..00.',
	  '..0..',
	  '..0..',
	  '.....'],
	 ['.....',
	  '.....',
	  '.000.',
	  '...0.',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..0..',
	  '.00..',
	  '.....']]

L = [['.....',
	  '...0.',
	  '.000.',
	  '.....',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..0..',
	  '..00.',
	  '.....'],
	 ['.....',
	  '.....',
	  '.000.',
	  '.0...',
	  '.....'],
	 ['.....',
	  '.00..',
	  '..0..',
	  '..0..',
	  '.....']]

T = [['.....',
	  '..0..',
	  '.000.',
	  '.....',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..00.',
	  '..0..',
	  '.....'],
	 ['.....',
	  '.....',
	  '.000.',
	  '..0..',
	  '.....'],
	 ['.....',
	  '..0..',
	  '.00..',
	  '..0..',
	  '.....']]

shapes = [
	{"shape": S, "color": (0, 255, 0) },
	{"shape": Z, "color": (255, 0, 0) },
	{"shape": I, "color": (0, 255, 255)},
	{"shape": O, "color": (255, 255, 0)},
	{"shape": J, "color": (255, 165, 0)},
	{"shape": L, "color": (0, 0, 255)},
	{"shape": T, "color": (128, 0, 128)}
]

class Piece:
	def __init__(self, col:int , row:int, shape):
		self.x = col
		self.y = row
		self.shape = shape
		self.color = [s for s in shapes if s["shape"] == shape][0]['color']
		self.rotation = 0

def gen_grid(occupied_state={}):
	"""
	occupied format = {(x, y): (r, g, b)}
	"""
	grid = []
	for row_i in range(int(p_height/block_s)):
		row = []
		for col_i in range(int(p_width/block_s)):
			if (col_i, row_i) in occupied_state:
				row.append(occupied_state[(col_i, row_i)])
			else:
				row.append((0, 0, 0))
		grid.append(row)

	return grid

def get_shape():
	global shapes
	choice = random.choice(range(7))
	chosen_shape = shapes[choice]
	return Piece(5,0, chosen_shape["shape"])

def draw_grid_lines(surface):
	for n in range(int(p_height/block_s)):
		pg.draw.line(surface, (128,128,128), (game_x, game_y + n*block_s), (game_x + p_width, game_y + n*block_s))
	for n in range(int(p_width/block_s)):
		pg.draw.line(surface, (128,128,128), (game_x + n*block_s, game_y), (game_x + n*block_s, game_y + p_height))

def draw_grid(surface, grid, score=0, last_score=0):
	surface.fill((0,0,0))
	# Tetris Title
	font = pg.font.SysFont('Aerial', 60)
	label = font.render('TETRIS', 1, (255,255,255))
	surface.blit(label, (game_x + p_width / 2 - (label.get_width() / 2), 30))

	font = pg.font.SysFont('Aerial', 30)
	label = font.render('Score: ' + str(score), 1, (255,255,255))

	sx = game_x + p_width + 50
	sy = game_y + p_height/2 - 100

	surface.blit(label, (sx + 20, sy + 160))
	# last score
	label = font.render('High Score: ' + str(last_score), 1, (255,255,255))

	sx = game_x - 200
	sy = game_y + 200
	
	for i, row in enumerate(grid):
		for j, row_item in enumerate(row):
			pg.draw.rect(surface, (grid[i][j]),  (game_x + j* 30, game_y + i * 30, 30, 30), 0)
	
	draw_grid_lines(surface)
	pg.draw.rect(surface, (128,128,128), (game_x, game_y, p_width, p_height), 5)
	pg.display.update()

def check_bound(shape, grid):
	empty_spaces = []
	for i, row in enumerate(grid):
		for j, pixel in enumerate(row):
			if pixel == (0, 0, 0):
				empty_spaces.append((j, i))

	shape_occupied_space = convert_shape(shape)

	for coor in shape_occupied_space:
		if coor not in empty_spaces:
			if coor[1] > -1:
				return False
		
	return True

def check_lost(positions):
	for pos in positions:
		if pos[1] < 1:
			return True
	return False

def convert_shape(piece:Piece):
	position = []
	layout = piece.shape[piece.rotation % len(piece.shape)]

	for i, row in enumerate(layout):
		for  j, symbol in enumerate(row):
			if symbol == "0":
				position.append((piece.x + j - 2, piece.y + i - 4))

	return position

def draw_next(surface, piece:Piece):
	font = pg.font.SysFont('Aerial', 30)
	label = font.render("Next Shape", 1, (255,255,255))

	sx = game_x + p_width + 50
	sy = game_y + p_height / 2 - 100
	shape = piece.shape[piece.rotation % len(piece.shape)]

	for i, line in enumerate(shape):
		row = list(line)
		for j, column in enumerate(row):
			if column =='0':
				pg.draw.rect(surface, piece.color, (sx + j*block_s, sy+i*block_s, block_s, block_s), 0)  

	surface.blit(label, (sx + 10, sy - 30))

def clear_row(grid, locked:{}): # type: ignore
	rows_to_clear = []
	for i in range(len(grid)-1,-1,-1):
		row = grid[i]
		if (0, 0, 0) not in row:
			rows_to_clear.append(i)
			for j in range(len(row)):
				print(locked)
				del locked[(j, i)]

	temp = {}
	for coord, color in locked.items():
		x, y = coord
		if y not in temp:
			temp[y] = {coord: color}
		else:
			temp[y][coord] = color

	temp = sorted(temp.items(), key=lambda x:x[0], reverse = True)

	start = len(grid) -1
	for k, v in temp:
		for coor, colr in v.items():
			del locked[coor]
			locked[(coor[0], start)] = colr
				
		start -= 1

	return len(rows_to_clear)

def draw_text_middle(surface, text, size, color):
    font = pg.font.SysFont("Aerial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (game_x + p_width /2 - (label.get_width()/2), game_y + p_height/2 - label.get_height()/2))

def main_menu(win):  # *
	run = True
	while run:
		win.fill((0,0,0))
		draw_text_middle(win, 'TETRIS', 60, (255,255,255))
		pg.display.update()
		for event in pg.event.get():
			if event.type == pg.QUIT:
				run = False
			if event.type == pg.KEYDOWN:
				main()

	pg.display.quit()

def update_score(nscore):
    score = max_score()

    with open(r'C:\Users\ACER\Desktop\VS Code\tetris\assets\scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open(r'C:\Users\ACER\Desktop\VS Code\tetris\assets\scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score

def main():
	global grid 

	score = 0
	last_score = max_score()

	locked_position = {}	# (x,y):(255,0,0)
	grid = gen_grid(locked_position)
	changed_piece = False
	run = True
	current_piece = get_shape()
	next_piece = get_shape()
	clock = pg.time.Clock()
	fall_time = 0


	while run:
		fall_speed = 0.2

		grid = gen_grid(locked_position)
		fall_time += clock.get_rawtime()
		clock.tick()
	
		if fall_time/1000 >= fall_speed:
			fall_time = 0
			current_piece.y += 1
			if not (check_bound(current_piece, grid)) and current_piece.y > 0:
				current_piece.y -= 1
				changed_piece = True
		
		grid = gen_grid(locked_position)
		

		for event in pg.event.get():
			if event.type == pg.QUIT:
				run = False
				pg.display.quit()
				quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_LEFT:
					current_piece.x  -= 1
					if not check_bound(current_piece, grid):
						current_piece.x += 1
				elif event.key == pg.K_RIGHT:
					current_piece.x  += 1
					if not check_bound(current_piece, grid):
						current_piece.x -= 1
				elif event.key == pg.K_UP:
					current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
					if not check_bound(current_piece, grid):
						current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
				elif event.key == pg.K_DOWN:
					current_piece.y  += 1
					if not check_bound(current_piece, grid):
						current_piece.y -= 1

		shape_pos = convert_shape(current_piece)
		for i, pos in enumerate(shape_pos):
			x, y = pos[0], pos[1]
			if y > -1:
				grid[y][x] = current_piece.color

		if changed_piece:
			for pos in shape_pos:
				locked_position[pos] = current_piece.color
			current_piece = next_piece
			next_piece = get_shape()
			changed_piece = False

			score += clear_row(grid, locked_position) * 10


		draw_grid(win, grid, score, last_score=0)
		draw_next(win, next_piece)
		pg.display.update()
		if check_lost(locked_position):
			pg.time.delay(1500)
			update_score(score)
			main_menu(win)
			run = False

	while run == False:
		grid = gen_grid(locked_position)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				run = False
				pg.display.quit()
				quit()

	
	win = pg.display.set_mode((s_width, s_height))
	main_menu(win)