import copy
from random import choice
from modMath import modInv, modSqrt
from ellipticMath import EllipticPoints


class montGomery(EllipticPoints):
    """
    Montgomery curve subclass of EllipticPoints.

    Curve: B*y^2 = x^3 + A*x^2 + x   (mod p)
    """

    def __init__(self, x=None, y=None,
                 A=486662,
                 B=1,
                 p=(2**255 - 19),
                 name=""):

        # core coordinates and curve params
        self.x = x
        self.y = y

        self.A = A
        self.B = B
        self.p = p

        # name handling consistent with EllipticPoints
        self.name = f"[1]{name}"
        self._nameIsDirty = False

        self.complete()

        assert self.isValid, "Invalid point"

    # ----------------------------
    # Utilities
    # ----------------------------
    def clone(self):
        obj = copy.deepcopy(self)
        obj.name = self.name + "-copy"
        return obj

    def is_infinity(self):
        return self.x is None and self.y is None

    @staticmethod
    def infinity(A=486662, B=1, p=(2**255 - 19)):
        return montGomery(None, None, A, B, p)

    # ----------------------------
    # Complete missing coordinate
    # ----------------------------
    def complete(self):

        # Recover y from x
        if self.x is not None and self.y is None:

            rhs = (
                self.x**3 +
                self.A * self.x**2 +
                self.x
            ) % self.p

            y2 = (rhs * modInv(self.B, self.p)) % self.p

            y = modSqrt(y2, self.p)

            self.y = choice([y, (-y) % self.p])

        self.isO = self.is_infinity()
        self.isValid = self._check()

    # ----------------------------
    # Curve membership check
    # ----------------------------
    def _check(self):

        if self.is_infinity():
            return True

        lhs = (self.B * self.y * self.y) % self.p

        rhs = (
            self.x**3 +
            self.A * self.x**2 +
            self.x
        ) % self.p

        return (
            0 <= self.x < self.p and
            0 <= self.y < self.p and
            lhs == rhs
        )

    # ----------------------------
    # Equality
    # ----------------------------
    def __eq__(self, Q):
        return (
            self.x == Q.x and
            self.y == Q.y
        )

    # ----------------------------
    # Negation
    # ----------------------------
    def __neg__(self):

        if self.is_infinity():
            return self.clone()

        return montGomery(
            self.x,
            (-self.y) % self.p,
            self.A,
            self.B,
            self.p,
            self.name
        )

    # ----------------------------
    # Point addition
    # ----------------------------
    def __add__(self, Q):

        # O + Q = Q
        if self.is_infinity():
            return Q.clone()

        # P + O = P
        if Q.is_infinity():
            return self.clone()

        # P + (-P) = O
        if self.x == Q.x and (self.y + Q.y) % self.p == 0:
            return montGomery.infinity(self.A, self.B, self.p)

        # P + P
        if self == Q:
            return self.double()

        # slope:
        # alpha = (y2 - y1)/(x2 - x1)
        alpha = (
            (Q.y - self.y) *
            modInv((Q.x - self.x) % self.p, self.p)
        ) % self.p

        # x3 = B*alpha^2 - A - x1 - x2
        x3 = (
            self.B * alpha * alpha
            - self.A
            - self.x
            - Q.x
        ) % self.p

        # y3 = alpha*(x1 - x3) - y1
        y3 = (
            alpha * (self.x - x3)
            - self.y
        ) % self.p

        res = montGomery(
            x3,
            y3,
            self.A,
            self.B,
            self.p,
            self.name
        )

        # name management similar to EllipticPoints
        if self != Q:
            res.name = self.name + "+" + Q.name
        res.isO = False

        return res

    # ----------------------------
    # Point doubling
    # ----------------------------
    def double(self):

        if self.is_infinity():
            return self.clone()

        # tangent vertical -> infinity
        if self.y % self.p == 0:
            return montGomery.infinity(self.A, self.B, self.p)

        # alpha =
        # (3*x1^2 + 2*A*x1 + 1)/(2*B*y1)

        numerator = (
            3 * self.x * self.x +
            2 * self.A * self.x +
            1
        ) % self.p

        denominator = (
            2 * self.B * self.y
        ) % self.p

        alpha = (
            numerator *
            modInv(denominator, self.p)
        ) % self.p

        # x3 = B*alpha^2 - A - 2*x1
        x3 = (
            self.B * alpha * alpha
            - self.A
            - 2 * self.x
        ) % self.p

        # y3 = alpha*(x1 - x3) - y1
        y3 = (
            alpha * (self.x - x3)
            - self.y
        ) % self.p

        res = montGomery(
            x3,
            y3,
            self.A,
            self.B,
            self.p,
            self.name
        )

        # update name to reflect doubling
        res.name = self.name
        try:
            res._namex2()
            res._nameIsDirty = False
        except Exception:
            # if name not in expected format, leave as-is
            pass

        return res

    # ----------------------------
    # Scalar multiplication
    # Montgomery binary method
    # ----------------------------
    def mul(self, k):

        if k == 0:
            return montGomery.infinity(self.A, self.B, self.p)

        bits = bin(k)[2:]

        # R0 = P
        # R1 = [2]P
        R0 = self.clone()
        R1 = self.double()

        # iterate from second bit onward
        for bit in bits[1:]:

            if bit == '0':

                # (R0, R1) = ([2]R0, R0 + R1)
                R0, R1 = (
                    R0.double(),
                    R0 + R1
                )

            else:

                # (R0, R1) = (R0 + R1, [2]R1)
                R0, R1 = (
                    R0 + R1,
                    R1.double()
                )

        # final name like EllipticPoints.mul
        try:
            base = self.name.split("]")[-1]
            R0.name = f"[{k}]{base}"
        except Exception:
            R0.name = self.name

        return R0

    # ----------------------------
    # Pretty print
    # ----------------------------
    def __repr__(self):

        if self.is_infinity():
            return "Point(O)"

        return f"Point(x={self.x}, y={self.y})"
