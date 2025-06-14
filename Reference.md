## outube動画をAIに理解させてテキストコンテンツを自動生成


今回はchatGPTを活用したコンテンツ自動生成系のネタを持って参りました、一言で言うと"AIにyoutube見せてテキストコンテンツを自動生成させよう"という試みです。

動画をAIに解釈させる手法って動画音声の入力からが多かったと思いますが、今回は動画のシーン解析と音声解析をセットにしてchatGPTに渡してみたら、思ったよりも精度が高く"このまま使えるやん"と気付きましたのでお披露目します。


目次
動作はこんな感じ
用途
コスト
必要な物
仕組み
動画取得
映像解析
音声解析
chatGPTで返答
課題

すべて表示
動作はこんな感じ

動画内容を把握するシステムって色々ありますが、"音声+映像+LLM"の組み合わせって僕は見た事なかったので作って見ましたら、想像よりも汎用性の高そうな物に仕上がりました。

用途
当システム最大のメリットは"人間が動画を見なくても高い精度でAIが内容を把握できる"事で、要は疑似的な【目+耳+脳みそ】のコンボを個人が安価に利用できるようになったという点です。

各業界の隅々まで調べれば数えきれないくらいのニーズを発掘できると思いますが、ぱっと思い付いたのはこんな感じ。

◆ youtube台本の再現：
　→ 他のyoutuberからネタを拝借
◆ 教育動画コンテンツの要約、整理：
　→ 教科書作れちゃう
◆ 動画トピック・チャプターの自動生成（動画の検索性向上）：
　→ 映像の内容をキーワード検索できる
◆ テキストコンテンツの自動生成：
　→ 書籍/ブログ/メルマガなんでもござれ
◆ インタビュー要約・ハイライト生成：
　→ 映像情報も含めた1ランク上の文字起こしを実現
◆ アニメ、ドラマ、映画などの評論生成：
　→ 口下手なあなたの代わりにLLMが無限の語彙力でサポート
◆ 専門コンテンツをかみ砕いて解説：
　→ 動画内容が難し過ぎてもLLMが理解をサポート

いかがでしょうか。LLM使ってテキストコンテンツを生成している方も多いと思いますが、内容がイマイチだと思った事ありません？

当システムはプロンプトだけでなく動画情報をベースとしてスタートするので、こちらが細かく指示しなくても似たような雰囲気の動画を指定するだけで、いい感じのテキストを出力してくれます。

コスト
延べ10数時間程度の動画解析を行った結果、金額のボリューム感はこんな感じに。

画像
200円くらいでした、安っ！

生成したコンテンツのボリューム的には、ブログ記事にして1ヶ月分は出力したと思います。

課金額はchatGPTへの入出力トークン数で決まりますんで、インパクトの大きい要素は①シーン切替数,②レスポンスの文字数です。

つまり、長時間の動画やシーン切替検出の感度を高くするとコストは増加しますが、いずれもパラメータによってコントロールできますし、ほぼ無制限で使用した結果が上記画像なのでこんなもんです。

必要な物
python

openaiAPIKEY

openaiアカウントへお金チャージ

パソコンのスペックも高級な物は不要です、GPUなしでも十分に使えるように作りました。

仕組み
ざっくり工程をまとめるとこんな感じ。

1. 動画取得
2. シーン検出
3. 映像解析
4. 音声文字起こし
5. chatGPTで返答

割とシンプル構成かなと思います。

動画取得
youtube動画の取得はyt_dlpが使いやすくてお気に入りです。

yt-dlp/yt-dlp: A feature-rich command-line audio/video downloader
A feature-rich command-line audio/video downloader - yt-dlp/yt-dlp

GitHub
映像解析
色々検討した結果、現状では"scenedetect+GPT-4o-mini"のコンボが安価で高精度という結論になりました。やっている事はこんな感じ。

1. scenedetectで動画のシーンを検出＆保存
2. 紙芝居みたいになった画像をすべてopenAIAPIへ渡す
3. 1シーンごとに力技でGPT-4o-miniが内容をテキスト化

例えばこの動画を映像解析してみるとこんなレスポンスが返ってくる。


