## guess_the_number.py

- 最低値と最高値を入力し、その間に存在する数値がランダムで作成されるので、その数値を当てるゲーム。
- 実行コマンド
  `python guess_the_number.py`

## file_manipulator.py

- reverse inputpath outputpath: inputpath にあるファイルを受け取り、outputpath に inputpath の内容を逆にした新しいファイルを作成します。
- copy inputpath outputpath: inputpath にあるファイルのコピーを作成し、outputpath として保存します。
  duplicate-contents inputpath n: inputpath にあるファイルの内容を読み込み、その内容を複製し、複製された内容を inputpath に n 回複製します。
- replace-string inputpath needle newstring: inputpath にあるファイルの内容から文字列 'needle' を検索し、'needle' の全てを 'newstring' に置き換えます。
- 実行コマンド例
  `python file_manipulator.py copy sample.txt sample_out.txt`
