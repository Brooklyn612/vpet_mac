from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QPixmap, QDrag
from PyQt6.QtCore import Qt, QMimeData, QPoint

class FoodDragHelper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("桌宠食物盒")
        self.resize(300, 200)
        
        # 创建中央部件和主布局
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # 添加说明标签
        instruction_label = QLabel("拖动下方的食物图标到桌宠上喂食")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instruction_label)
        
        # 创建食物容器区域
        food_layout = QHBoxLayout()
        food_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 添加食物图标
        self.add_food_item(food_layout, "food_fish.png", "小鱼")
        self.add_food_item(food_layout, "food_candy.png", "糖果")
        self.add_food_item(food_layout, "food_apple.png", "苹果")
        
        main_layout.addLayout(food_layout)
        
        # 添加关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button)
        
        self.setCentralWidget(central_widget)
    
    def add_food_item(self, layout, image_path, name):
        """添加一个可拖拽的食物图标"""
        try:
            container = QWidget()
            container_layout = QVBoxLayout(container)
            
            # 创建食物图标标签
            food_label = DraggableLabel(image_path)
            food_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # 创建食物名称标签
            name_label = QLabel(name)
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            container_layout.addWidget(food_label)
            container_layout.addWidget(name_label)
            
            layout.addWidget(container)
        except Exception as e:
            print(f"添加食物项时出错: {e}")

class DraggableLabel(QLabel):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        
        # 加载图片
        try:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
                self.setPixmap(scaled_pixmap)
            else:
                self.setText(f"无法加载: {image_path}")
                print(f"错误: 无法加载图片 {image_path}")
        except Exception as e:
            self.setText(f"错误: {str(e)}")
            print(f"加载图片时出错: {e}")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()
    
    def mouseMoveEvent(self, event):
        # 检查是否是拖动操作
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
            
        # 检查移动距离是否足够触发拖动
        if (event.position().toPoint() - self.drag_start_position).manhattanLength() < 10:
            return
            
        # 创建拖放操作
        drag = QDrag(self)
        mime_data = QMimeData()
        
        # 设置拖放的数据为图片路径
        mime_data.setText(self.image_path)
        drag.setMimeData(mime_data)
        
        # 设置拖放时显示的图像
        pixmap = self.pixmap()
        if not pixmap.isNull():
            drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
        
        # 执行拖放操作
        drag.exec(Qt.DropAction.CopyAction)

# 独立运行测试
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    food_helper = FoodDragHelper()
    food_helper.show()
    sys.exit(app.exec())