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
<img src="images/workflow.svg"><br>
</p>

<h3>　STEP.0　カラーマップから色相の配列を作成する</h3>
<p>
　　python src2\colormap2npy.py <br>
　　この処理は一度実施するだけでよい(実施済)<br>
    <img src="src/spectral.png"><br>
</p>

<h3>　STEP.1　Lotus-2 の WEB デモで画像から深度画像を作成する</h3>
<p>
　　<a href="https://huggingface.co/spaces/haodongli/Lotus-2_Depth">Lotus-2のDepth推定デモページ</a><br>
　　カラーマップ(Spectral)の深度推定結果が得られる。<br>
    <img src="images/Lotus2_web_demo.png"><br>
　　・画面右上のダウンロードボタンを押して深度画像をダウンロードする。<br>
　　・MS Paintなどでダウンロードした深度画像(.webp)を .png に変換する。<br>
</p>

<h3>　STEP.2　カラーマップ(Spectral)の深度画像をグレースケールの深度画像に変換する</h3>
           
<p>
　　python src2\Spectral2Grayscale.py (Spectral Depth Image)<br>
</p>
    
<h3>　STEP.3　深度画像を補間する</h3>
<p>
　　カラーマップをグレースケールにした深度画像は諧調数が少なく深度にギャップができるので, 補間～ぼかしにより諧調を復元する。<br>
<br>
 　　python src2\interpolate_and_blur.py (グレースケール深度画像) [(ぼかすレベル)]<br>
<br>
　　※ 1ラインずつ2パス処理するので時間が掛かる･･･<br>
</p>
<img src="images/interpolation_and_blur.svg">
<br>
　　※ 鼻のあたまが掛けているのは Lotus2の推定深度が飽和しているため<br>
</p>

<h3>　STEP.4　RGB画像, 深度画像からPLYファイルを作成する</h3>

<p>
　　python src2\RgbDepth2PLY.py　(RGB画像) (深度画像)<br>
</p>

<h3>　STEP.5　PLYファイルを表示する</h3>

<p>
　　python src2\o3d_display_ply.py　(PLYファイル) [(z値スケール)]<br>
<br>
　　・<strong>マウスドラッグ</strong>：　点群の回転<br>
　　・<strong>ホイールボタン＋マウスドラッグ</strong>：　点群の移動<br>
　　・<strong>`@`キー, '['キー</strong>：　表示画角変更<br>
<img src="images/view_angle.png"><br>
　　・<strong>'-'キー,'＾'キー</strong>：　点群のサイズ変更<br>
<img src="images/point_cloud_size.png"><br>
　　・<strong>pキー</strong>：　スクリーンキャプチャー<br>
　　・<strong>1/2/3キー</strong>：　点群の回転,　<strong>＋Shiftキー</strong>：　逆回転,　<strong>＋Ctrlキー</strong>：　回転量10倍<br>
　　・<strong>4/5/6キー</strong>：　点群の平行移動,　<strong>＋Shiftキー</strong>：　逆方向に行移動　<strong>＋Ctrlキー</strong>：　移動量10倍<br>
　　・<strong>7キー</strong>：　回転ステップを下げる,　<strong>＋Shiftキー</strong>：　回転ステップを上げる<br>
　　・<strong>8キー</strong>：　平行移動ステップを下げる,　<strong>＋Shiftキー</strong>：　平行移動ステップを上げる<br>
　　・<strong>ESCキー</strong>:　終了　
</p>
</body>
</html>
