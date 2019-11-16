import random
import time
import threading as th

class MyBarrier:
    def __init__(self, number = 2):
        self.number = number
        self.mutex = th.RLock()
        self.go = th.Lock()
        self.go.acquire()
        self.current = 0
        
    def arrived(self):
        self.mutex.acquire()
        self.current += 1
        print("arrived {}th".format(self.current))
        if self.current == self.number:
            self.current -= 1
            self.mutex.release()
            self.go.release()
        else:
            self.mutex.release()
            self.go.acquire()
            self.mutex.acquire()
            self.current -= 1
            if self.current > 0:
                self.go.release()
            self.mutex.release()
        print("left {}".format(self.current))
        
def barriertest(barrier):
    time.sleep(1 + random.random()*3)
    barrier.arrived()
    time.sleep(1 + random.random()*5)
    print("completed")
    # use same barrier for completion
    barrier.arrived()
    
bar = MyBarrier(5)

t1 = th.Thread(target=barriertest, args=(bar,))
t2 = th.Thread(target=barriertest, args=(bar,))
t3 = th.Thread(target=barriertest, args=(bar,))
t4 = th.Thread(target=barriertest, args=(bar,))
t5 = th.Thread(target=barriertest, args=(bar,))
t6 = th.Thread(target=barriertest, args=(bar,))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
print("all terminated")