#coding:utf-8
import os
from ultralytics import YOLO

# 构建相对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
data_yaml_path = os.path.join(current_dir, 'datasets/DogData/data.yaml')

# 加载预训练模型
model = YOLO("yolov8n.pt")
# Use the model
if __name__ == '__main__':
    # Use the model
    results = model.train(data=data_yaml_path, epochs=100, batch=4)  # 训练模型
    # 将模型转为onnx格式
    # success = model.export(format='onnx')