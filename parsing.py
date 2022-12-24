import math
import pandas as pd
def Create_External_Symbol_Table(HTERECORDPATH,PROGORDER,STARTING_ADDRESS):
    STAB_LIST = [{} for i in range(len(PROGORDER))]
    with open(HTERECORDPATH) as f:
        PROG_NAME = ""
        LOCAL_SYMTAB = {}
        for line in f:
            if(line[0]=="H"):
                prog_name_end = line.find("0");
                PROG_NAME = line[1:prog_name_end].upper().replace("X","")
                PROG_START = line[prog_name_end:prog_name_end+6]
                PROG_SIZE = line[prog_name_end+6:prog_name_end+12]
                LOCAL_SYMTAB[PROG_NAME]=PROG_START
                LOCAL_SYMTAB["LENGTH"]=PROG_SIZE
            if(line[0]=="D"):
                final_index = 1
                while(final_index<len(line)-1):
                    prev_index = final_index
                    final_index+=line[final_index:].find("0")
                    if(final_index==-1):
                        break
                    label = line[prev_index:final_index]
                    value = line[final_index:final_index+6]
                    LOCAL_SYMTAB[label]=value
                    final_index+=6



            if(line[0]=="E"):
                prog_index = PROGORDER.index(PROG_NAME)
                STAB_LIST[prog_index] = LOCAL_SYMTAB
                LOCAL_SYMTAB = {}
    ESTAB = {}
    for STAB in STAB_LIST:
        for SYMBOL in STAB.keys():
            if(SYMBOL!="LENGTH"):
                STAB[SYMBOL] = hex(int(STAB[SYMBOL],16)+STARTING_ADDRESS)[2:]
                ESTAB[SYMBOL] = STAB[SYMBOL].upper()
        if(len(STAB.keys())!=0):
            STARTING_ADDRESS = STARTING_ADDRESS+int(STAB["LENGTH"],16)
        ESTAB["END"]=STARTING_ADDRESS
    return ESTAB

