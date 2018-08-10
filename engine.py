import threading
from enginevars import EngineVars
from effects import Effects

class Engine:
    def __init__(self):
        self.vars = EngineVars()
        self.effects = Effects(self.vars)

    def start(self):
        if self.vars.effect == "static":
            self.a = threading.Thread(target=self.effects.static_effect)
            self.a.start()
        if self.vars.effect == "rainbow":
            self.a = threading.Thread(target=self.effects.rainbow_effect)
            self.a.start()
        if self.vars.effect == "random":
            self.a = threading.Thread(target=self.effects.random_group_effect)
            self.a.start()
        if self.vars.effect == "blink":
            self.a = threading.Thread(target=self.effects.appear_from_back)
            self.a.start()
        if self.vars.effect == "rswirl":
            self.a = threading.Thread(target=self.effects.rainbow_swirl)
            self.a.start()
        
    def stop(self):
        #Stop thread
        try:
            self.vars.running_effect = False
            self.a.join()
        except:
            pass
        
        self.effects.cleaning()