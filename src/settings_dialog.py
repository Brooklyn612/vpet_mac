from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QComboBox, 
                            QLabel, QPushButton, QCheckBox, QSlider, QGroupBox)
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent, image_manager):
        super().__init__(parent)
        self.parent = parent
        self.image_manager = image_manager
        
        self.setWindowTitle("桌宠设置")
        self.resize(300, 350)
        
        # 创建布局
        self.create_layout()
    
    def create_layout(self):
        main_layout = QVBoxLayout()
        
        # 外观设置组
        appearance_group = QGroupBox("外观设置")
        appearance_layout = QVBoxLayout()
        
        # 皮肤选择
        skin_layout = QHBoxLayout()
        skin_label = QLabel("选择皮肤:")
        self.skin_combo = QComboBox()
        for skin in self.image_manager.available_skins:
            self.skin_combo.addItem(skin.capitalize())
        
        # 设置当前选中的皮肤
        current_index = self.image_manager.available_skins.index(self.image_manager.current_skin)
        self.skin_combo.setCurrentIndex(current_index)
        
        skin_layout.addWidget(skin_label)
        skin_layout.addWidget(self.skin_combo)
        appearance_layout.addLayout(skin_layout)
        
        # 大小设置
        size_layout = QHBoxLayout()
        size_label = QLabel("大小:")
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setMinimum(50)
        self.size_slider.setMaximum(150)
        self.size_slider.setValue(int(self.parent.scale_factor * 100))
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_slider)
        appearance_layout.addLayout(size_layout)
        
        appearance_group.setLayout(appearance_layout)
        main_layout.addWidget(appearance_group)
        
        # 行为设置组
        behavior_group = QGroupBox("行为设置")
        behavior_layout = QVBoxLayout()
        
        # 自动动画设置
        self.enable_animations = QCheckBox("启用随机动画（眨眼/伸懒腰）")
        self.enable_animations.setChecked(self.parent.animation_manager.special_animation_timer.isActive())
        behavior_layout.addWidget(self.enable_animations)
        
        # 睡眠设置
        self.enable_sleep = QCheckBox("启用睡眠模式（长时间不活动）")
        self.enable_sleep.setChecked(self.parent.animation_manager.sleep_check_timer.isActive())
        behavior_layout.addWidget(self.enable_sleep)
        
        # 情绪设置
        self.enable_emotions = QCheckBox("显示情绪气泡")
        self.enable_emotions.setChecked(self.parent.show_emotions)
        behavior_layout.addWidget(self.enable_emotions)
        
        behavior_group.setLayout(behavior_layout)
        main_layout.addWidget(behavior_group)
        
        # 交互设置组
        interaction_group = QGroupBox("交互设置")
        interaction_layout = QVBoxLayout()
        
        # 拖放设置
        self.enable_food = QCheckBox("启用食物拖放功能")
        self.enable_food.setChecked(self.parent.accept_food_drops)
        interaction_layout.addWidget(self.enable_food)
        
        # 摸头设置
        self.enable_headpat = QCheckBox("启用摸头反应")
        self.enable_headpat.setChecked(self.parent.enable_headpat)
        interaction_layout.addWidget(self.enable_headpat)
        
        interaction_group.setLayout(interaction_layout)
        main_layout.addWidget(interaction_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        apply_button = QPushButton("应用")
        apply_button.clicked.connect(self.apply_settings)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(apply_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def apply_settings(self):
        # 应用皮肤设置
        selected_skin = self.image_manager.available_skins[self.skin_combo.currentIndex()]
        if selected_skin != self.image_manager.current_skin:
            self.image_manager.set_skin(selected_skin)
            self.parent.update_image()
        
        # 应用大小设置
        scale_factor = self.size_slider.value() / 100.0
        self.parent.set_scale(scale_factor)
        
        # 应用行为设置
        if self.enable_animations.isChecked():
            self.parent.animation_manager.special_animation_timer.start()
        else:
            self.parent.animation_manager.special_animation_timer.stop()
            
        if self.enable_sleep.isChecked():
            self.parent.animation_manager.sleep_check_timer.start()
        else:
            self.parent.animation_manager.sleep_check_timer.stop()
            
        self.parent.show_emotions = self.enable_emotions.isChecked()
        
        # 应用交互设置
        self.parent.accept_food_drops = self.enable_food.isChecked()
        self.parent.enable_headpat = self.enable_headpat.isChecked()
        
        self.accept()