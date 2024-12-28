import cv2
import time

class Camera:
    def __init__(self, camera_url=None):
        """カメラの初期化"""
        self.camera_url = camera_url or 'https://192.168.179.20:4343/video'
        self.cap = None

    def start(self):
        """カメラストリームの開始"""
        try:
            print(f"接続先URL: {self.camera_url}")
            self.cap = cv2.VideoCapture(self.camera_url)
            
            # 接続確認
            if not self.cap.isOpened():
                print("カメラの初期化に失敗しました")
                print("接続状態:", self.cap.isOpened())
                raise RuntimeError("カメラの初期化に失敗しました")
                
            # テストフレームの取得
            ret, frame = self.cap.read()
            if not ret or frame is None:
                raise RuntimeError("テストフレームの取得に失敗しました")
                
            print("カメラ接続成功")
            return self.cap
            
        except Exception as e:
            print(f"カメラ接続エラー: {str(e)}")
            raise

    def read_frame(self):
        """フレームの読み取り"""
        if self.cap is None:
            raise RuntimeError("カメラが初期化されていません")
        return self.cap.read()

    def release(self):
        """カメラリソースの解放"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None