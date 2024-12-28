import cv2
import numpy as np

class ObjectDetector:
    def __init__(self):
        # ウィンドウとトラックバーの設定
        self.window_name = 'Object Detector'
        cv2.namedWindow(self.window_name)
        
        # トラックバーの初期値
        self.threshold = 128
        self.min_area = 1000
        self.blur = 5
        
        # トラックバーの作成
        cv2.createTrackbar('Threshold', self.window_name, self.threshold, 255, self.on_threshold_change)
        cv2.createTrackbar('Min Area', self.window_name, self.min_area, 10000, self.on_area_change)
        cv2.createTrackbar('Blur', self.window_name, self.blur, 20, self.on_blur_change)

    def on_threshold_change(self, value):
        self.threshold = value

    def on_area_change(self, value):
        self.min_area = value

    def on_blur_change(self, value):
        if value % 2 == 0:
            value += 1
        self.blur = value

    def detect(self, frame):
        """物体検出の実行"""
        if frame is None:
            return frame, 0

        # 元のフレームのコピーを作成
        display_frame = frame.copy()

        # グレースケール変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ブラー処理
        if self.blur > 1:
            gray = cv2.GaussianBlur(gray, (self.blur, self.blur), 0)

        # 二値化
        _, binary = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY)

        # デバッグ用の画像表示
        cv2.imshow('Binary', binary)

        # 輪郭検出
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_area:
                valid_contours.append(contour)

                # 輪郭を描画
                cv2.drawContours(display_frame, [contour], -1, (0, 255, 0), 2)

                # バウンディングボックスを描画
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # 面積を表示
                cv2.putText(display_frame, f'Area: {int(area)}', (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # 検出数を表示
        cv2.putText(display_frame, f'Count: {len(valid_contours)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return display_frame, len(valid_contours)

    def __del__(self):
        cv2.destroyAllWindows()