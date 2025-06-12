import os
import shutil
from pathlib import Path

def organize_labels_to_match_images(images_root_dir, labels_source_dir):
    """
    将labels文件移动到与images同级的labels文件夹中
    
    参数:
        images_root_dir: 包含train/val/test子文件夹的images根目录
        labels_source_dir: 当前存放labels文件的源目录
    """
    images_root = Path(images_root_dir)
    labels_source = Path(labels_source_dir)
    
    # 遍历images目录结构
    for split_dir in ['train', 'valid', 'test']:
        images_split_dir = images_root / split_dir
        labels_split_dir = images_root.parent / 'labels' / split_dir
        
        # 确保目标labels目录存在
        labels_split_dir.mkdir(parents=True, exist_ok=True)
        
        # 遍历该split下的所有图片文件
        for image_path in images_split_dir.glob('*'):
            if image_path.is_file():
                # 构建对应的label文件名（假设labels与images同名，只是扩展名不同）
                label_filename = image_path.stem + '.txt'  # 修改扩展名如果你的labels不是.txt
                source_label_path = labels_source / label_filename
                
                # 如果label文件存在，则移动到目标位置
                if source_label_path.exists():
                    shutil.move(str(source_label_path), str(labels_split_dir / label_filename))
                else:
                    print(f"警告: 未找到匹配的label文件 {source_label_path}")

    print("Labels整理完成！")

# 使用示例
if __name__ == "__main__":
    # 假设你的目录结构如下：
    # datasets/
    # ├── images/
    # │   ├── train/
    # │   ├── val/
    # │   └── test/
    # └── labels_source/  # 所有labels文件当前存放在这里
    
    images_directory = "ok/train/images"  # 替换为你的images目录路径
    labels_source_directory = "train/labels"  # 替换为你的labels源目录路径
    
    organize_labels_to_match_images(images_directory, labels_source_directory)