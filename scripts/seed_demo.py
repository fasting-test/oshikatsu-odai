# -*- coding: utf-8 -*-
# デモ用の見本データ(架空の5期メンバー)。使い方: python3 seed_demo.py <gasのURL>
import sys, json, urllib.request
URL = sys.argv[1]
def call(body):
    req = urllib.request.Request(URL, data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "text/plain"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode("utf-8"))
    if isinstance(d, dict) and d.get("error"):
        raise SystemExit("error: %s %s" % (d["error"], body.get("action")))
    return d

A = {  # 名前: [(日付, 答え, 五感)]
 u"さくら": [
  ("2026-12-03", u"子どもが学校から帰ってきて「今日楽しかった」と話してくれて、うれしかった。", "hearing"),
  ("2026-12-04", u"朝の散歩で見た霜がキラキラしていて、思わず立ち止まった。", "sight"),
  ("2026-12-05", u"雨の音を聞きながら本を読んで、心が落ち着いた。", "hearing"),
  ("2026-12-06", u"柚子の香りのハンドクリーム。冬が来たなとうれしくなった。", "smell,touch"),
  ("2026-12-08", u"予定が詰まりすぎて、自分の時間がないことにモヤモヤした。", ""),
  ("2026-12-09", u"静かな時間があると、気持ちが整う自分に気づいた。", ""),
  ("2026-12-10", u"来年、自分のやりたいことにどれだけ時間を使えるか、よく考えている。", ""),
 ],
 u"ゆり": [
  ("2026-12-03", u"友達から久しぶりにLINEが来て、心があたたかくなった。", ""),
  ("2026-12-05", u"台所でお湯が沸く音。なんだかほっとする。", "hearing"),
  ("2026-12-07", u"湯たんぽを抱えて寝たら、ぐっすり眠れた。", "touch"),
  ("2026-12-09", u"「ちゃんとしなきゃ」と思うと疲れる。肩の力を抜きたい。", ""),
 ],
 u"みずき": [
  ("2026-12-04", u"スーパーの花売り場のポインセチア。赤がきれいで元気が出た。", "sight"),
  ("2026-12-06", u"焼き芋の甘い香りに、子どもの頃を思い出した。", "smell,taste"),
  ("2026-12-08", u"家族に頼まれごとが重なって、イライラしてしまった。", ""),
  ("2026-12-10", u"仕事と家のこと、どちらも中途半端な気がして、よく考えている。", ""),
 ],
 u"あおい": [
  ("2026-12-03", u"同僚に「助かったよ」と言われて、うれしかった。", "hearing"),
  ("2026-12-06", u"朝いれたコーヒーの香りで、一日がいい気分で始まった。", "smell"),
  ("2026-12-09", u"楽しいと感じるのは、人と話しているときだと気づいた。", ""),
 ],
}
NOTES = {u"さくら": ["2026-12-03", "2026-12-04", "2026-12-06", "2026-12-07", "2026-12-09"], u"ゆり": ["2026-12-05", "2026-12-08"], u"みずき": ["2026-12-04"]}

ids, recs = {}, {}
for name, rows in A.items():
    s = call({"action": "registerOrResume", "display_name": name})
    ids[name] = s["id"]
    for date, text, senses in rows:
        s = call({"action": "saveRecord", "student_id": ids[name], "date": date, "text": text, "senses": senses})
    recs[name] = {r["date"]: r["id"] for r in s["my_records"]}
    for d in NOTES.get(name, []):
        call({"action": "toggleNote", "student_id": ids[name], "date": d, "on": True})
    print(name, len(rows), "records")

def react(who, author, date, t):
    call({"action": "react", "student_id": ids[who], "post_id": recs[author][date], "type": t})
def comment(who, author, date, text, parent=""):
    return call({"action": "addComment", "student_id": ids[who], "post_id": recs[author][date], "parent_id": parent, "text": text})

react(u"ゆり", u"さくら", "2026-12-03", "like"); react(u"みずき", u"さくら", "2026-12-03", "like")
react(u"あおい", u"さくら", "2026-12-09", "understand"); react(u"ゆり", u"さくら", "2026-12-09", "understand")
react(u"さくら", u"みずき", "2026-12-06", "energy"); react(u"あおい", u"みずき", "2026-12-06", "like")
react(u"さくら", u"ゆり", "2026-12-09", "understand"); react(u"みずき", u"ゆり", "2026-12-09", "understand")
react(u"さくら", u"あおい", "2026-12-06", "try")
comment(u"ゆり", u"さくら", "2026-12-09", u"わかります!私も一人の時間があると、やさしくなれる気がします。")
comment(u"さくら", u"みずき", "2026-12-06", u"焼き芋の香り、いいですね。私も食べたくなりました。")
comment(u"みずき", u"ゆり", "2026-12-09", u"肩の力を抜く、私も意識してみます。")
print("done")
