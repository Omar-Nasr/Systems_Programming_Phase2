import pandas as pd
def generate_memory_table(start,end):
 

    length = int((end - start)/16)
    memory_dictionary = {}
    row_indexes = []
    for i in range(16):
        memory_dictionary[hex(i)[2:].upper()]=[]
    for i in range(length):
        row_indexes.append(hex((int(start/16)+i)*16)[2:].upper())
        for j in range(16):
            memory_dictionary[hex(j)[2:].upper()].append("0")
    memory_table = pd.DataFrame(data=memory_dictionary)
    memory_table.index = row_indexes
    return memory_table


