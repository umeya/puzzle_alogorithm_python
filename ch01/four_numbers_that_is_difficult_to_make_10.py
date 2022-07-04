# coding: utf-8

"""
「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）のテンパズルソルバー（24~25ページ）を梅屋萬年堂がpythonで書き直したものです。
27ページの”10を作ることが難しいパターン”の処理をしています。
2022/05/25

"""
from number_puzzle_solver import NumberPuzzleSolver
from fractions import Fraction  as fr

class NumberPuzzleSolverOnleFraction(NumberPuzzleSolver):
	def calc_poland_check_fraction(self, exp: str) -> bool:
		space = []
		for c in exp:
			if '0' <= c <= '9':
				space.append(int(c))
			else:
				second = space.pop()
				first = space.pop()
				if c == '+':
					space.append(first + second)
				elif c == '-':
					space.append(first - second)
				elif c == '*':
					space.append(first * second)
				else:  # c is '/'
					if second == 0:
						return False
					fs = fr(first, second)
					if fs.denominator != 1:
						return True
					space.append(fs)
		return False

#  -----------------------------------------------------

import tkinter as tk
from tkinter import ttk

class DifficultMake10(ttk.Frame):
	def __init__(self, master: tk.Tk):
		super().__init__(master)

		master.title('ten puzzule solver')
		fr0 = ttk.Frame(self)
		lbl01 = tk.Label(fr0, width=46, relief=tk.RIDGE, bd=5,
						 text="「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）\n"
							  + "テンパズルソルバーの分数を使わないと10を作れない数（27ページ）\n"
							  + "梅屋萬年堂がpythonで書き直したものです(2022/05)")

		fr2 = ttk.Frame(self)
		btn_search = ttk.Button(fr2, text='検索開始'
								, command=self.on_btn_search)
		fr3 = ttk.LabelFrame(self, text='検索結果')
		self.lstbx_results = tk.Listbox(fr3, width=41)

		fr4 = ttk.Frame(self)
		self.var_status =tk.StringVar(self)
		self.var_status.set("")
		self.status = ttk.Label(fr4, textvariable=self.var_status)

		self.grid(column=0, row=0, sticky=tk.NSEW, padx=3, pady=3)
		master.grid_anchor(tk.CENTER)
		fr0.grid(column=0, row=0, padx=3, pady=3, ipadx=10, ipady=10)
		lbl01.grid(column=0, row=0, padx=10, pady=10, ipadx=10, ipady=10)

		fr2.grid(column=0, row=2, padx=3, pady=3)
		btn_search.grid(column=0, row=0, padx=3, pady=3)
		fr3.grid(column=0, row=3, padx=3, pady=3)
		self.lstbx_results.grid(column=0, row=0, padx=3, pady=3)
		fr4.grid(column=0, row=4, padx=3, pady=3)
		self.status.grid(column=0, row=0, padx=3, pady=3)


	def on_btn_search(self):
		self.var_status.set("検索しています、お待ちください")
		self.lstbx_results.delete(0, tk.END)
		self.update()
		results = self.search_all()
		for d, exps in results:
			self.lstbx_results.insert(tk.END, d)
			self.lstbx_results.insert(tk.END, "     " + " , ".join(exps))
		self.lstbx_results.insert(tk.END, "   ---------------")
		self.lstbx_results.insert(tk.END, f"   {len(results)} 通り")
		self.var_status.set("")
		self.update()

	def search_all(self):
		results = []
		nps = NumberPuzzleSolverOnleFraction()
		for d in nps.generate_4digits_number_for_ten_puzzle():
			ret = nps.solve(d, 10, False)
			for exp in ret:
				if '/' not in exp:
					break
			else:
				difficult = []
				for exp in ret:
					if not nps.calc_poland_check_fraction(exp):
						difficult = []
						break
					difficult.append(nps.decode_poland(exp))
				else:
					if difficult:
						results.append((d, difficult))
		del nps
		return results
if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('500x500')
	app = DifficultMake10(master=root)
	app.mainloop()

# nps = NumberPuzzleSolverOnleFraction()
# list_of_4number = []
# for d in nps.generate_4digits_number_for_ten_puzzle():
# 	ret2 = nps.solve(d, 10, False)
# 	for exp in ret2:
# 		if '/' not in exp:
# 			break
# 	else:
# 		difficult = []
# 		for exp in ret2:
# 			if not nps.calc_poland_check_fraction(exp):
# 				difficult = []
# 				break
# 			difficult.append(nps.decode_poland(exp))
# 		else:
# 			if difficult:
# 				list_of_4number.append((d, difficult))
#
# for d, exps in list_of_4number:
# 	print(d, ':', exps)
#
"""
1158 : ['8/(1-1/5)']
1199 : ['(1+1/9)*9', '(1/9+1)*9', '9*(1+1/9)', '9*(1/9+1)']
1337 : ['(1+7/3)*3', '3*(1+7/3)', '3*(7/3+1)', '(7/3+1)*3']
3478 : ['(3-7/4)*8', '8*(3-7/4)']
"""