import threading

# 线程类
class CustomizeFunctionThread(threading.Thread):
    def __init__(self, func, args=()):
        super(CustomizeFunctionThread, self).__init__()
        self.func = func
        self.args = args
        self.result = []

    def run(self):
        try:
            self.result = self.func(*self.args)
        except Exception as e:
            print(f"An error occurred during function execution: {e}")
            self.result = None 

    def get_result(self):
            return self.result
