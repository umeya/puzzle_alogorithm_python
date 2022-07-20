# coding: utf-8

class SuudokuSolver():
	def __init__(self, field:list):
		self.board = [[field[r][c] for c in range(9)] for r in range(9)]

	def find_choices(self, r:int, c:int)->list:
		res = [n for n in range(1,10)]
		for i in range(9):
			if self.board[r][i] in res:
				res.remove(self.board[r][i])
			if self.board[i][c] in res:
				res.remove(self.board[i][c])
		br, bc = (r//3)*3, (c//3)*3
		for i in range(3):
			for j in range(3):
				if self.board[br+i][bc+j] in res:
					res.remove(self.board[br+i][bc+j])
		return res

	def find_empty(self)->bool: # False または　(r,c)でtrue
		for r in range(9):
			for c in range(9):
				if self.board[r][c] == -1:
					return (r, c)
		return (9, 9)

	def solve(self):
		rc0 = self.find_empty()
		if rc0 == (9, 9):
			return self.board
		else:
			r0, c0 = rc0
			can_use0 =  self.find_choices(r0, c0)
			node0 = [[r0, c0, can_use0]]
			return self.dfs(node0)

	def dfs(self, node)->str:
		while node != []:
			r, c, can_use = node.pop()
			while can_use != []:
				v = can_use.pop()
				self.board[r][c] = v
				rc = self.find_empty()
				if rc == (9,9):
					return self.board
				else:
					node.append([r,c,can_use])
					r, c = rc
					can_use = self.find_choices(r, c)
			self.board[r][c] = -1
		return False





