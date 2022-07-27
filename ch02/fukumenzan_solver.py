# coding: utf-8

class FukumenzanSolver():
	def __init__(self, probrem_):
		'''

		:param probrem_: 問題の文字列のリスト（刺繍要素は、合計値の文字列）
			このクラスの中では、左からの桁位置を扱いやすくするため、逆順にしておく。数字が入る　board_もその位置に対応するように扱う。
			probrem_ ['SEND', 'MORE', 'MONEY']
			, self.probrem_['DNES', 'EROM', 'YENOM']
			, self.board_ [[v11,v12,v13,v14], [....], [v31,v32,v33,v34,v35]]
			          v11 は文字Dの数字、v12 は文字Nの数字、v13 は文字Eの数字、v14 は文字Sの数字、　　　、v32 は文字Eの数字(=v11)
		'''
		self.probrem_, self.board_ = [], []
		self.used_, self.fu_dict, self.chrs = [], {}, []
		self.NOTIN = -1
		for r, row in enumerate(probrem_):
			self.probrem_.append(list(reversed(row)))
			self.board_.append([self.NOTIN for _ in range(len(row))])

		for d in range(len(self.probrem_[-1])):
			for r in range(len(self.probrem_)):
				if d < len(self.probrem_[r]):
					c = self.probrem_[r][d]
					if c in self.fu_dict:
						self.fu_dict[c]['rd'].append((r,d))
						self.fu_dict[c]['nodes'] += 1
					else:
						self.fu_dict[c] = {'rd':[(r, d)], 'val':0, 'nodes':1}
						self.chrs.append(c)


	def get_size(self):
		return len(self.probrem_)

	def get_digit(self, row:int = -1):
		return len(self.probrem_[row])

	def is_used(self, val:int)->bool:
		return True	if val in self.used_ else False

	def get_val(self, row:int, digit:int)->int:
		if digit >= self.get_digit(row):
			return 0
		else:
			return self.board_[row][digit]

	def set_val_with_chr(self, c, val:int):
		for r, d in self.fu_dict[c]['rd']:
			self.board_[r][d] = val
		self.used_.append(val)

	def reset_val_with_chr(self, c:str):
		for r, d in self.fu_dict[c]['rd']:
			val = self.board_[r][d]
			if val != self.NOTIN:
				self.board_[r][d] = self.NOTIN
				if val in self.used_:
					self.used_.remove(val)

	def is_valid(self):
		for val in self.board_:
			if val[-1]==0:
				return False
		kuriage:int = 0
		number_targets = sum_row_number= self.get_size() - 1
		for digit in range(self.get_digit()):
			sum:int = 0
			for row in range(number_targets):
				v:int = self.get_val(row, digit)
				if  v == self.NOTIN:
					return True
				if row != number_targets:
					sum += v
			sum_digit = self.get_val(sum_row_number, digit)
			if sum_digit == self.NOTIN:
				return True
			sum += kuriage
			kuriage, sum = divmod(sum, 10)
			if sum != sum_digit:
				return False
		return (kuriage == 0)

	def solve(self):

		ret = self.dfs(0)
		if ret:
			return self.board_
		else:
			return []

	def dfs(self, idx:int)->bool:
		while  True:
			if idx >= len(self.chrs):
				return True
			elif idx < 0:
				return False

			target_c = self.chrs[idx]
			val = self.fu_dict[target_c]['val']
			if val > 9:
				self.reset_val_with_chr(target_c)
				self.fu_dict[target_c]['val'] = 0
				idx -= 1
				self.reset_val_with_chr(self.chrs[idx])
				self.fu_dict[self.chrs[idx]]['val'] += 1
			else:
				if self.is_used(val):
					self.fu_dict[target_c]['val'] += 1
				else:
					self.set_val_with_chr(target_c, val)
					if self.is_valid():
						idx += 1
						if idx < len(self.chrs):
							self.fu_dict[self.chrs[idx]]['val'] = 0
					else:
						self.reset_val_with_chr(target_c)
						self.fu_dict[target_c]['val'] += 1
