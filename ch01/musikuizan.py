# coding: utf-8
"""
「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社） 虫食算（52-75ページ)
	梅屋萬年堂がpythonで書き直したものです(2022/07)
"""
import os
import time
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog

from brute_force_musikuizan import BruteForceMusikuizan

class Musikuizan(ttk.Frame):
	def __init__(self, master: tk.Tk):
		super().__init__(master)

		master.title('虫食算')

		menubar = tk.Menu(master)
		master.config(menu=menubar)
		filemenu = tk.Menu(menubar, tearoff=False)
		filemenu.add_command(label='虫食算ファイルの読み込み', command=self.set_probrems_from_file)
		menubar.add_cascade(label='File', menu=filemenu)

		fr0 = ttk.Frame(self)
		lbl01 = tk.Label(fr0, width=46, relief=tk.RIDGE, bd=5, justify=tk.LEFT,
						 text="「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）\n"+ "虫食算（52-75ページ)\n"
						 	  + "\n"
						 	  + "梅屋萬年堂がpythonで書き直したものです(2022/07)")

		self.fr1 = ttk.Frame(self)
		self.cmb_questions = ttk.Combobox(self.fr1)
		self.btn_search = ttk.Button(self.fr1, text='検索開始'
								, command=self.on_btn_search)
		self.lbl_result = ttk.Label(self.fr1, text='検索結果')
		self.lbl_time = ttk.Label(self.fr1, text='探索にかかった時間')

		self.grid(column=0, row=0, sticky=tk.NSEW, padx=3, pady=3)
		master.grid_anchor(tk.CENTER)
		fr0.grid(column=0, row=0, padx=3, pady=3, ipadx=10, ipady=10)
		lbl01.grid(column=0, row=0, padx=10, pady=10, ipadx=10, ipady=10)

		self.fr1.grid(column=0, row=1, padx=3, pady=3)
		self.cmb_questions.grid(column=0, row=0, padx=3, pady=10)
		self.btn_search.grid(column=0, row=1, padx=3, pady=10)
		self.lbl_result.grid(column=0, row=2, padx=3, pady=10)
		self.lbl_time.grid(column=0, row=3, padx=3, pady=10)

		self.set_probrems()
		# self.set_probrems_from_file()


	def on_btn_search(self):
		qno = self.cmb_questions.get()
		if qno:
			self.lbl_result['text'] = ' '
			self.lbl_time['text'] = ' '
			self.fr1.update()
			probrem = self.probrems_dic[qno]
			start = time.time()
			bm = BruteForceMusikuizan(*probrem)
			ret = bm.search()
			elapsed_time = time.time() - start
			self.lbl_result['text'] = f'{ret}'
			self.lbl_time['text'] = f'{elapsed_time:.12f} 秒'
			self.fr1.update()
			del bm
		else:
			print('no selc')

	def set_probrems(self):
		self.probrems_dic = {
		"Q1" : ['9', '*', [], '27'],
		"Q2" : ['27', '*', [], '**9'],
		"Q3" : ['*9*', '*', [], '2*7'],
		"Q4" : ['***3', '*', [], '*6491'],
		"Q5" : ['**96', '*', [], '*13*4'],
		"Q6" : ['*1', '2*', ['*4*', '**3'], '****'],
		"Q7" : ['2*', '4*', ['*8', '6*'], '***'],
		"Q8" : ['7*', '**', ['**', '*5*'], '*3*'],
		"Q9" : ['*1*', '**', ['**3', '2***'], '***4'],
		"Q10" : ['**', '*8', ['*6', '**6'], '****'],
		"Q11" : ['1**', '7*', ['***', '****'], '***5', ['**3*', '0']],
		"Q12" : ['*9', '**', ['***', '*6*'], '*3**'],
		"Q13" : ['*6*', '*4*', ['***', '****', '**9*'], '**13*'],
		"Q14" : ['*33**', '*3*', ['***33', '****3', '*33**'], '********'],
		"Q15" : ['*1**', '2***', ['***6', '****5', '**4**', '*3**'], '****7**'],
		"Q16" : ['***', '*7***', ['****', '***', '***', '0', '****'], '********', ['***', '****', '***', '****', '0']],
		"Q17" : ['******', '****', ['***7890', '****6*', '****5**', '1234***'], '**********'],
		"Q18" : ['****', '***', ['**777', '*7**', '*7***'], '*******', ['**7*', '*7***', '0']],
		"Q19" : ['*1*****', '******', ['********', '****7*8', '*******', '**4*5*6*', '********', '2*3****'],'*******9*****'],
		"Q20" : ['****', '*******', ['****', '0', '0', '*****', '****', '****', '****'], '********000',
				 ['***', '****', '*****', '*****', '****', '****', '0']],
		"Q21" : ['****7*', '**7**', ['******', '*******', '*7****', '****7**', '******'], '**7*******',
			     ['*****7*', '*7****', '*******', '******', '0']]

		}
		self.cmb_questions['values'] = list(self.probrems_dic.keys())

	def set_probrems_from_file(self):
		iDir = os.path.abspath((os.path.dirname(__file__)))
		file_name = tkinter.filedialog.askopenfilename(initialdir=iDir)
		if not iDir:
			return
		self.probrems_dic  = {}
		with open(file_name, 'r', encoding='utf8') as f:
			ls = f.read()
			for line in ls.split('\n'):
				if 'comment' in line:
					break
				e1, e2 = line.split('=')
				self.probrems_dic[e1.strip()] = eval(e2)
			self.cmb_questions['values'] = list(self.probrems_dic.keys())




if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('500x500')
	app = Musikuizan(master=root)
	app.mainloop()

