import re
import pickle
import MeCab

PATH = "text/"
FILENAME = "akutagawa_kumonoito"

# テキストファイルの読み込み
file_r = PATH + FILENAME + ".txt"
with open(file_r) as f:
    text = f.read()

# 前処理
text = re.split(r"\-{5,}", text)[2]  # ハイフンより上を削除
text = re.split(r"底本：", text)[0]  # 「底本：」より下を削除
text = re.sub(r"［＃８字下げ.*?中見出し］", "", text)  # 中見出しを削除
text = re.sub("※", "", text)  # 「※」を削除
text = re.sub(r"《.*?》", "", text)  # 《...》を削除
text = re.sub(r"［.*?］", "", text)  # ［...］を削除
text = re.sub(r"（.*?）", "", text)  # （...）を削除
text = re.sub(r"｜", "", text)  # 「｜」を削除
text = re.sub("\n", "", text)  # 改行を削除
text = re.sub(r"\u3000", "", text)  # 全角スペースを削除
text = re.sub(r"。", "<period>", text)  # 句点を<period>に

# 「」内の<period>を句点に置換
pattern = re.compile("「.*?」")
match_sents = pattern.findall(text)
for i, m_sent in enumerate(match_sents):
    new_sent = m_sent.replace("<period>", "。")
    text = text.replace(m_sent, new_sent)

# <period>で分割
text_splitted = text.split("<period>")

# 空要素を取り除く
text_splitted = list(filter(None, text_splitted))


# １文ずつ形態素解析
mecab = MeCab.Tagger("-Owakati")
for i in range(len(text_splitted)):
    text_splitted[i] = mecab.parse(text_splitted[i]).split()
print(text_splitted)  # 確認

# テキストファイルに書き込む
file_w = PATH + FILENAME + "_splitted.txt"
s = ""
with open(file_w, mode="w") as f:
    for text in text_splitted:
        s += " ".join(text) + "\n"
    f.write(s)

# pickle化
file_wb = PATH + FILENAME + ".pickle"
with open(file_wb, mode='wb') as f:
    pickle.dump(text_splitted,f)
