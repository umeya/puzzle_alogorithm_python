# coding: utf-8

import tkinter as tk
from tkinter import messagebox
from tkinter import  filedialog
import time
from suudoku_solver import SuudokuSolver


class Sudoku():
	def __init__(self, root, title):
		self.root = root
		self.initUI(title)
		self.centerWindow()

	def initUI(self, title=u'数　独'):

		self.root.title(title)

		menubar = tk.Menu(self.root)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label=u'問題の読み込み', command=self.mondai_in)
		filemenu.add_command(label=u'問題の書き出し', command=self.mondai_out)
		filemenu.add_separator()
		filemenu.add_command(label=u'問題のリセット', command=self.clear_entTable_field)
		menubar.add_cascade(label=u'問題', menu=filemenu)
		self.root.config(menu=menubar)

		self.label01 = tk.Label(self.root,
								text=
								"「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）\n" + "虫食算（52-75ページ)\n"
								+ "梅屋萬年堂がpythonで書き直したものです(2022/07)\n"
								+ " ----------------------------------------------\n\n"
								  u'問題を左のテーブルに入力（または、メニュー「問題読み込み」）し、「探索開始」ボタンを押してください\n' +
								u'（問題や解答のファイルへの書き込み読み込みがメニューからできます）')
		self.label01.pack()

		self.sudoku_message = tk.StringVar()
		self.sudoku_msg = tk.Label(self.root, foreground='red',textvariable=self.sudoku_message)
		self.sudoku_msg.pack()

		self.field = [[-1 for _ in range(9)] for _ in range(9)]
		self.ent_var= [[tk.StringVar() for _ in range(9)] for _ in range(9)]
		self.kai_var = [[tk.StringVar() for _ in range(9)] for _ in range(9)]

		# --------------------------------------------------------------

		self.sdFr1 = tk.Frame(self.root, relief=tk.FLAT, bd=30)
		self.sdFr1.pack()
		self.ent, self.kai = [], []
		for r in range(9):
			ce, ck, br = [], [], r // 3
			for c in range(9):
				bc = c // 3
				if br == 1:
					if bc == 1:
						bcolor = 'lightblue1'
					else:
						bcolor = 'white'
				else:
					if bc == 1:
						bcolor = 'white'
					else:
						bcolor = 'lightblue1'
				ce.append(tk.Entry(self.sdFr1, width=2, bg=bcolor, justify=tk.CENTER,
								   textvariable=self.ent_var[r][c]))
				ce[-1].grid(row=r, column=c)
				ck.append(tk.Entry(self.sdFr1, width=2,state='readonly', readonlybackground=bcolor, justify=tk.CENTER, textvariable=self.kai_var[r][c]))
				ck[-1].grid(row=r, column=c + 12)
				self.ent_var[r][c].trace_add('write',
											 lambda name, index, mode, var=self.ent_var[r][c], r=r, c=c
											 : self.entryupdate(var, r, c))

				self.ent.append(ce)
			self.kai.append(ck)

		self.btnStart = tk.Button(self.sdFr1, text=u'探索開始', bd=5, relief=tk.SOLID,padx=20, pady=6, command=self.OnBtnStart)
		self.btnStart.grid(row=3, column=10)
		# self.time_var = tk.StringVar(value=u'(計算時間)')
		# self.lblTime = tk.Label(self.sdFr1, textvariable=self.time_var,padx=20, pady=6)
		# self.lblTime.grid(row=5, column=10)

	# ---------------------------------------------------------------
	def centerWindow(self):
		w, h = 800, 500
		sw = self.root.winfo_screenwidth()
		sh = self.root.winfo_screenheight()
		x, y = (sw - w) // 2, (sh - h) // 2
		self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def entryupdate(self, sv, r, c):
		ms = ' '
		e = sv.get().strip()
		if len(e) > 1:
			ms ='２個以上の文字が入力されました。'
		elif len(e) == 1 and (e not in '123456789'):
				ms = '1から9の数字以外が入力されました。'
		elif len(e) == 1:
			ret = self.check_row_column_block(r, c, int(e))
			if ret[0] == False:
				ms = ret[1]
			else:                     # 重複しない正しい数字が入力された
				self.field[r][c] = int(e)
		else:                         # len(e)=0 この欄の数字を削除する
			if self.field[r][c] != -1:
				self.field[r][c] = -1
		self.sudoku_message.set(ms)

	def check_row_column_block(self, r, c, n):
		if n in self.field[r]:
			return (False, str(n) + ' が行の中で重複しています。')
		elif n in [self.field[i][c] for i in range(9)]:
			return (False, str(n) + ' が列の中で重複しています。')
		br, bc = (r//3)*3, (c//3)*3
		if n in [self.field[br+i][bc+j] for i in range(3) for j in range(3)]:
			return (False, str(n) + ' がブロックの中で重複しています。')
		return (True, '')


	def mondai_in(self):

		filename = filedialog.askopenfilename()
		if filename:
			d = [[-1 for _ in range(9)] for _ in range(9)]
			data_format_error = ''
			dr = [[] for _ in range(9)]
			dc = [[] for _ in range(9)]
			db = [[[] for _ in range(3)] for _ in range(3)]
			with open(filename, 'r', encoding='utf8') as f:
				for r, ll in enumerate(f):
					if r > 8:
						data_format_error = u'データが９行を超えています。'
						break
					l = ll.strip('\n')
					if len(l) != 9:
						data_format_error = u'１行の文字数が９文字ではありません。'
						break
					for c, n in enumerate(l):
						if n == '*':
							continue
						if n not in '123456789':
							data_format_error = u'＊または１から９の数字以外の文字が入っています。'
							break
						d[r][c] = int(n)
						if d[r][c] in dr[r]:
							data_format_error = u'行に重複した文字があります。'
							break
						dr[r].append(d[r][c])
						if d[r][c] in dc[c]:
							data_format_error = u'列に重複した文字があります。'
							break
						br, bc = r//3, c // 3
						if d[r][c] in db[br][bc]:
							data_format_error = u'ブロック内に重複した文字があります。'
							break
						db[br][bc].append(d[r][c])
					else:
						continue
					break

				if data_format_error != '':
					messagebox.showerror(title=u'データフォーマットのエラー',
										message='読み込んだデータの形式が不正です。\n' + data_format_error)
					return

				for r in range(9):
					for c in range(9):
						if d[r][c] == -1:
							v = ''
						else:
							v = str(d[r][c])
						self.ent_var[r][c].set(v)
						self.kai_var[r][c].set('')
				self.sudoku_message.set('')

	def mondai_out(self):
		filename = filedialog.asksaveasfilename()
		if filename:
			with open(filename, 'w', encoding='utf8') as f:
				for l in self.field:
					f.write(''.join(['*' if e == -1 else str(e) for e in l]) + '\n')

	def clear_entTable_field(self):
		self.field = [[-1 for _ in range(9)] for _ in range(9)]
		L = [['' for i in range(9)] for j in range(9)]
		for r in range(9):
			for c in range(9):
				self.ent_var[r][c].set('')
				self.kai_var[r][c].set('')
		self.sudoku_message.set('')


	def OnBtnStart(self):
		hints = sum([1 for r in range(9) for c in range(9) if self.field[r][c] != -1])
		if hints < 17:
			self.sudoku_message.set(u'数独問題にはヒントとなる数字が１７個以上が必要です。問題を訂正してください。')
			return
		self.sudoku_message.set(u'解を探索しています')
		self.sudoku_msg.update()
		sds = SuudokuSolver(self.field)
		start_time = time.time()
		ret = sds.solve()
		elapsed_time = f'{time.time() -start_time:12.6f}秒'
		self.sudoku_message.set(u'計算に' + elapsed_time + ' かかりました')
		if ret:
			for r, l in enumerate(ret):
				for c, v in enumerate(l):
					self.kai_var[r][c].set(str(v))
		else:
			self.sudoku_message.set(u'解はありませんでした')



def main():
	root = tk.Tk()
	root.lift()
	root.attributes('-topmost', True)
	root.after_idle(root.attributes, '-topmost', False)

	sudo = Sudoku(root, u'数　独   from  梅屋萬年堂')
	root.mainloop()


# ----------------------------------------- mainloop
if __name__ == '__main__':
	main()

