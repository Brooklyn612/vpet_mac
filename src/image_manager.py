import os
import sys
import random
from PyQt6.QtGui import QPixmap

class ImageManager:
    def __init__(self):
        # 当前选择的皮肤
        self.current_skin = "default"
        self.available_skins = ["default", "hat", "scarf", "glasses"]
        
        # 首次启动时随机选择一个皮肤
        self.randomize_skin()
        
        # 定义不同状态的图片集
        self.load_skin_images()
        
        # 表情气泡图片
        self.emotion_bubbles = {
            "happy": "emotion_happy.png",
            "bored": "emotion_bored.png",
            "angry": "emotion_angry.png",
            "food": "food_bubble.png"
        }
        
        # 验证所有图片文件
        self.verify_images()
    
    def randomize_skin(self):
        """随机选择一个皮肤"""
        self.current_skin = random.choice(self.available_skins)
        print(f"已选择皮肤: {self.current_skin}")
    
    def set_skin(self, skin_name):
        """设置特定皮肤"""
        if skin_name in self.available_skins:
            self.current_skin = skin_name
            self.load_skin_images()
            print(f"已切换皮肤: {self.current_skin}")
            return True
        return False
    
    def load_skin_images(self):
        """加载当前皮肤的所有图片集"""
        skin_prefix = "" if self.current_skin == "default" else f"{self.current_skin}_"
        
        # 基本状态图片
        self.idle_images = [f"{skin_prefix}idle1.png", f"{skin_prefix}idle3.png", 
                           f"{skin_prefix}idle1.png", f"{skin_prefix}idle2.png"]
        self.walk_images = [f"{skin_prefix}walk1.png", f"{skin_prefix}walk2.png", 
                           f"{skin_prefix}walk3.png", f"{skin_prefix}walk2.png"]
        self.click_images = [f"{skin_prefix}shock1.png", f"{skin_prefix}shock2.png"]
        
        # 新增的状态图片
        self.sleep_images = [f"{skin_prefix}sleep1.png", f"{skin_prefix}sleep2.png"]
        self.blink_images = [f"{skin_prefix}blink1.png", f"{skin_prefix}blink2.png"]
        self.stretch_images = [f"{skin_prefix}stretch1.png", f"{skin_prefix}stretch2.png"]
        self.angry_images = [f"{skin_prefix}angry1.png", f"{skin_prefix}angry2.png"]
        self.headpat_images = [f"{skin_prefix}headpat1.png", f"{skin_prefix}headpat2.png"]
        self.eating_images = [f"{skin_prefix}eat1.png", f"{skin_prefix}eat2.png", f"{skin_prefix}eat3.png"]
        
        # 对话气泡图片
        self.bubble_image = "bubble.png"
    
    def verify_images(self):
        """验证所有图片文件是否存在"""
        print(f"当前工作目录: {os.getcwd()}")
        print(f"当前皮肤: {self.current_skin}")
        
        # 收集所有可能的图片路径
        all_images = []
        all_images.extend(self.idle_images)
        all_images.extend(self.walk_images)
        all_images.extend(self.click_images)
        all_images.extend(self.sleep_images)
        all_images.extend(self.blink_images)
        all_images.extend(self.stretch_images)
        all_images.extend(self.angry_images)
        all_images.extend(self.headpat_images)
        all_images.extend(self.eating_images)
        all_images.append(self.bubble_image)
        
        # 添加情绪气泡图片
        all_images.extend(self.emotion_bubbles.values())
        
        # 检查哪些图片文件存在
        missing_images = []
        for img in all_images:
            full_path = os.path.join(os.getcwd(), img)
            if not os.path.exists(full_path):
                missing_images.append(img)
                print(f"警告：找不到图片文件 {full_path}")
            else:
                print(f"找到图片文件: {full_path}")
        
        # 如果有缺失的图片，尝试使用默认皮肤
        if missing_images and self.current_skin != "default":
            print(f"尝试切换到默认皮肤")
            self.current_skin = "default"
            self.load_skin_images()
            self.verify_images()
    
    def load_image(self, image_path):
        """加载并返回图像"""
        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                print(f"错误：无法加载图片 {image_path}")
                # 尝试加载相应的默认皮肤图片
                if self.current_skin != "default":
                    default_image = image_path.replace(f"{self.current_skin}_", "")
                    print(f"尝试加载默认皮肤图片: {default_image}")
                    pixmap = QPixmap(default_image)
                    if not pixmap.isNull():
                        return pixmap
                return None
            return pixmap
        except Exception as e:
            print(f"加载图片时出错: {e}")
            return None
    
    def get_image_for_state(self, state, frame):
        """根据状态和帧索引返回对应的图像路径"""
        if state == "idle" and frame < len(self.idle_images):
            return self.idle_images[frame]
        elif state == "walk" and frame < len(self.walk_images):
            return self.walk_images[frame]
        elif state == "click" and frame < len(self.click_images):
            return self.click_images[frame]
        elif state == "sleep" and frame < len(self.sleep_images):
            return self.sleep_images[frame % len(self.sleep_images)]
        elif state == "blink" and frame < len(self.blink_images):
            return self.blink_images[frame % len(self.blink_images)]
        elif state == "stretch" and frame < len(self.stretch_images):
            return self.stretch_images[frame % len(self.stretch_images)]
        elif state == "angry" and frame < len(self.angry_images):
            return self.angry_images[frame % len(self.angry_images)]
        elif state == "headpat" and frame < len(self.headpat_images):
            return self.headpat_images[frame % len(self.headpat_images)]
        elif state == "eating" and frame < len(self.eating_images):
            return self.eating_images[frame % len(self.eating_images)]
        return None
    
    def get_bubble_image(self):
        """返回气泡图像路径"""
        return self.bubble_image
    
    def get_emotion_bubble(self, emotion):
        """返回情绪气泡图像路径"""
        if emotion in self.emotion_bubbles:
            return self.emotion_bubbles[emotion]
        return None