Scene 1: Start: 0.00s - End: 5.17s
Image Path: images/scene_1_frame_0.jpg
Analysis: 画像は、空の電車内を示している。座席は青いシートが張られ、通路は広く整然としている。照明は明るく、車両の構造が清潔感を保っている印象を与える。人がいないため、静けさが感じられるシーンである。このような状況は、運行中の電車がまだ乗客を迎える前の瞬間か、または終点に到着した後の様子と推測できる。

Scene 2: Start: 5.17s - End: 47.91s
Image Path: images/scene_2_frame_155.jpg
Analysis: 画像はぼやけており、詳細を確認することは難しい。おそらく、夜間や暗い場所で撮影された鉄道車両の一部が映っている可能性がある。明かりが点灯しているような箇所が見受けられ、駅やホーム付近での情景かもしれない。全体的に不明瞭であるため、正確な状況を把握することは困難である。

Scene 3: Start: 47.91s - End: 59.76s
Image Path: images/scene_3_frame_1436.jpg
Analysis: 暗い背景に光源が一つあり、周囲はぼんやりとした影に包まれている。光の周りには何かが浮かんでいるように見えるが、詳細は不明である。夜間のシーンであり、光が特定の対象を照らしている可能性がある。全体的に神秘的な雰囲気を持った画像である。

Scene 4: Start: 59.76s - End: 74.87s
Image Path: images/scene_4_frame_1791.jpg
Analysis: 画像は暗い背景の中に光のスポットが見える状況を示しています。文字には「完全にとれたでしょうの」と書かれており、何かの状況や状態が完全に収束したことを示唆しています。このシーンは、動画撮影や状況の記録が行われている場面の一部である可能性があります。光の効果から、周囲の環境は不明ですが、暗闇の中での明るさの対比が印象的です。

Scene 5: Start: 74.87s - End: 82.55s
Image Path: images/scene_5_frame_2244.jpg
Analysis: 画像は暗い環境で撮影されており、青色の網が中央に配置されている。網の向こうには水面が見え、微かな光が反射している。周囲には岩のような構造物があり、水辺で何かを捕まえようとしている様子が窺える。全体としては、夜間の探検や釣り、あるいは水生生物の観察を行っているシーンと推測される。

Scene 6: Start: 82.55s - End: 109.38s
Image Path: images/scene_6_frame_2474.jpg
Analysis: 青いネットの中に魚がいる様子が見受けられ、文字には「アブラハヤだ」と記載されている。これはアブラハヤという淡水魚の一種であり、捕獲されたシーンと思われる。光が当たっている部分から、周囲は暗い環境であると推測される。魚の形状や特徴から、観察や釣りなどのアクティビティが行われている可能性が高い。

==長いので省略==

かなり精度高くないですか？音声データなしですよ。

音声解析
whisperというライブラリがあるのでこれ1本で解決、ちなみにwhisperもopenAI製。ヤバすぎ。

openai/whisper: Robust Speech Recognition via Large-Scale Weak Supervision
Robust Speech Recognition via Large-Scale Weak Supervision - openai/whisper

GitHub
使いごこちは記事にまとめましたので気になる方は一読下さい。

【耳以上】音声認識AI whisperをpythonで動かしてyoutube動画を文字起こしする
youtubeの音声をpythonで文字起こしする機会がありまして、音声認識ライブラリのSpeechRecognition
diy-programming.site
chatGPTで返答
上記の映像解析と音声解析で計算した結果をopenaiAPI経由でまたまたGPT-4o-miniへ渡します。

この時に一緒に渡すプロンプトで返答内容を指示できます、これは上記の章"用途"で出したアイデアの話ですね。台本を作って下さい/インタビューを要約して下さい/評論して下さいみたいな事です。

で、これらの作業をやってみるとこんな感じで返答してくれます。

【サンプル1：専門性の高いコンテンツをテキスト化】


messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f'''
                以下は動画の映像と音声の解析結果です\n
                マニュアルを作成するための詳細なアウトラインを作成して下さい\n
                各アウトラインごとに分かりやすく読み応えのある解説テキストを生成して下さい\n
                解説のテキストは
                🎬 **映像解析結果**:
                {analysis_results}
                🎧 **音声解析結果**:
                {transcription_results}
                '''
            }
        ]
    }
]

copy
### レザークラフトのためのマニュアル

#### 1. はじめに
- **概要**: このマニュアルでは、初心者向けにレザークラフトの基本を解説します。视频を参考にしながら実際に道具を使って手を動かしていくことが重要です。

