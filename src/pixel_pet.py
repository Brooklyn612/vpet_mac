from PyQt6.QtWidgets import QLabel, QWidget, QMenu, QApplication
from PyQt6.QtGui import QPixmap, QAction, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize, QMimeData
import os
from image_manager import ImageManager
from animation_manager import AnimationManager

class PixelPet(QWidget):
    def __init__(self):
        super().__init__()
        print("初始化 PixelPet...")
        
        # 设置窗口属性
        self.setup_window()
        
        # 创建图像管理器
        self.image_manager = ImageManager()
        
        # 创建标签用于显示图像
        self.setup_label()
        
        # 创建动画管理器
        self.animation_manager = AnimationManager(self, self.image_manager)
        
        # 设置初始位置
        self.set_initial_position()
        
        # 拖动相关变量
        self.dragging = False
        self.offset = QPoint()
        
        # 接受拖放操作
        self.setAcceptDrops(True)
        
        # 创建右键菜单
        self.setup_context_menu()
        
        # 气泡和情绪气泡标签
        self.bubble_label = None
        self.emotion_bubble_label = None
        
        # 食物拖放功能
        self.food_items = ["food_fish.png", "food_candy.png", "food_apple.png"]
        
        self.scale_factor = 1.0
        self.show_emotions = True
        self.accept_food_drops = True
        self.enable_headpat = True

        print("初始化完成")
    
    def setup_window(self):
        """设置窗口属性"""
        # 修改窗口标志
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # 设置窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
    
    def setup_label(self):
        """设置显示标签"""
        print("创建标签...")
        self.label = QLabel(self)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 加载初始图片
        initial_pixmap = self.image_manager.load_image(self.image_manager.idle_images[0])
        if initial_pixmap is None:
            print("错误：无法加载初始图片")
            import sys
            sys.exit(1)
        else:
            print(f"成功加载初始图片，尺寸: {initial_pixmap.width()}x{initial_pixmap.height()}")
            
        self.label.setPixmap(initial_pixmap)
        self.resize(initial_pixmap.size())
        
        # 设置窗口尺寸策略
        self.label.adjustSize()
        self.adjustSize()
    
    def setup_context_menu(self):
        """设置右键菜单"""
        self.context_menu = QMenu(self)
        
        # 切换皮肤选项
        self.skin_menu = QMenu("更换外观", self)
        for skin in self.image_manager.available_skins:
            action = QAction(skin.capitalize(), self)
            action.triggered.connect(lambda checked, s=skin: self.change_skin(s))
            self.skin_menu.addAction(action)
        
        self.context_menu.addMenu(self.skin_menu)
        
        # 互动选项
        self.context_menu.addSeparator()
        feed_action = QAction("喂食", self)
        feed_action.triggered.connect(self.feed_pet)
        self.context_menu.addAction(feed_action)
        
        pet_action = QAction("摸头", self)
        pet_action.triggered.connect(lambda: self.animation_manager.set_headpat_state())
        self.context_menu.addAction(pet_action)
        
        talk_action = QAction("说话", self)
        talk_action.triggered.connect(self.show_bubble)
        self.context_menu.addAction(talk_action)
        
        # 退出选项
        self.context_menu.addSeparator()
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        self.context_menu.addAction(exit_action)
    
    def set_initial_position(self):
        """设置窗口初始位置"""
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
    
    def update_image(self):
        """更新当前显示的图像"""
        state = self.animation_manager.state
        frame = self.animation_manager.current_frame
        
        # print(f"更新图片 - 当前状态: {state}, 帧: {frame}")
        
        image_path = self.image_manager.get_image_for_state(state, frame)
        if image_path:
            # 先清除当前图像
            self.label.clear()
            
            pixmap = self.image_manager.load_image(image_path)
            if pixmap:
                # 确保图像有透明背景
                scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
                self.label.setPixmap(scaled_pixmap)
                self.resize(scaled_pixmap.size())
                self.label.adjustSize()
                self.adjustSize()
                # print(f"图片更新成功: {image_path}")
    
    def mousePressEvent(self, event):
        """鼠标按下事件处理"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.position().toPoint()
            
            # 设置点击状态
            self.animation_manager.set_click_state()
        elif event.button() == Qt.MouseButton.RightButton:
            # 显示右键菜单
            self.context_menu.exec(event.globalPosition().toPoint())
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件处理"""
        if self.dragging:
            # 切换到走路状态
            self.animation_manager.set_walk_state()
            
            # 移动窗口
            self.move(event.globalPosition().toPoint() - self.offset)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件处理"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            
            # 停止走路动画
            self.animation_manager.stop_walk_animation()
            
            # 恢复闲置状态
            self.animation_manager.restore_idle()
    
    def show_bubble(self):
        """显示对话气泡"""
        if hasattr(self, "bubble_label") and self.bubble_label and self.bubble_label.isVisible():
            self.bubble_label.hide()
            return

        bubble_pixmap = self.image_manager.load_image(self.image_manager.bubble_image)
        if bubble_pixmap:
            if not self.bubble_label:
                self.bubble_label = QLabel(self)
            self.bubble_label.setPixmap(bubble_pixmap)
            self.bubble_label.move(self.width(), -30)  # 调整位置
            self.bubble_label.show()
            QTimer.singleShot(3000, self.bubble_label.hide)
        else:
            print("错误：无法加载气泡图片")
    
    def show_emotion_bubble(self, emotion):
        """显示情绪气泡"""
        emotion_image = self.image_manager.get_emotion_bubble(emotion)
        if not emotion_image:
            return
            
        emotion_pixmap = self.image_manager.load_image(emotion_image)
        if emotion_pixmap:
            if not self.emotion_bubble_label:
                self.emotion_bubble_label = QLabel(self)
            self.emotion_bubble_label.setPixmap(emotion_pixmap)
            self.emotion_bubble_label.move(self.width() - 10, -50)  # 调整位置
            self.emotion_bubble_label.show()
            QTimer.singleShot(2000, self.emotion_bubble_label.hide)
    
    def change_skin(self, skin_name):
        """更换皮肤"""
        if self.image_manager.set_skin(skin_name):
            # 更新当前显示的图像
            self.update_image()
    
    def feed_pet(self):
        """喂食"""
        self.animation_manager.set_eating_state()
        self.show_emotion_bubble("food")
    
    # 拖放功能支持
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖放进入事件"""
        mime_data = event.mimeData()
        
        # 接受文件拖放
        if mime_data.hasUrls():
            for url in mime_data.urls():
                file_name = url.fileName().lower()
                # 检查是否为图片文件并且文件名符合食物项
                if any(food in file_name for food in self.food_items) or file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    event.acceptProposedAction()
                    return
        
        # 接受文本拖放（可能是表示食物的文本）
        if mime_data.hasText():
            text = mime_data.text().lower()
            if any(food_name.lower() in text for food_name in ['fish', 'candy', 'apple', '鱼', '糖果', '苹果']):
                event.acceptProposedAction()
                return
    
    def dropEvent(self, event: QDropEvent):
        """拖放事件处理"""
        # 执行吃东西的动画
        self.animation_manager.set_eating_state()
        event.acceptProposedAction()