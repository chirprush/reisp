class Env:
    def __init__(self):
        self.frames = [{}]

    def get(self, name):
        for frame in self.frames[::-1]:
            if name in frame:
                return frame[name]
        return None

    def add(self, name, value):
        self.frames[-1][name] = value

    def push(self):
        self.frames.append({})

    def pop(self):
        self.frames.pop()