---

#### 2. 必要な道具
- **道具のリスト**:
- トーグ
- ヘラ
- ガラス板
- カッター
- ビニプライ
- シャーペンや定規
- 各種穴開けツール、針
- ボンド

- **詳細な解説**:
初めてレザークラフトを始める方にとって、必要な道具を知ることが不可欠です。**トーグ**は皮に穴を開けたり、型紙を叩きつけたりする時に便利です。**ヘラ**は、塗っていく際に用いることが多く、家にあるものを代用できます。**ガラス板**は加工した皮を滑らかに仕上げるために使い、代用としては平らな木の板などでも可能です。

---

#### 3. 材料の準備
- **皮の下処理**:
- トーグの使用方法
- カットするための道具選び

- **解説**:
皮の準備段階ではトーグを使用して、皮の端を整えることから始まります。次に、切り出しを行うのですが、この際には切れ味の良い**カッター**を選ぶことが重要です。オルファシャのカッターが初心者にはオススメです。

---

#### 4. 穴開け作業
- **必要なツールの紹介**:
- **ディバイダー**: 線を引くための道具。微調整が可能で、正確な線を描けます。
- **しめうち**: 穴を開けるための道具。様々なサイズのものがあるため、用途に合わせて選びます。

- **解説**:
穴開け作業では、まずディバイダーで印を付け、その後しめうちで実際に穴を開けます。これにより、縫い目の位置を正確に決めることができます。

---

#### 5. 縫製作業
- **必要な道具**:
- **針と糸**: 糸は丈夫である必要があり、メーカーやタイプによって特性が異なります。
- **糸切りバサミ**: 短い糸をカットするために使用します。

- **解説**:
縫製作業には、適切な糸や針を選ぶことが鍵となります。糸の強度と素材を考慮し、必要に応じて選んでください。また、糸切りバサミは家庭にあるもので代用できるでしょう。

---

#### 6. 製作プロセス
- **作業の流れ**:
1. 皮の選定とカット
2. 穴開け
3. 縫製
4. 最終仕上げ

- **解説**:
製作過程は創造的で楽しめる作業です。皮のカットから始め、印を付けて穴を開け、最後に縫製するという流れです。プロセスを丁寧に行うことで、より完成度の高い作品が仕上がります。

---

#### 7. 仕上げ作業
- **必要な器具**:
- ボンドや接着剤、仕上げ用の道具（ドレッサーなど）。

- **解説**:
仕上げの段階では、細かな部分にボンドを使用して、全体を美しく整えます。道具の使い方に慣れてくることで、より仕上げの質も向上します。

---

#### 8. おすすめの参考文献と情報
- **コミュニティの活用**: オンラインフォーラムやYouTubeチャンネルでのレザークラフトのコミュニティに参加することで、他の人の作品や技術を参考にできる良い機会が得られます。

- **書籍**: 基本的な技術や材料について、更に深く学べる書籍を読むこともおすすめです。

---

#### 9. まとめ
- **プロジェクトの振り返り**: 各ステップごとに振り返り、必要なことと改善点を考えて次に生かしていきましょう。

- **感謝の言葉**: 最後まで読んでいただきありがとうございます。これからのレザークラフトの旅を楽しんでください。

---

このガイドが、あなたのレザークラフトのスタートを助けることができれば幸いです。楽しんで創作をしてください！

【サンプル2：時事ニュースをSNS用に短縮】


messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f'''
                以下は動画の映像と音声の解析結果です\n
                ニュース映像をSNSで投稿するために映像・音声両面から要点を分かりやすくまとめて欲しい\n
                🎬 **映像解析結果**:
                {analysis_results}
                🎧 **音声解析結果**:
                {transcription_results}
                '''
            }
        ]
    }
]

copy
🏅 **ニュース要点まとめ** 🏅

- 映像はロサンゼルス・ドジャース対ニューヨーク・メッツの野球試合を中心に展開。
- 試合の進行中、ドジャースが2点をリードし、選手たちが活況を呈している様子が捉えられている。
- 大谷選手が重要な3点ホームランを打ち、観客の興奮が最高潮に達する瞬間も描かれている。
- 試合はナショナルリーグ選手権シリーズの一部で、観客席は多くのファンで賑わっている。

