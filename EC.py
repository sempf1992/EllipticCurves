#
class FiniteFieldElem:
    
    def FiniteFieldElem(self, field, x_):
        self.Field = field
        self.val = x_
        return
    
    def __add__(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot add FiniteFieldElem with another instance')
        if (self.Field != other.Field):
            raise ValueError('Cannot add two elements of different finite fields')
        return FiniteFieldElem(self.Field, self.val + other.val % self.Field)
    
    def __sub__(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot subtract FiniteFieldElem with another instance')
        if (self.Field != other.Field):
            raise ValueError('Cannot subtract two elements of different finite fields')
        return FiniteFieldElem(self.Field, self.val - other.val % self.Field)
        
    def __mul__(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot multiply FiniteFieldElem with another instance')
        if (self.Field != other.Field):
            raise ValueError('Cannot multiply two elements of different finite fields')
        return FiniteFieldElem(self.Field, self.val * other.val % self.Field)
    
    def is_(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot compare FiniteFieldElem with another instance')
        if (self.Field != other.Field):
            raise ValueError('Cannot compare two elements of different finite fields')
        return self.val == other.val
        
    def __div__(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot add FiniteFieldElem with another instance')
        if (self.Field != other.Field):
            raise ValueError('Cannot divide two elements of different finite fields')
        #do the extended euclidean algorithm
        
        
class Curve:
    
    #initialiseer een curve
    #gooit een exceptie als hij singulier is
    def __init__(self, Prime, alpha, beta):
        self.Prime = Prime
        self.a = FiniteFieldElem(Prime,alpha)
        self.b = FiniteFieldElem(beta)
        
        #test if it is not singular
        if self.Determinant() == 0:
            raise ValueError('Curves must not be singular')
        return;
    
    #Determinant van curve
    def Determinant(self):
        return -16*(4 * self.a ** 3 + 27 * self.b ** 2)
    
    def TestPunt(self, x, y):
        return y*y == x * x * x + self.a * x + self.b
    #functie die je een nieuw punt aan laat maken
    def NieuwPunt(self,x,y):
        return Punt(self, FiniteFieldElem(self.Prime, x), FiniteFieldElem(self.Prime, y))
        
class Punt:
    def __init__(self, curve, x_, y_):
        self.curve = curve
        #maak punten x en y aan
        self.x = x_
        self.y = y_
        if not curve.TestPunt(self.x,self.y):
           raise ValueError('Point is not a point on the curve')
        return
    
    #schrijf operatoren
    