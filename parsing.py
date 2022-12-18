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
    for STAB in STAB_LIST:
        for SYMBOL in STAB.keys():
            if(SYMBOL=="LENGTH"):
                continue;
            STAB[SYMBOL] = hex(int(STAB[SYMBOL],16)+STARTING_ADDRESS)[2:]

        if(len(STAB.keys())!=0):
            STARTING_ADDRESS = STARTING_ADDRESS+int(STAB["LENGTH"],16)

    return STAB_LIST
def Apply_T_RECORDS(HTERECORDPATH,STAB_LIST,PROGORDER,MEMORY_TABLE):
    with open(HTERECORDPATH) as f:
        PROG_STARTING_ADDRESS=0
        for line in f:
            if(line[0]=="H"): 
                prog_name_end = line.find("0")
                PROG_NAME = line[1:prog_name_end].upper().replace("X","")
                PROG_INDEX = PROGORDER.index(PROG_NAME)
                PROG_STARTING_ADDRESS = int(STAB_LIST[PROG_INDEX][PROG_NAME],16)
                
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
        return MEMORY_TABLE

                    

                












