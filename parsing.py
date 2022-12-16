def Create_External_Symbol_Table(HTERECORDPATH,PROGORDER,STARTING_ADDRESS):
    STAB_LIST = [{} for i in range(len(PROGORDER))]
    with open(HTERECORDPATH) as f:
        PROG_NAME = ""
        LOCAL_SYMTAB = {}
        for line in f:
            if(line[0]=="H"):
                prog_name_end = line.find("0");
                PROG_NAME = line[1:prog_name_end].upper().replace("X","")
                print(PROG_NAME)
                PROG_START = line[prog_name_end:prog_name_end+6]
                print(PROG_START)
                PROG_SIZE = line[prog_name_end+6:prog_name_end+12]
                LOCAL_SYMTAB[PROG_NAME]=PROG_START
                LOCAL_SYMTAB["LENGTH"]=PROG_SIZE
            if(line[0]=="D"):
                final_index = 0
                while(final_index<len(line)):
                    prev_index = final_index
                    final_index+=line[final_index:].find("0")
                    if(final_index==-1):
                        break
                    label = line[prev_index:final_index]
                    value = line[final_index:final_index+6]
                    LOCAL_SYMTAB[label]=value
                    final_index+=6

                
                
            if(line[0]=="E"):
                print(PROG_NAME)
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
                
            


    
