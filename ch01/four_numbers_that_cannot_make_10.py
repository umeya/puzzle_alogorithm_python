# coding: utf-8
"""
「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）のテンパズルソルバー（24~25ページ）を梅屋萬年堂がpythonで書き直したものです。
テンパズルソルバーの10を作れない４つの数の組み合わせ一覧（26ページ）を作るのクラスです。
2022/05/25

"""
import tkinter as tk
from tkinter import ttk

from number_puzzle_solver import NumberPuzzleSolver

class CannotMake10(ttk.Frame):
	def __init__(self, master: tk.Tk):
		super().__init__(master)

		master.title('ten puzzule solver')
		fr0 = ttk.Frame(self)
		lbl01 = tk.Label(fr0, width=46, relief=tk.RIDGE, bd=5,
						 text="「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）\n"
							  + "テンパズルソルバーの10を作れない４つの数の組み合わせ一覧（26ページ）\n"
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
		l = ""
		for i, d in enumerate(results):
			l = l + " " + d
			if i % 10 == 9:
				self.lstbx_results.insert(tk.END, l)
				l = ""
		l = l + f"   {len(results)} 通り"
		self.lstbx_results.insert(tk.END, l)
		self.var_status.set("")
		self.update()

	def search_all(self):
		results = []
		nps = NumberPuzzleSolver()
		for d in nps.generate_4digits_number_for_ten_puzzle():
			ret = nps.solve(d, 10)
			if len(ret) == 0:
				results.append(d)
		del nps
		return results

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('500x500')
	app = CannotMake10(master=root)
	app.mainloop()


# nps = NumberPuzzleSolver()
# i = 0
# for d in nps.generate_4digits_number_for_ten_puzzle():
# 	ret = nps.solve(d, 10)
# 	if len(ret) == 0:
# 		i += 1
# 		if i % 10 == 0:
# 			print(d)
# 		else:
# 			print(d, end=' ')
# print(f'  合計 {i} 通り')

"""
0000 0001 0002 0003 0004 0005 0006 0007 0008 0009
0011 0012 0013 0014 0015 0016 0017 0018 0022 0023
0024 0026 0027 0029 0033 0034 0035 0036 0038 0039
0044 0045 0047 0048 0049 0056 0057 0058 0059 0066
0067 0068 0069 0077 0078 0079 0088 0089 0099 0111
0112 0113 0114 0116 0117 0122 0123 0134 0144 0148
0157 0158 0166 0167 0168 0177 0178 0188 0222 0233
0236 0269 0277 0279 0299 0333 0335 0336 0338 0344
0345 0348 0359 0366 0369 0388 0389 0399 0444 0445
0447 0448 0457 0478 0479 0489 0499 0566 0567 0577
0588 0589 0599 0666 0667 0668 0677 0678 0689 0699
0777 0778 0788 0799 0888 1111 1112 1113 1122 1159
1169 1177 1178 1179 1188 1399 1444 1499 1666 1667
1677 1699 1777 2257 3444 3669 3779 3999 4444 4459
4477 4558 4899 4999 5668 5788 5799 5899 6666 6667
6677 6777 6778 6888 6899 6999 7777 7788 7789 7799
7888 7999 8899   合計 163 通り
"""
