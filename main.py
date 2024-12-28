from camera import Camera
from detector import ObjectDetector
import cv2

def main():
    camera = Camera()
    detector = ObjectDetector()
    
    try:
        # カメラ初期化
        camera.start()
        
        while True:
            # フレーム取得
            ret, frame = camera.read_frame()
            if not ret:
                print("フレーム取得エラー")
                continue

            # リサイズ（必要に応じて）
            frame = cv2.resize(frame, (640, 480))
            
            # 検出実行
            result_frame, count = detector.detect(frame)
            
            # 結果表示
            cv2.imshow('Object Detector', result_frame)
            
            # qキーで終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()