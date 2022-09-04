import sys
tekst=[]
dubina = 0

prog_scope = {}

def obradi(tekst):
    novi = []
    for e in tekst:
        bez_raz = e.strip()
        if not (bez_raz.startswith('<') or bez_raz.startswith('$')):
            novi.append(bez_raz) 
    return novi

def kr_za(tekst,scope,dubina, z):
    if (z==1):
        return -1
    dubina+=1
    i = 1
    delta = 0
    tr_scope = {}
    if bool(scope):
        for k, v in scope.items():
            tr_scope[k] = v
    za_ele = tekst[0].split()
    
    if (za_ele[2] in tr_scope.keys()):
        stari_key = za_ele[2]
        stari_val = tr_scope.get(za_ele[2])
        tr_scope[za_ele[2]] = za_ele[1]
    else:
        stari_key = za_ele[2]
        tr_scope[za_ele[2]] = za_ele[1]
        stari_val = za_ele[1]
   
    while i < (len(tekst)):
       
        if z==1:
            return -1
        ele = tekst[i].split()
        
        if (ele[0] == 'IDN'):
            if (tekst[i+1].startswith('OP_PRIDRUZI')):
                if not (ele[2] in tr_scope.keys()):
                    tr_scope[ele[2]] = ele[1]
                i+=1
                    
            elif (tekst[i-1].startswith('KR_ZA')):
                
                pocetak = i
                
                ret = kr_za(tekst[i:],tr_scope,dubina,z)
                if ret == -1:
                    return -1
                else:
                    i = i+ ret
                
                
            else:
                
                if ele[2] in tr_scope.keys():
                    
                    if (tr_scope.get(ele[2]) == ele[1]):
                        print ("err", ele[1], ele[2] )
                        z = 1
                        return -1
                    else:
                        print(ele[1], tr_scope.get(ele[2]), ele[2])
                else:
                    
                    print("err", ele[1], ele[2])
                    z = 1
                    return -1
                i +=1
        
        elif (ele[0] == 'KR_AZ'):
            
            tr_scope= scope
            dubina -=1
            
            return i
        else:
            i+=1
        

def petlja(tekst):
    delta = 0
    pocetak = 0
    dubina = 0
    i=0
    z =0
    while i < (len(tekst)):
        if z == 1:
            return
           
        ele = tekst[i].split()
        if (ele[0] == 'IDN'):
            if (i+1 == len(tekst)):
                if ele[2] in prog_scope.keys():
                    if (prog_scope.get(ele[2]) == ele[1]):
                        print ("err",ele[1], ele[2])
                        z = 1
                        return
                    if (i > (pocetak + delta)):
                        print(ele[1], prog_scope.get(ele[2]), ele[2])
                        
                else:
                    print("err", ele[1], ele[2])
                    z = 1
                i+=1
            else:
                if (tekst[i+1].startswith('OP_PRIDRUZI')):
                    if not (ele[2] in prog_scope.keys()):
                        prog_scope[ele[2]] = ele[1]
                    i+=1
                elif (tekst[i-1].startswith('KR_ZA')):
                
                    ret = kr_za(tekst[i:],prog_scope,dubina,z)
                    if ret == -1:
                        return
                    else:
                        i = i+ ret
                
                else:
                    if ele[2] in prog_scope.keys():
                        if (prog_scope.get(ele[2]) == ele[1]):
                            print ("err",ele[1], ele[2])
                            z = 1
                            return
                        if (i > (pocetak + delta)):
                            print(ele[1], prog_scope.get(ele[2]), ele[2])
                        
                    else:
                        print("err", ele[1], ele[2])
                        z = 1
                    i+=1
        else:
            i +=1
        
for ul in sys.stdin:
    ul=ul.strip("\n")
    if len(ul)!=0:
        redak = ul
        tekst.append(redak)
    else:
        break

txt = obradi(tekst)  

petlja(txt)
