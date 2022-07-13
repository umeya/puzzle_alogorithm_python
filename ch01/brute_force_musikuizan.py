# coding: utf-8
"""
「パズルで鍛えるアルゴリズム力」（大槻兼資　著、技術評論社）虫食い算の力ませの探索（62-64ページ)
	梅屋萬年堂がpythonで書き直したものです(2022/07)
"""
import time
from itertools import product as n_product

class BruteForceMusikuizan():
	"""
		 掛け算の筆算での虫食い算を力まかせの探索で解く
	"""
	def __init__(self, multiplicand:str, multiplier:str, partial_pruduct:list, product:str, partial_remainder:list = []):
		'''
		以下のパラメターの説明にはにはテキストの図１−３９の例を使用している。-は空きの穴を表す
		:param multiplicand: 被乗数書く桁の数字の入ったリスト -1-----は '*1*****'
		:param multiplier:   乗数のリスト------は '******'
		:param partial_pruduct:部分積のリスト
		        下の例はテキスト５８ページ乗法Q19
		        multiplicand '*1*****', multiplier '******'
		                         k, partial_product[k]
		           2-3----       5, '2*3****',
		         --------        4, '********'
		        --4-5-6-       は 3, '**4*5*6*',
		        -------           2, '*******',
		    ----7-8               1, '****7*8',
		  --------                0, '********'
		:param product:
		      -------9-----   は '*******9*****'

		       テキスト５６ページ除法の例Q16
		       multiplicand(=divisor) '***', multiplier(=dividend) '*7***'

		                 k, partial_product
		                     , partial_remaimder
		    *7***
		   _________
		***)********
		    ****        k=0,  '***'
		    ________
		      ***             ,'***'
		      ***       k=1,  '***'
		      ______
		      ****            , '****'
		       ***      k=2, '***'
		      _______
		                      ,'***'     ここは次に２桁お「おろされて」いるので補った部分
		                k=3,  '0'
		      _______
		        ****       ,  '****'
		        ****    k=4,  '****'
		      ______
		           0          ,'0'

		以上の引数は以下の形式のリストを展開している
		乗法の場合
		    [被乗数 , 乗数, 部分積のリスト, 積]
		除法の場合
		    [除数, 尚, 部分積のリスト, 被除数, 部分剰余のリスト]
		'''
		self.multiplicand, self.multiplier, self.partial_pruduct, self.product\
			= self.make_number_list(multiplicand), self.make_number_list(multiplier), partial_pruduct, product
		self.plican_len, self.plier_len = len(multiplicand), len(multiplier)
		self.partial_remainder = partial_remainder


	def search(self):
		for plicand_l in n_product(*self.multiplicand):
			plicand = int(''.join(plicand_l))
			res = self.next_multiplier(plicand)
			if res:
				return res
		else:
			return 'no solution'

	def next_multiplier(self, plicand:int):
		k = 0
		multiplier_ki = [-1 for _ in range(self.plier_len)]
		while True:
			if k < 0:
				return False
			if k < self.plier_len:
				multiplier_ki[k] += 1
				if multiplier_ki[k] >= len(self.multiplier[k]):
					multiplier_ki[k] = -1
					k -= 1
				else:
					if self.partial_pruduct == []:
						k += 1
					else:
						d = int(self.multiplier[k][multiplier_ki[k]])
						if self.check_product(str(plicand * d), self.partial_pruduct[k]):
							k += 1

			elif k >= self.plier_len:
				multiplier = int(''.join([self.multiplier[i][ki] for i, ki in enumerate(multiplier_ki)]))
				if self.check_product(str(plicand * multiplier), self.product):
					if not self.partial_remainder:
						return f'{plicand} * {multiplier} = {plicand*multiplier}'
					else:
						if self.check_remainder(plicand, str(multiplier)):
							return f'{plicand*multiplier} / {plicand} = {multiplier}'
				k -= 1
				if k < 0:
					return False




	def make_number_list(self, e:str):
		"""
				:param e: 虫食いで空白がある数の文字列
				　　　　　　（例）　'b7b' は百と一の位が虫食いの空白
				:return: 生成された数の各桁の数字ののリスト
				"""
		e_l = []
		for i, d in enumerate(e):
			if d != '*':
				e_l.append(d)
			else:
				if i == 0:
					e_l.append('123456789')
				else:
					e_l.append('0123456789')
		return e_l

	def check_product(self, p1, p2):
		if len(p1) != len(p2):
			return False
		for i, p2d in enumerate(p2):
			if p2d == '*':
				continue
			if p1[i] != p2d:
				return False
		return True

	def check_remainder(self,plicand:int , plier_l:str):
		prd = str(plicand * int(plier_l)) +'0'
		# p_rem_p = len(self.partial_pruduct[0])
		p_rem_p = len(prd) -len(plier_l)
		p_rem = int(prd[:p_rem_p])
		for k in range(len(self.partial_remainder)):
			p_prd = plicand * int(plier_l[k])
			p_rem = (p_rem - p_prd) * 10 + int(prd[p_rem_p + k])
			if not self.check_product(str(p_rem), self.partial_remainder[k]):
				return False

		return True


