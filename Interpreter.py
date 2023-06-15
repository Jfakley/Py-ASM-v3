def get_file_by_lines(file): #gets a file and returns a list containeing each line
    file_data = []
    with open(file, 'r') as f:
        for i in f.readlines():
            file_data.append(i)

    return file_data



def lexer(line, INSTRUCTIONS, reg, pnt, lineNum, lables=[], ram=None ): 

    ##########
    # This function takes an input and turns it into tokens
    ##########


    line_splt = line.split(' ')
    flag_str = 0
    flag_float = 0
    string = ''
    tokens = []

    for tok in line_splt:
        tok = tok.strip('\n,') # Remove newlines in input
        tok = tok.replace('\\0', '\0') # Allows for \0 escape
        tok = tok.replace('\\n', '\n') # Allows for \n escape
        tok = tok.replace('\\033[', '\033[') # Allows for \033 escape

        if tok:
            if tok[-1] == "'" or tok[-1] == "\"": # Is end of string OR string has no spaces
                if tok[0] == "'" or tok[0] == "\"":
                    string += tok.strip('\'"')

                    tokens.append(['str', string])

                else:
                    string += tok.strip('\'"')
                    tokens.append(['str', string])
                    flag_str = 0
                string = ''
                
            elif flag_str:  # Is in a string
                string += tok + ' '

            elif flag_float: # Is a float
                tokens.append(['float', float(tok)])
                flag_float = 0

            elif tok[0] == "'" or tok[0] == "\"": # Is start of string
                string = ''
                string += tok.strip('\'"') + ' '
                flag_str = 1

            elif tok[0] == '@': # Is value of reg
                if isinstance(reg[tok.strip('@')], list):
                    tokens.append(reg[tok.strip('@')])

                else:
                    tokens.append(['???', reg[tok.strip('@')]])

            elif tok[0] == '*': # Is pointer
                x = tok[1:].strip(']').split('[')

                for i in pnt:
                    if i[0] == x[0]:

                        if x[1] == '':
                            tokens.append([x[0], ''.join(map(str, i[1]))])

                        elif x[1][:2] == '0x':
                            tokens.append([x[0], i[1][int(x[1].strip('$'), base=16)]])

                        elif x[1][0] == '%':
                            tokens.append([x[0], i[1][int(x[1].strip('%'), base=2)]])

                        elif x[1][0] == '@':
                            tokens.append([x[0], i[1][reg[x[1].strip('@')]]])
                        
                        else:
                            tokens.append([x[0], i[1][int(x[1], base=10)]]) 


            elif tok[0] == '%': #bin
                tokens.append(['bin', int(tok.strip('%'), base=2)])
                
            elif tok[:2] == '0x': #hex
                tokens.append(['hex', int(tok.strip('$'), base=16)])

            elif tok == '__float':
                flag_float = 1


            elif tok[-1] == ":": # Creates new lable
                tokens.append(['label', lineNum, tok.strip(':')])
            

            elif tok in reg.keys(): # Is refrincing reg
                tokens.append(['reg ref', tok])

            elif tok in INSTRUCTIONS: # Is an instruction
                tokens.append(['inst', INSTRUCTIONS[tok]])
                

            elif tok[0] == ';': # If a ";" is found STOP
                break

            else: 
                for i in lables:
                    if i[1] == tok:
                        tokens.append(['label ref', i[0]])

                try:
                    tokens.append(['int', int(tok, base=10)])

                except ValueError:
                    tokens.append(tok)
    return tokens



