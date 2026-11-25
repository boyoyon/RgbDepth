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
<h2>DepthPro 2 を試してみた</h2>
入力画像
<img src="images/input_image.png">
点群化　例１
<img src="images/depthpro2_landscape2.gif">
点群化　例２
<img src="images/depthpro2_face.gif">
<p>
(環境構築)<br>
・https://github.com/apple-aiml-research/ml-depth-pro-2<br>
　Code --> Download ZIP<br>
・ml-depth-pro-2-main.zip を解凍する<br>
・cd ml-depth-pro-2-main<br>
<br>
・conda create -y -n depth_pro_2 python=3.10<br>
・conda activate depth_pro_2<br>
・pip install av<br>
・pip install numpy<br>
・pip install timm<br>
・pip install pillow_heif<br>
・pip install opencv-python<br>
<br>
・src_depthpro2\test_depth_pro_2_img2npy.py を ml-depth-pro-2-main\src フォルダに配置<br>
<br>
・DepthPro2で画像から深度データを作成する<br>
　src_depthpro2\test_depth_pro_2_img2npy.py　(画像ファイル)<br>
　src_depthpro2\test_depth_pro_2_img2npy.py　(画像ファイルへのワイルドカード 例：*.png)<br>
　src_depthpro2\test_depth_pro_2_img2npy.py　(画像ファイル1)　(画像ファイル2)　･･･<br>
<br>
・最初の実行時に3.25GBのパラメータがダウンロードされる。<br>
・CPUでも数分で推定完了<br>
・メートル単位で深度が推定される。屋外画像などでは inf も含まれる<br>
<br>
・画像と深度データから点群を作成する<br>
　src_depthpro2\ImgNpy2Pcd.py　(画像ファイル)　(深度データ(.npy))　[(zスケール)]<br>
　sキー押下で点群データが displayed.ply に保存される<br>
<br>
・使い勝手が悪いが、以下のツールで余計な点を削除した<br>
　<a href="https://github.com/boyoyon/PLY_EDIT">src/pcd_edit.py</a><br>　
　src\axisXYZ.ply、src\plane_x0.ply、src\plane_y0.ply、src\plane_z0.ply も必要<br>
　(console)<br>
　　L　(点群 plyファイル) ･･･ 点群 ply をロード～スケーリングする<br>
　　※ 点群が大きすぎたり小さすぎたりすると編集できないので、大文字 L でロードした場合は<br>
    　　スケーリングすることにした。<br>
　　l　(点群 plyファイル) ･･･ 点群 ply をロード (スケーリングなし)<br>    
　(visualizer)<br>
　　削除したい点と残したい点を面で分離できるように、点群を回転、平行移動する<br>
    <br>
　　1キー：x軸周りに点群を回転　+shiftで反対周り、+ctlで高速回転<br>
　　2キー：y軸周りに点群を回転　+shiftで反対周り、+ctlで高速回転<br>
　　3キー：z軸周りに点群を回転　+shiftで反対周り、+ctlで高速回転<br>
　　4キー：x軸方向に平行移動　+shiftで反対方向、+ctlで高速移動<br>
　　5キー：y軸方向に平行移動　+shiftで反対方向、+ctlで高速移動<br>
　　6キー：z軸方向に平行移動　+shiftで反対方向、+ctlで高速移動<br>
　　7キー：回転ステップを小さくする　+shiftで大きくする<br>
　　8キー：平行移動ステップを小さくする　+shiftで大きくする<br>
　　↑↓キー：スケールアップ／ダウン<br>
　　aキー：座標軸　表示/非表示<br>
　　xキー：x平面　表示/非表示<br>
　　yキー：y平面　表示/非表示<br>
　　zキー：z平面　表示/非表示<br>
<br>
  (console)<br>
　　remove　x：　x>0 の点を削除する<br>
　　remove　-x：　x<0 の点を削除する<br>
　　※ y、-y、z、-z も同様<br>
<br>
　　save　(plyファイル名)：編集した点群をセーブする
</p>
<img src="images/pcd_edit.svg">
<p>
・点群plyを表示する<br>
　src2/o3d_display　(plyファイル)　[(z値スケール)]<br>
    <br>
　　bキー：背景の白/黒トグル<br>
　　1~3キー：カメラ(視点)の回転　+shift：逆方向回転　ctl:回転量増加<br>
　　4~6キー：カメラ(視点)の平行移動　+shift:逆方向移動　ctl：移動量増加<br>
　　7キー：回転ステップを下げる　+shift:上げる<br>
　　8キー：平行移動ステップを下げる　+shift:下げる<br>
　　↑↓：ズームイン/アウト<br>
　　sキー：点群を displayed.ply に保存<br>
　　-----<br>
　　マウスドラッグ：カメラ(視点)の回転<br>
　　ホィール回転：ズームイン/アウト<br>
　　ホィールを押してドラッグ：カメラ(視点)の移動<br>
　　-, ^:　点を小さくする/大きくする<br>
　　@, [： 視角を狭める、広げる<br>
　　p：スクリーンキャプチャー<br>
　　ESCキー：終了
</p>
<h2>YOLO26n-depthを試してみた</h2>
<p>
(準備)<br>
・モデルの重みをダウンロードする<br>
　<a href="https://platform.ultralytics.com/ultralytics/yolo26/yolo26n-depth">https://platform.ultralytics.com/ultralytics/yolo26/yolo26n-depth</a><br>
　clone model をクリックし、yolo26n-depth.pt(12.7MB)をダウンロードし、src2フォルダに格納する<br>
・pip install opencv-python open3d ultralytics
</p>
<p>
(試し方)<br>
・画像から depth 画像を作成する<br>
　python src2/estimate_by_yolo26n-depth.py (画像ファイル)<br>
  カレントフォルダに 画像ファイル_depth.png という名前でdepth画像が作成される。<br>
・RGB画像、depth画像からplyファイルを作成する<br>
　python　src2/RgbDepth2ply.py　(RGB画像ファイル)　(depth画像ファイル)<br>
<br>
顔は歪んだ平面になる･･･
</p>
<img src="images/yolo26n.gif">
        
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
<h3>ply表示</h3>
<p>
python　src2\o3d_display.py (plyファイル)　[(zScale)]<br>
・Line Set PLY / Point Cloud PLY / Triangle Mesh PLY を表示可能<br>
・1/2/3/4/5/6キー押下：オブジェクトの回転、平行移動<br>
　　　　　　　　　　　　+shiftで反対方向に回転、平行移動<br>
    　　　　　　　　　　+ctrlで回転量、平行移動量up<br>
・7/8キー押下：回転量、平行移動量を小さくする/大きくする<br>
・↑/↓：オブジェクトの拡大/縮小<br>
・sキー：plyにセーブ
(Visualizerの元々の機能はhキー押下でコンソールに表示される)<br>
(例)
・Lキー押下：ライティングのon/offをトグル<br>
</p>
<h3>pcd→mesh</h3>
<p>
python src2/PointCloud2Mesh.py (pcd PLY)<br>
・裏返しに変換される場合は、-reverseをつける<br>
　python　src2/PointClound2Mesh.py (pcd PLY) -reverse
</p>

</body>
</html>
