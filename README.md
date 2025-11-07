# 项目摘要

本项目基于 Ultralytics YOLO 模型，通过基于YOLOv8模型的模型训练与基于PyQt5的图形界面，提供犬类目标检测与识别的训练脚本和可视化推理界面，支持单张图片或视频流的检测。

# 项目结构

```
├── Main.py              # PyQt5 图形界面，加载 YOLO 模型执行检测
├── train.py             # 使用 Ultralytics API 训练自定义模型
├── detect_tools.py      # 图像处理、绘图与 YOLO 坐标转换工具函数
├── Config.py            # 模型路径及品种标签配置
├── models/              # 存放预训练与自训练权重（默认包含 best.pt）
├── datasets/            # 数据集及标注
├── runs/detect/         # 训练输出目录（自动生成）
├── requirements.txt     # Python 依赖
├── installPackages.py   # 快速安装依赖脚本
├── setup.py             # Ultralytics 打包脚本
```

# 使用数据集
本项目的训练数据集采用斯坦福大学提供的来自世界各地的犬类数据集，使用 ImageNet 中的图像和注释构建，用于细粒度图像分类任务。其详细数据为:
- 犬种类：120
- 图像数：20,580
- 注释：类标签、边界框

# 运行准备

1. 创建并激活虚拟环境：

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```

2. 安装依赖：

   ```powershell
   pip install -r requirements.txt
   ```

3. （可选）若需使用 `setup.py` 打包安装额外的 `ultralytics` 组件，可执行：

   ```powershell
   pip install -e .
   ```

# 数据与模型

- 训练数据描述位于 `datasets/DogData/data.yaml`。
- 预训练权重 `yolov8n.pt` 存放于根目录，作为初始训练模型。
- 训练完成后生成的最佳权重需保存到 `models/best.pt`（`Main.py` 默认从该路径加载模型）。
- 若需替换权重，请同步更新 `Config.py` 中的标签映射及 `Main.py` 的模型加载路径。

# 运行说明

## 训练模型

```powershell
python train.py
```

- 默认使用 `yolov8n.pt` 预训练权重，训练参数可在 `train.py` 内根据需要修改；
- 训练日志与输出会保存在 `runs/detect` 目录下，迭代次数可在结果中的results.csv中看到。

## 使用模型进行犬种识别

```powershell
python Main.py
```

- 打开界面后，点击 “Open Image or Video” 选择图片或视频；
- 选择视频后，界面提示点击 “Start Detection” 开始逐帧检测；
- 若要更换识别标签或文字语言，可在 `Config.py` 与 `detect_tools.py` 中调整相关配置。

# 常见问题

- **PyQt5 窗口黑屏或无响应**：确认已安装兼容版本的 PyQt5/Qt，必要时尝试更新显卡驱动。
- **模型无法加载**：检查 `models/best.pt` 是否存在且与当前 Ultralytics 版本兼容。
