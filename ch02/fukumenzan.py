# coding: utf-8
import tkinter as tk
from tkinter import messagebox
from tkinter import  filedialog
import time
from fukumenzan_dialog import FukumenzanDialog
from fukumenzan_solver import FukumenzanSolver


class Fukumenzan():
	def __init__(self, root):
		self.root = root
		self.probrem_ = []
		self.probrem_number = 0

		self.a_cha_wpxl = 13.0

		self.initUI()
		self.centerWindow()

	def initUI(self, title=u'覆面算'):

		self.root.title(title)

		menubar = tk.Menu(self.root)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label=u'問題の読み込み', command=self.mondai_in)
		filemenu.add_command(label=u'問題の保存', command=self.mondai_out)
		filemenu.add_separator()
		make_mondai = tk.Menu(filemenu, tearoff=0)
		make_mondai.add_command(label=u'2個の数の足し算', command=lambda : self.mondai_dlg(2))
		make_mondai.add_command(label=u'3個の数の足し算', command=lambda : self.mondai_dlg(3))
		make_mondai.add_command(label=u'4個の数の足し算', command=lambda: self.mondai_dlg(4))
		make_mondai.add_command(label=u'5個の数の足し算', command=lambda: self.mondai_dlg(5))
		make_mondai.add_command(label=u'6個の数の足し算', command=lambda: self.mondai_dlg(6))
		make_mondai.add_command(label=u'7個の数の足し算', command=lambda: self.mondai_dlg(7))
		make_mondai.add_command(label=u'8個の数の足し算', command=lambda: self.mondai_dlg(8))
		make_mondai.add_command(label=u'9個の数の足し算', command=lambda: self.mondai_dlg(9))
		make_mondai.add_command(label=u'10個の数の足し算', command=lambda: self.mondai_dlg(10))
		make_mondai.add_command(label=u'11個の数の足し算', command=lambda: self.mondai_dlg(11))
		make_mondai.add_command(label=u'12個の数の足し算', command=lambda: self.mondai_dlg(12))
		make_mondai.add_command(label=u'13個の数の足し算', command=lambda: self.mondai_dlg(13))
		make_mondai.add_command(label=u'14個の数の足し算', command=lambda: self.mondai_dlg(14))
		make_mondai.add_command(label=u'15個の数の足し算', command=lambda: self.mondai_dlg(15))
		filemenu.add_separator()
		filemenu.add_cascade(label=u'問題の記入', menu=make_mondai)
		filemenu.add_command(label=u'問題の編集', command=self.edit_mondai)
		filemenu.add_command(label=u'問題のリセット', command=self.clear_mondai)
		menubar.add_cascade(label=u'覆面算の問題', menu=filemenu)
		self.root.config(menu=menubar)

		lbl0 = tk.Label(self.root,justify=tk.CENTER, text=u'　　問　題')
		lbl0.grid(row=0, column=0)
		self.canvas_probrem = tk.Canvas(self.root, width=370, height=450, bg='light gray')
		self.canvas_probrem.grid(row=1, column=0)
		self.solution_var = tk.StringVar(value= u'　　解　答')
		self.lbl_sol = tk.Label(self.root, justify=tk.CENTER, textvariable=self.solution_var)
		self.lbl_sol.grid(row=0, column=3)


		self.btn_start = tk.Button(self.root, text=u'探索開始',
							  bd=5, relief=tk.SOLID,padx=20, pady=6, command=self.OnBtnStart)
		self.btn_start.grid(row=1, column=2)

		self.canvas_solution = tk.Canvas(self.root, width=370, height=450, bg='light gray')
		self.canvas_solution.grid(row=1, column=3)


	def centerWindow(self):
		w, h = 850, 500
		sw = self.root.winfo_screenwidth()
		sh = self.root.winfo_screenheight()
		x, y = (sw - w) // 2, (sh - h) // 2
		self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def mondai_in(self):
		filename = filedialog.askopenfilename()
		if filename:
			self.clear_mondai()
			with open(filename, 'r', encoding='utf8') as f:
				fin = f.readline()
				self.probrem_ = fin.strip().split(',')
			self.probrem_number = len(self.probrem_) - 1
			self.draw_probrem(self.canvas_probrem, self.probrem_)

	def mondai_out(self):
		if self.probrem_ == []:
			return
		filename = filedialog.asksaveasfilename()
		if filename:
			with open(filename, 'w', encoding='utf8') as f:
				f.write(','.join(self.probrem_))

	def edit_mondai(self):
		if  2 <= self.probrem_number <=15:
			self.mondai_dlg(self.probrem_number, self.probrem_)

	def clear_mondai(self):
		self.probrem_ = []
		self.probrem_number = 0
		self.solution_var.set(' ')
		self.lbl_sol.update()
		self.canvas_probrem.delete('all')
		self.canvas_solution.delete('all')

	def mondai_dlg(self, mondaisuu:int, mondai=[]):
		self.probrem_number = mondaisuu
		dlg = FukumenzanDialog(self.root, self.probrem_number, mondai)
		ret = dlg.show()
		if ret != '':
			self.clear_mondai()
			self.probrem_ = ret
			self.draw_probrem(self.canvas_probrem, self.probrem_)

	def draw_probrem(self, cvs:tk.Canvas, fukumen_l:list):
		cvs.delete('all')
		right_most_pos  = cvs.winfo_width() / 2 + (len(fukumen_l[-1]) / 2) * self.a_cha_wpxl
		y_offset = 20

		for r in range(len(fukumen_l) -1):
			for i, c in enumerate(reversed(fukumen_l[r])):
				cvs.create_text(right_most_pos - i*self.a_cha_wpxl, 10+r*20 + y_offset,text=c)

		cvs.create_text(right_most_pos - (len(fukumen_l[-1]) - 1)  * self.a_cha_wpxl - 40,
						-5 + self.probrem_number * 20 + y_offset,
						text='+')
		cvs.create_line(right_most_pos - (len(fukumen_l[-1]) - 1) * self.a_cha_wpxl - 50,
						5 + self.probrem_number * 20 + y_offset,
						right_most_pos + 10, 5 + self.probrem_number * 20 + y_offset)
		for i, c in enumerate(reversed(fukumen_l[-1])):
			cvs.create_text(right_most_pos - i * self.a_cha_wpxl, 20 + self.probrem_number * 20 + y_offset,
											text=c)
		cvs.update()

	def OnBtnStart(self):
		self.solution_var.set('検索しています ........')
		self.lbl_sol.update()
		if self.probrem_ ==[]:
			messagebox.showinfo('この問題', '問題の指定がありません。')
		else:
			start_time = time.time()
			fu = FukumenzanSolver(self.probrem_)
			if len(fu.chrs) > 10:
				messagebox.showinfo('この問題', '覆面文字が１０を超えています。')
			else:
				ret = fu.solve()
				elps_time = time.time()  -start_time
				if ret != []:
					self.solution_var.set(f'検索時間  {elps_time:.6f} 秒')
					ret_r = [list(reversed(s)) for s in ret]
					self.draw_probrem(self.canvas_solution, ret_r)
				else:
					self.solution_var.set('解はありませんでした。')





def main():
	root = tk.Tk()
	root.lift()
	root.attributes('-topmost', True)
	root.after_idle(root.attributes, '-topmost', False)

	Fukumenzan(root)
	root.mainloop()


# ----------------------------------------- mainloop
if __name__ == '__main__':
	main()
