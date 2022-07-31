# coding: utf-8
"""
maze editor
「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社） 迷路最短経路探索の迷路を作成するアプリです。（158-172ページ)
	梅屋萬年堂がpythonで書きました(2022/07)
"""
import tkinter as tk
from tkinter import filedialog
import time
from collections import deque

class Maze(tk.Frame):
	def __init__(self, master:tk.Tk):
		super().__init__(master)
		self.master = master
		self.square_length = 40
		self.maze_size_value = [4,5,6,7,8,9,10,11,12]
		self.maze_width, self.maze_height = 8, 8
		self.maze_width_var, self.maze_height_var = tk.IntVar(value=self.maze_width), tk.IntVar(value=self.maze_height)
		self.maze_data = []
		self.new_maze_info = None
		self.click_mode = tk.StringVar(value='S') # S s スタート、 G ゴール、 . 通路、 # 壁

		self.master.title('迷  路')
		self.grid(column=0, row=0)
		# ------- menu
		menubar = tk.Menu(master=self.master)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label='新規の迷路', command=self.new_maze)
		filemenu.add_command(label='この迷路のクリア', command=self.maze_clear)
		filemenu.add_separator()
		filemenu.add_command(label='迷路のデータファイル保存', command=self.maze_save)
		filemenu.add_command(label='迷路のデータファイル読み込み', command=self.maze_load)
		filemenu.add_separator()
		filemenu.add_separator()
		filemenu.add_command(label='終了', command=self.master.quit)
		menubar.add_cascade(label='ファイル', menu=filemenu)
		solvermunu = tk.Menu(menubar, tearoff=0)
		solvermunu.add_command(label='最短経路の長さ探索', command=self.compute_short_path_number)
		solvermunu.add_separator()
		solvermunu.add_command(label='階の消去', command=self.erase_shortest_path)
		menubar.add_cascade(label='迷路探索', menu=solvermunu)
		self.master.config(menu=menubar)

		# --------- frm0
		self.frm0 = tk.Frame(self)
		self.frm0.grid(column=0, row=0)
		self.frm0a = tk.LabelFrame(self.frm0, text='迷路のサイズ')
		self.frm0a.grid(column=0, row=0, sticky=tk.NW, padx=5)
		lbl0a1 = tk.Label(self.frm0a, text=u'縦', width=9)
		lbl0a1.grid(column=0, row=0)
		self.lbl_maze_width = tk.Label(self.frm0a, textvariable=self.maze_height_var)
		self.lbl_maze_width.grid(column=1, row=0)
		lbl0a2 = tk.Label(self.frm0a, text = '横')
		lbl0a2.grid(column=0, row=1)
		self.lbl_maze_height = tk.Label(self.frm0a, textvariable=self.maze_width_var)
		self.lbl_maze_height.grid(column=1, row=1)

		self.frm0b = tk.LabelFrame(self.frm0, text='クリックモード')
		self.frm0b.grid(column=0, row=1,sticky=tk.NW, padx=5)
		lbl0b1 = tk.Label(self.frm0b, text='スタート(S)', width=8).grid(column=0, row=0)
		self.radio_start = tk.Radiobutton(self.frm0b,
					value='S', variable=self.click_mode)
		self.radio_start.grid(column=1, row=0)
		lbl0b2 = tk.Label(self.frm0b, text='ゴール(G)', width=8).grid(column=0, row=1)
		self.radio_gaol = tk.Radiobutton(self.frm0b,
											  value='G', variable=self.click_mode)
		self.radio_gaol.grid(column=1, row=1)
		lbl0b3 = tk.Label(self.frm0b, text='壁(#)', width=8).grid(column=0, row=2)
		self.radio_wall = tk.Radiobutton(self.frm0b,
											  value='#', variable=self.click_mode)
		self.radio_wall.grid(column=1, row=2)
		lbl0b1 = tk.Label(self.frm0b, text='通路(.)', width=8).grid(column=0, row=3)
		self.radio_path = tk.Radiobutton(self.frm0b,
											  value='.', variable=self.click_mode)
		self.radio_path.grid(column=1, row=3)
		# ------- frm1
		self.frm1 = tk.Frame(self,  width=self.square_length*self.maze_size_value[-1] + 40,
								  height=self.square_length*self.maze_size_value[-1] + 40)
		self.frm1.grid(column=1, row=0, rowspan=2, padx=8, pady=8)
		self.cvs_maze = tk.Canvas(self.frm1,width=self.square_length*self.maze_size_value[-1],
								  height=self.square_length*self.maze_size_value[-1], bg='white',
								  highlightthickness=0)
		self.cvs_maze.grid(column=0, row=0, padx=8, pady=8, ipadx=5, ipady=5)
		self.cvs_maze.bind('<Button-1>', self.on_cvs_maze_click)
		# ------------
		self.mes_var = tk.StringVar(value='')
		self.lbl_mes = tk.Label(self, textvariable=self.mes_var)
		self.lbl_mes.grid(column=1, row=1)

		self.maze_clear()
		self.radio_wall.select()

	def new_maze(self):
		self.new_maze_info = None
		self.new_maze_dlg()
		if self.new_maze_info is not None:
			self.maze_width, self.maze_height = self.new_maze_info
			self.maze_width_var.set(self.maze_width)
			self.maze_height_var.set(self.maze_height)
			self.maze_clear()

	def new_maze_dlg(self):
		def sub_win_btn_ok():
			self.new_maze_info = (int(spinbox_x.get()), int(spinbox_y.get()))
			sub_win.destroy()
		def sub_win_btn_cancel():
			self.new_maze_info = None
			sub_win.destroy()
		sub_win = tk.Toplevel()
		sub_win.title('新規の迷路のマス数　設定')
		sub_win.geometry("240x180+100+200")
		label_sub1 = tk.Label(sub_win, text=u'横')
		label_sub1.place(width=100, height=40, x=10, y=10)
		spinbox_x = tk.Spinbox(sub_win, state='readonly',
							   values=self.maze_size_value)
		spinbox_x.place(width=80, height=40, x=150, y=10)
		label_sub2 = tk.Label(sub_win, text=u'縦')
		label_sub2.place(width=100, height=40, x=10, y=50)
		spinbox_y = tk.Spinbox(sub_win, state='readonly',
							   values=self.maze_size_value)
		spinbox_y.place(width=80, height=40, x=150, y=50)
		button_ok = tk.Button(sub_win, text=u'設定',command=sub_win_btn_ok)
		button_ok.place(width=80, height=40, x=20, y=120)
		button_cancel = tk.Button(sub_win, text=u'キャンセル',command=sub_win_btn_cancel)
		button_cancel.place(width=80, height=40, x=120, y=120)
		self.new_maze_info = None
		# sub_win.grab_set()
		# sub_win.focus_set()
		# sub_win.transient(self.master)
		self.master.wait_window(sub_win)


	def maze_clear(self):
		self.maze_data = [ ['.' for _ in range(self.maze_width)]  for _ in range(self.maze_height)]
		self.cvs_maze.delete('all')
		for r in range(self.maze_height+1):
			self.cvs_maze.create_line(0, r*self.square_length, self.maze_width*self.square_length, r*self.square_length)
			for c in range(self.maze_width+1):
				self.cvs_maze.create_line(c*self.square_length, 0, c*self.square_length, self.maze_height*self.square_length)

	def maze_save(self):
		filename = filedialog.asksaveasfilename(
			title='迷路データの保存',
			filetypes=(('text file', '*.txt'),)
		)
		if filename:
			with open(filename, 'w') as f:
				f.write(f'{self.maze_height} {self.maze_width}\n')
				for row in self.maze_data:
					f.write(''.join(row) + '\n' )

	def maze_load(self):
		filename = filedialog.askopenfilename(
			title='Maze データの読み込み',
			filetypes=(('text file', '*.txt'),)
		)
		if filename:
			with open(filename) as f:
				lines = f.readlines()
				hw = lines[0].strip('\n').split(' ')
				self.maze_height, self.maze_width = int(hw[0]), int(hw[1])
				self.maze_height_var.set(self.maze_height)
				self.maze_width_var.set(self.maze_width)
				self.maze_data = []
				for l in lines[1:]:
					self.maze_data.append(list(l.strip('\n')))
			self.draw_maze()

	def draw_maze(self):
		for r, row in enumerate(self.maze_data):
			for c, mode in enumerate(row):
				if mode == '#':
					self.cvs_maze.create_rectangle(c * self.square_length, r * self.square_length,
												   (c + 1) * self.square_length, (r + 1) * self.square_length,
												   fill='brown')
				elif mode == '.':
					self.cvs_maze.create_rectangle(c * self.square_length, r * self.square_length,
												   (c + 1) * self.square_length, (r + 1) * self.square_length,
												   fill='white')
				elif mode == 'S':
					self.cvs_maze.create_rectangle(c * self.square_length, r * self.square_length,
												   (c + 1) * self.square_length, (r + 1) * self.square_length,
												   fill='white')
					self.cvs_maze.create_text(c * self.square_length + 20, r * self.square_length + 20, text='S',
											  font=('', 24))
				else:  # mode == 'G':
					self.cvs_maze.create_rectangle(c * self.square_length, r * self.square_length,
												   (c + 1) * self.square_length, (r + 1) * self.square_length,
												   fill='white')
					self.cvs_maze.create_text(c * self.square_length + 20, r * self.square_length + 20, text='G',
											  font=('', 24))


	def on_cvs_maze_click(self, e):
		x, y = self.cvs_maze.canvasx(e.x),self.cvs_maze.canvasy(e.y)
		c, r = int(x/self.square_length), int(y/self.square_length)
		if 0 <= r < self.maze_height and 0 <= c < self.maze_width:
			mode = self.click_mode.get()
			if mode == '#':
				self.cvs_maze.create_rectangle(c*self.square_length, r*self.square_length,
											   (c+1)*self.square_length, (r+1)*self.square_length,
											   fill='brown')
			elif mode == '.':
				self.cvs_maze.create_rectangle(c*self.square_length, r*self.square_length,
											   (c+1)*self.square_length, (r+1)*self.square_length,
											   fill='white')
			elif mode == 'S':
				self.cvs_maze.create_rectangle(c*self.square_length, r*self.square_length,
											   (c+1)*self.square_length, (r+1)*self.square_length,
											   fill='white')
				self.cvs_maze.create_text(c*self.square_length+20, r*self.square_length+20,text='S',
										  font=('', 24))
			else:   #  mode == 'G':
				self.cvs_maze.create_rectangle(c*self.square_length, r*self.square_length,
											   (c+1)*self.square_length, (r+1)*self.square_length,
											   fill='white')
				self.cvs_maze.create_text(c * self.square_length + 20, r * self.square_length + 20, text='G',
										  font=('', 24))
			self.maze_data[r][c] = mode

		# maze solver --------------
	def comput_shortest_path_preparation(self):
		self.path_finded, self.goal, self.start = False, None, None
		self.board = [[0 for _ in range(self.maze_width)] for _ in range(self.maze_height)]
		for r, row in enumerate(self.maze_data):
			for c, v in enumerate(row):
				if v == '#':
					self.board[r][c] = -1
				elif v == 'S':
					self.start = (r, c)
				elif v == 'G':
					self.goal = (r, c)


	def compute_short_path_number(self):
		start_time = time.time()
		if self.solve():
			elapse_time = time.time() - start_time
			self.mes_var.set(
				f'この迷路の最短経路は {self.board[self.goal[0]][self.goal[1]][2]} ステップで、所要時間は{elapse_time:.6f}秒でした。'
			)
			self.draw_shortest_path()
		else:
			self.mes_var.set('この迷路の解（最短経路）は見つかりませんでした。')

	def solve(self):
		self.comput_shortest_path_preparation()
		DIR = [(1, 0), (0, 1), (-1, 0), (0, -1)]
		nodes, shortest_path_finded = deque([(*self.start, 0)]), False
		while len(nodes) != 0:
			r, c, routes = nodes.popleft()
			for dr, dc in DIR:
				next_r = r + dr
				next_c = c + dc
				if 0 <= next_r < self.maze_height and 0 <= next_c < self.maze_width:
					if self.board[next_r][next_c] != 0 or self.maze_data[next_r][next_c] == 'S':
						continue
					else:
						nodes.append((next_r, next_c, routes + 1))
						self.board[next_r][next_c] = (r, c, routes + 1)
						if self.goal == (next_r, next_c):
							shortest_path_finded = True

		return shortest_path_finded

	def draw_shortest_path(self):
		point, path  = self.goal, []
		while point != self.start:
			path.append(point)
			point = self.board[point[0]][point[1]][:2]
		path.append(self.start)
		path_xy = []
		for r, c in reversed(path):
			path_xy.append(c*self.square_length+20)
			path_xy.append(r*self.square_length+20)
		self.cvs_maze.create_line(*path_xy, width=1, fill='red', arrow=tk.LAST)

		for r, row in enumerate(self.maze_data):
			for c, v in enumerate(row):
				if v == '.':
					self.cvs_maze.create_text(c*self.square_length+20, r*self.square_length+20,
											  text= f'{self.board[r][c][2]:>3}',font=('', 12))

	def erase_shortest_path(self):
		self.draw_maze()


def main():
	win = tk.Tk()
	app = Maze(master=win)
	app.mainloop()

if __name__ == '__main__':
	main()
