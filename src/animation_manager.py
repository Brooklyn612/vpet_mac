from PyQt6.QtCore import QTimer, QTime, Qt
import random

class AnimationManager:
    def __init__(self, parent, image_manager):
        self.parent = parent
        self.image_manager = image_manager
        
        # 动画状态
        self.state = "idle"
        self.current_frame = 0
        
        # 闲置状态计数
        self.idle_counter = 0
        self.idle_durations = [20, 5, 20, 1]
        
        # 随机特殊动画计时
        self.last_special_animation = QTime.currentTime()
        self.idle_time_counter = 0
        self.drag_count = 0
        self.last_drag_time = QTime.currentTime()
        
        # 状态记录
        self.mood = "normal"  # normal, happy, bored, angry
        self.last_interaction_time = QTime.currentTime()
        
        # 初始化计时器
        self.setup_timers()
    
    def setup_timers(self):
        """设置动画计时器"""
        # 站立动画计时器
        self.idle_timer = QTimer(self.parent)
        self.idle_timer.timeout.connect(self.animate_idle)
        self.idle_timer.start(100)
        
        # 走路动画计时器
        self.walk_timer = QTimer(self.parent)
        self.walk_timer.timeout.connect(self.animate_walk)
        self.walk_timer.setInterval(200)
        
        # 点击恢复计时器
        self.click_timer = QTimer(self.parent)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.restore_idle)
        
        # 气泡计时器
        self.bubble_timer = QTimer(self.parent)
        self.bubble_timer.timeout.connect(self.check_mood_change)
        self.bubble_timer.start(10000)  # 每10秒检查一次心情变化
        
        # 随机特殊动画计时器
        self.special_animation_timer = QTimer(self.parent)
        self.special_animation_timer.timeout.connect(self.trigger_special_animation)
        self.special_animation_timer.start(5000)  # 每5秒检查一次是否触发特殊动画
        
        # 睡眠检查计时器
        self.sleep_check_timer = QTimer(self.parent)
        self.sleep_check_timer.timeout.connect(self.check_sleep_state)
        self.sleep_check_timer.start(30000)  # 每30秒检查一次是否该睡觉
    
    def animate_idle(self):
        """闲置动画帧更新"""
        if self.state == "idle":
            self.idle_counter += 1
            self.idle_time_counter += 1
            
            # 检查当前帧是否应该切换
            if self.idle_counter >= self.idle_durations[self.current_frame]:
                self.idle_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.image_manager.idle_images)
                self.parent.update_image()
    
    def animate_walk(self):
        """走路动画帧更新"""
        if self.state == "walk":
            self.current_frame = (self.current_frame + 1) % len(self.image_manager.walk_images)
            self.parent.update_image()
    
    def set_click_state(self):
        """设置为点击状态"""
        self.state = "click"
        self.current_frame = 0
        self.parent.update_image()
        self.click_timer.start(300)
        
        # 更新最后交互时间
        self.last_interaction_time = QTime.currentTime()
        
        # 检查点击位置是否在头部，若是则触发"摸头"动画
        cursor_pos = self.parent.mapFromGlobal(self.parent.cursor().pos())
        pet_height = self.parent.height()
        if cursor_pos.y() < pet_height * 0.4:  # 假设头部在上方40%的区域
            self.set_headpat_state()
    
    def set_headpat_state(self):
        """设置为摸头状态"""
        self.state = "headpat"
        self.current_frame = 0
        self.parent.update_image()
        self.click_timer.start(800)  # 摸头动画持续时间稍长
        
        # 触发心情变好
        self.mood = "happy"
        self.parent.show_emotion_bubble("happy")
    
    def set_walk_state(self):
        """设置为走路状态"""
        if self.state != "walk":
            self.state = "walk"
            self.current_frame = 0
            self.parent.update_image()
            # 启动走路动画计时器
            if not self.walk_timer.isActive():
                self.walk_timer.start()
            
            # 记录拖动次数和时间，用于检测暴力拖动
            current_time = QTime.currentTime()
            if self.last_drag_time.secsTo(current_time) < 2:  # 2秒内的拖动视为连续
                self.drag_count += 1
                if self.drag_count > 5:  # 5次以上连续快速拖动
                    self.set_angry_state()
                    self.drag_count = 0
            else:
                self.drag_count = 1
            
            self.last_drag_time = current_time
            self.last_interaction_time = current_time
    
    def set_angry_state(self):
        """设置为生气状态"""
        self.state = "angry"
        self.current_frame = 0
        self.parent.update_image()
        self.mood = "angry"
        self.parent.show_emotion_bubble("angry")
        # 生气状态持续时间
        QTimer.singleShot(3000, self.restore_idle)
    
    def set_sleep_state(self):
        """设置为睡觉状态"""
        if self.state != "sleep":
            self.state = "sleep"
            self.current_frame = 0
            self.parent.update_image()
            self.idle_time_counter = 0
            self.mood = "sleeping"
    
    def set_blink_state(self):
        """设置为眨眼状态"""
        self.state = "blink"
        self.current_frame = 0
        self.parent.update_image()
        # 眨眼持续时间短
        QTimer.singleShot(500, self.restore_idle)
    
    def set_stretch_state(self):
        """设置为伸懒腰状态"""
        self.state = "stretch"
        self.current_frame = 0
        self.parent.update_image()
        # 伸懒腰持续时间
        QTimer.singleShot(1200, self.restore_idle)
    
    def set_eating_state(self):
        """设置为吃东西状态"""
        self.state = "eating"
        self.current_frame = 0
        self.parent.update_image()
        # 吃东西的动画持续时间
        QTimer.singleShot(1500, self.restore_idle)
        
        # 吃东西会让心情变好
        self.mood = "happy"
        self.parent.show_emotion_bubble("happy")
    
    def stop_walk_animation(self):
        """停止走路动画"""
        if self.walk_timer.isActive():
            self.walk_timer.stop()
    
    def restore_idle(self):
        """恢复到闲置状态"""
        previous_state = self.state
        self.state = "idle"
        self.current_frame = 0
        self.idle_counter = 0
        
        # 如果从睡眠状态恢复，执行"醒来"的伸懒腰动画
        if previous_state == "sleep":
            self.set_stretch_state()
            return
            
        self.parent.update_image()
    
    def trigger_special_animation(self):
        """触发随机特殊动画 (眨眼/伸懒腰)"""
        # 只在闲置状态下触发特殊动画
        if self.state != "idle":
            return
        
        # 检查距离上次特殊动画的时间
        current_time = QTime.currentTime()
        if self.last_special_animation.secsTo(current_time) < 10:
            return  # 10秒内不重复触发
        
        # 随机决定是否触发特殊动画 (10-30秒范围内的随机概率)
        random_interval = random.randint(10, 30)
        if random.random() < 1.0 / random_interval:
            # 随机选择眨眼或伸懒腰
            animation_type = random.choice(["blink", "stretch"])
            if animation_type == "blink":
                self.set_blink_state()
            else:
                self.set_stretch_state()
            
            self.last_special_animation = current_time
    
    def check_sleep_state(self):
        """检查是否应该进入睡眠状态"""
        current_time = QTime.currentTime()
        
        # 如果超过10分钟没有互动，进入睡眠状态
        if self.last_interaction_time.secsTo(current_time) > 600 and self.state != "sleep":
            self.set_sleep_state()
    
    def check_mood_change(self):
        """检查并更新心情状态"""
        current_time = QTime.currentTime()
        
        # 如果长时间（3分钟以上）没有互动，变得无聊
        if self.mood != "bored" and self.mood != "sleeping" and self.last_interaction_time.secsTo(current_time) > 180:
            self.mood = "bored"
            self.parent.show_emotion_bubble("bored")
        
        # 如果心情是愉快，随着时间推移恢复正常
        if self.mood == "happy" and self.last_interaction_time.secsTo(current_time) > 60:
            self.mood = "normal"