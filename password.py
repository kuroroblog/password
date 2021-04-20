#! python3

# shelve : https://www.mutable.work/entry/python-shelve
import shelve, sys, random, re, string
# pyperclip : https://tonari-it.com/python-pyperclip-paste/
import pyperclip

# アプリ情報を出力する関数
# ファイル実行した場合に、ターミナル上へpasswordと表示される。
def appName():
    YELLOW = '\033[33m'
    END = '\033[0m'
    print()
    # 標準出力に関する、色の設定(https://hacknote.jp/archives/51672/)
    print(YELLOW + "     ########    ###     ######   ######  ##     #     ##   #####   ########  ######" + END)
    print(YELLOW + "     ##    ##  ##   ##  ##       ##        ##   ###   ##  ##     ## ##     ## ##    ##" + END)
    print(YELLOW + "     ######## #########  ######   ######    ## ## ## ##   ##     ## ########  ##    ##" + END)
    print(YELLOW + "     ##       ##     ##       ##       ##    ###   ###    ##     ## ##    ##  ##    ##" + END)
    print(YELLOW + "     ##       ##     ##  ######   ######     ##    ##       #####   ##     ## ######" + END)
    print()

# コマンドラインに関する案内を行う関数
# コマンドライン : https://wa3.i-3-i.info/word11158.html
# 第一引数が入力されていない場合に呼び出される。
def announce():
    print('※ 第一引数へ操作したい文字列を入力ください。以下入力例になります。')
    print(' ◯ python password.py list: 現在登録中のパスワードに紐づく名前一覧を出力します。')
    # クリップボードの意味(https://www.724685.com/word/wd140423.htm#:~:text=%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3%E7%94%A8%E8%AA%9E%E3%81%A7%E3%80%8C%E3%82%AF%E3%83%AA%E3%83%83%E3%83%97%E3%83%9C%E3%83%BC%E3%83%89%E3%80%8D%E3%81%A8,%E9%A0%98%E5%9F%9F%EF%BC%89%E3%80%8D%E3%81%AE%E3%81%93%E3%81%A8%E3%81%A7%E3%81%99%E3%80%82&text=%E3%80%8C%E3%82%B3%E3%83%94%E3%83%BC%E3%80%8D%E3%81%97%E3%81%A6%E3%80%8C%E8%B2%BC%E3%82%8A,%E3%81%B0%E3%80%8C%E7%A7%BB%E5%8B%95%E3%80%8D%E3%81%A8%E3%81%AA%E3%82%8A%E3%81%BE%E3%81%99%E3%80%82)
    print(' ◯ python password.py xxx: xxxに紐づくパスワードが登録済の場合、保存されているパスワードをコピーします。未登録の場合、新規でパスワード登録するのか、設問されます。yと選択する場合、パスワード登録してコピーします。')
    sys.exit()

# 生成されたパスワード文字列が、セキュリティ的に問題ないのか判定する関数
# passwordが強ければTrue, そうでなければFalseを返す
def pwStrengthTest(password):
    # search() : https://note.nkmk.me/python-re-match-search-findall-etc/
    # 正規表現の先頭のr(raw文字列である。エスケープ文字列が存在しないことを意味する。) : https://docs.pyq.jp/python/library/string.html#raw
    # 正規表現 : https://userweb.mnet.ne.jp/nakama/
    # エスケープ文字 : https://e-words.jp/w/%E3%82%A8%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%97%E5%87%A6%E7%90%86.html#:~:text=%E3%82%A8%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%97%E5%87%A6%E7%90%86%E3%81%A8%E3%81%AF%E3%80%81%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0,%E3%82%92%E3%80%8C%E3%82%A8%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%97%E6%96%87%E5%AD%97%E3%80%8D%E3%81%A8%E3%81%84%E3%81%86%E3%80%82
    # re.search(re.compile(r'[A-Z]+'), password) : passwordの文字列内にA~Zの文字が1回以上存在するのか確認している
    # re.search(re.compile(r'[a-z]+'), password) : passwordの文字列内にa~zの文字が1回以上存在するのか確認している
    # re.search(re.compile(r'[0-9]+'), password) : passwordの文字列内に0~9の文字が1回以上存在するのか確認している
    # re.search(re.compile('[!-/:-@[-`{-~]+'), password) : passwordの文字列内に[!-/:-@[-`{-~]内の記号文字が1回以上存在するのか確認している
    if re.search(re.compile(r'[A-Z]+'), password) and re.search(re.compile(r'[a-z]+'), password) and re.search(re.compile(r'[0-9]+'), password) and re.search(re.compile('[!-/:-@[-`{-~]+'), password):
        return True
    else:
        return False

