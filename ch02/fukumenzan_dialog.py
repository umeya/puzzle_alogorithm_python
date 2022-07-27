# coding: utf-8
import tkinter as tk

class FukumenzanDialog(tk.Toplevel):
	def __init__(self, parent, numbers_of_targets, mondai=[]):
		tk.Toplevel.__init__(self, parent)
		self.parent = parent
		self.numbers_of_targets = numbers_of_targets
		self.mondai = mondai
		self.return_ok = False
		self.title(u'覆面算: ' + str(numbers_of_targets) + '個の数と合計の記入')
		if self.mondai == []:
			self.ent_num_var = [tk.StringVar() for _ in range(numbers_of_targets)]
			self.ent_sum_var = tk.StringVar()
		else:
			self.ent_num_var = [tk.StringVar(value=self.mondai[i]) for i in range(numbers_of_targets)]
			self.ent_sum_var = tk.StringVar(value=self.mondai[-1])

		self.ent = []
		self.lbl = []
		for r in range(numbers_of_targets):
			self.ent.append(tk.Entry(self, relief=tk.GROOVE,justify=tk.RIGHT,font=("", 24), textvariable=self.ent_num_var[r]))
			self.ent[r].grid(row=r, column=1, pady=8)
			self.lbl.append(tk.Label(self, justify=tk.CENTER,text=str(r+1) + u' 番目の数'))
			self.lbl[r].grid(row=r, column=0)

		self.lbl1 = tk.Label(self, text='-'*42)
		self.lbl1.grid(row=numbers_of_targets, column=0, columnspan=3)

		self.ent_sum = tk.Entry(self, relief=tk.GROOVE, justify=tk.RIGHT, font=("", 24), textvariable=self.ent_sum_var)
		self.ent_sum.grid(row=numbers_of_targets+1, column=1)
		self.lbl_sum = tk.Label(self, justify=tk.CENTER, text=u'合計の数')
		self.lbl_sum.grid(row=numbers_of_targets+1, column=0)
		self.ok_button = tk.Button(self, text=u"記入", relief=tk.SOLID,command=self.on_ok)
		self.ok_button.grid(row=numbers_of_targets+2, column=1, padx=5, pady=10, ipadx=6, ipady=6)
		self.ok_button = tk.Button(self, text=u"取消", relief=tk.SOLID,command=self.on_cancel)
		self.ok_button.grid(row=numbers_of_targets+2, column=2, padx=10, pady=20, ipadx=6, ipady=6)

	def on_ok(self, event=None):
		self.return_ok = True
		self.destroy()

	def on_cancel(self, event=None):
		self.return_ok = False
		self.destroy()


	def show(self):
		self.wm_deiconify()
		self.ent[0].focus_force()
		self.wait_window()
		if self.return_ok:
			return [self.ent_num_var[r].get() for r in range(self.numbers_of_targets)] + [self.ent_sum_var.get()]
		else:
			return ''
