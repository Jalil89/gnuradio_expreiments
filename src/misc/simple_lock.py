from threading import Lock

class SimpleLock:
    def __init__(self):
        self.is_locked = False
        self.mutex = Lock()
    
    def lock(self):
        self.mutex.acquire()
        self.is_locked = True
        
    def unlock(self):
        self.mutex.release()
        self.is_locked = False
        
    def is_locked(self):
        return self.is_locked