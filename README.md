# MSX BASIC Auto Line Numbering Tool

MSX BASICをPCで書くときに使えるお助けツールです。  
以下の機能を含んでいます。

- 自動行番号付け機能
- 行番号ラベルエイリアス
- 大文字化

## 自動行番号付け機能

行番号を付けていないMSX BASICに行番号を自動的に付け、webMSXや実機などに`LOAD`できるようにします。
```
$ python autonum.py src.bas dest.bas
```
### 例
以下のようなプログラムを
```
print "Hello World"
print "Hello MSX BASIC"
```
以下のように変換します。
```
10 print "Hello World"
20 print "Hello MSX BASIC"
```
`-s`オプションで行番号の増分を指定できます。
```
$ python autonum.py -s 20 src.bas dest.bas
```

## 行番号ラベルエイリアス
`GOTO`コマンドなどで使用する行番号を`@`から始まるラベルによって表現できます。  
この機能はデフォルトで有効になっています。
### 例
以下のようなプログラムを
```
print "program launched!"
@loop_label
print "endless loop"
goto @loop_label
```
以下のように変換します。
```
10 print "program launched!"
20 print "endless loop"
30 goto 20
```

## 大文字化
プログラム上の英字を大文字化します。文字列リテラルやコメント内に含まれる文字は大文字化せずそのまま残します。  
`-U`オプションを使用することでこの機能を有効化します。
```
$ python autonum.py -U src.bas dest.bas
```
### 例
以下のようなプログラムを
```
print a
print "Hello World!"
rem ----comment-----
```
以下のように変換します。
```
10 PRINT A
20 PRINT "Hello World!"
30 REM ----comment-----
```