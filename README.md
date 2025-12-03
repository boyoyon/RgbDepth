<html lang="ja">
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
        <h1><center>RgbDepth</center></h1>
        <h2>なにものか？</h2>
        <p>
            RGB画像とdepth画像を指定して、3Dオブジェクトを表示します。<br>
            <br>
            入力画像<br>
            <img src="data/cat.png"><br>
            3Dオブジェクト表示<br>
            <img src="images/cat.gif">
        </p>
        <h2>環境構築方法</h2>
        <p>
            pip install opencv-python open3d
        </p>
        <h2>使い方</h2>
        <p>
            python  RgbDepth.py  (RGB画像ファイル)  (depth画像ファイル)  [(Zscale) (fx) (fy) (cx) (cy)]<br>
            ※ ピクセルとz値の比率が不明のため、Zscale引数で調整します。<br>
               その他のパラメータは下図参照<br>
            <img src="images/RgbDepth.png">
            <table border="1">
                <tr><th>操作</th><th>機能</th></tr>
                <tr><td>左ボタン押下＋ドラッグ</td><td>3Dモデルの回転</td></tr>
                <tr><td>ホイールボタン押下＋ドラッグ</td><td>3Dモデルの移動</td></tr>
                <tr><td>ホイール回転</td><td>3Dモデルの拡大・縮小</td></tr>
                <tr><td>PrintScreenキー押下</td><td>スクリーンショット保存</td></tr>
                <tr><td>ウィンドウ閉じるボタン押下　</td><td>プログラム終了</td></tr>
            </table>
            <h3>使用例</h3>
            <img src="images/RgbDepth2.png">             
        </p>
        <h2>RGB画像からdepth画像の作成例</h2>
        <h3>depth推定ソフトウェアで画像からdepth画像を作成する。</h3>
        <p>
            Depth Anything V2 などを使って画像からdepth画像を作成する。<br>
            <a href="https://huggingface.co/spaces/depth-anything/Depth-Anything-V2">https://huggingface.co/spaces/depth-anything/Depth-Anything-V2</a><br>
            <br>
            <img src="images/step1_1.svg">
        </p>
                <h2>Lotus-2が良さそうだったので試してみた</h2>
        <p>
            Lotus-2という深度推定器はなかなか良さそう。
        <p>
        <img src="images/Lotus2.svg">
        <p>
            Githubでコードが公開されているが、GPUメモリ40GBなどと記されており諦めてWEBデモを試してみた。<br>
            ・出力がグレースケールではなく、ヒートマップ表示だったので, 泥臭くdepth画像に変換してみた。<br>
            ・もっとスマートな方法があるとは思うが、やりかたを知らないので･･･<br>
            <br>
            [0] ヒートマップ画像を探して、値順の色相の配列を作成 (spectral.npy作成用。作成済なので実行不要)<br>
            python colormap2npy.py <br>
            <img src="src/spectral.png"><br>
            <br>
            [1] Lotus-2のWEBデモで画像から深度画像(ヒートマップ)を作成する。<br>
            <a href="https://huggingface.co/spaces/haodongli/Lotus-2_Depth">Lotus-2のDepth推定デモページ</a>　SSDマシンはダメみたい<br>
            ヒートマップの深度推定結果が得られる。(data/colormap_*.png 参照。鼻の頭の深度が飽和している･･･)<br>
            <br>
            [2] spectral.npyを参照して、グレースケールの深度画像に変換する。<br>
            python heatmap2depth.py (ヒートマップ画像)<br>
            <br>
            [3] 3D表示する。<br>
            python RgbDepth2.py (RGB画像) (グレースケールの深度画像)<br>
            ・ゴミが表示される･･･デバッグ中<br>
            ・鼻の頭がつぶれる･･･Lotus-2のヒートマップで潰れているので直せない<br>
            ・’@'キー, '[' キー押下で画角を変更可能。'[' キーを目いっぱい押した方が良いようだ。<br>
            ・1キー～6キーでモデルを回転できる。<br>
            ・出っ張り具合（Z scale)は第三引数で指定する。<br>
            ・縦に長くしたい場合は第四引数を大きくする。<br>
             <img src="images/point_clound.gif"><br>
            RgbDepth2.py の以下のコメントを有効化(#を削除)すれば、ESCキー押下で点群をplyファイルに書き出しする。<br>
            その代わりプログラム終了に時間が掛かるようになる。<br>
            # base = os.path.basename(argv[1])<br>
            # filename, _ = os.path.splitext(base)<br>
            # dst_path = '%s_o3d.ply' % filename<br>
            # o3d.io.write_point_cloud(dst_path, pcd)<br>
            # print('save %s' % dst_path)<br>
        </p>
    </body>
</html>
