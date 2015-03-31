# encoding: utf-8
# KiPa(KisaPalvelu), tuloslaskentajärjestelmä partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi

from decimal import *

import log

def decimal_uni(self) :
        return str(self.quantize(Decimal('0.1'),rounding=ROUND_HALF_UP ) )
def decimal_repr(self) :
        return unicode(self.quantize(Decimal('0.1'),rounding=ROUND_HALF_UP ) )

Decimal.__repr__= decimal_repr
Decimal.__unicode__= decimal_uni

class SequenceOperations :
        def __add__(self,other): return self.operate_to_all( lambda a,b: a+b , other)
        def __radd__(self,other): return self.operate_to_all(lambda a,b: a+b , other)
        def __sub__(self,other): return self.operate_to_all( lambda a,b: a-b , other)
        def __rsub__(self,other): return self.operate_to_all( lambda a,b: b-a , other)
        def __mul__(self,other): return self.operate_to_all( lambda a,b: a*b , other)
        def __rmul__(self,other): return self.operate_to_all( lambda a,b: a*b , other)
        def __div__(self,other): return self.operate_to_all( lambda a,b: a/b , other)
        def __rdiv__(self,other): return self.operate_to_all( lambda a,b: b/a , other)
        def __lt__(self, other): return self.operate_to_all( lambda a,b: a<b , other)
        def __le__(self, other): return self.operate_to_all( lambda a,b: a<=b, other)
        def __eq__(self, other): return self.operate_to_all( lambda a,b: a==b, other)
        def __ne__(self, other): return self.operate_to_all( lambda a,b: a!=b, other)
        def __gt__(self, other): return self.operate_to_all( lambda a,b: a>b , other)
        def __ge__(self, other): return self.operate_to_all( lambda a,b: a>=b, other)

class MathDict(SequenceOperations,dict):
        """
        Sanakirja jonka alkioille voi tehda massoittain 
        laskutoimituksia toisten sanakirjan vastaavien alkioiden kesken.
        """
        def operate_to_all(self,function2, other) :
                if type(other) == MathDict :
                        oper = MathDict({})
                        for k in self.keys() : 
                                try:
                                        oper[k]=function2(self[k],other[k])
                                except KeyError: pass
                                except TypeError : pass
                elif type(other) == MathList :
                        oper=MathListDict({})
                        for k in self.keys() : 
                                try:
                                    oper[k]= [(function2(self[k],l,*args) for l in other)]
                                except KeyError: pass
                                except TypeError : pass
                else: 
                        oper = MathDict({})
                        for k in self.keys() : 
                            try:
                                oper[k]=function2(self[k],other)

                            except KeyError: pass
                            except TypeError : pass
                return oper

        def listaksi(self) :
                """
                Palauttaa kaikki alkiot yhdessä listasa
                """
                lista=[]
                for k,v in self.items(): lista.append(v)
                return lista

        def __unicode__(self):
                stringi = u"{"
                for k,v in self.items(): 
                        if v:stringi+= unicode(k) + ": " + unicode(v) + ", "
                stringi=stringi[:-2]
                stringi+="}"
                return stringi

class MathList(SequenceOperations,list):
        """
        Lista jonka alkioille voi tehda massoittain 
        laskutoimituksia toisten listojen vastaavien alkioiden kesken.
        """
        def operate_to_all(self,function2, other,*args) :
                oper = None
               	if type(other) == MathList : 
                        oper = MathList([function2(self[i],other[i],*args) for i in range(len(self))])
                elif type(other) == MathDict :
                        oper = MathListDict({})
                        for k,v in other.items() :
                                oper[k]=[]
                                for l in self :
                                    try:
                                        oper[k].append( function2(l,v,*args) )

                                    except KeyError: pass
                                    except TypeError : pass
                else :
                        oper = MathList([function2( v ,other,*args) for v in self])
                return oper 
        def suorita_lista(self,funktio) :
                for l in self :
                        ajettava

        def listaksi(self) : return list(self)

        def __unicode__(self):
                stringi=u"["
                for l in self :
                        if l : stringi+= unicode(l) + ", " 
                stringi= stringi[:-2]
                stringi+="]"
                return stringi

class MathListDict(SequenceOperations,dict) :
        """
        Lista jonka alkioina on sanakirjoja, sekä sanakirja jonka alkioina on listoja. 
        Operoida voi kummalla vaan, tai vaikka toisella MathListDictionarylla.
        """
        def operate_to_all(self,function2,other,*args) :
                oper={}
                if type(other) == MathListDict :
                        for k,v in self.items() :
                                for i in range(len(v)) :
                                        oper[k]=[]
                                        try: 
                                                oper[k].append( function2( v[i],other[k][i],*args) )
                                        except KeyError: pass
                                        except IndexError: pass
                                        except TypeError : pass
                elif type(other) == MathList :
                        for k,v in self.items() :
                            try: 
                                oper[k] = MathList([function2(self[k][i],other[i],*args) for i in range(len(self[k]))])
                            except KeyError: pass
                            except TypeError : pass

                elif type(other) == MathDict :
                        for k,v in other.items() :
                                if k in self.keys(): # ainoastaan alkiot jotka löytyvät
                                        oper[k]=[]
                                        for l in self[k] : 
                                            try:
                                                oper[k].append( function2(l,v,*args) )
                                            except KeyError: pass
                                            except TypeError : pass

                else : # muu (oletetaan skalaariksi)
                        for k,v in self.items(): 
                                oper[k]=[]
                                for l in v :
                                    try:
                                        oper[k].append( function2(l,other,*args) )
                                    except KeyError: pass
                                    except TypeError : pass
                return oper
        
        def listaksi(self) : 
                """
                Palauttaa kaikki alkiot yhdessä listassa
                """
                lista=[]
                for k,v in self.items():
                        lista.extend(v)
                return lista

