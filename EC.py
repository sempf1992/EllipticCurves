#
class FiniteFieldElem:
    
    def __init__(self, field, x_):
        self.Field = field
        if not isinstance(x_, int):
            raise ValueError('Value must be an integer')
        self.val = x_
        return
    
    def __add__(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot add FiniteFieldElem with another instance')
        if (self.Field != other.Field):
            raise ValueError('Cannot add two elements of different finite fields')
        return FiniteFieldElem(self.Field, (self.Field + self.val + other.val) % self.Field)
    
    def __sub__(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot subtract FiniteFieldElem with another instance')
        if (self.Field != other.Field):
            raise ValueError('Cannot subtract two elements of different finite fields')
        return FiniteFieldElem(self.Field, (self.Field + self.val - other.val) % self.Field)
        
    def __neg__(self):
        return FiniteFieldElem(self.Field, (self.Field-self.val) % self.Field)
        
    def __mul__(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot multiply FiniteFieldElem with another instance')
        if (self.Field != other.Field):
            raise ValueError('Cannot multiply two elements of different finite fields')

        return FiniteFieldElem(self.Field, self.val * other.val % self.Field)
    
    def __pow__(self, other):
        if not isinstance(other, int):
            raise ValueError('Cannot take FiniteFieldElem to a non integer power')
        return self.exp_by_squaring(other)

    def exp_by_squaring(self, other):
        if other == 1:
            return self
        if other == 0:
            return FiniteFieldElem(self.Field, 1)
        if other % 2 == 0:
            return (self * self).exp_by_squaring(other//2)
        return self * (self * self).exp_by_squaring(other//2)

    def __eq__(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot compare FiniteFieldElem with another instance')
        if (self.Field != other.Field):
            raise ValueError('Cannot compare two elements of different finite fields')
        return self.val == other.val

    def __div__(self, other):
        return self.__truediv__(other)
    
    def __truediv__(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot divide FiniteFieldElem by another instance than FiniteFieldElem')
        if (self.Field != other.Field):
            raise ValueError('Cannot divide two elements of different finite fields')
        return self * other.inverse()
        
    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def inverse(self):
        gdc, x, y = self.egcd(self.Field, self.val)
        return FiniteFieldElem(self.Field, y % self.Field)

    def Clone(self):
        return FiniteFieldElem(self.Field, self.val)

    def __str__(self):
        return str(self.val)
class Curve:
    
    #initialiseer een curve
    #gooit een exceptie als hij singulier is
    def __init__(self, Prime, alpha, beta):
        self.Prime = Prime
        self.a = FiniteFieldElem(Prime,alpha)
        self.b = FiniteFieldElem(Prime,beta)
        
        #test if it is not singular
        if self.Determinant() == FiniteFieldElem(Prime,0):
            raise ValueError('Curves must not be singular')
        return;
    
    #Determinant van curve
    def Determinant(self):
        a3 = self.a ** 3
        b2 = self.b ** 2
        return -FiniteFieldElem(self.Prime, 16)*(FiniteFieldElem(self.Prime,4) * a3 + FiniteFieldElem(self.Prime,27) * b2)
    
    def TestPunt(self, x, y):
        return y*y == x * x * x + self.a * x + self.b

    #functie die je een nieuw punt aan laat maken
    def NieuwPunt(self,x,y):
        return Punt(self, FiniteFieldElem(self.Prime, x), FiniteFieldElem(self.Prime, y))
        
class Punt:

    def __init__(self, curve, x_, y_):
        self.Curve = curve
        #maak punten x en y aan
        self.x = x_
        self.y = y_
        if not curve.TestPunt(x_,y_):
           raise ValueError('Point is not a point on the curve')
        return
    
    def __add__(self,other): #gaat ervan uit dat je twee punten meegeeft
        if not self.Curve == other.Curve:
            raise ValueError('Points are on different curves')
        if isinstance(other, Eenheid):
            return self
        if (self.x == other.x) == False:
            p = self
            q = other

            L = (q.y - p.y)/(q.x - p.x)

            x = L**2 - p.x - q.x
            y = L * ( p.x - x) - p.y

            return Punt(self.Curve, x, -y)
            #labda = (self.y.Clone() - other.y.Clone())/(self.x.Clone() - other.x.Clone())
            #x = labda.Clone() * labda.Clone() - self.x.Clone() - other.x.Clone()
            #y = labda.Clone() * (x.Clone()-self.x.Clone()) + self.y.Clone()
            #return Punt(self.Curve, x, y)
        elif (self.x == - other.x.Clone()):
            return Eenheid(self.Curve) # point to infinity and B3Y0ND
        else:
            #curve is van de vorm y^2=x^3 +ax +b 
            p = self
            q = other
            
            x2 = self.x ** 2
            L = x2 + x2 + x2 + self.Curve.a.Clone()
            L = L / ( p.y + p.y)
            
            x = L**2 - p.x - q.x
            y = L * ( p.x - x) - p.y
            return Punt(self.Curve, x, -y)
        return self
        
    def __neg__(self): # reflecteert in de x-as
        return Punt(self.Curve, self.x, -self.y.Clone())
    
    def __sub__(self,other): # trekt b van a af
        if not self.curve == other.curve:
            raise ValueError('Points are on different curves')
        return self  +  (-1 * other)

    def __mul__(self,scalar): # telt a scalar maal bij a op
        return scalar * self

    def __rmul__(self, scalar):
        if not isinstance(scalar, int) :
            raise ValueError('Cannot multiply by non-integer')
        if isinstance(self,Eenheid): # veelvoud van eenheid is eenheid
            return self
        if scalar ==0:
            return Eenheid(self.curve) # point to infinity and B3Y0ND!
        elif scalar ==1: # keer 1 is identiteitsoperatie
            return self
        elif scalar >1:
            if scalar%2==0: # splitst de vermenigvuldiging in tweeën
                a = (scalar//2)*self
                return a+a
            else: # hier ook maar dan voor oneven
                scalar = scalar -1
                a = (scalar//2)*self
                return self + a + a
            return (scalar-1)*self + self # dit zodat hij in ieder geval iets wat goed is teruggeeft, is minder efficient
        else:
            return (-scalar)* (-self) # maal mingetal is zelfde als positievegetal keer gespiegelde punt
    
    def Clone(self):
        return Punt(self.Curve, self.x.Clone(), self.y.Clone())
    def __str__(self):
        return "( "+str(self.x)+ " , " + str(self.y)+ " ) "

class Eenheid(Punt):
    def __init__(self, curve): # het is alleen belangrijk op welke curve hij zit
        self.Curve = curve
        return

    def __add__(self,other): # gaat ervan uit dat je twee punten meegeeft
        if not self.Curve == other.Curve:
            raise ValueError('Points are on different curves')
        return other
        
    def __neg__(self): # negatie van eenheid is eenheid
        return self
    
    def __sub__(self,other): # trekt b van a af
        if not self.Curve == other.Curve:
            raise ValueError('Points are on different curves')
        return -other

    def __mul__(self,scalar): # telt a scalar maal bij a op
        return self
    def __str__(self):
        return "id"
