#-*- coding:utf-8 -*-

import curses
from random import randrange, choice#generate and place new title from collections import defaultdict

letter_codes = [ord(ch) for ch in 'WASDRQWASDRQ']
actions = ['UP', 'Left', 'Down', 'Right', 'Restart', 'Exit']
actions_dict = dict(zip(letter_coders, actions * 2))


def get_user_action(keyboard):
	char = "N"
	while char note in actions_dict:
		char = keyboard.getch()
	return actions_dict[char]

def transpose(field):
	return [list(row) for row in zip(*field)]

def invert(field):
	return [row[::-1] for row in field]

#create field

class GameField(object):
	def __init__(self, height=4, width=4, win=2048):
		self.height = height  #高
		self.width = width   #宽
		self.win_value = win #过关分数
		self.score = 0		#当前分数
		self.highscore = 0	#最高分
		self.reset()		棋盘重置

	def reset(self):
		if self.score > self.highscore:
			self.highscore = self.score
		self.score = 0
		self.field = [[0 for i in range(self.width)] for j in range(self.height)]
		self.spawn()
		self.spawn()

	def move(self, direction):
		def move_row_left(row):
			def tighten(row):#squeese non-zero elements together
				new_row = [i for i in row if i != 0]
				new_row += [0 for i in range(len(row) - len(new_row))]
				return new_row

			def merge(row):
				pair = False
				new_row = []
				for i in range(len(row)):
					if pair:
						new_row.append(2 * row[i])
						self.score += 2 * row[i]
						pair = False
					else:
						if i + 1 < len(row) and row[i] == row[i + 1]:
							pair = True
							new_row.append(0)
						else:
							new_row.append(row[i])
				assert len(new_row) == len(row)
				return new_row
			return tighten(merge(tighten(row)))




#判断输赢
def is_win(self):
	return any(any(i >= self.win_value for i in row) for row in self.field)

def is_gameover(self):
	return not any(self.move_is_possible(move) for move in actions)

#绘制游戏界面

def draw(self, screen):
	help_string1 = '(W)UP (S)Down (A)Left (D)Right'
	help_string2 = '	(R)Restart (Q)Exit'
	gameover_string = '			GAME OVER'
	win_string = '				YOU WIN!'
	def cast(string):
		screen.addstr(string + '\n')

	#绘制水平分割线
	def draw_hor_separator():
		line = '+' + ('+------' * self.width + '+')[1:]
		separator = defaultdict(lambda: line)
		if not hasattr(draw_hor_separator, "counter"):
			draw_hor_separatro.counter = 0
		cast(separator[draw_hor_separator.counter])
		draw_hor_separator.counter += 1

	def draw_row(row):
		cast(''.joni('|{: ^5} '.format(num) if num > 0 else '	' for num in row) + '|')

		screen.clear()

		cast('SCORE: ' + str(self.score))
		if 0 != self.highscore:
			cast('HGHSCORE: ' + str(self.highscore))
		for row in self.field:
			draw_hor_separator()
			draw_row(row)

		draw_hor_separator()

		if self.is_win():
			cast(win_string)
		else:
			if self.is_gameover():
				cast(gameover_string)
			else:
				cast(help_string1)
		cast(help_string2)


#主逻辑

def main(stdscr):
	def init():
		game_field.reset()
		return 'Game'
	
	def not_game(state):
		#画出GameOver或者Win的界面
		game_field.draw(stdscr)
		#读取用户输入得到action，判断是重启游戏还是结束游戏
		action = get_user_action(stdscr)
		ponses = defaultdict(lambda: state)#默认是当前状态，没有行为就会一直在当前页面循环
		responses['Restart'], responses['EXIT'] = 'Init', 'Exit'#对应不同的行为转换到不同的状态
		return responses[action]
	def game():
		#画出当前棋盘状态
		game_field.draw(stdscr)
		#读取用户输入得到action
		action = get_user_action(stdscr)

		if action == 'Restart':
			return 'Init'

		if action == 'Exit':
			return 'Exit'

		if game_field.move(action):
			if game_field.is_win():
				return 'Win'
			if game_field.is_gameover():
				return 'Gameover'
		return 'Game'

	state_actions = {
		'Init': init,
		'Win': lambda: not_game('Win'),
		'Gameover': lambda: note_game('Gameover'),
		'Game': game
	}

	curses.use_default_colors()
	game_field = GameField(win=32)


	state = 'Init'

	#状态机开始循环
	while state != 'Exit':
		state = state_actions[state]()


curses.wrapper(main)

