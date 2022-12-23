import parsing 
import visualization
## Input From User
starting_address = int(input("Please Enter The Starting Address"),16)
ProgramOrder = input("Please enter the Program Loading Order seperated by commas").strip().split(",")
ProgramOrder = [i.upper() for i in ProgramOrder]

# Calculate where the Table Starts and Ends Then Create the Memory Table
start = starting_address-starting_address%16
end = int("4140",16)
memory_table = visualization.generate_memory_table(start,end) 
ESTAB = parsing.Create_External_Symbol_Table("HDRTME.txt",ProgramOrder,starting_address)
memory_table = parsing.Apply_T_RECORDS("HDRTME.txt",ESTAB,memory_table)
print(ESTAB)
print(memory_table)
    
