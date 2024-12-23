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
            python  RgbDepth.py  (RGB画像ファイル)  (depth画像ファイル)  [(zスケール)]<br>
            ※ ピクセルとz値の比率が不明のため、zスケール引数で調整します。<br>
            <table border="1">
                <tr><th>操作</th><th>機能</th></tr>
                <tr><td>左ボタン押下＋ドラッグ</td><td>3Dモデルの回転</td></tr>
                <tr><td>ホイールボタン押下＋ドラッグ</td><td>3Dモデルの移動</td></tr>
                <tr><td>ホイール回転</td><td>3Dモデルの拡大・縮小</td></tr>
                <tr><td>PrintScreenキー押下</td><td>スクリーンショット保存</td></tr>
                <tr><td>ウィンドウ閉じるボタン押下　</td><td>プログラム終了</td></tr>
            </table>
        </p>
        <h2>RGB画像からdepth画像の作成例</h2>
        <h3>depth推定ソフトウェアで画像からdepth画像を作成する。</h3>
        <p>
            Depth Anything V2 などを使って画像からdepth画像を作成する。<br>
            <a href="https://huggingface.co/spaces/depth-anything/Depth-Anything-V2">https://huggingface.co/spaces/depth-anything/Depth-Anything-V2</a><br>
            <br>
            <img src="images/step1_1.svg">
        </p>
    </body>
</html>
