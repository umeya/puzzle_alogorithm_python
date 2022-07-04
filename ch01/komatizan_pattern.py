# coding: utf-8
"""
「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社） 小町算のパターン（49~50ページ
  梅屋萬年堂がpythonで書き直したものです(2022/05)
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from komatizan import Komatizan

class KomatizanForPattern(Komatizan):
	def __init__(self, target=100):
		super().__init__(target)
		self.patterns = dict()

	def rec(self, k:int):
		if k == 8:
			ret = self.calc()
			if ret[0] == self.target:
				key, val = tuple(ret[1]), self.decode(ret[1], ret[2])
				if key in self.patterns:
					self.patterns[key].append(val)
				else:
					self.patterns[key] = [val]
			return
		for sign_no in range(5):
			self.sign[k] = sign_no
			self.rec(k+1)

class KomatizanPattern(ttk.Frame):
	def __init__(self, master: tk.Tk):
		super().__init__(master)

		self.retured_patterns = None

		master.title('小町算')
		fr0 = ttk.Frame(self)
		lbl01 = tk.Label(fr0, width=46, relief=tk.RIDGE, bd=5, justify=tk.LEFT,
						 text="「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）\n"
							  + "小町算のパターン（49~50ページ）\n"
							+ "　　　　　　　　梅屋萬年堂がpythonで書き直したものです(2022/05)")

		fr1 = ttk.LabelFrame(self, text='目標の値')
		tcl_onValidate_target = master.register(self.onValidate_target)
		entry_target = tk.Entry(fr1, width=7, justify=tk.RIGHT, validate='key', vcmd=(tcl_onValidate_target, '%P'))
		entry_target.insert(0, "100")
		fr2 = ttk.Frame(self)
		self.btn_search = ttk.Button(fr2, text='検索開始'
								, command=lambda: self.on_btn_search(entry_target.get()))
		self.btn_save = ttk.Button(fr2, text='検索結果の保存', state=tk.DISABLED
								, command=lambda: self.on_btn_save(entry_target.get()))
		fr3 = ttk.LabelFrame(self, text='検索結果')
		self.lstbx_results = tk.Listbox(fr3, width=30)

		fr4 = ttk.Frame(self)
		self.var_status = tk.StringVar(self)
		self.var_status.set("")
		self.status = ttk.Label(fr4, textvariable=self.var_status)

		self.grid(column=0, row=0, sticky=tk.NSEW, padx=3, pady=3)
		master.grid_anchor(tk.CENTER)
		fr0.grid(column=0, row=0, padx=3, pady=3, ipadx=10, ipady=10)
		lbl01.grid(column=0, row=0, padx=10, pady=10, ipadx=10, ipady=10)
		fr1.grid(column=0, row=1, padx=3, pady=3)
		entry_target.grid(column=1, row=0, padx=3, pady=3)
		fr2.grid(column=0, row=2, padx=3, pady=3)
		self.btn_search.grid(column=0, row=0, padx=3, pady=3)
		self.btn_save.grid(column=1, row=0, padx=3, pady=3)
		fr3.grid(column=0, row=3, padx=3, pady=3)
		self.lstbx_results.grid(column=0, row=0, padx=3, pady=3)
		fr4.grid(column=0, row=4, padx=3, pady=3)
		self.status.grid(column=0, row=0, padx=3, pady=3)

	def onValidate_target(self, P):
		if P == '' or P.isdigit():
			return True
		else:
			return False

	def on_btn_search(self, target: int):
		if target == '':
			return
		self.btn_save['state'] = tk.DISABLED
		self.retured_patterns = None
		self.var_status.set("検索しています、お待ちください")
		self.lstbx_results.delete(0, tk.END)
		self.update()
		komatizan = KomatizanForPattern(int(target))
		komatizan.rec(0)
		self.retured_patterns = komatizan.patterns
		self.lstbx_results.insert(tk.END,
								  f' 目標値={target} : {len(self.retured_patterns)} パターン')
		for ptt, exps in self.retured_patterns.items():
			self.lstbx_results.insert(tk.END, f'{ptt}: ----- {len(exps)} 通り')
			l = ' , '.join(exps)
			self.lstbx_results.insert(tk.END, f'{l}')
		self.var_status.set("")
		self.btn_save['state'] = tk.NORMAL
		self.update()

	def on_btn_save(self, target: int):
		if self.retured_patterns is None:
			return
		filename = filedialog.asksaveasfilename( title='小町算パターンの保存ファイル',
												filetypes=[('cvs file', '*.cvs')])
		if filename:
			with open(filename, 'w', encoding='UTF-8') as f:
				f.write(f' 目標値={target} ; {len(self.retured_patterns)}\n' )
				for ptt, exps in self.retured_patterns.items():
					f.write(f'{ptt} ; {len(exps)}\n')
					f.write(' ; '.join(exps) + '\n')


if __name__ == '__main__':
	root = tk.Tk()
	# root.geometry('500x500')
	app = KomatizanPattern(master=root)
	app.mainloop()
