import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QPoint

class PixelPet(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 加载动画帧
        self.idle_images = ["idle1.png", "idle2.png"]  # 站立动画
        self.walk_images = ["walk1.png", "walk2.png", "walk3.png"]  # 走路动画
        self.click_images = ["shock1.png", "shock2.png"]  # 点击动画
        self.current_frame = 0
        self.state = "idle"  # 初始状态
        
        self.label = QLabel(self)
        self.update_image()
        
        self.resize(self.label.pixmap().size())
        
        # 定时器：控制站立动画
        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self.animate_idle)
        self.idle_timer.start(1000)  # 每 1 秒变换一次
        
        # 定时器：控制点击动画恢复
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.restore_idle)
        
        # 定时器：每小时弹出对话框
        self.bubble_timer = QTimer(self)
        self.bubble_timer.timeout.connect(self.show_bubble)
        self.bubble_timer.start(3600000)  # 每小时提醒
        
        self.dragging = False  # 记录是否在拖拽
        self.offset = QPoint()
    
    def update_image(self):
        """更新宠物的图片"""
        if self.state == "idle":
            pixmap = QPixmap(self.idle_images[self.current_frame])
        elif self.state == "walk":
            pixmap = QPixmap(self.walk_images[self.current_frame])
        elif self.state == "click":
            pixmap = QPixmap(self.click_images[self.current_frame])
        else:
            pixmap = QPixmap(self.idle_images[0])
        
        self.label.setPixmap(pixmap)
        self.resize(pixmap.size())
    
    def animate_idle(self):
        """站立动画"""
        if self.state == "idle":
            self.current_frame = (self.current_frame + 1) % len(self.idle_images)
            self.update_image()
    
    def animate_walk(self):
        """走路动画"""
        if self.state == "walk":
            self.current_frame = (self.current_frame + 1) % len(self.walk_images)
            self.update_image()
    
    def mousePressEvent(self, event):
        """鼠标点击事件，触发特殊动作"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.position().toPoint()
            
            # 播放点击动画
            self.state = "click"
            self.current_frame = 0
            self.update_image()
            self.click_timer.start(300)  # 300ms 后恢复
    
    def mouseMoveEvent(self, event):
        """鼠标拖动事件，移动桌宠并播放走路动画"""
        if self.dragging:
            self.state = "walk"
            self.animate_walk()
            self.move(event.globalPosition().toPoint() - self.offset)
    
    def mouseReleaseEvent(self, event):
        """释放鼠标时停止拖拽，恢复站立状态"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.state = "idle"
            self.current_frame = 0
            self.update_image()
    
    def restore_idle(self):
        """恢复站立状态"""
        self.state = "idle"
        self.current_frame = 0
        self.update_image()
    
    def show_bubble(self):
        """弹出提醒对话框"""
        self.bubble_label = QLabel(self)
        self.bubble_label.setPixmap(QPixmap("bubble.png"))
        self.bubble_label.move(self.width() + 10, 0)  # 让气泡出现在宠物旁边
        self.bubble_label.show()
        
        # 3 秒后自动隐藏气泡
        QTimer.singleShot(3000, self.bubble_label.hide)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = PixelPet()
    pet.show()
    sys.exit(app.exec())
