import sys
tekst = []
ispis = ""
prog_scope = {}
mem_lok=0
dubina = 0
petlja_d =0

mn_dj ="""
MD_SGN MOVE 0, R6
 XOR R0, 0, R0
 JP_P MD_TST1
 XOR R0, -1, R0
 ADD R0, 1, R0
 MOVE 1, R6
MD_TST1 XOR R1, 0, R1
 JP_P MD_SGNR
 XOR R1, -1, R1
 ADD R1, 1, R1
 XOR R6, 1, R6
MD_SGNR RET
MD_INIT POP R4 
 POP R3 
 POP R1 
 POP R0 
 CALL MD_SGN
 MOVE 0, R2 
 PUSH R4 
 RET
MD_RET XOR R6, 0, R6 
 JP_Z MD_RET1
 XOR R2, -1, R2 
 ADD R2, 1, R2
MD_RET1 POP R4 
 PUSH R2 
 PUSH R3 
 PUSH R4 
 RET
MUL CALL MD_INIT
 XOR R1, 0, R1
 JP_Z MUL_RET 
 SUB R1, 1, R1
MUL_1 ADD R2, R0, R2
 SUB R1, 1, R1
 JP_NN MUL_1 
MUL_RET CALL MD_RET
 RET
DIV CALL MD_INIT
 XOR R1, 0, R1
 JP_Z DIV_RET 
DIV_1 ADD R2, 1, R2
 SUB R0, R1, R0
 JP_NN DIV_1
 SUB R2, 1, R2
DIV_RET CALL MD_RET
 RET

"""


class Cvor:
    def __init__(self, dubina, scope, redak):
        self.dubina=dubina
        self.scope = scope
        self.redak=redak


def racunaj_izraz(lista_operatora,lista_operanada, scope, ispis, redosljed, petlja_d):
    z=0
    #print(lista_operatora)
    operacija = lista_operatora.pop()
    #print(lista_operanada)    
    while (lista_operanada):
        operand = lista_operanada.pop()
        #dohvati idn ili brojeve iz scope-a
        if (operand[0]=='IDN'):
            for i in range(petlja_d, 0, -1):
                lok_var = operand[2]+str(i)
                if (lok_var in scope.keys()):  
                    val2 = scope[lok_var]
                    ispis+=" LOAD R0, ("+ val2 + ")\n"
                    z=1
                    break
            if z==0:
                val2 = scope[operand[2]]
                ispis+=" LOAD R0, ("+ val2 + ")\n"
        else:
            val2 = operand[2]
            ispis+=" MOVE %D "+ val2 + ", R0\n"
        ispis+=" PUSH R0\n"
             
    #greneriraj frisc naredbe za računanje
    if (operacija[0] == 'OP_PLUS'):
        ispis+=" POP R0\n"
        ispis+=" POP R1\n"
        ispis+=" ADD R0, R1, R2\n"
        ispis+=" PUSH R2\n"

    if (operacija[0] == 'OP_MINUS'):
        ispis+=" POP R0\n"
        ispis+=" POP R1\n"
        if redosljed==1:
            
            ispis+=" SUB R0, R1, R2\n"
        else:
            ispis+=" SUB R1, R0, R2\n"
        ispis+=" PUSH R2\n"

    if (operacija[0] == 'OP_PUTA'):
       
        ispis+=" CALL MUL\n"
        ispis+=" PUSH R2\n"

    if (operacija[0] == 'OP_DIJELI'):
        ispis+=" CALL DIV\n"
        ispis+=" PUSH R2\n"

    

    return ispis


def obradi_Tlistu(i, ispis, petlja_d):
    lista_operatora = []
    lista_operanada = []
    opT = tekst[i-1].split()
    lista_operanada.insert(0, opT)
    lista_operatora.insert(0, tekst[i+1].split())
    z=0
    for j in range(i, len(tekst)):
        naziv_lista = tekst[j].split()
        
        if (naziv_lista[0]==('IDN') or naziv_lista[0]==('BROJ')):
            prz = tekst[j+4].split()
            
            if(prz[0] != ('$')):
                
                z=j
            lista_operanada.insert(0, naziv_lista)
            i = j+1
            break
    
    ispis = racunaj_izraz(lista_operatora,lista_operanada, cvor.scope,ispis,0, petlja_d)
    if (z!=0):
        i, ispis = obradi_Elistu(z+3,ispis,z, petlja_d)
    return i, ispis


