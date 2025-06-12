import os
import shutil
from pathlib import Path

def extract_class_images(dataset_dir, target_class, output_dir):
    """
    提取包含特定类别的图片到单独文件夹
    
    参数:
        dataset_dir: 数据集目录(包含images和labels子目录)
        target_class: 要提取的类别ID
        output_dir: 输出目录
    """
    # 创建输出目录
    output_dir = Path(output_dir)
    (output_dir / 'images').mkdir(parents=True, exist_ok=True)
    (output_dir / 'labels').mkdir(parents=True, exist_ok=True)
    
    # 获取标签文件列表
    labels_dir = Path(dataset_dir) / 'labels'
    images_dir = Path(dataset_dir) / 'images'
    
    count = 0
    for label_file in labels_dir.glob('*.txt'):
        with open(label_file, 'r') as f:
            # 检查是否包含目标类别
            contains_class = any(
                line.strip() and int(line.split()[0]) == target_class
                for line in f
            )
            
            if contains_class:
                # 查找对应的图片文件
                img_stem = label_file.stem
                img_path = None
                for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                    potential_img = images_dir / f"{img_stem}{ext}"
                    if potential_img.exists():
                        img_path = potential_img
                        break
                
                if img_path:
                    # 复制图片和标签
                    shutil.copy2(img_path, output_dir / 'images' / img_path.name)
                    shutil.copy2(label_file, output_dir / 'labels' / label_file.name)
                    count += 1
    
    print(f"找到并提取了 {count} 张包含类别 {target_class} 的图片")

# 使用示例
extract_class_images(
    dataset_dir="./totol_datasets/train",
    target_class=0,  # 要提取的类别ID
    output_dir="./output/class_2_images"
)