class DictDecimal(SequenceOperations,Decimal) :
        """
        Desimaali luokka , johon on toteutettu operoiminen MathDict sekä MathList instansseilla.
        """
        def operate_to_all(self,function2,other ) :
                oper=DictDecimal()
                if type(other) == MathDict :
                        oper = MathDict(other)
                        for k in other.keys() : 
                                try:
                                        oper[k]=function2(self,other[k])
                                except KeyError: pass
                                except TypeError : pass
                elif type(other) == MathList :
                        oper = MathList([])
                        for v in other : 
                                try:
                                    oper.append(function2(self,v))
                                except KeyError: pass
                                except TypeError : pass
                else:  
                        try:
                            oper = DictDecimal( function2(Decimal(self), other) )
                        except KeyError: pass
                        except TypeError : pass
                return oper
        __repr__=decimal_repr

        def listaksi(self) :
                return [self]
     
def karsi(lista,lfunktio):
        """
        Yhdistää listan alkiot keskenään ajamalla listafunktiota vastinalkioiden kesken
        """
        karsittu=[]
        index=0
        tavaraa=1;
        while tavaraa : 
            varvi=[]
            tavaraa=0
            for l in lista :
                if hasattr(l, 'keys') :  # on sanakirja
                        pakotus=1 # Tähän täytyisi tehdä rekursiivinen sanakirjojen operointi
                
                elif hasattr(l, '__contains__') : # on lista
                        if len(l)>index and not type(l)==str and not type(l)==unicode :
                                        tavaraa=1
                                        varvi.append( l[index] )
                else: 
                        varvi.append(l)
                #if type(varvi[-1])==unicode : 
                #        varvi.pop(-1)
            if tavaraa==0 and index>0 : break;
            index+=1 ;
            if len(varvi) : karsittu.append( lfunktio(*varvi) )
        if len(karsittu)==1:
                return karsittu[0]
        else :
                return karsittu

def listaksi(a,*opt):
        """
        Muuttaa sanakirjan tai desimaalin listaksi jos syote on joukkio, muuten palauttaa muuttujan itsessaan.
        """
        if type(a)==MathList:
                a=list(a)

        if len(opt) : 
                joukkio = [a]
                joukkio += opt
        else : joukkio = a 
        
        if type( joukkio )==DictDecimal or type(joukkio)==bool: 
		        joukkio = [joukkio]
        if type( joukkio )==Decimal: 
		        joukkio = [DictDecimal(joukkio)]
        elif type( joukkio )==unicode or type( joukkio )==str:
                return joukkio
        #elif type( joukkio )== MathDict:
        #	return joukkio
        if type(joukkio)==list:
                lista=[]
                for v in joukkio :
                        if type(v)==DictDecimal or type(v)==Decimal :
                                lista.append(DictDecimal(v))
                        else : lista.append(v)
                return lista
        try:
                lista=[]
                for k in joukkio.keys() :
                        if type(joukkio[k])==DictDecimal or type(joukkio[k])==Decimal :
                                lista.append(DictDecimal(joukkio[k]))
                return lista
        except :
                return None 

def run_dict(list,funktio,*param):
        mdict=None
        params=[]
        for p in param: 
                if type(p)==type([]): 
                    params.append(MathList(p))
                else : 
                    params.append(p)
                if type(p) == MathDict and not mdict : mdict=p
        if not mdict :
                if not list :
                        return funktio(*params)
                else :
                        return karsi(params,funktio)

        rValue=MathDict({})
        for k in mdict.keys() :
                parametrit = []
	
                for p in params :
                       	if type(p)== MathDict and k in p.keys() : parametrit.append(p[k])
                        else : parametrit.append(p)

                if list: 
                        rValue[k]=  karsi(listaksi(*parametrit),funktio)
                        #rValue[k] = funktio(listaksi(*parametrit))
                else : 
                        try: rValue[k]= funktio(*parametrit)
                        except: 
                                pass # Pass all elemets that could not be calculated.
        return rValue        

def suorita(funktio,*param):
        tulos=None
        log.muteLogging()
        try :
                tulos= run_dict(0,funktio,*param)
        except :
                tulos= Decimal(0)
        log.unmuteLogging()
        log.logFunction(funktio,param,tulos)
        return tulos

def suorita_lista(funktio,a,*param ) :
        tulos=None
        if len(param)==0 :
                if not type(a)==bool and not type(a)==Decimal and not type(a)==DictDecimal and len(a)==0 :
                        raise KeyError
                elif type(a)==unicode : 
                        tulos=None
                elif type(a) == Decimal or type(a)==bool : 
                        tulos=karsi(listaksi(a),funktio) 
                elif type(a)==list : 
                        tulos=karsi(a,funktio)
                else : 
                        tulos=karsi(listaksi(a.listaksi()), funktio) 

                parametrit= [a]
                log.logFunction(funktio,parametrit,tulos)
        else : 
                tulos= run_dict(1,funktio,a,*param)
                parametrit= [a]
                for p in param :
                        parametrit.append(p)
                log.logFunction(funktio,parametrit,tulos)
        return tulos

