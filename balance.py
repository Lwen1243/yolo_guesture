import os
import random
import shutil
from collections import defaultdict
from pathlib import Path

def balance_yolo_dataset(original_dir, output_dir, ratios=(0.7, 0.2, 0.1), seed=42):
    """
    平衡YOLO数据集，使每个类别的分布均匀
    
    参数:
        original_dir: 原始数据集目录(包含train/val/test子目录)
        output_dir: 平衡后的输出目录
        ratios: 训练/验证/测试集比例(总和应为1.0)
        seed: 随机种子
    """
    # 设置随机种子
    random.seed(seed)
    
    # 验证比例
    print(sum(ratios))
    assert sum(ratios) - 1.0 <= 0.01, "比例总和必须为1.0"
    train_ratio, val_ratio, test_ratio = ratios
    
    # 创建输出目录结构
    output_dir = Path(output_dir)
    subsets = ['train', 'val', 'test']
    for subset in subsets:
        (output_dir / subset / 'images').mkdir(parents=True, exist_ok=True)
        (output_dir / subset / 'labels').mkdir(parents=True, exist_ok=True)
    
    # 第一步：收集所有标签文件并分类
    class_files = defaultdict(list)
    
    # 遍历原始数据集中的所有标签文件
    for subset in subsets:
        labels_path = Path(original_dir) / subset / 'labels'
        if not labels_path.exists():
            continue
            
        for label_file in labels_path.glob('*.txt'):
            with open(label_file, 'r') as f:
                # 获取文件中出现的所有类别
                classes_in_file = set()
                for line in f:
                    if line.strip():
                        class_id = int(line.split()[0])
                        classes_in_file.add(class_id)
                
                # 记录文件及其包含的类别
                img_stem = label_file.stem
                img_path = None
                for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                    potential_img = Path(original_dir) / subset / 'images' / f"{img_stem}{ext}"
                    if potential_img.exists():
                        img_path = potential_img
                        break
                
                if img_path:
                    for class_id in classes_in_file:
                        class_files[class_id].append((img_path, label_file))
    
    # 第二步：对每个类别进行分层抽样
    balanced_files = {subset: set() for subset in subsets}
    
    for class_id, files in class_files.items():
        # 打乱文件顺序
        random.shuffle(files)
        
        # 计算分割点
        total = len(files)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)
        
        # 分配文件到不同子集
        balanced_files['train'].update(files[:train_end])
        balanced_files['val'].update(files[train_end:val_end])
        balanced_files['test'].update(files[val_end:])
    
    # 第三步：复制文件到新目录(避免重复)
    for subset in subsets:
        print(f"处理 {subset} 集...")
        for img_path, label_path in balanced_files[subset]:
            # 复制图片
            img_dest = output_dir / subset / 'images' / img_path.name
            if not img_dest.exists():
                shutil.copy2(img_path, img_dest)
            
            # 复制标签
            label_dest = output_dir / subset / 'labels' / label_path.name
            if not label_dest.exists():
                shutil.copy2(label_path, label_dest)
    
    # 第四步：验证结果
    print("\n平衡后的数据集统计:")
    analyze_dataset_distribution(output_dir)

def analyze_dataset_distribution(dataset_dir):
    """分析数据集中各类别的分布"""
    subsets = ['train', 'val', 'test']
    class_counts = {subset: defaultdict(int) for subset in subsets}
    
    for subset in subsets:
        labels_dir = Path(dataset_dir) / subset / 'labels'
        if labels_dir.exists():
            for label_file in labels_dir.glob('*.txt'):
                with open(label_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            class_id = int(line.split()[0])
                            class_counts[subset][class_id] += 1
    
    # 打印统计信息
    all_classes = set()
    for subset in subsets:
        all_classes.update(class_counts[subset].keys())
    
    print("\n| 类别 | 训练集 | 验证集 | 测试集 | 总计 |")
    print("|------|--------|--------|--------|------|")
    for class_id in sorted(all_classes):
        train = class_counts['train'].get(class_id, 0)
        val = class_counts['val'].get(class_id, 0)
        test = class_counts['test'].get(class_id, 0)
        total = train + val + test
        print(f"| {class_id:4} | {train:6} | {val:6} | {test:6} | {total:4} |")
    
    # 打印总计
    train_total = sum(class_counts['train'].values())
    val_total = sum(class_counts['val'].values())
    test_total = sum(class_counts['test'].values())
    print(f"| 总计 | {train_total:6} | {val_total:6} | {test_total:6} | {train_total+val_total+test_total:4} |")

if __name__ == "__main__":
    # 配置参数
    ORIGINAL_DIR = "./totol_datasets"  # 原始数据集目录
    BALANCED_DIR = "./test_datasets"  # 平衡后的输出目录
    
    # 设置分割比例
    TRAIN_RATIO = 0.7
    VAL_RATIO = 0.2
    TEST_RATIO = 0.1
    
    # 执行数据集平衡
    balance_yolo_dataset(
        original_dir=ORIGINAL_DIR,
        output_dir=BALANCED_DIR,
        ratios=(TRAIN_RATIO, VAL_RATIO, TEST_RATIO),
        seed=42
    )