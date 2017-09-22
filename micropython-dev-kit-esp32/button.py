from usched import Timeout

class Button(object):
    DEBOUNCETIME = 0.02
    def __init__(self, objSched, pin):
        self.pin = pin
        self.released_func = None
        self.released_func_args = ()
        self.pressed_func = None
        self.pressed_func_args = ()
        self.switchstate = self.pin.value()
        objSched.add_thread(self.switchcheck())

    def __call__(self):
        return self.switchstate

    def on_released(self, callback, callback_args = ()):
        self.released_func = callback
        self.released_func_args = callback_args

    def on_pressed(self, callback, callback_args = ()):
        self.pressed_func = callback
        self.pressed_func_args = callback_args

    def switchcheck(self):
        wf = Timeout(Button.DEBOUNCETIME)
        while True:
            state = self.pin.value()
            if state != self.switchstate:
                self.switchstate = state
                if state == 0 and self.released_func:
                    self.released_func(*self.released_func_args)
                elif state == 1 and self.pressed_func:
                    self.pressed_func(*self.pressed_func_args)
            yield wf()
