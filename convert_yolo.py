import json
from pathlib import Path

def convert_bbox_to_yolo(x_tl, y_tl, width, height):
    """
    将 [x_top_left, y_top_left, width, height] 转换为YOLO格式 [x_center, y_center, width, height]
    假设输入坐标已经是归一化的(0-1)
    """
    x_center = x_tl + width / 2.0
    y_center = y_tl + height / 2.0
    
    # 确保值在0-1范围内
    x_center = max(0.0, min(1.0, x_center))
    y_center = max(0.0, min(1.0, y_center))
    width = max(0.0, min(1.0, width))
    height = max(0.0, min(1.0, height))
    
    return x_center, y_center, width, height

def json_to_yolo(json_data, output_dir, class_mapping=None):
    """
    将JSON数据转换为YOLO格式
    
    参数:
        json_data: 包含标注数据的JSON字典
        output_dir: 输出目录路径
        class_mapping: 类别名称到ID的映射字典
    """
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 默认类别映射
    if class_mapping is None:
        class_mapping = {"ok": 0}  # 根据实际类别设置
    
    # 处理每个条目
    for image_id, annotations in json_data.items():
        # 准备YOLO格式内容
        yolo_lines = []
        
        # 处理每个边界框
        for bbox in annotations.get("bboxes", []):
            x_tl, y_tl, width, height = bbox
            
            # 转换为YOLO格式
            x_center, y_center, width, height = convert_bbox_to_yolo(x_tl, y_tl, width, height)
            
            # 获取类别ID
            label = annotations["labels"][0]  # 取第一个标签
            class_id = class_mapping.get(label, 0)  # 默认为0
            
            # 构建YOLO格式行
            yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
            yolo_lines.append(yolo_line)
        
        # 写入文件 (假设image_id也是文件名)
        output_path = Path(output_dir) / f"{image_id}.txt"
        with open(output_path, 'w') as f:
            f.write('\n'.join(yolo_lines))
        
        print(f"已转换 {image_id} 的标注数据")

# 示例使用
if __name__ == "__main__":
    with open("./annotations/train/three_gun.json") as f:
        json_data = json.load(f)
    # 类别映射
    class_mapping = {
        "three_gun": 3,
        }  # 根据实际情况添加更多类别
    
    # 转换为YOLO格式
    json_to_yolo(json_data, "train/labels", class_mapping)