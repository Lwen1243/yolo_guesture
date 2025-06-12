import os
from collections import defaultdict
from pathlib import Path

def count_class_distribution(labels_dir):
    """
    统计YOLO标签文件中各类别的数量
    
    参数:
        labels_dir: 包含YOLO格式标签文件的目录
        
    返回:
        class_counts: 字典 {class_id: count}
    """
    class_counts = defaultdict(int)
    
    for label_file in Path(labels_dir).glob('*.txt'):
        with open(label_file, 'r') as f:
            for line in f:
                if line.strip():  # 跳过空行
                    class_id = int(line.split()[0])  # 第一个数字是类别ID
                    class_counts[class_id] += 1
    
    return dict(sorted(class_counts.items()))

def analyze_dataset_distribution(dataset_dir, class_names=None):
    """
    分析数据集中各类别在训练/验证/测试集中的分布
    
    参数:
        dataset_dir: 数据集根目录(包含train/val/test子目录)
        class_names: 可选的类别名称列表
    """
    # 定义要分析的子集
    subsets = ['train', 'val', 'test']
    
    # 初始化统计结果
    stats = {
        subset: defaultdict(int) for subset in subsets
    }
    total_counts = defaultdict(int)
    
    # 统计每个子集
    for subset in subsets:
        labels_dir = Path(dataset_dir) / subset / 'labels'
        if labels_dir.exists():
            subset_counts = count_class_distribution(labels_dir)
            for class_id, count in subset_counts.items():
                stats[subset][class_id] = count
                total_counts[class_id] += count
    
    # 打印结果
    print("\nYOLO数据集类别分布统计:")
    print("=" * 60)
    
    # 表头
    header = "| {:<5} | {:<20} |".format("类别", "类别名称") if class_names else "| {:<5} |"
    for subset in subsets:
        header += " {:<8} |".format(subset)
    header += " {:<8} |".format("总计")
    print(header)
    print("|" + "-"*(len(header)-2) + "|")
    
    # 每行数据
    for class_id in sorted(total_counts.keys()):
        class_name = class_names[class_id] if class_names and class_id < len(class_names) else str(class_id)
        row = "| {:<5} | {:<20} |".format(class_id, class_name) if class_names else "| {:<5} |".format(class_id)
        for subset in subsets:
            row += " {:<8} |".format(stats[subset].get(class_id, 0))
        row += " {:<8} |".format(total_counts[class_id])
        print(row)
    
    # 打印总计
    print("|" + "-"*(len(header)-2) + "|")
    total_row = "| {:<5} | {:<20} |".format("总计", "") if class_names else "| {:<5} |".format("总计")
    for subset in subsets:
        total_row += " {:<8} |".format(sum(stats[subset].values()))
    total_row += " {:<8} |".format(sum(total_counts.values()))
    print(total_row)
    print("=" * 60)

if __name__ == "__main__":
    # 配置参数
    DATASET_DIR = "./totol_datasets"  # 替换为你的数据集目录
    
    # 可选的类别名称列表(按class_id顺序)
    CLASS_NAMES = ['heart', 'thumb_up', 'ok', 'gun', 'rock', 'scissors', 'paper']
    
    # 执行分析
    analyze_dataset_distribution(DATASET_DIR, CLASS_NAMES)