# 現在登録中のパスワードに紐づく名前一覧を出力する関数
def displayList():
    # パスワードに紐づく名前一覧を配列型で格納する
    nameList = list(pwShelf.keys())
    # 大文字小文字を区別しない文字列比較を行い、ソートする
    # https://docs.python.org/ja/3/howto/sorting.html#key-functions
    nameList.sort(key=str.lower)

    print('アルファベット順'.center(20, '-'))
    for name in nameList:
        print(name)
    print('-' * 28)

    sys.exit()

# パスワードをコピーする関数
def pwCopy(name):
    print(name + 'のパスワードを確認しました')

    # パスワードをクリップボードへコピーする。
    # https://www.724685.com/word/wd140423.htm#:~:text=%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3%E7%94%A8%E8%AA%9E%E3%81%A7%E3%80%8C%E3%82%AF%E3%83%AA%E3%83%83%E3%83%97%E3%83%9C%E3%83%BC%E3%83%89%E3%80%8D%E3%81%A8,%E9%A0%98%E5%9F%9F%EF%BC%89%E3%80%8D%E3%81%AE%E3%81%93%E3%81%A8%E3%81%A7%E3%81%99%E3%80%82&text=%E3%80%8C%E3%82%B3%E3%83%94%E3%83%BC%E3%80%8D%E3%81%97%E3%81%A6%E3%80%8C%E8%B2%BC%E3%82%8A,%E3%81%B0%E3%80%8C%E7%A7%BB%E5%8B%95%E3%80%8D%E3%81%A8%E3%81%AA%E3%82%8A%E3%81%BE%E3%81%99%E3%80%82
    pyperclip.copy(pwShelf[name])

    print('パスワードをコピーしました')

    sys.exit()

# コマンドライン入力にてエラーが発生した場合に終了する関数
# コマンドライン : https://wa3.i-3-i.info/word11158.html
def inputError(text):
    print(text + '\n新規でパスワードを生成することなく終了いたします。')
    sys.exit()

# パスワードを登録する関数
def registerPw(name, password):
    pwShelf[name] = password
    print('パスワードを登録しました')
    pwCopy(name)

if __name__ == "__main__":
    appName()
    try:
        name = sys.argv[1]
    # 第一引数が存在しない場合は、password.pyを実行するための案内処理を行う。
    except:
        announce()

    pwShelf = shelve.open('pw')
    if name == 'list':
        displayList()

    # 第一引数で指定した名前に紐づくパスワードが存在する場合
    if name in pwShelf.keys():
        pwCopy(name)

    print(name + 'のパスワードが登録されていません\nパスワードを生成して登録しますか？(y/n)')
    selectInput = input()
    if selectInput == 'y':
        print('パスワードを生成します\nパスワードの文字数を8文字以上で入力してください')
        # コマンドラインにて、パスワードの文字数の入力を受け付ける。
        # コマンドライン : https://wa3.i-3-i.info/word11158.html
        try:
            characterNum = int(input())
        except:
            inputError('パスワードの文字数入力に、数字以外の文字列が含まれていました。')

        if characterNum < 8:
            inputError('文字数入力が8以上ではありませんでした。')

        while True:
            # string.ascii_letters : https://docs.python.org/ja/3/library/string.html#string.ascii_letters
            # string.digits : https://docs.python.org/ja/3/library/string.html#string.digits
            # string.punctuation : https://docs.python.org/ja/3/library/string.html#string.punctuation
            # sample() : https://note.nkmk.me/python-random-choice-sample-choices/
            # 文字列の長さ分だけ配列型で1文字づつランダム取得する。文字の重複なし
            password = random.sample(string.ascii_letters + string.digits + string.punctuation, characterNum)
            # 配列の文字を結合する
            # join() : https://note.nkmk.me/python-string-concat/
            password = ''.join(password)

            # 強いパスワードが生成された場合、ループを抜ける
            if pwStrengthTest(password):
                registerPw(name, password)
    else:
        print('新規でパスワードを生成することなく終了しました。')
