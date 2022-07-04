# coding: utf-8

"""
「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）のテンパズルソルバー（24~25ページ）を梅屋萬年堂がpythonで書き直したものです。
目標合計値targetとなる式の探索本体のクラスです。
2022/05/25
"""
from fractions import Fraction as fr

class NumberPuzzleSolver():
	def solve(self, digits:str, taget:int, decode_reverse_politish_notatio:bool =True) -> list:
		"""

		:param digits: 使用する４個の数字
		:param taget: 目標の合計値
		:param decode_reverse_politish_notatio:逆ポーランド記法で式を作り探索しているが、
		　　　　　　　　結果を通常の式に戻すときにTrue,逆ポーランド記法のままの時はFaulse
		:return: 目標合計値となる式（文字列）のリスト
		"""
		results = []
		n, e, ne = self.four_digits_pattern(digits)
		for di in self.generate_repeated_perm_r_tings_from_e(n, e, 4):
			d = [ne[i - 1] for i in di]
			for op1 in '+-*/':
				for op2 in '+-*/':
					for op3 in '+-*/':
						exps = ["".join([d[0], d[1], d[2], d[3], op1, op2, op3]),
								"".join([d[0], d[1], d[2], op1, d[3], op2, op3]),
								"".join([d[0], d[1], d[2], op1, op2, d[3], op3]),
								"".join([d[0], d[1], op1, d[2], d[3], op2, op3]),
								"".join([d[0], d[1], op1, d[2], op2, d[3], op3])]
						for exp in exps:
							if self.calc_poland(exp) == taget:
								if decode_reverse_politish_notatio:
									results.append(self.decode_poland(exp))
								else:
									results.append(exp)
		return results

	def calc_poland(self, exp: str) -> fr:
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
						return None
					space.append(fr(first, second))
		return space.pop()

	def decode_poland(self, exp: str) -> str:
		space = []
		for c in exp:
			if '0' <= c <= '9':
				space.append(c)
			else:
				second = space.pop()
				first = space.pop()
				if c in '*/':
					if len(first) > 1:
						first = '(' + first + ')'
					if len(second) > 1:
						second = '(' + second + ')'
				space.append(first + c + second)
		return space.pop()

	def four_digits_pattern(self, four_digits: str) -> tuple:
		"""
		:param four_digits: ４桁の数の文字列　この関数内部でソートされたリストにする
							（例　"2113" は　['1','1','2','3'])
		:return:tuple (n, e, ne)
						n 数字の個数　（例　3）
						e 各数字の個数　（例　[2,1,1])
						ne 各数字　（例　['1', '2', '3']
		"""
		n, dd = 0, 0
		e0, ne0 = ['dummy'], [0]
		for d in sorted(four_digits):
			if d != ne0[n]:
				n += 1
				e0.append(1)
				ne0.append(d)
			else:
				e0[n] = e0[n] + 1
		return (n, e0[1:], ne0[1:])

	def generate_repeated_perm_r_tings_from_e(self, n: int, e: list, r: int) -> list:
		"""
		「組み合わせアルゴリズム」（千波一郎、サイエンス社）の重複順列生成アルゴリズムを参考にし作成した
		重複順列生成ジェネレータです。

		要素がXi個あるn種類のものから重複を許してr個取り出してできる順列
		:param n: 種類数
		:param x: e[0]　種類1の個数、e[1]　種類２の個数、…、e[n-1]　種類nの個数
		:param r: 取り出す個数（順列の長さ）
		:return: 生成された順列のリスト
		"""
		x = [1] + e + [0]
		p = [0 for i in range(r + 1)]
		k = 0
		while True:
			while k < r and x[p[k]] > 0:
				x[p[k]] = x[p[k]] - 1
				k += 1
				p[k] = 1
			if k == r and x[p[k]] > 0:
				yield (p[1:])
			while p[k] == n:
				k -= 1
				x[p[k]] = x[p[k]] + 1
			p[k] = p[k] + 1
			if k == 0:
				return

	def generate_4digits_number_for_ten_puzzle(self):
		"""
		:return: ４桁の数 d1 d2 d3 d4
		           d1 <= d2 <= d3 <= d4
		"""
		for d1 in range(10):
			for d2 in range(d1, 10):
				for d3 in range(d2, 10):
					for d4 in range(d3, 10):
						d = str(d1) + str(d2) + str(d3) + str(d4)
						yield d



if __name__ == '__main__':
	#  テキスト２５ページの例
	solver = NumberPuzzleSolver()
	print(solver.solve('3478', 10))
