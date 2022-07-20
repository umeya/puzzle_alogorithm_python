**このレポジトリ**

ここにあるものは、「パズルで鍛えるアルゴリズム力」（大槻兼資、技術評論社）のソルバーなどをC++からpythonで書き換え、一部のものはpyinstallerで実行ファイルしたものです。
各章のbinフォルダーにはpyinstallerで作成した実行ファイルがあります。

**各章にあるファイル**
###### 第１章

* number_puzzle_solver.py <br>テンパズル探索本体のクラス
* ten_puzzle_solver.py <br>テンパズルのメインクラス
*  four_numbers_that_cannot_make_10.py <br>合計値10を作れない４桁の数
*  four_numbers_that_is_difficult_to_make_10.py <br>合計値10を作ることが困難な（分数を使わないとできない）４桁の数
*  komatizan_target.py <br>小町算ソルバー
*  komatizan_pattern <br>小町算のパターン探索
*    musikizan.py 虫食い算<br>musikuizan.txt 虫食い算の問題のファイル

###### 第２章
* suudoku_solver.py 数独ソルバー<br>suudoku.py 数独問題の入力などの処理<br>sd2_3.txt テキスト（９１ページ）にある問題、<br>sd17hints.txt テキスト（１０２ページ）にある問題ですが、ここのソルバーでは時間がかかりすぎです。(^^;