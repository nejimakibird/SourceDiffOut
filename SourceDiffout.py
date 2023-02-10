import os
import re
import shutil
import difflib

def diffout(new_filename , old_filename, out_dir):
### Differクラスでファイルを比較

    file1 = open(old_filename)
    encode = 'cp932'
    try:
        str1 = file1.readlines()
    except:
        #ダメだったら、ファイル閉じてUTFで読み直してリトライ
        file1.close()
        file1 = open(old_filename, encoding = 'utf-8')
        str1 = file1.readlines()
        encode = 'utf-8'

    

    file2 = open(new_filename)
    try:
        str2 = file2.readlines()
    except:
        #ダメだったら、ファイル閉じてUTFで読み直してリトライ
        file2.close()
        file2 = open(new_filename, encoding = 'utf-8')
        str2 = file2.readlines()
        encode = 'utf-8'

    output_diff = difflib.unified_diff(str1, str2)
    # 得られたリストを加工
    o=[]
    pattern = re.compile('---|\+\+\+|\@\@|-|\s|}')
    pattern2 = re.compile('^\+')
    for item in output_diff:
        # 文字列の判定
        # 先頭"---","+++","@@"," "(先頭スペース),"-"はコピーしない
        if re.match(pattern,item):
            # 一致したので何もしない
            # print(item + " 対象外行として判定")
            pass
        else:
            # 先頭の"+"を除去して文字列をリストに追加する
                item = re.sub(pattern2, '',item)
                o.append(item)

    # ファイル出力
    outfilename = os.path.basename(new_filename)
    outfilename = os.path.join(out_dir, outfilename)

    with open(outfilename, 'w',encoding = encode) as f:
        f.writelines(o)
        f.close()

    file1.close()
    file2.close() 


# 最終的にはプロンプトで対話的に取得できるようにする
oldtop=input("古いファイルを保管するフォルダ")
top=input("新しいファイルを保管するフォルダ")
outtop=input("差分ファイルを保管するフォルダ")

# ディレクトリ存在確認
if os.path.isdir(oldtop):
    pass
else:
    print(oldtop + 'がありません。処理を中断します。')
    exit()

if os.path.isdir(top):
    pass
else:
    print(top + 'がありません。処理を中断します。')
    exit()

if os.path.isdir(outtop):
    pass
else:
    print(outtop + 'がありません。処理を中断します。')
    exit()

for root, dirs, files in os.walk(top):
    for dir in dirs:
        #格納先ディレクトリ構造を生成
        dirPath = os.path.join(root, dir)
        outpath = dirPath.replace(top, outtop)
        if os.path.isdir(outpath):
            pass
        else:
        # ない場合にはフォルダを生成
            os.makedirs(outpath)

    for file in files:
        newfileName = os.path.join(root, file)
        print(f'filePath = {newfileName}')
        oldfileName = newfileName.replace(top, oldtop)
        if os.path.isfile(oldfileName):
            #print(oldfilepath + " が存在")
            #ここで、差分があるか確認してなければスキップ。あれば差分ファイルを生成。
            outdir = root.replace(top, outtop)
            diffout(newfileName, oldfileName, outdir)
        else:
            print(oldfileName + " がない")
            #ないものについては、ファイルコピーする
            outfilepath = newfileName.replace(top, outtop)
            shutil.copy2(newfileName, outfilepath)

