#
class FiniteFieldElem:
    
    def FiniteFieldElem(self, field, x_):
        self.Field = field
        self.val = x_
        return
    
    
class Curve:
    
    #initialiseer een curve
    #gooit een exceptie als hij singulier is
    def __init__(self, Prime, alpha, beta):
        
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
        return y*y == x * x * x + self.a * x + b
    #functie die je een nieuw punt aan laat maken
    def NieuwPunt(self):
        return Punt(self)
        
class Punt:
    def __init__(self, curve, x_, y_):
        self.curve = curve
        #maak x en y de identiteit
        self.x = x_
        self.y = y_
        if 
        return
    
    #schrijf operatoren
    #CREATE FORK
