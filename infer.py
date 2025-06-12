import cv2
from ultralytics import YOLO
from time import time

class UltralyticsYOLODetector:
    def __init__(self, model_path, conf_thresh=0.5, iou_thresh=0.45):
        """
        初始化 Ultralytics YOLO 检测器
        
        参数:
            model_path: 模型路径(.pt文件)
            conf_thresh: 置信度阈值(默认0.5)
            iou_thresh: NMS的IOU阈值(默认0.45)
        """
        # 加载模型
        self.model = YOLO(model_path)
        
        # 设置模型参数
        self.model.conf = conf_thresh  # 置信度阈值
        self.model.iou = iou_thresh    # NMS IOU阈值
        
        # 获取类别名称
        self.class_names = self.model.names
        
        print(f"Model classes: {self.class_names}")
    
    def draw_detections(self, frame, results):
        """
        在图像上绘制检测结果
        
        参数:
            frame: 原始图像帧
            results: 检测结果
        
        返回:
            frame: 绘制了检测结果的图像
        """
        # 遍历所有检测结果
        for result in results:
            for box in result.boxes:
                # 获取边界框坐标
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # 获取类别和置信度
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = self.class_names[cls_id]
                
                # 绘制边界框
                color = (0, 255, 0)  # 绿色
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # 绘制标签和置信度
                label = f"{cls_name} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame
    
    def run_camera(self, camera_id=0, window_name="YOLO Detection"):
        """
        运行摄像头实时检测
        
        参数:
            camera_id: 摄像头ID(默认0)
            window_name: 显示窗口名称
        """
        # 打开摄像头
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        
        # 用于计算FPS
        prev_time = 0
        
        try:
            while True:
                # 读取帧
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame.")
                    break
                
                # 执行检测
                results = self.model(frame, verbose=False)  # verbose=False关闭控制台输出
                
                # 绘制检测结果
                frame = self.draw_detections(frame, results)
                
                # 计算并显示FPS
                curr_time = time()
                fps = 1 / (curr_time - prev_time)
                prev_time = curr_time
                cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # 显示结果
                cv2.imshow(window_name, frame)
                
                # 按'q'退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            # 释放资源
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # 替换为你的模型路径
    MODEL_PATH = "best.pt"  # 可以是官方模型或你的自定义模型
    
    # 创建检测器实例
    detector = UltralyticsYOLODetector(MODEL_PATH)
    
    # 运行摄像头检测
    print("Starting camera detection...")
    detector.run_camera()
