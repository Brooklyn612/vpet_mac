import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QPoint
import os

class PixelPet(QWidget):
    def __init__(self):
        super().__init__()
        print("初始化 PixelPet...")
        
        # 修改窗口标志
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # 设置窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        
        # 添加图片存在性检查
        self.idle_images = ["idle1.png", "idle3.png", "idle1.png", "idle2.png"]
        self.walk_images = ["walk1.png", "walk2.png", "walk3.png", "walk2.png"]
        self.click_images = ["shock1.png", "shock2.png"]
        
        print(f"当前工作目录: {os.getcwd()}")
        
        # 验证所有图片文件是否存在
        all_images = self.idle_images + self.walk_images + self.click_images + ["bubble.png"]
        for img in all_images:
            full_path = os.path.join(os.getcwd(), img)
            if not os.path.exists(full_path):
                print(f"错误：找不到图片文件 {full_path}")
                sys.exit(1)
            else:
                print(f"找到图片文件: {full_path}")
        
        self.current_frame = 0
        self.state = "idle"
        
        self.idle_counter = 0
        self.idle_durations = [20, 5, 20, 1]  
        
        print("创建标签...")
        self.label = QLabel(self)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 确保初始图片加载成功
        initial_pixmap = QPixmap(self.idle_images[0])
        if initial_pixmap.isNull():
            print("错误：无法加载初始图片")
            sys.exit(1)
        else:
            print(f"成功加载初始图片，尺寸: {initial_pixmap.width()}x{initial_pixmap.height()}")
            
        self.label.setPixmap(initial_pixmap)
        self.resize(initial_pixmap.size())
        
        # 设置窗口尺寸策略
        self.label.adjustSize()
        self.adjustSize()
        
        # 设置初始位置在屏幕中央
        screen = QApplication.primaryScreen().geometry()
        center_pos = screen.center() - self.rect().center()
        self.move(center_pos)
        print(f"窗口位置设置为: x={center_pos.x()}, y={center_pos.y()}")
        
        # 确保窗口可见
        self.raise_()
        self.show()
        print(f"窗口是否可见: {self.isVisible()}")
        print(f"窗口大小: {self.width()}x{self.height()}")
        
        # 站立动画计时器
        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self.animate_idle)
        self.idle_timer.start(100)
        
        # 走路动画计时器 - 设置为500毫秒
        self.walk_timer = QTimer(self)
        self.walk_timer.timeout.connect(self.animate_walk)
        self.walk_timer.setInterval(200)  # 每500毫秒更新一次走路动画
        
        # 点击恢复计时器
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.restore_idle)
        
        # 气泡计时器
        self.bubble_timer = QTimer(self)
        self.bubble_timer.timeout.connect(self.show_bubble)
        self.bubble_timer.start(3600000)
        
        # 上次移动的时间戳
        self.last_move_time = 0
        
        self.dragging = False
        self.offset = QPoint()
        
        print("初始化完成")

    def update_image(self):
        print(f"更新图片 - 当前状态: {self.state}, 帧: {self.current_frame}")
        current_images = {
            "idle": self.idle_images,
            "walk": self.walk_images,
            "click": self.click_images
        }

        if self.state in current_images:
            images = current_images[self.state]
            if self.current_frame < len(images):
                # 先清除当前图像
                self.label.clear()
                
                pixmap = QPixmap(images[self.current_frame])

                if not pixmap.isNull():
                    # 确保图像有透明背景
                    scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                    self.label.setPixmap(scaled_pixmap)
                    self.resize(scaled_pixmap.size())
                    self.label.adjustSize()
                    self.adjustSize()
                    print(f"图片更新成功: {images[self.current_frame]}")
                else:
                    print(f"错误：无法加载图片 {images[self.current_frame]}")

    def animate_idle(self):
        if self.state == "idle":
            self.idle_counter += 1
            # 检查当前帧是否应该切换
            if self.idle_counter >= self.idle_durations[self.current_frame]:
                self.idle_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle_images)
                self.update_image()
    
    def animate_walk(self):
        if self.state == "walk":
            self.current_frame = (self.current_frame + 1) % len(self.walk_images)
            self.update_image()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.position().toPoint()
            
            self.state = "click"
            self.current_frame = 0
            self.update_image()
            self.click_timer.start(300)
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            # 切换到走路状态
            if self.state != "walk":
                self.state = "walk"
                self.current_frame = 0
                self.update_image()
                # 启动走路动画计时器
                if not self.walk_timer.isActive():
                    self.walk_timer.start()
            
            # 移动窗口
            self.move(event.globalPosition().toPoint() - self.offset)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            
            # 停止走路动画计时器
            if self.walk_timer.isActive():
                self.walk_timer.stop()
            
            self.state = "idle"
            self.current_frame = 0
            self.idle_counter = 0  # 重置 idle 计数器
            self.update_image()
    
    def restore_idle(self):
        self.state = "idle"
        self.current_frame = 0
        self.idle_counter = 0  # 重置 idle 计数器
        self.update_image()
    
    def show_bubble(self):
        if hasattr(self, "bubble_label") and self.bubble_label.isVisible():
            return

        bubble_pixmap = QPixmap("bubble.png")
        if not bubble_pixmap.isNull():
            self.bubble_label = QLabel(self)
            self.bubble_label.setPixmap(bubble_pixmap)
            self.bubble_label.move(self.width() + 10, 0)
            self.bubble_label.show()
            QTimer.singleShot(3000, self.bubble_label.hide)
        else:
            print("错误：无法加载气泡图片")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("创建 QApplication 实例")
    
    pet = PixelPet()
    print("正在进入事件循环...")
    sys.exit(app.exec())