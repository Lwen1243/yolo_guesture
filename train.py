from ultralytics import YOLO
from ultralytics import RTDETR



if __name__ == '__main__':
    # 加载模型
    # model = YOLO(r'ultralytics/cfg/models/11/yolo11.yaml')  # 不使用预训练权重训练
    model = YOLO(r'yolo11m.pt')  # 使用预训练权重训练
    # 训练参数 ----------------------------------------------------------------------------------------------
    model.train(
        data=r'./test_datasets/data.yaml',
        epochs=300,  # (int) 训练的周期数
        imgsz=640,  # (int) 输入图像的大小
        device=[0, 1, 2, 3, 4, 5, 6, 7],
        batch=64,  # (int) 每个GPU的批次大小
        workers=60,  # (int) 数据加载的工作线程数
        amp = False
    )