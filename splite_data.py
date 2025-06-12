import os
import random
import shutil
from pathlib import Path

def split_images(source_dir, train_ratio=0.7, test_ratio=0.2, valid_ratio=0.1, seed=None):
    if seed is not None:
        random.seed(seed)
    
    # 检查比例总和是否为1
    if not (0.999 <= (train_ratio + test_ratio + valid_ratio) <= 1.001):
        raise ValueError("比例总和必须等于1")
    
    # 创建目标文件夹
    source_path = Path(source_dir)
    train_dir = source_path / 'train'
    test_dir = source_path / 'test'
    valid_dir = source_path / 'valid'
    
    for dir_path in [train_dir, test_dir, valid_dir]:
        dir_path.mkdir(exist_ok=True)
    
    # 获取所有图片文件
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    image_files = [f for f in source_path.iterdir() 
                  if f.is_file() and f.suffix.lower() in image_extensions]
    
    # 打乱文件顺序
    random.shuffle(image_files)
    
    # 计算分割点
    total_files = len(image_files)
    train_end = int(total_files * train_ratio)
    test_end = train_end + int(total_files * test_ratio)
    
    # 分割文件
    for i, file_path in enumerate(image_files):
        if i < train_end:
            dest_dir = train_dir
        elif i < test_end:
            dest_dir = test_dir
        else:
            dest_dir = valid_dir
        
        shutil.move(str(file_path), str(dest_dir / file_path.name))
    
    print(f"分割完成: {train_end}张训练集, {test_end-train_end}张测试集, {total_files-test_end}张验证集")

# 使用示例
if __name__ == "__main__":
    ok_folder = "three_gun"  # 替换为你的文件夹路径
    split_images(ok_folder, seed=42)  # 使用seed保证可重复性