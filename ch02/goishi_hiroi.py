# coding: utf-8
"""
goishi_hiroi.py
「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社） 幅優先探索の碁石拾いアプリです。（188-192ページ)
	梅屋萬年堂がpythonで書きました(2022/07,08)
"""
import tkinter as tk
from tkinter import filedialog
import time
from collections import deque
from copy import copy

class GoishiHiroi(tk.Frame):
	def __init__(self, master:tk.Tk):
		super(GoishiHiroi, self).__init__()
		self.master = master
		self.square_length = 50
		self.goban_size_value = [4,5,6,7,8,9,10]
		self.goban_width, self.goban_height = 5, 4
		self.goban_width_var = tk.IntVar(value=self.goban_width)
		self.goban_height_var = tk.IntVar(value=self.goban_height)
		self.goban = []
		self.goishi_id = []
		self.new_goban_info = None
		#  ----------for solver
		self.goban_points = []
		self.nodes = deque([])
		self.DIR = [(0,-1), (0, 1), (-1,0), (1,0) ] # (dr, dc) 左、右、上、下
		self.solution_id = []

		#  init UI
		self.master.title('碁　石　拾　い')
		self.grid(column=0, row=0)
		#  ---- menu
		menubar = tk.Menu(master=self.master)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label='新規の碁盤', command=self.new_goban)
		filemenu.add_command(label='この碁盤のクリア', command=self.goban_clear)
		filemenu.add_separator()
		filemenu.add_command(label='碁盤のデータファイル保存', command=self.goban_save)
		filemenu.add_command(label='碁盤のデータファイル読み込み', command=self.goban_load)
		filemenu.add_separator()
		filemenu.add_separator()
		filemenu.add_command(label='終了', command=self.master.quit)
		menubar.add_cascade(label='ファイル', menu=filemenu)
		solvermunu = tk.Menu(menubar, tearoff=0)
		solvermunu.add_command(label='碁石拾い経路の探索', command=self.compute_path)
		solvermunu.add_separator()
		solvermunu.add_command(label='解の消去', command=self.erase_path)
		menubar.add_cascade(label='碁石拾い探索', menu=solvermunu)
		self.master.config(menu=menubar)

		# --------- frm0
		self.frm0 = tk.Frame(self)
		self.frm0.grid(column=0, row=0)
		self.frm0a = tk.LabelFrame(self.frm0, text='碁盤のサイズ')
		self.frm0a.grid(column=0, row=0, sticky=tk.NW, padx=5)
		lbl0a1 = tk.Label(self.frm0a, text=u'縦', width=9)
		lbl0a1.grid(column=0, row=0)
		self.lbl_maze_width = tk.Label(self.frm0a, textvariable=self.goban_height_var)
		self.lbl_maze_width.grid(column=1, row=0)
		lbl0a2 = tk.Label(self.frm0a, text='横')
		lbl0a2.grid(column=0, row=1)
		self.lbl_maze_height = tk.Label(self.frm0a, textvariable=self.goban_width_var)
		self.lbl_maze_height.grid(column=1, row=1)

		self.frm0b = tk.Frame(self.frm0)
		self.frm0b.grid(column=0, row=1, sticky=tk.NW, padx=5)
		lbl0b1 = tk.Label(self.frm0b, text=' クリックで\n 碁石を置く\n （取る)\n ができます', width=8).grid(column=0, row=0)

		# ------- frm1
		self.frm1 = tk.Frame(self, width=self.square_length * self.goban_size_value[-1] + 40,
							 height=self.square_length * self.goban_size_value[-1] + 40)
		self.frm1.grid(column=1, row=0, rowspan=2, padx=8, pady=8)
		self.cvs_goban = tk.Canvas(self.frm1, width=self.square_length * self.goban_size_value[-1],
								  height=self.square_length * self.goban_size_value[-1], bg='white',
								  highlightthickness=0)
		self.cvs_goban.grid(column=0, row=0, padx=8, pady=8, ipadx=5, ipady=5)
		self.cvs_goban.bind('<Button-1>', self.on_cvs_goban_click)
		# ------------
		self.mes_var = tk.StringVar(value='')
		self.lbl_mes = tk.Label(self, textvariable=self.mes_var)
		self.lbl_mes.grid(column=1, row=1)

		self.goban_clear()

	def on_cvs_goban_click(self, e):
		x, y = self.cvs_goban.canvasx(e.x), self.cvs_goban.canvasy(e.y)
		c, r = int(x / self.square_length), int(y / self.square_length)
		if 0 <= r < self.goban_height and 0 <= c < self.goban_width:
			goishi = self.goban[r][c]
			if goishi == 0:
				self.goban[r][c] = 1
				dxdy = 7
				self.goishi_id[r][c] = self.cvs_goban.create_oval(c * self.square_length+dxdy, r * self.square_length+dxdy,
											   (c + 1) * self.square_length - dxdy, (r + 1) * self.square_length -dxdy,
											   fill='white')
			else:
				self.goban[r][c] = 0
				self.cvs_goban.delete(self.goishi_id[r][c])
				self.goishi_id[r][c] = None
				self.cvs_goban.create_line((c+0.5) * self.square_length, r * self.square_length,
											   (c + 0.5) * self.square_length, (r + 1) * self.square_length)
				self.cvs_goban.create_line(c * self.square_length, (r+0.5) * self.square_length,
											   (c + 1) * self.square_length, (r + 0.5) * self.square_length)



	def new_goban(self):
		self.new_goban_info = None
		self.new_goban_dlg()
		if self.new_goban_info is not None:
			self.goban_width, self.goban_height = self.new_goban_info
			self.goban_width_var.set(self.goban_width)
			self.goban_height_var.set(self.goban_height)
			self.goban_clear()


	def new_goban_dlg(self):
		def sub_win_btn_ok():
			self.new_goban_info = (int(spinbox_x.get()), int(spinbox_y.get()))
			sub_win.destroy()
		def sub_win_btn_cancel():
			self.new_goban_info = None
			sub_win.destroy()
		sub_win = tk.Toplevel()
		sub_win.title('新規の碁盤サイズ　設定')
		sub_win.geometry("240x180+100+200")
		label_sub1 = tk.Label(sub_win, text=u'横')
		label_sub1.place(width=100, height=40, x=10, y=10)
		spinbox_x = tk.Spinbox(sub_win, state='readonly',
							   values=self.goban_size_value)
		spinbox_x.place(width=80, height=40, x=150, y=10)
		label_sub2 = tk.Label(sub_win, text=u'縦')
		label_sub2.place(width=100, height=40, x=10, y=50)
		spinbox_y = tk.Spinbox(sub_win, state='readonly',
							   values=self.goban_size_value)
		spinbox_y.place(width=80, height=40, x=150, y=50)
		button_ok = tk.Button(sub_win, text=u'設定',command=sub_win_btn_ok)
		button_ok.place(width=80, height=40, x=20, y=120)
		button_cancel = tk.Button(sub_win, text=u'キャンセル',command=sub_win_btn_cancel)
		button_cancel.place(width=80, height=40, x=120, y=120)
		self.new_goban_info = None
		self.master.wait_window(sub_win)


	def goban_clear(self, goban=[]):
		if goban == []:
			self.goban  = [[ 0 for _ in range(self.goban_width)] for _ in range(self.goban_height)]
		self.goishi_id = [[None for _ in range(self.goban_width)] for _ in range(self.goban_height)]
		self.cvs_goban.delete('all')
		for r in range(self.goban_height):
			self.cvs_goban.create_line(0, (r+0.5)*self.square_length,
									   self.goban_width*self.square_length, (r+0.5)*self.square_length)
			for c in range(self.goban_width):
				self.cvs_goban.create_line((c+0.5)*self.square_length, 0,
										   (c+0.5)*self.square_length, self.goban_height*self.square_length)

	def goban_save(self):
		filename = filedialog.asksaveasfilename(
			title='碁石拾いデータの保存',
			filetypes=(('text file', '*.txt'),)
		)
		if filename:
			with open(filename, 'w') as f:
				f.write(f'{self.goban_height},{self.goban_width}\n')
				for row in self.goban:
					f.write(','.join(list([str(g) for g in row])) + '\n')

	def goban_load(self):
		filename = filedialog.askopenfilename(
			title='碁盤 データの読み込み',
			filetypes=(('text file', '*.txt'),)
		)
		if filename:
			with open(filename) as f:
				lines = f.readlines()
				hw = lines[0].strip('\n').split(',')
				self.goban_height, self.goban_width = int(hw[0]), int(hw[1])
				self.goban_height_var.set(self.goban_height)
				self.goban_width_var.set(self.goban_width)
				self.goban = []
				for l in lines[1:]:
					self.goban.append([int(g) for g in l.strip('\n').split(',')])
			self.draw_goban()

	def draw_goban(self):
		self.goban_clear(self.goban)
		for r, row in enumerate(self.goban):
			for c, g in enumerate(row):
				if g == 1:
					dxdy = 7
					self.goishi_id[r][c] = \
						self.cvs_goban.create_oval(c * self.square_length + dxdy,
													r * self.square_length + dxdy,
													(c + 1) * self.square_length - dxdy,
													(r + 1) * self.square_length - dxdy,
													fill='white')
	#  goishi hiroi solver
	def compute_path_preparation(self):
		#  goban_point の設定。周りの碁石から拾うようにする
		self.goban_points = []
		if self.goban_height > 2 and self.goban_width > 2:
			for c, g in enumerate(self.goban[0]):
				if g == 1:
					self.goban_points.append((0, c))
			for c, g in enumerate(self.goban[-1]):
				if g == 1:
					self.goban_points.append((self.goban_height-1, c))
			for r in range(1, self.goban_height-1):
				if self.goban[r][0] == 1:
						self.goban_points.append((r, 0))
				if self.goban[r][-1] == 1:
					self.goban_points.append((r, self.goban_width-1))
			for r in range(1, self.goban_height-1):
				for c in range(1, self.goban_width-1 ):
					if self.goban[r][c] == 1:
						self.goban_points.append((r,c))
		else:
			for r, row in enumerate(self.goban):
				for c, g in enumerate(row):
					if g == 1:
						self.goban_points.append((r,c))
		self.goban_points.reverse()

	def compute_path(self):
		self.compute_path_preparation()
		path = self.goishi_hiroi_solver()
		if path:
			self.draw_path(path)

	def goishi_hiroi_solver(self):
		goishi_set_start = copy(self.goban_points)
		self.nodes = deque([])
		while True:
			if len(self.goban_points) == 0:
				return []
			start = self.goban_points.pop()
			rmg_start = copy(goishi_set_start)
			rmg_start.remove(start)
			for dir in self.DIR:
				remaining_goishi = copy(rmg_start)
				last_picked_goishi = (start, dir)
				path = [start]
				self.nodes.append((remaining_goishi, last_picked_goishi, path))
			while len(self.nodes) > 0:
				remaining_goishi, last_picked_goishi, path = self.nodes.popleft()
				next_goishi = self.find_nex_gosishi(last_picked_goishi, remaining_goishi)
				if next_goishi is not None:
					path.append(next_goishi)
					if len(remaining_goishi) == 1:
						return path
					rmg = copy(remaining_goishi)
					rmg.remove((next_goishi))
					pt = copy(path)
					last_dr, last_dc = last_picked_goishi[1]
					turn_back_dir = (-1*last_dr, -1*last_dc)
					for dir in self.DIR:
						if dir == turn_back_dir:
							continue
						remaining_goishi = copy(rmg)
						path = copy(pt)
						self.nodes.append((remaining_goishi, (next_goishi, dir), path))



	def find_nex_gosishi(self, last_picked, remainings):
		(next_r, next_c), (dr, dc) = last_picked
		while True:
			next_r += dr
			next_c += dc
			if 0 <= next_r < self.goban_height and 0 <= next_c < self.goban_width:
				if (next_r, next_c) in remainings:
					return (next_r, next_c)
			else:
				return None

	def draw_path(self, path):
		self.solution_id = []
		dxdy = 25
		line_xy = []
		for n, (r,c) in enumerate(path, 1):
			id = self.cvs_goban.create_text(c * self.square_length + dxdy, r * self.square_length + dxdy,
											text=f'{n:^3}')
			self.solution_id.append(id)
			line_xy.append(c*self.square_length+20)
			line_xy.append(r*self.square_length+20)
		id = self.cvs_goban.create_line(*line_xy, width=1, fill='red')
		self.solution_id.append(id)


	def erase_path(self):
		for id in self.solution_id:
			self.cvs_goban.delete(id)

def main():
	win = tk.Tk()
	app = GoishiHiroi(master=win)
	app.mainloop()

if __name__ == '__main__':
	main()