🏆 期待と緊張感溢れるスポーツイベントとして、試合の焦点が大谷選手に集まっていることが伺える。

【サンプル3：youtunerの台本再現】


messages=[
    {"role": "system", "content": "あなたはyoutube専門の脚本家です、視聴者が最後まで見てしまうような台本を書いて下さい"},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f'''次の映像解析と音声解析の結果から動画の台本を作成して下さい\n
                台本には元動画を参考にしてオリジナルな要素を追加して下さい\n
                映像解析: {analysis_results}\n
                音声解析: {transcription_results}'''
            }
        ]
    }
]

copy
# 台本：夜の川辺での冒険と料理

---

### シーン 1: 静寂の中に始まる旅 (0:00 - 1:50)
*映像: 明るい公共交通機関の車内。静かな雰囲気。*

**ナレーション**
>「誰も乗っていない静かな車内。外はまだ暗く、これからの冒険への期待感が漂っている。今日は特別な夜。どこへ向かうのか、何が待っているのか楽しみだね！」

### シーン 2: 田舎の夜に到着 (1:51 - 3:00)
*映像: 黄色い街灯が点灯する夜道。*

**ナレーション**
>「到着しました！超田舎に来ましたね。月が綺麗じゃない？周りには何も見えないけれど、ワクワクする瞬間です。真っ暗な中、川へ向かう準備をしよう！」

### シーン 3: 夜の川探検 (3:01 - 7:00)
*映像: 川の流れる音、微かな水音が響く。*

**ナレーション**
>「皆さんこんばんは。今日は夜の川での探検です。魚たちが寝ている時間だから、捕まえるチャンス！空腹も満たしつつ、楽しんでいきましょう！」

### シーン 4: 魚の発見 (7:01 - 10:00)
*映像: 手の中に捕まえた魚を映す。*

**ナレーション**
>「見て見て！魚が普通にいる。ライトで照らしても逃げないなんて、今日は楽勝に捕まえられそうだ！」

### シーン 5: 安価な網と釣りの楽しさ (10:01 - 13:00)
*映像: 100円の網を手にする。*

**ナレーション**
>「100円の網をゲットしました！さて、これで一匹捕まえられるかな…？完全に捕れた瞬間を楽しみにしていてください！」

### シーン 6: 釣りの成功 (13:01 - 15:00)
*映像: 捕まえた魚を映す。*

**ナレーション**
>「お、捕れた捕れた！この瞬間、絶対にたまらないよね。みんなも挑戦してみて！」

### シーン 7: 夜の川の気配 (15:01 - 18:30)
*映像: 暗く静かな川辺。*

**ナレーション**
>「今、夜の川辺で静かなひとときを楽しんでいます。危険もあるので、必ず仲間と一緒に来てね。油の匂いも気になる…、お腹も空いたし、どんどん捕まえていくよ！」

### シーン 8: 食材集め (18:31 - 22:00)
*映像: 複数の魚やカニを捕まえるシーン。*

**ナレーション**
>「見てください、サワガニも捕まえました！まさに自然の恵み。これから料理にして、皆で美味しくいただきます！」

### シーン 9: 料理の準備 (22:01 - 26:00)
*映像: 料理の準備過程。油が温まっている。*

**ナレーション**
>「今からささっと料理していきます！新鮮な魚とカニ。香ばしい香りがするわ。待ちきれない！」

### シーン 10: 料理の完成 (26:01 - 30:00)
*映像: 魚やカニが焼かれている様子。*

**ナレーション**
>「できました！みんなで作った料理、これから味わいます。最高のごちそうだよ！」

### シーン 11: 食べる瞬間 (30:01 - 33:00)
*映像: 魚を味わうシーン。*

**ナレーション**
>「いただきます！あぁ、うまい！新鮮で最高、今日は最高の夜になりました！」

### シーン 12: 次回の予告 (33:01 - 35:00)
*映像: 夜空と川辺の風景。*

**ナレーション**
>「次回は海の生き物を捕まえに行きます。どんな冒険が待っているのか、楽しみにしていてください。チャンネル登録と高評価も忘れずに！」

---

*映像はフェードアウトし、次回の予告が映し出される。*

レスポンスに関してはプロンプトを研究すればもっと精度が精度が上がると思いますが、仕組み的には実用レベルと言えそうです。

