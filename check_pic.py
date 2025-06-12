import os
from pathlib import Path

def delete_images_without_labels(images_dir, labels_dir, image_extensions=('.jpg', '.jpeg', '.png', '.bmp')):
    """
    删除没有对应标签的图片文件
    
    参数:
        images_dir: 图片文件夹路径
        labels_dir: 标签文件夹路径
        image_extensions: 支持的图片扩展名元组
    """
    # 获取所有标签文件名（不带扩展名）
    label_files = set(
        Path(file).stem for file in os.listdir(labels_dir) 
        if file.lower().endswith('.txt')
    )
    
    # 遍历图片文件
    deleted_count = 0
    total_images = 0
    
    for ext in image_extensions:
        for image_file in os.listdir(images_dir):
            if image_file.lower().endswith(ext):
                total_images += 1
                image_stem = Path(image_file).stem
                
                # 如果没有对应的标签文件
                if image_stem not in label_files:
                    image_path = Path(images_dir) / image_file
                    try:
                        os.remove(image_path)
                        print(f"已删除: {image_path}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"删除 {image_path} 失败: {e}")
    
    print(f"\n完成! 共检查 {total_images} 张图片")
    print(f"删除 {deleted_count} 张无标签的图片")
    print(f"剩余图片: {total_images - deleted_count}")
    print(f"标签文件数: {len(label_files)}")

if __name__ == "__main__":
    # 配置路径 - 修改为你的实际路径
    IMAGES_DIR = "./ok"
    LABELS_DIR = "./train/labels"
    
    # 执行清理（先打印将要删除的文件而不实际删除）
    # check_images_without_labels(IMAGES_DIR, LABELS_DIR)
    
    # 实际执行删除
    delete_images_without_labels(IMAGES_DIR, LABELS_DIR)