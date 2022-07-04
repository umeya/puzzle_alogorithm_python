# coding: utf-8
"""
「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）\n"+ "小町算とそのおまけ（32~47ページ)
	梅屋萬年堂がpythonで書き直したものです(2022/05)
"""
import tkinter as tk
from tkinter import ttk

from komatizan import Komatizan

class KomatizanTarget(ttk.Frame):
	def __init__(self, master: tk.Tk):
		super().__init__(master)

		master.title('小町算')
		fr0 = ttk.Frame(self)
		lbl01 = tk.Label(fr0, width=46, relief=tk.RIDGE, bd=5, justify=tk.LEFT,
						 text="「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）\n"+ "小町算とそのおまけ（32~47ページ）\n"
						 	  + "例　目標値 100 : 1*2+3+4*5+6+7 8-9\n"
						 	  + "                           7と8の間「空白」で78になる\n"
							  + "梅屋萬年堂がpythonで書き直したものです(2022/05)")

		fr1 = ttk.LabelFrame(self, text='目標の値')
		tcl_onValidate_target = master.register(self.onValidate_target)
		entry_target = tk.Entry(fr1, width=7, justify=tk.RIGHT, validate='key', vcmd=(tcl_onValidate_target, '%P'))
		entry_target.insert(0, "100")
		fr2 = ttk.Frame(self)
		btn_search = ttk.Button(fr2, text='検索開始'
								, command=lambda :self.on_btn_search(entry_target.get()))
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
		btn_search.grid(column=0, row=0, padx=3, pady=3)
		fr3.grid(column=0, row=3, padx=3, pady=3)
		self.lstbx_results.grid(column=0, row=0, padx=3, pady=3)
		fr4.grid(column=0, row=4, padx=3, pady=3)
		self.status.grid(column=0, row=0, padx=3, pady=3)

	def onValidate_target(self, P):
		if P == '' or P.isdigit():
			return True
		else:
			return False


	def on_btn_search(self, target:int):
		if target == '':
			return
		self.var_status.set("検索しています、お待ちください")
		self.lstbx_results.delete(0, tk.END)
		self.update()
		komatizan = Komatizan(int(target))
		komatizan.rec(0)
		ret = komatizan.results
		for exp in ret:
			self.lstbx_results.insert(tk.END, exp)
		self.lstbx_results.insert(tk.END, f' ----- {len(ret)}通り')
		self.var_status.set("")
		self.update()


if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('500x500')
	app = KomatizanTarget(master=root)
	app.mainloop()