課題
今回作ったシステムは個人が手元で使う分には十分なレベルと思いますが、改善ポイントとして課題に感じている事が3つあります。これらを解消できれば普通に有料サービスとして通用するんじゃないかしら。

処理の高速化
普通のパソコンで使う事を前提に作りましたんでCPUで動作する仕組みになっています、つまり"まぁまぁ遅い"って事です。

例えばこの動画を処理するとこれくらいの時間が必要。


画像
8:13の動画を処理するのに6:40くらいかかりました。

これはpytorchとかでGPUに対応させれば割と簡単に改善できる気がします。

最終的にはシーン検出精度と処理速度がトレードオフなので、精度を取るか速度をとるかという話になると思いますが、とりあえずGPUに対応させれば爆速になるハズです。

whisperで話者分離
whisperはデフォで声の分類ができません、どのセリフを誰が言ったか分類できれば恐らくcahtGPTのレスポンス精度も向上するでしょう。

研究している方は結構いるので、実装はそこまで難しくは無さそうに思います。

Whisperで文字起こしをした議事録の発話者の名前を自動的に判定する！ - Qiita
こんにちは！逆瀬川 ( @gyakuse ) です！今日は最近作った議事録文字起こしアプリに話者分離機能をくっつけたものを
qiita.com
pyannote.audioで簡単話者分離〜whisperを添えて〜 - Qiita
音声認識の世界では、OpenAIが開発したwhisperというモデルが話題になりましたね。99言語に対応しており、日本語の
qiita.com
GPT-4o-miniの入出力限界
GPT-4o-miniは入力で128,000トークン / 出力で16,384トークンが上限です。

gh640/openai-models-ja: (Japanese) OpenAI 社が提供するモデルの一覧
(Japanese) OpenAI 社が提供するモデルの一覧. Contribute to gh640/openai-models-ja development by creating an account on GitHub.

GitHub
日本語で言えば入力：約160,000文字 / 出力：20,000文字程度ですが、当システムはテキストだけでなく映像もトークン化してchatGPTに渡しているので、入力できるトークン数はさらに制限されます。

こちらもシーン検出精度とトレードオフなので"動画時間が〇分なら〇トークン"とは一概には言えませんが、実際に使っている感じだと数十分程度の動画であればレスポンスに不足なしという印象です。

もし128kトークン制限に抵触するほど長大な動画を処理する場合は、動画側を一定時間以下に分割してからchatGPTに渡してレスポンスを結合する、みたいな処理が必要になると思います。

コピペスクリプト
まずファイルの構造はこちら。

画像
【requirements.txt】

annotated-types==0.7.0
anyio==4.6.0
Brotli==1.1.0
certifi==2024.8.30
charset-normalizer==3.4.0
click==8.1.7
colorama==0.4.6
distro==1.9.0
exceptiongroup==1.2.2
filelock==3.16.1
fsspec==2024.9.0
h11==0.14.0
httpcore==1.0.6
httpx==0.27.2
idna==3.10
Jinja2==3.1.4
jiter==0.6.1
llvmlite==0.43.0
MarkupSafe==3.0.1
more-itertools==10.5.0
mpmath==1.3.0
mutagen==1.47.0
networkx==3.4.1
numba==0.60.0
numpy==2.0.2
openai==1.51.2
openai-whisper @ git+https://github.com/openai/whisper.git@25639fc17ddc013d56c594bfbf7644f2185fad84
opencv-python==4.10.0.84
pillow==10.4.0
platformdirs==4.3.6
pycryptodomex==3.21.0
pydantic==2.9.2
pydantic_core==2.23.4
regex==2024.9.11
requests==2.32.3
scenedetect==0.6.4
six==1.16.0
sniffio==1.3.1
sympy==1.13.3
tiktoken==0.8.0
torch==2.4.1
tqdm==4.66.5
typing_extensions==4.12.2
urllib3==2.2.3
websockets==13.1
yt-dlp==2024.10.7

copy
【main.py】

import os
import shutil
import time
from youtube_dl import download_youtube_video
from scene import detect_scene_changes_pyscenedetect
from scene_analysis import analyze_image
from transcription import transcribe_video
from make_text import create_text_manual