def Link_And_Load(HTERECORDPATH,ESTAB,MEMORY_TABLE):
    with open(HTERECORDPATH) as f:
        PROG_STARTING_ADDRESS=0
        for line in f:
            if(line[0]=="H"): 
                prog_name_end = line.find("0")
                PROG_NAME = line[1:prog_name_end].upper().replace("X","")
                PROG_STARTING_ADDRESS = int(ESTAB[PROG_NAME],16)
                
            if(line[0]=="T"):
                T_RELATIVE_STARTING_ADDRESS = int(line[1:7],16)
                T_ABSOLUTE_STARTING_ADDRESS = T_RELATIVE_STARTING_ADDRESS+PROG_STARTING_ADDRESS
                T_RECORD = line[9:].replace("\n","")
                CURRENT_ADDRESS = T_ABSOLUTE_STARTING_ADDRESS
                for i in range(0,len(T_RECORD),2):
                    byte = T_RECORD[i:i+2]
                    offset = CURRENT_ADDRESS%16
                    column = hex(offset)[2:].upper()
                    row = hex(CURRENT_ADDRESS-offset)[2:].upper()
                    MEMORY_TABLE.at[row,column]=byte
                    CURRENT_ADDRESS+=1
            if(line[0]=="M"):
                M_RELATIVE_ADDRESS = int(line[1:7],16)
                M_RECORD_SIZE = int(line[7:9],16)
                M_ABSOLUTE_STARTING_ADDRESS = M_RELATIVE_ADDRESS+PROG_STARTING_ADDRESS
                M_RECORD_END = M_ABSOLUTE_STARTING_ADDRESS + math.ceil(M_RECORD_SIZE/2)
                M_RECORD_SIGN = line[9:10]
                M_RECORD_VALUE = int(ESTAB[line[10:-1].upper()],16)
                BEFORE_VALUE=""
                CURRENT_ADDRESS=M_ABSOLUTE_STARTING_ADDRESS
                for i in range(M_RECORD_END-M_ABSOLUTE_STARTING_ADDRESS):
                    offset = (CURRENT_ADDRESS+i)%16
                    column = hex(offset)[2:].upper()
                    row = hex(CURRENT_ADDRESS+i-offset)[2:].upper()
                    byte = MEMORY_TABLE.at[row,column]
                    BEFORE_VALUE+=byte
                BEFORE_VALUE_CHANGED_PART = BEFORE_VALUE[len(BEFORE_VALUE)-M_RECORD_SIZE:]
                BEFORE_VALUE_UNCHANGED_PART = BEFORE_VALUE[0:len(BEFORE_VALUE)-M_RECORD_SIZE]
                BEFORE_VALUE_CHANGED_PART = int(BEFORE_VALUE_CHANGED_PART,16)
                if(M_RECORD_SIGN=="+"):
                    BEFORE_VALUE_CHANGED_PART+= M_RECORD_VALUE
                elif(M_RECORD_SIGN=="-"):
                    BEFORE_VALUE_CHANGED_PART-=M_RECORD_VALUE
                if(BEFORE_VALUE_CHANGED_PART>0):
                    BEFORE_VALUE_CHANGED_PART = hex(BEFORE_VALUE_CHANGED_PART)[2:].rjust(M_RECORD_SIZE,"0")
                else:
                    BEFORE_VALUE_CHANGED_PART = hex(BEFORE_VALUE_CHANGED_PART & (2**(M_RECORD_SIZE*4)-1))[2:]
                if(len(BEFORE_VALUE_UNCHANGED_PART)>0):
                    AFTER_VALUE = BEFORE_VALUE_CHANGED_PART.rjust(6,BEFORE_VALUE_UNCHANGED_PART)
                else:
                    AFTER_VALUE = BEFORE_VALUE_CHANGED_PART
                CURRENT_ADDRESS=M_ABSOLUTE_STARTING_ADDRESS
                j = 0
                for i in range(M_RECORD_END-M_ABSOLUTE_STARTING_ADDRESS):
                    byte = AFTER_VALUE[j:j+2]
                    offset = (CURRENT_ADDRESS+i)%16
                    column = hex(offset)[2:].upper()
                    row = hex(CURRENT_ADDRESS+i-offset)[2:].upper()
                    MEMORY_TABLE.at[row,column]=byte.upper()
                    j+=2
            
            

                

                
        return MEMORY_TABLE
def ABSOLUTE_LOAD(HTERECORDPATH):   
    with open(HTERECORDPATH) as f:
        memory_table= pd.DataFrame()
        for line in f:
            # print(line)
            if line[0]=='T':
                T_RELATIVE_STARTING_ADDRESS = int(line[1:7],16)
                T_RECORD = line[9:].replace("\n","")
                CURRENT_ADDRESS = T_RELATIVE_STARTING_ADDRESS
                for i in range(0,len(T_RECORD),2):
                    byte = T_RECORD[i:i+2]
                    offset = CURRENT_ADDRESS%16
                    column = hex(offset)[2:].upper()
                    row = hex(CURRENT_ADDRESS-offset)[2:].upper()
                    memory_table.at[row,column]=byte
                    CURRENT_ADDRESS+=1


            elif line[0]=='H':
                prog_name_end = line.find("0")
                PROG_START = line[prog_name_end:prog_name_end+6]
                PROG_SIZE = line[prog_name_end+6:prog_name_end+12] 
                length = int(int(PROG_SIZE,16))
                prog_start_as_int = int(PROG_START,16)
                prog_end = prog_start_as_int+length
                actual_end = prog_end+(16-prog_end%16)
                real_length = int((actual_end-prog_start_as_int)/16)            
                memory_dictionary = {}
                row_indexes = []
                for i in range(16):
                    memory_dictionary[hex(i)[2:].upper()]=[]
                for i in range(real_length):
                    row_indexes.append(hex((int(prog_start_as_int/16)+i)*16)[2:].upper())
                    for j in range(16):
                        memory_dictionary[hex(j)[2:].upper()].append("00")
                memory_table = pd.DataFrame(data=memory_dictionary)
                memory_table.index = row_indexes
        return memory_table
                # print(PROG_SIZE)
                # print(int(PROG_SIZE,16)

                        

                