def Main():

    INSTRUCTIONS = {} # Instructions are stored here when they are defined 
    comp = [0,0,0,0,0,0] # Compares two values ex(==, !=, >, <,) and enters a 1 if true
    pnt = [] # Pointers are stored here
    lables=[] # Labels are stored here
    stack = [] # The stack, values can be pushed to and poped from here
    ram_val = [] 
    reg = {
            'ax':['int', 0],
            'bx':['int', 0],
            'cx':['int', 0],
            'dx':['int', 0],
            'eax':['int', 0],
            'ebx':['int', 0],
            'ecx':['int', 0],
            'edx':['int', 0],

            'esp':['int', 0],
            'esi':['int', 0],
            
        }   # Registers
    




    instruction_pointer = 0 # What line number we are curently on
    lines = get_file_by_lines('Defult_Setup.asm') 

    while True:
        tokens = lexer(lines[instruction_pointer], INSTRUCTIONS, reg, pnt, instruction_pointer, lables)
            
        #print(tokens)

        if tokens:

            if tokens[0][0] == 'label':
                lables.append([tokens[0][1], tokens[0][2]])

            else:

                """
                Add coustom instructions below ex:

                case #:
                    "INSTRUCTIONS"

                """
                match tokens[0][1]:

                    case 1:
                        exit()

                    case 2:
                        for i in tokens[1:]:
                            print(i[1], end='')

                    case 3: #define new instruction
                        INSTRUCTIONS.update({tokens[1]:tokens[2][1]})

                    case 4: #jump
                        instruction_pointer = tokens[1][1] - 2

                    case 5: # cmp
                        comp[0] = tokens[1][1] == tokens[2][1]
                        comp[1] = tokens[1][1] != tokens[2][1]
                        comp[2] = tokens[1][1] > tokens[2][1]
                        comp[3] = tokens[1][1] < tokens[2][1]
                        comp[4] = tokens[1][1] >= tokens[2][1]
                        comp[5] = tokens[1][1] <= tokens[2][1]

                    case 6: # mov
                        reg[tokens[1][1]] = tokens[2][1]

                    case 7: # INC
                        reg[tokens[1][1]] = reg[tokens[1][1]] + 1

                    case 8: # DEC
                        reg[tokens[1][1]] = reg[tokens[1][1]] - 1

                    case 9: #jump if equal
                        if comp[0]:
                            instruction_pointer = tokens[1][1] - 2

                    case 10: #jump if NOT equal
                        if comp[1]:
                            instruction_pointer = tokens[1][1] - 2

                    case 11: #jump if Grater than
                        if comp[2]:
                            instruction_pointer = tokens[1][1] - 2

                    case 12: #jump if Less than
                        if comp[3]:
                            instruction_pointer = tokens[1][1] - 2

                    case 13: #jump if Grater than or equal to
                        if comp[4]:
                            instruction_pointer = tokens[1][1] - 2

                    case 14: #jump if Less than or equal to
                        if comp[5]:
                            instruction_pointer = tokens[1][1] - 2

                    case 15: # Int
                        match tokens[1][1]:

                            case 0: # 0x0 Nop
                                pass

                            case 1: #0x1 run new file
                                instruction_pointer = 0
                                lines = get_file_by_lines(tokens[2][1])

                            case 2: #0x2 Get len
                                reg['esp'] = len(tokens[2][1]) - 1

                    case 16: # Define byte
                        x = []
                        for i in tokens[2:]:
                            x.append(i[1])

                        if len(x) == 1:
                            x = ''.join(x)

                        pnt.append([tokens[1], x])

                    case 17:
                        if tokens[1] in pnt:
                            pnt.remove(tokens[1])

                    case 18: # convert int to bin
                        reg['esp'] = "{0:b}".format(tokens[1][1])

                    case 19: # Push item onto stack
                        stack.append(tokens[1][1])

                    case 20: # pop item from stack and store in esp
                        reg['esp'] = stack.pop()

                    case 21: # set
                        reg[tokens[1]] = ['int', 0]
                        if len(tokens) == 3:
                            reg[tokens[1]] = tokens[2]
                            
                        
                        

                    

                            

                        

        
        
        instruction_pointer = instruction_pointer + 1




if __name__ == '__main__':
    Main()