def main():
    start_time = time.time()  # 処理開始時間を記録
    
    video_id = "video_id"
    video_path = f'videos\\{video_id}.mp4'
    images_folder = './images'
    videos_folder = './videos'
    
    # 動画と画像をリセット
    shutil.rmtree(videos_folder)
    os.mkdir(videos_folder)
    shutil.rmtree(images_folder)
    os.mkdir(images_folder)
    
    # YouTube動画ダウンロード
    download_youtube_video(video_id, "./videos")

    # シーン検出
    scene_changes = detect_scene_changes_pyscenedetect(video_path)

    # 画像の解説
    analysis_results = []  # 解析結果を保存するリスト
    for scene in scene_changes:
        image_path = scene['image_path']
        result = analyze_image(image_path)
        if result:
            scene_analysis = {
                'scene_number': scene['scene_number'],
                'start_time': scene['start_time'],
                'end_time': scene['end_time'],
                'image_path': scene['image_path'],
                'analysis': result
            }
            analysis_results.append(scene_analysis)
            print(f"Scene {scene['scene_number']}: Start: {scene['start_time']:.2f}s - End: {scene['end_time']:.2f}s\nImage Path: {scene['image_path']}\nAnalysis: {result}\n")
        else:
            print(f"Error processing {image_path}")
            
    print(analysis_results)     

    # ビデオの文字起こし
    transcription_results = transcribe_video(video_path)
    
    print(transcription_results)

    # テキストマニュアルの生成
    manual = create_text_manual(analysis_results, transcription_results)
    
    # 生成されたマニュアルをファイルに保存
    with open('contents.txt', 'w', encoding='utf-8') as f:
        f.write(manual)
    
    end_time = time.time()  # 処理終了時間を記録
    elapsed_time = end_time - start_time  # 経過時間を計算
    print(f"処理が完了しました。所要時間: {elapsed_time:.2f}秒")

if __name__ == "__main__":
    main()

copy
【youtube_dl.py】

ここから先は有料部分です
import yt_dlp

def download_youtube_video(video_id, output_path):
    
    video_url = "https://www.youtube.com/watch?v="+video_id
    
    try:
        # yt-dlpオプションを設定
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{output_path}/{video_id}.%(ext)s'
        }

        # ダウンロードを実行
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

copy
【scene.py】

import cv2
import os
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector

def detect_scene_changes_pyscenedetect(video_path):
    # 設定変数
    threshold = 60.0  # シーン検出のしきい値 下げると敏感に 上げると鈍感に
    output_folder = 'images'  # 画像保存先フォルダ

    # Videoを開き、SceneManagerの初期化
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    # 動画を解析してシーンの境界を見つける
    scene_manager.detect_scenes(video)

    # 検出されたシーンのリストを取得
    scene_list = scene_manager.get_scene_list()
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # フォルダの作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    scenes_with_length = []

    for i, scene in enumerate(scene_list):
        start_frame = scene[0].get_frames()
        #end_frame = scene[1].get_frames() 
        end_frame = scene[1].get_frames() - 1 #シーン最後のフレームを保存する場合
        start_time = start_frame / fps
        end_time = end_frame / fps
        scene_length = end_time - start_time

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        ret, frame = cap.read()
        if ret:
            image_path = f"{output_folder}/scene_{i + 1}_frame_{start_frame}.jpg"
            cv2.imwrite(image_path, frame)
            scenes_with_length.append({
                "scene_number": i + 1,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "start_time": start_time,
                "end_time": end_time,
                "length": scene_length,
                "image_path": image_path
            })

    # タイムスタンプ順に並べ替える
    scenes_with_length = sorted(scenes_with_length, key=lambda x: x["start_time"])

    cap.release()
    return scenes_with_length

copy
【scene_analysis.py】

import os
import base64
from openai import OpenAI

# OpenAI APIキーの設定
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# 画像をエンコードする関数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 画像を解析する関数
def analyze_image(image_path):
    
    # 画像をbase64にエンコード
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=10000,
        messages = [
            {
                "role": "system",
                "content": "あなたは画像解析の専門家です。以下の画像についての客観的なコメントをしてください。"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "この画像の客観的なコメントを返す,文字が含まれている場合は優先的に考慮する,どんなシーンか推測,コメントに前置きは不要,である調,必ず日本語"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ]
    )

    # レスポンスのcontent部分を抽出して返却
    try:
        return response.choices[0].message.content
    except (AttributeError, IndexError):
        return "解析結果が取得できませんでした。"

