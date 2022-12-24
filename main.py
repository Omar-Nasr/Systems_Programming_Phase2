import parsing 
import visualization
## Input From User
SICORSICXE = input("Please Enter The Type of Machine:Sic or SicXE")
if(SICORSICXE.upper()=="SIC"):
    memory_table = parsing.ABSOLUTE_LOAD("HTE.txt")
    visualization.display_resulting_table(memory_table)
else:
    starting_address = int(input("Please Enter The Starting Address"),16)
    ProgramOrder = input("Please enter the Program Loading Order seperated by commas").strip().split(",")
    ProgramOrder = [i.upper() for i in ProgramOrder]

    # Calculate where the Table Starts and Ends Then Create the Memory Table
    start = starting_address-starting_address%16

    ESTAB = parsing.Create_External_Symbol_Table("HDRTME.txt",ProgramOrder,starting_address)
    end = ESTAB["END"]+16-ESTAB["END"]%16
    memory_table = visualization.generate_memory_table(start,end) 


    memory_table = parsing.Link_And_Load("HDRTME.txt",ESTAB,memory_table)
    visualization.display_resulting_table(memory_table)
        
