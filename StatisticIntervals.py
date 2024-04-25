import pandas as pd
import numpy as np
from scipy import stats

class StatisticIntervalsDiffMu():
    @classmethod
    def UnknowDistincVariances(self,N1,N2,mu1,mu2,sigma1,sigma2,alpha,delta=None):
        
        #Confidence intervals
        alpha_medios=alpha/2
        v=round(((((sigma1**2)/N1)+((sigma2**2)/N2))**2)/((((sigma1**2)/N1)**2)/(N1-1)+(((sigma2**2)/N2)**2)/(N2-1)),0)
        Z_tabla=stats.t.ppf(alpha_medios,v)
        #Inferior confidence limit
        LIC=abs(mu1-mu2)-abs(Z_tabla)*(((sigma1**2)/N1)+((sigma2**2)/N2))**0.5
        #Superior  confidence limit
        LSC=abs(mu1-mu2)+abs(Z_tabla)*(((sigma1**2)/N1)+((sigma2**2)/N2))**0.5
        
        #Hipotesis Test
        if delta != None:
            t_calculate=((mu1-mu2)-delta)/((sigma1/N1+sigma2/N2)**0.5)
            P_value=stats.t.sf(abs(t_calculate),v)
        else:
            t_calculate=None
            P_value=None
        data={
            "LIC":LIC,
            "LSC":LSC,
            "Statistic":t_calculate,
            "P_value":P_value}
            
        return data
        
    @classmethod
    def UnknowEqualVariances(self,N1,N2,mu1,mu2,sigma1,sigma2,alpha,delta=None):
        
        #Confidence intervals
        alpha_medios=alpha/2
        df=N1+N2-2
        sp=(((N1-1)*sigma1**2+(N2-1)*sigma2**2)/(N1+N2-2))**0.5
        Z_tabla=stats.t.ppf(alpha_medios,df)
        #Inferior confidence limit
        LIC=abs(mu1-mu2)-abs(Z_tabla)*sp*((1/N1)+(1/N2))**0.5
        #Superior  confidence limit
        LSC=abs(mu1-mu2)+abs(Z_tabla)*sp*((1/N1)+(1/N2))**0.5
        
        #Hipotesis Test
        if delta != None:
            t_calculate=((mu1-mu2)-delta)/(sp*(1/N1+1/N2)**0.5)
            P_value=stats.t.sf(abs(t_calculate),df=N1+N2-2)
        else:
            t_calculate=None
            P_value=None
        data={
            "LIC":LIC,
            "LSC":LSC,
            "Statistic":t_calculate,
            "P_value":P_value}
            
        return data

    @classmethod
    def KnowEqualVariances(self,N1,N2,mu1,mu2,sigma1,sigma2,alpha):
        alpha_medios=alpha/2
        Z_tabla=stats.norm.ppf(alpha_medios)
        #Inferior confidence limit
        LIC=abs(mu1-mu2)-abs(Z_tabla)*(((sigma1**2)/(N1))+((sigma2**2)/(N2)))**0.5
        #Superior  confidence limit
        LIS=abs(mu1-mu2)+abs(Z_tabla)*(((sigma1**2)/(N1))+((sigma2**2)/(N2)))**0.5
        return LIC,LIS
    
    @classmethod
    def PareadInterval(self,N1,mu1,sigma1,alpha):
        
        alpha_medios=alpha/2
        df=N1-1
        Z_tabla=stats.t.ppf(alpha_medios,df)
        #Inferior confidence limit
        LIC=mu1-abs(Z_tabla)*(sigma1/(N1**0.5))
        #Superior  confidence limit
        LIS=mu1+abs(Z_tabla)*(sigma1/(N1**0.5))
        return LIC,LIS

class StatisticIntervalsMu():
    @classmethod
    def tConfidenceInterval(self,N,mu,sigma,alpha):
        df=N-1
        alpha_medios=alpha/2
        t_tabla=stats.t.ppf(alpha_medios,df)
        #Inferior confidence limit
        LIC=mu-abs(t_tabla)*(sigma/(N**0.5))
        #Superior  confidence limit
        LSC=mu+abs(t_tabla)*(sigma/(N**0.5))
        error=(abs(t_tabla)*sigma/(N**0.5))
        return LIC,LSC,error

    @classmethod
    def zConfidenceInterval(self,N,mu,sigma,alpha):
        df=N-1
        alpha_medios=alpha/2
        Z_tabla=stats.norm.ppf(alpha_medios)
        #Inferior confidence limit
        LIC=mu-abs(Z_tabla)*(sigma/(N**0.5))
        #Superior  confidence limit
        LSC=mu+abs(Z_tabla)*(sigma/(N**0.5))
        error=(abs(Z_tabla)*sigma/(N**0.5))
        return LIC,LSC,error
    
    @classmethod
    def tPredictionInterval(self,N,mu,sigma,alpha):
        df=N-1
        alpha_medios=alpha/2
        t_tabla=stats.t.ppf(alpha_medios,df)
        #Inferior prediction limit.
        LIP=mu-abs(t_tabla)*(sigma)*((1+1/N)**0.5)
        #Suoerior prediction limit.
        LSP=mu+abs(t_tabla)*(sigma)*((1+1/N)**0.5)
        return LIP,LSP

    @classmethod
    def zPredictionInterval(self,N,mu,sigma,alpha):
        df=N-1
        alpha_medios=alpha/2
        z_tabla=stats.norm.ppf(alpha_medios)
        #Inferior prediction limit.
        LIP=mu-abs(z_tabla)*(sigma)*((1+1/N)**0.5)
        #Suoerior prediction limit.
        LSP=mu+abs(z_tabla)*(sigma)*((1+1/N)**0.5)
        return LIP,LSP

    
    @classmethod
    def ToleranceInterval(self,K,mu,sigma):
        #Inferior tolerance limit.
        LIT=mu-abs(K)*(sigma)
        #Superior tolerance limit.
        LST=mu+abs(K)*(sigma)
        return LIT,LST
    
class StatisticIntervalsP():
    
    @classmethod
    def ConfidenceInterval(self,N,P,alpha):
        Q=1-P
        alpha_medios=alpha/2    
        z_tabla=stats.norm.ppf(alpha_medios)
        #Inferior confidence limit
        LIC=P-abs(z_tabla)*((P*Q/(N))**0.5)
        #Superior  confidence limit
        LSC=P+abs(z_tabla)*((P*Q/(N))**0.5)
        error=abs(z_tabla)*((P*Q/(N))**0.5)
        return LIC,LSC,error
    
    @classmethod
    def ConfidenceIntervaldiff(self,N1,N2,P1,P2,alpha):
        Q1=1-P1
        Q2=1-P2
        alpha_medios=alpha/2
        z_tabla=stats.norm.ppf(alpha_medios)
        #Inferior confidence limit
        LIC=(P1-P2)-abs(z_tabla)*(((P1*Q1/N1)+(P2*Q2/N2))**0.5)
        #Superior  confidence limit
        LSC=(P1-P2)+abs(z_tabla)*(((P1*Q1/N1)+(P2*Q2/N2))**0.5)
        
        return LIC,LSC
    
    

    