if __name__ == '__main__':
	Q1 = ['9', '*', [], '27']
	Q2 = ['27', '*', [], '**9']
	Q3 = ['*9*', '*', [], '2*7']
	Q4 = ['***3', '*', [], '*6491']
	Q5 = ['**96', '*', [], '*13*4']
	Q6 = ['*1', '2*', ['*4*', '**3'], '****']
	Q7 = ['2*', '4*', ['*8', '6*'], '***']
	Q8 = ['7*', '**', ['**', '*5*'], '*3*']
	Q9 = ['*1*', '**', ['**3', '2***'], '***4']
	Q10 = ['**', '*8', ['*6', '**6'], '****']
	Q11 = ['1**', '7*', ['***', '****'], '***5', ['**3*', '0']]
	Q12 = ['*9', '**', ['***', '*6*'], '*3**']
	Q13 = ['*6*', '*4*', ['***', '****', '**9*'], '**13*']
	Q14 = ['*33**', '*3*', ['***33', '****3', '*33**'], '********']
	Q15 = ['*1**', '2***', ['***6', '****5', '**4**', '*3**'], '****7**']
	Q16 = ['***', '*7***', ['****', '***', '***', '0', '****'], '********', ['***', '****', '***', '****', '0']]
	Q17 = ['******', '****', ['***7890', '****6*', '****5**', '1234***'], '**********']
        #  0.8014097213745117 (176315, 6487)
	Q18 = ['****', '***', ['**777', '*7**', '*7***'], '*******', ['**7*', '*7***', '0']]
	    # 0.06418204307556152 5252489 / 5753 = 913
	Q19 = ['*1*****', '******', ['********', '****7*8', '*******', '**4*5*6*', '********', '2*3****'], '*******9*****']
        #  1.903304100036621 (1165096, 981992)
	Q20 = ['****', '*******', ['****', '0', '0', '*****', '****', '****', '****'], '********000', ['***', '****', '*****', '*****', '****', '****', '0']]
	    #  9.910115003585815 10000016000 / 1664 = 6009625
	Q21 = ['****7*', '**7**', ['******', '*******', '*7****', '****7**', '******'], '**7*******', ['*****7*', '*7****', '*******', '******', '0']]
	    #  0.3083310127258301 7375428413 / 125473 = 58781
	Q22 = [                            '************************',
		   '********************',
									   ['*********************9*0*', '********************8*1**',
										'******************6*3****', '******************7*2***',
										'*****************5*4*****', '***************3*6*******',
										'***************4*5******', '*************1*8*********',
										'*************2*7********', '***********0*9**********',
										'**********9*0***********', '*********8*1************',
										'*******6*3**************', '*******7*2*************',
										'******5*4***************', '*****4*5****************',
										'****2*7******************', '****3*6*****************',
										'**0*9********************', '**1*8*******************'],

				   '*********************************************']

	start = time.time()
	bm = BruteForceMusikuizan(*Q22)
	res = bm.search()
	elapsed_time = time.time() - start
	print(elapsed_time, res)
