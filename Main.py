import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import cv2
from ultralytics import YOLO  # Ensure you have YOLOv8 model loaded

# 加载模型
path = 'models/best.pt'
model = YOLO(path, task='detect')


class YOLOApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLOv8 Object Detection")
        self.setGeometry(100, 100, 800, 600)

        # 创建显示图像的标签
        self.image_label = QLabel("Please open a file", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(800, 600)

        # 创建按钮
        self.btn_load = QPushButton("Open Image or Video", self)
        self.btn_detect = QPushButton("Start Detection", self)

        self.btn_load.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")
        self.btn_detect.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px;")

        self.btn_load.clicked.connect(self.load_file)
        self.btn_detect.clicked.connect(self.detect_file)

        # 信息标签
        self.info_label = QLabel("CDS521", self)
        self.info_label.setAlignment(Qt.AlignRight)
        self.info_label.setStyleSheet("font-size: 16px; font-weight: bold; color: blue;")

        # 小组标签
        self.group_label = QLabel("Group13: Five Guys", self)
        self.group_label.setAlignment(Qt.AlignRight)
        self.group_label.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_detect)

        info_layout = QHBoxLayout()
        info_layout.addStretch(1)
        info_layout.addWidget(self.info_label)

        school_layout = QHBoxLayout()
        school_layout.addWidget(self.group_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(info_layout)
        main_layout.addLayout(school_layout)
        self.setLayout(main_layout)

        # 新增
        self.file_path = None
        self.is_video = False
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_frame)

    def load_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Select Image or Video", "", "Images and Videos (*.png *.jpg *.jpeg *.mp4 *.avi)")
        if fname:
            self.file_path = fname
            # 判断是图片还是视频
            if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.is_video = False
                self.display_image(fname)
            elif fname.lower().endswith(('.mp4', '.avi')):
                self.is_video = True
                self.display_image('')  # 先清空画面
                self.image_label.setText("Video loaded, click 'Start Detection'")

    def detect_file(self):
        if not self.file_path:
            self.image_label.setText("Please select a file first")
            return

        if self.is_video:
            self.cap = cv2.VideoCapture(self.file_path)
            self.timer.start(30)  # 每30ms处理一帧
        else:
            # 检测图片
            results = model(self.file_path)
            result_img = results[0].plot()
            self.display_array(result_img)

    def process_frame(self):
        if self.cap is None or not self.cap.isOpened():
            self.timer.stop()
            return

        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            self.timer.stop()
            return

        # 检测每一帧
        results = model.predict(source=frame, save=False, verbose=False)
        result_img = results[0].plot()

        self.display_array(result_img)

    def display_image(self, path):
        if path:
            pixmap = QPixmap(path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
        else:
            self.image_label.clear()

    def display_array(self, img_array):
        rgb_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YOLOApp()
    window.show()
    sys.exit(app.exec_())

