

class Op:
    def __init__(self, op, args, inp=None):
        self.id = str(id(self))
        self.op = op
        self.args = args
        self.inp = inp


class Sample:
    def __init__(self, n):
        self.n = n

    def __call__(self, op):
        return Op(op="SAMPLE", args=[self.n], inp=op)


class Next:
    def __init__(self, n):
        self.n = n

    def __call__(self):
        return Op(op="NEXT", args=[self.n])