copy
【transcription.py】

import whisper

def transcribe_video(video_path):
    try:
        # モデルの指定
        model = whisper.load_model("small")
        # ファイルの指定と文字起こしの実行
        result = model.transcribe(video_path, verbose=True, fp16=False, language="ja")
        segments = result['segments']
        extracted_data = [
            {
                "start": segment['start'],
                "end": segment['end'],
                "text": segment['text']
            } for segment in segments
        ]
        return extracted_data
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

copy
【make_text.py】

import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def create_text_manual(analysis_results, transcription_results):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=10000,
        messages=[
            {"role": "system", "content": "あなたはyoutube専門の脚本家です、視聴者が最後まで見てしまうような台本を書いて下さい"},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f'''次の映像解析と音声解析の結果から動画の台本を作成して下さい\n
                        台本は元動画が分からないように脚色しオリジナルな要素を追加して下さい\n
                        映像解析: {analysis_results}\n
                        音声解析: {transcription_results}'''
                    }
                ]
            }
        ]
    )
    
    # レスポンスのcontent部分を抽出して返却
    try:
        return response.choices[0].message.content
    except (AttributeError, IndexError):
        return "解析結果が取得できませんでした。"

copy
使い方
実際に使い始めるまでに必要な手順をまとめました。

環境の構築
上記のプロジェクト環境とpythonファイルをコピペして用意します。

必要ライブラリのインストール
pip install -r requirements.txt

copy
必須パラメータ設定
必要なのは下記の2点だけです。

youtube_id（main.py）

OPENAI_API_KEY（scene_analysis.py, make_text.py）

まずはこの二つを埋めて下さい。

処理実行
python main.py

copy
CPUで動作する用なので処理時間は結構かかります、おおよそ動画時間と同じくらいは必要かなと思います。

処理が終わったらmain.pyと同じ階層に"contents.txt"が生成されます、この中に指示したプロンプトに従ったコンテンツが保存されているので確認して下さい。

コントロール可能なパラメータ
レスポンスのクオリティに関係する部分をまとめました。

main.py：13行目 video_id = "video_id"（youtube動画のID）
→ https://www.youtube.com/watch?v=〇〇〇  ←マルの値

scene.py：8行目 threshold = 50.0（シーン検出の感度）
→ 上げると鈍感,下げると敏感に。高い値からスタートして精度が足りなければ下げて行くスタイルがオススメ

scene.py：33行目 end_frame = scene[1].get_frames() - 1（シーンの最初と最後どっち使か）
→ スライド資料的な時間経過で情報が追加される映像はシーン最後を使った方が精度上がる

scene_analysis.py：28行目（画像認識プロンプト）
→ 映像によって変えた方が精度出るかも

transcription.py：13行目 language="ja" （文字起こしする言語）
→ 日本語ならja、英語ならenなど

make_text.py：14行目 （出力用プロンプト）
→ 用途に合わせて指示を変える

とりあえずここら辺を覚えておけば不足なく使えると思います。

レスポンスの精度が低い場合のtips
◆ シーン検出の閾値を敏感にしてみる
　→ その代わり多少コストが嵩む
◆ 検出シーンで使うフレームを最初・最後で変えてみる
　→ 基本的には最後の方が精度上がると思うけど、最初の方がいい場合もあるかも
◆ 出力用プロンプトの見直し
　→ プロンプトもchatGPTに考えて貰った方が大抵クオリティ上がります
◆ モデル変更（"gpt-4o-mini"→"gpt-4o"）
　→ 最終手段、1回辺りのコストが十数倍になっちゃうぞ

まとめ
今まではyoutube動画を自動生成するネタが多かったですが、youtubeに存在する無尽蔵な動画コンテンツを活かして何か出来ないかなという発想から今回のネタが生まれました。

動画の内容って音声からだけじゃ把握できない内容も多くて、作業動画とかvlogみたいなジャンルだと声って入らない場合多いんですよ。

風景+テロップでの解説がメインになっていても、今回のシステムであれば映像から得られる情報もchatGPTが理解できるので結構な精度が期待できます。

皆様が今回のシステムを上手いこと使ってボロ儲け出来る事をお祈り申し上げておきますm(_ _)m