import copy
from modMath import modInv, modSqrt
from random import choice

class EllipticPoints():
    # on an elliptic curve E : Y^2 = X^3 + aX + b mod N

    # ----------------------------
    # Constructor / Public interface
    # ----------------------------
    def __init__(self, x=None, y=None, a=497, b=1768, N=9739, name=""):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.N = N
        self.complete()
        self.name = "[1]" + name
        self._nameIsDirty = False
        assert self.isValid, "Invalid point"

    def clone(self):
        obj = copy.deepcopy(self)
        obj.name = self.name + "-copy"
        return obj

    def mul(self, a):
        if (type(a) == int) and a > 0:
            Q = self.clone()
            R = EllipticPoints()
            n = a
            while n > 0:
                if n % 2 == 1:
                    R = R + Q
                Q = Q + Q
                n = n // 2

            R.name = f"[{a}]{self.name.split(']')[-1]}"
            return R
        return None

    def _mul(self, a): # montgomery multiplication
        # a is a binary number
        if type(a) == int:
            a = bin(a)
            
        R0 = self.clone()
        R1 = R0.mul(2)
        bits = a[2:]
        n = len(bits)
        for i in range(n-2, 0, -1):
            if bits[i] == 0:
                R0, R1 = R0.mul(2), (R0 + R1)
            else:
                R0, R1 = (R0 + R1), R1.mul(2)

        R0.name = f"[{a}]{self.name.split(']')[-1]}"
        return R0
    
    def inverse(self):
        return EllipticPoints(self.x, -(self.y) % self.N)

    def __add__(self, Q):
        if self.isO:
            return Q
        elif Q.isO:
            return self
        elif self.isInverse(Q):
            return EllipticPoints()
        else:
            res = EllipticPoints()

            if self != Q:
                lamb = ((Q.y - self.y) % self.N) * modInv((Q.x - self.x) % self.N, self.N)
                res.name = self.name + "+" + Q.name
            elif self == Q and self.y % self.N == 0:
                return EllipticPoints()
            else:
                lamb = ((3 * (Q.x ** 2) + self.a) % self.N) * modInv((2 * Q.y) % self.N, self.N)
                res.name = self.name
                res._namex2()
                res._nameIsDirty = False

            lamb %= self.N
            res.x = (lamb ** 2 - self.x - Q.x) % self.N
            res.y = (lamb * (self.x - res.x) - self.y) % self.N
            res.isO = False

            assert res.isValid, "Addition failure, check algo"
            return res

    def __eq__(self, Q):
        return (self.x == Q.x) and (self.y == Q.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    # ----------------------------
    # Internal / structural helpers
    # ----------------------------
    def complete(self):
        if (self.x != None) and (self.y == None):
            y2 = (self.x**3 + self.a * self.x + self.b) % self.N
            y = modSqrt(y2, self.N)
            self.y = choice([y, (-y)%self.N]) # ;)
        self.isO = not any([self.x, self.y])
        self.isValid = self._check()
        
    def _check(self):
        if self.isO:
            return True
        c1 = 0 <= self.x < self.N
        c2 = 0 <= self.y < self.N
        c3 = ((self.y**2) % self.N) == ((self.x**3 + self.a * self.x + self.b) % self.N)
        return c1 and c2 and c3

    def isInverse(self, Q):
        return (self.x == Q.x) and ((self.y + Q.y) % self.N == 0)

    # ----------------------------
    # Internal name management
    # ----------------------------
    def _namex2(self):
        name = self.name.split("]")[-1]
        num = int(self.name.split("]")[0].strip("["))
        num *= 2
        self.name = f"[{num}]{name}"
        self._nameIsDirty = True

    def _nameUp1(self):
        name = self.name.split("]")[-1]
        num = int(self.name.split("]")[0].strip("["))
        num += 1
        self.name = f"[{num}]{name}"
        self._nameIsDirty = True

    # ----------------------------
    # Debug utilities
    # ----------------------------
    def _printAll(self):
        print(f"""
        {self.x} = x
        {self.y} = y
        {self.a} = a
        {self.b} = b
        {self.N} = N
        {self.isO} = isO
        {self.isValid} = isValid
        {self.name} = name
        {self._nameIsDirty} = dirtyName
        """)


# ----------------------------
# Main
# ----------------------------
def main():
    x = EllipticPoints(5274, 2841, name="x")
    y = EllipticPoints(8669, 740, name="y")
    p = EllipticPoints(5323, 5438, name="P")

    assert (x + x) == EllipticPoints(7284, 2107)
    assert (x + y) == EllipticPoints(1024, 4440)
    
    # assert p.mul(1337) == p._mul(1337)
    (p._mul(1337))._printAll()
    
    print("---")
    
    p.mul(1337)._printAll()

    print("All assertions passed")


if __name__ == "__main__":
    main()