def obradi_Elistu(i, ispis, z, petlja_d):
    lista_operatora = []
    lista_operanada = []
    opE = tekst[i-3].split()
    if z==0:
        lista_operanada.insert(0, opE)
    lista_operatora.insert(0, tekst[i+1].split())
    
    for j in range( i, len(tekst)):
        
        naziv_lista = tekst[j].split()
        if (naziv_lista[0]==('IDN') or naziv_lista[0]==('BROJ')):
            przT = tekst[j+2].split()
            przE = tekst[j+4].split()
            if (przT[0]==('$')):
                
                lista_operanada.insert(0, naziv_lista)
                
                ispis = racunaj_izraz(lista_operatora,lista_operanada, cvor.scope,ispis,0, petlja_d)
                i = j+1
                
                if (przE[0]=='OP_MINUS' or przE[0]=='OP_PLUS'):
                    i, ispis = obradi_Elistu(j+3, ispis, 1, petlja_d)
                break
            else:
                
                i, txt = obradi_Tlistu(j+1, ispis, petlja_d)
                rasp=1
                ispis =txt
                ispis = racunaj_izraz(lista_operatora,lista_operanada, cvor.scope,ispis,rasp, petlja_d)
                break
    
    return i, ispis

def obradi_nrprid(cvor,ispis, mem_lok, petlja_d):
    z = 0
    i = cvor.redak+3
    
    while i < len(tekst):
        
        #print(tekst[i])
        dubina = 0
        for e in tekst[i]:
            if e == " ":
                dubina+=1
            else:
                break

        petlj_chk = tekst[i].split()
        if dubina<=cvor.dubina or petlj_chk[0]=='KR_DO' or petlj_chk[0]=='<lista_naredbi>':
            break
        
        else:
            naziv_lista = tekst[i].split()
            if (naziv_lista[0]==('IDN') or naziv_lista[0]==('BROJ')):
                operator_T = tekst[i+ 2].split()
                operator_E = tekst[i+ 4].split()

                minus_chk = tekst[i-2].split()
                if (minus_chk[0] == 'OP_MINUS'):
                    
                    if (naziv_lista[0]==('IDN')):
                        val2 = scope[naziv_lista[2]]
                        ispis+=" LOAD R0, ("+ val2 + ")\n"
                        ispis+=" PUSH R0\n"
                        ispis+=" SUB 0, R0, R2\n"
                        ispis+=" STORE R0, ("+ val2 +")\n"
                                                 
                    if (naziv_lista[0]==('BROJ')):
                        naziv_lista[2]= str(int(naziv_lista[2])*-1)
                        


                
                #provjeri <T_listu>
                if operator_T[0] == ('OP_PUTA') or operator_T[0] == ('OP_DIJELI'):
                    z=1
                    
                    i, txt = obradi_Tlistu(i+1,ispis, petlja_d)
                    ispis =txt
                    
                #provjeri <E_listu>
                if (operator_E[0] == ('OP_PLUS') or operator_E[0] == ('OP_MINUS')):
                    
                    i, txt = obradi_Elistu(i+3,ispis, z, petlja_d)
                    z=1
                    ispis =txt
                    

                if (z==0):
                    #dohvati idn ili brojeve iz scope-a
                    
                    if (naziv_lista[0]=='IDN'):
                        
                        val2 = cvor.scope[naziv_lista[2]]
                        ispis+=" LOAD R0, ("+ val2 + ")\n"
                    
                    else:
                        
                        val2 = naziv_lista[2]
                        ispis+=" MOVE %D "+ val2 + ", R0\n"
                    ispis+=" PUSH R0\n"
        i+=1
    #spremi rez u scope
       
    rez = tekst[cvor.redak+1].split()


    
    if (rez[0]!=('IDN')):
        return cvor, ispis, mem_lok
    
    if not(rez[2] in cvor.scope.keys()):
        cvor.scope[rez[2]]= str("V"+str(mem_lok))
        mem_lok +=1
    
      
    cvor= Cvor(dubina, cvor.scope, i)
    ispis+=" POP R0\n"
    ispis+=" STORE R0,"+ " ("+ cvor.scope[rez[2]]+ ")\n"
    return cvor, ispis,mem_lok

        
