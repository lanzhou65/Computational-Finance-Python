
from scipy.stats import norm  
from math import sqrt, pi, log, e, erf

class EquityOption: 
    
    RiskfreeRate = 0.01
    Vol = 0.2
   
    #constructor 
    def __init__ (self, *args):
        self.CallFlag = int(args[0])
        self.Spot = float(args[1])
        self.Strike = float(args[2])
        self.Maturity = float(args[3])
        self.DividendYield =  float(args[4])
        # write a if statement that if we supply more than 5 variables, execute the following statements, 
        #if supplied less than or equal to 4, do not execute the following statements
        RiskfreeRate = float(args[5])
        Vol = float(args[6])

    def __repr__(self):
        call_put = 'Call' if self.CallFlag else 'Put'
        repr_output = "_repr_ is called. " + "It's a " + call_put + " option with Spot = " + str(self.Spot) + ", Strike = " + str(self.Strike) + '\n' \
        + "Maturity = " + str(self.Maturity) + ", DividendYield = " + str(self.DividendYield) + '\n' \
        + "RiskfreeRate = " + str(self.RiskfreeRate) + ", Volitility = " + str(self.Vol) + '\n'  
        return repr_output 

    def __str__(self):
        call_put = 'Call' if self.CallFlag else 'Put'
        str_output = "_str_ is called. " + "It's a " + call_put + " option with Spot = " + str(self.Spot) + ", Strike = " + str(self.Strike) + '\n' \
        + "Maturity = " + str(self.Maturity) + ", DividendYield = " + str(self.DividendYield) + '\n' \
        + "RiskfreeRate = " + str(self.RiskfreeRate) + ", Volitility = " + str(self.Vol) + '\n'  
        return str_output 

    #overload imul for stock split
    def __imul__(self, stock_split):
        self.Spot = self.Spot * stock_split 
        self.Strike = self.Strike * stock_split
        return self

    # to change class attribute
    @classmethod 
    def setRiskFree(cls, rate):
        EquityOption.RiskfreeRate = rate
    def setVol(cls, vol):
        EquityOption.Vol = vol
        
  # to change the instance attribute  
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    
    @staticmethod 
    def N(x): 
        return (0.5*(1+ erf(x / sqrt(2.0))))
 
    def d1(self):
        return float((log(self.Spot/self.Strike) + (self.RiskfreeRate - self.DividendYield + (self.Vol**2) / 2  ) * self.Maturity) / (self.Vol * sqrt(self.Maturity)));
    
    
    def d2(self): 
        return float(self.d1() - self.Vol*sqrt(self.Maturity))

    def BS_Option(self, v=Vol):
        self.Vol = v #essential step
        dfq = e**(-self.DividendYield * self.Maturity)
        dfr = e**(-self.RiskfreeRate * self.Maturity)
        if self.CallFlag: 
            return self.Spot * dfq* self.N(self.d1()) - self.Strike*dfr * self.N(self.d2())
        else: 
            return self.Strike*dfr * self.N(-self.d2()) - self.Spot * dfq* self.N(-self.d1())

    def delta(self):
        dfq = e**(-self.DividendYield * self.Maturity)
        if self.CallFlag:
            return dfq * norm.cdf(self.d1())
        else:
            return -dfq * norm.cdf(-self.d1())

    def gamma(self):
        return e**(-self.DividendYield * self.Maturity) * norm.pdf(self.d1()) / (self.Spot * self.Vol * sqrt(self.Maturity))

    #for 1% change in vol
    def vega(self, v=Vol):
        self.Vol = v
        return 0.01*self.Spot * e**(-self.DividendYield * self.Maturity) * sqrt(self.Maturity) * norm.pdf(self.d1())

    #theta for 1 day change
    def theta(self):
        dfr = e**(-self.RiskfreeRate * self.Maturity)
        dfq = e**(-self.DividendYield * self.Maturity)
        if self.CallFlag:
            return (1/365) *((-0.5*self.Spot * self.Vol * dfq * norm.pdf(self.d1())) / ( sqrt(self.Maturity)) + self.DividendYield * self.Spot * dfq * norm.cdf(self.d1()) - self.RiskfreeRate*self.Strike *dfr *norm.cdf(self.d2()))
        else: 
            return (1/365) * ((-0.5*self.Spot * self.Vol * dfq * norm.pdf(self.d1())) / (sqrt(self.Maturity)) - self.DividendYield * self.Spot * dfq * norm.cdf(-self.d1()) + self.RiskfreeRate*self.Strike *dfr *norm.cdf(-self.d2()))
        
        
    def implied_Vol_Newton(self, c):
        self.c = c
        MAX_ITERATIONS = 100
        PRECISION = 1.0e-4
        sigma = 0.01
        for i in range(0, MAX_ITERATIONS):

            diff = self.BS_Option(sigma) - c  # our root
            #print (i, sigma, diff)
            if (abs(diff) < PRECISION):
                return sigma
            sigma = sigma - diff/(self.vega(sigma)*100) # f(x) / f'(x)
        return sigma


    def implied_Vol_Bisec(self, c):
        
        tot_app = 0.00000001
        tot_int = 0.000001
        x_l = 0.000001
        x_r = 1
        #print( 'x_l ', x_l, 'x_r', x_r)
        
        while (max(abs(self.BS_Option(x_l) - c), abs(self.BS_Option(x_r) -c )) > tot_app or (x_r - x_l) > tot_int) :
            x_m = (x_r + x_l)/2
            
            if ((self.BS_Option(x_l) - c) * (self.BS_Option(x_m) -c)  < 0) :
                x_r = x_m
            else:
                x_l = x_m
            #print('x_m is ', x_m, 'x_l ', x_l, 'x_r', x_r)
        return x_m

    
#C1=EquityOption(1, 100, 100, 20/365, 0, 0.05, 0.3);
#print(C1)
#print('d1 ', C1.d1())
#print('option price is', C1.BS_Option())
#print('delta is ', C1.delta())
#print('gamma is', C1.gamma())
#print('vega is', C1.vega())
#print('theta is', C1.theta())
#print ("the newton IV is", C1.implied_Vol_Newton(1))
#print("bisec IV is", C1.implied_Vol_Bisec(1), "\n")
#
##change instance attribute
#C1.Strike = 1000
#print('updated strike is ', C1.Strike)
#
##change class attributes
#C1.setRiskFree(0.08)
#print("updated RiskFree is ", C1.RiskfreeRate)
#print(C1)


C2=EquityOption(0, 50,55, 0.05, 0, 0.03)
print(C2)

C2.setVol(0.3)
print("updated vol is ", C2.Vol)

C2.Spot = 80
print('updated spot is', C2.Spot)

#test imul
C2*=0.5
print('after 2 to 1 split, C2 is now ', C2)


