import os
from pathlib import Path

def clean_orphaned_labels(images_dir, labels_dir, image_extensions=('.jpg', '.jpeg', '.png', '.bmp')):
    """
    删除没有对应图片的标签文件
    
    参数:
        images_dir: 图片文件夹路径
        labels_dir: 标签文件夹路径
        image_extensions: 支持的图片扩展名元组
    """
    # 获取所有图片文件名（不带扩展名）
    image_files = set()
    for ext in image_extensions:
        image_files.update(
            Path(file).stem for file in os.listdir(images_dir) 
            if file.lower().endswith(ext)
        )
    
    # 获取所有标签签文件名（不带扩展名）
    label_files = set(
        Path(file).stem for file in os.listdir(labels_dir) 
        if file.lower().endswith('.txt')
    )
    
    # 找出没有对应图片的标签文件
    orphaned_labels = label_files - image_files
    
    # 删除这些标签文件
    deleted_count = 0
    for label_stem in orphaned_labels:
        label_path = Path(labels_dir) / f"{label_stem}.txt"
        try:
            os.remove(label_path)
            print(f"已删除: {label_path}")
            deleted_count += 1
        except Exception as e:
            print(f"删除 {label_path} 失败: {e}")
    
    print(f"\n完成! 共删除 {deleted_count} 个无对应图片的标签文件")
    print(f"剩余标签文件: {len(label_files) - deleted_count}")
    print(f"图片文件数: {len(image_files)}")

if __name__ == "__main__":
    # 配置路径 - 修改为你的实际路径
    IMAGES_DIR = "./ok"
    LABELS_DIR = "./train/labels"
    
    # 执行清理
    clean_orphaned_labels(IMAGES_DIR, LABELS_DIR)