def obradi_zapetlju(cvor,ispis, mem_lok, petlja_d, br_poz):
    petlja_d +=1
    tr_scope = cvor.scope
    
    mem_lok+=1
    
    tekst[cvor.redak+2] = tekst[cvor.redak+2]+str(petlja_d)

    add_var = tekst[cvor.redak+2].split()[2]
    
    i= cvor.redak + 1
    while (i< len(tekst)):
        dubina = 0
        for e in tekst[i]:
            if e == " ":
                dubina+=1
            else:
                break
        
        if dubina<=cvor.dubina:
            break
        
        else:
            naziv_lista=tekst[i].split()
            
            if (naziv_lista[0]=='KR_ZA'):
                poc_cvor = Cvor(dubina-1, tr_scope, i)
            if (naziv_lista[0]=='KR_DO'):
                kr_cvor = Cvor(dubina-1, tr_scope, i-2)
        i+=1

    
    #print(poc_cvor.scope)
    #print(kr_cvor.scope)
    cvor, ispis,mem_lok = obradi_nrprid(poc_cvor, ispis, mem_lok, petlja_d)
    ispis+='L'+str(br_poz)+'\n'
    ispis, mem_lok = ucitavaj_redak(poc_cvor, ispis,mem_lok, petlja_d)

    ispis+=" LOAD R0, ("+ cvor.scope[add_var] + ")\n"
    ispis+=" ADD R0, 1, R0\n"
    ispis+=" STORE R0, ("+ cvor.scope[add_var] + ")\n"
    cvor, ispis, mem_lok = obradi_nrprid(kr_cvor, ispis, mem_lok, petlja_d)

    ispis+=" LOAD R0, ("+ cvor.scope[add_var] + ")\n"
    ispis+=" POP R1\n"
    ispis+=" CMP R0, R1\n"
    ispis+=" JP_SLE L"+str(br_poz)+"\n"
    pet_cv=Cvor(dubina, tr_scope, i)
    petlja_d-=1
    return pet_cv, ispis,mem_lok
    
def ucitavaj_redak(cvor,ispis, mem_lok, petlja_d):
    br_poz=0
    i = cvor.redak
    while i < len(tekst):
        dubina = 0
        
        for e in tekst[i]:
            if e == " ":
                dubina+=1
            else:
                break
        
        naziv_lista = tekst[i].split()
        
        if naziv_lista[0]== 'KR_AZ':
            break
        if naziv_lista[0] == "<naredba_pridruzivanja>":
            
            cvor = Cvor(dubina, cvor.scope,i)
            cvor, ispis, mem_lok = obradi_nrprid(cvor, ispis, mem_lok, petlja_d)
            i = cvor.redak
           
        elif naziv_lista[0] == "<za_petlja>":
            br_poz+=1
            cvor = Cvor(dubina,cvor.scope, i)
            cvor, ispis,mem_lok = obradi_zapetlju(cvor, ispis, mem_lok, petlja_d, br_poz)
            i = cvor.redak
            
        else:
            i+=1
    return ispis, mem_lok

for ul in sys.stdin:
    ul=ul.strip("\n")
    if len(ul)!=0:
        redak = ul
        tekst.append(redak)
    else:
        break

cvor = Cvor(dubina, prog_scope, 0)
ispis, mem_lok = ucitavaj_redak(cvor,ispis, mem_lok,petlja_d)


            
with open('a.frisc', 'w') as f:
    f.write(" MOVE 40000, R7\n")
    f.write(ispis)
    f.write(" LOAD R6, ("+ prog_scope['rez'] + ")\n")
    f.write(" HALT\n")
    for i in range(mem_lok):
        f.write("V"+ str(i) +" DW 0\n")
    
    f.write(mn_dj)
    
        
