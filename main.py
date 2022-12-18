import parsing 
import visualization
## Input From User
starting_address = int(input("Please Enter The Starting Address"),16)
ProgramOrder = input("Please enter the Program Loading Order seperated by commas").strip().split(",")

# Calculate where the Table Starts and Ends Then Create the Memory Table
start = starting_address-starting_address%16
end = int("4140",16)
memory_table = visualization.generate_memory_table(start,end) 
memory_table.at["4130","5"]="9"
STAB_LIST = parsing.Create_External_Symbol_Table("HDRTME.txt",ProgramOrder,starting_address)
memory_table = parsing.Apply_T_RECORDS("HDRTME.txt",STAB_LIST,ProgramOrder,memory_table)
# print(STAB_LIST)
print(memory_table)
    
