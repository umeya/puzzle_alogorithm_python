# coding: utf-8

"""
「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）のテンパズルソルバー（24~25ページ）を梅屋萬年堂がpythonで書き直したものです。
展パズルのGUI部分をTkinterで実装しているクラスです。
2022/05/25
"""
import tkinter as tk
from tkinter import ttk


from number_puzzle_solver import NumberPuzzleSolver

class TenPuzzleSolver(ttk.Frame):
	def __init__(self, master:tk.Tk):
		super().__init__(master)
		
		master.title('ten puzzule solver')
		fr0 = ttk.Frame(self)
		lbl01 = tk.Label(fr0, width=38, relief=tk.RIDGE, bd=5,
						text="「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）\n"
							+ "のテンパズルソルバー（24~25ページ）を\n"
							+  "梅屋萬年堂がpythonで書き直したものです\n"
							+  "                     2022/05")
		fr1 = ttk.LabelFrame(self, text='入力してください')
		lbl11 = ttk.Label(fr1,text='４桁の数字')
		tcl_onValidate_digits = master.register(self.onValidate_digits)
		entry_4digits = tk.Entry(fr1, width=7, validate='key', vcmd=(tcl_onValidate_digits, '%P'))
		lbl12 = ttk.Label(fr1, text='合計の数値')
		tcl_onValidate_target = master.register(self.onValidate_target)
		entry_target = tk.Entry(fr1, width=7, validate='key', vcmd=(tcl_onValidate_target, '%P'))
		fr2 = ttk.Frame(self)
		btn_search = ttk.Button(fr2, text='検索開始'
			, command=lambda: self.on_btn_search(entry_4digits.get(), entry_target.get(), lstbx_results))
		fr3 = ttk.LabelFrame(self, text='検索結果')
		lstbx_results = tk.Listbox(fr3, width=10)

		self.grid(column=0, row=0, sticky=tk.NSEW, padx=3, pady=3)
		master.grid_anchor(tk.CENTER)
		fr0.grid(column=0, row=0, padx=3, pady=3, ipadx=10, ipady=10)
		lbl01.grid(column=0, row=0, padx=10, pady=10, ipadx=10, ipady=10)
		fr1.grid(column=0, row=1, padx=3, pady=3)
		lbl11.grid(column=0, row=0, padx=3, pady=3)
		entry_4digits.grid(column=1, row=0, padx=3, pady=3)
		lbl12.grid(column=0, row=1, padx=3, pady=3)
		entry_target.grid(column=1, row=1, padx=3, pady=3)
		fr2.grid(column=0, row=2, padx=3, pady=3)
		btn_search.grid(column=0, row=0, padx=3, pady=3)
		fr3.grid(column=0, row=3, padx=3, pady=3)
		lstbx_results.grid(column=0, row=0, padx=3, pady=3)

	def onValidate_digits(self, P):
		if P == '' or (P.isdigit() and len(P) <= 4):
			return True
		else:
			return False

	def onValidate_target(self, P):
		if P == '' or (P.isdigit() and int(P) <= 9 * 9 * 9 * 9):
			return True
		else:
			return False

	def on_btn_search(self, four_digits:str, target:int, lstbx:tk.Listbox):
		solver = NumberPuzzleSolver()
		exps = solver.solve(four_digits, int(target))
		lstbx.delete(0, tk.END)
		if len(exps) == 0:
			lstbx.insert(tk.END, "作れません")
		else:
			for exp in exps:
				lstbx.insert(tk.END, exp)
			lstbx.insert(tk.END, ' -----------')
			lstbx.insert(tk.END, f'  {len(exps)} 通り')
		del solver

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('400x500')
	app = TenPuzzleSolver(master=root)
	app.mainloop()
