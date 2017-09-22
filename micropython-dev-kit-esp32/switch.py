from usched import Timeout

class Switch(object):
    DEBOUNCETIME = 0.02
    def __init__(self, objSched, pin, close_func=None, close_func_args=(), open_func=None, open_func_args=()):
        self.pin = pin
        self.close_func = close_func
        self.close_func_args = close_func_args
        self.open_func = open_func
        self.open_func_args = open_func_args
        self.switchstate = self.pin.value()
        objSched.add_thread(self.switchcheck())

    def __call__(self):
        return self.switchstate

    def switchcheck(self):
        wf = Timeout(Switch.DEBOUNCETIME)
        while True:
            state = self.pin.value()
            if state != self.switchstate:
                self.switchstate = state
                if state == 0 and self.close_func:
                    self.close_func(*self.close_func_args)
                elif state == 1 and self.open_func:
                    self.open_func(*self.open_func_args)
            yield wf()
