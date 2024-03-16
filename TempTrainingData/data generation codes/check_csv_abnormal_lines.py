def check(alp):
    file_path = f'{alp}.csv'  # Replace with your file path
    # Open the file with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read and process each line in the file
        line = file.readline()
        i=1
        j=1
        while line:
            # Process the line
            line=line.split('|')
            if(len(line)>=4):
                print(i,alp,j)
                j+=1
            # Read the next line
            line = file.readline()
            i+=1
            
s='bcnopqrstuvwz'
for x in s:
    check(x)