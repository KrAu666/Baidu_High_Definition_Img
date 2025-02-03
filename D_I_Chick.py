from pynput.keyboard import Controller, Listener, Key
import time
import threading

# 创建键盘控制器实例
keyboard = Controller()
# 用于控制循环是否继续的标志
running = True

def simulate_keypresses():
    global running
    # 等待一小段时间，给你切换到目标输入框的时间
    time.sleep(3)
    while running:
        # 模拟按下和释放 'd' 键
        keyboard.press('d')
        keyboard.release('d')

        # 等待 0.1 秒
        time.sleep(0.1)

        # 模拟按下和释放 'i' 键
        keyboard.press('i')
        keyboard.release('i')

        time.sleep(5)

def on_release(key):
    global running
    # 若按下 ESC 键，则停止监听并停止模拟按键循环
    if key == Key.esc:
        running = False
        return False


if __name__ == "__main__":
    # 启动模拟按键的线程
    key_thread = threading.Thread(target=simulate_keypresses)
    key_thread.start()

    # 创建键盘监听器，绑定释放事件的处理函数
    with Listener(on_release=on_release) as listener:
        listener.join()

    # 等待模拟按键线程结束
    key_thread.join()