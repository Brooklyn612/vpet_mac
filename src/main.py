import sys
from PyQt6.QtWidgets import QApplication
from pixel_pet import PixelPet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("创建 QApplication 实例")
    
    pet = PixelPet()
    print("正在进入事件循环...")
    sys.exit(app.exec())