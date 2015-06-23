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
        
    def __neg__(self):
        return FiniteFieldElem(self.Field, -self.val % self.Field)
        
    def __mul__(self, other):
        if not isinstance(other, FiniteFieldElem):
            raise ValueError('Cannot multiply FiniteFieldElem with another instance')
        if (self.Field != other.Field):
            raise ValueError('Cannot multiply two elements of different finite fields')
        return FiniteFieldElem(self.Field, self.val * other.val % self.Field)
    
    def __pow__(self, other):
        if not isinstance(other, int):
            raise ValueError('Cannot take FiniteFieldElem to a non integer power')
        if (other == 1):
            return self
        return self * self ** (other - 1)

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
        return self * other.inverse()
        
    def inverse(self):
        #do the extended euclidean algorithm to find an inverse for val
        R_0 = self.Field
        R_1 = self.val
        
        S_0 = 1
        S_1 = 0
        
        T_0 = 0
        T_1 = 1
        while (R_1 != 0):
            Q = R_0//R_1
            
            R_2 = R_0 % R_1
            S_2 = S_0 - S_1 * Q
            T_2 = T_0 = T_1 * Q
            
            R_0 = R_1
            R_1 = R_2
            
            S_0 = S_1
            S_1 = S_2
            
            T_0 = T_1
            T_1 = T_2
        
        return FiniteFieldElem(self.Field, T_2 % self.Field)
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
        self.Curve = curve
        #maak punten x en y aan
        self.x = x_
        self.y = y_
        if not curve.TestPunt(self.x,self.y):
           raise ValueError('Point is not a point on the curve')
        return
    
    def __add__(self,other): #gaat ervan uit dat je twee punten meegeeft
        if not self.curve == other.curve:
            raise ValueError('Points are on different curves')
        if (self.x == other.x) == False:
            labda = (self.y - other.y)/(self.x - other.x)
            x = labda*labda - self.x - other.x
            y = labda(x-self.x) + self.y
            return Punt(self.Curve, x, y)
        elif (self.x == - other.x):
            return Eenheid(self.curve) # point to infinity and B3Y0ND
        else:
            #curve is van de vorm y^2=x^3 +ax +b 
            a = self.Curve.a
            labda = (3 * self.x * self.x + a)/ (2* self.y)
            x = labda * labda - 2 * self.x
            y = labda (self.x - x) - self.y
            return Punt(self.Curve, x, y)
        return self
        
    def __neg__(self): # reflecteert in de x-as
        return Punt(self.Curve, self.x, -self.y)
    
    def __sub__(self,other): # trekt b van a af
        if not self.curve == other.curve:
            raise ValueError('Points are on different curves')
        return self  + other.inverteer()

    def __mul__(self,scalar): # telt a scalar maal bij a op
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
                a = (scalar/2)*self
                return a+a
            else: # hier ook maar dan voor oneven
                scalar = scalar -1
                a = (scalar/2)*self
                return self + a + a
            return (scalar-1)*self + self # dit zodat hij in ieder geval iets wat goed is teruggeeft, is minder efficient
        else:
            return (-scalar)* (-self) # maal mingetal is zelfde als positievegetal keer gespiegelde punt
class Eenheid(Punt):
    def __init__(self, curve): # het is alleen belangrijk op welke curve hij zit
        self.Curve = curve
        return

    def __add__(self,other): # gaat ervan uit dat je twee punten meegeeft
        if not self.curve == other.curve:
            raise ValueError('Points are on different curves')
        return other
        
    def __neg__(self): # negatie van eenheid is eenheid
        return self
    
    def __sub__(self,other): # trekt b van a af
        if not self.curve == other.curve:
            raise ValueError('Points are on different curves')
        return -other

    def __mul__(self,scalar): # telt a scalar maal bij a op
        return self
