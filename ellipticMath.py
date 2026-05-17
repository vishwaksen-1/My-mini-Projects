def modInv(a, N):
    return pow(a, N-2, N)

class EllipticPoints():
    # on an elliptic curve $E : Y^2 = X^3 + aX + b \mod N$
    def __init__(self, x=None, y=None, a=497, b=1768, N=9739):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.N = N
        self.isO = not all([x, y])
        self.isValid = self._check()
        assert self.isValid, "Invalid point"

    def __add__(self, Q):
        if self.isO:
            return Q
        elif Q.isO:
            return self
        elif self.isInverse(Q):
            return EllipticPoints()
        else:
            if self != Q:
                lamb = (Q.y - self.y) * modInv(Q.x - self.x, self.N)
            else:
                lamb = (3*(Q.x**2) + self.a) * modInv(2*Q.y, self.N)
            lamb %= self.N

            resx = (lamb**2 - self.x - Q.x)%self.N
            resy = (lamb*(self.x - resx) - self.y)%self.N
            res = EllipticPoints(resx, resy)
            assert res.isValid, "Addition failure, check algo"
            return res

    def _check(self):
        if self.isO:
            return True
        c1 = self.x <= self.N
        c2 = self.y <= self.N
        c3 = (((self.y**2)%self.N) == ((self.x**3 + self.a*self.x + self.b)%self.N))
        return (c1 & c2 & c3)

    def inverse(self):
        return EllipticPoints(self.x, -(self.y)%self.N)

    def __eq__(self, Q):
        return (self.x == Q.x) and (self.y == Q.y)

    def isInverse(self, Q):
        return (self.x == Q.x) and (self.y == -Q.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


def main():
    x = EllipticPoints(5274, 2841)
    y = EllipticPoints(8669, 740)

    assert (x + x) == EllipticPoints(7284, 2107)
    # x2 = x+x
    # print(x2)
    assert (x + y) == EllipticPoints(1024, 4440)
    # xy = x+y
    # print(xy)

    print("All assertions passed")

if __name__ == "__main__":
    main()
