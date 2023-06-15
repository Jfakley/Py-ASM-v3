INIT:
    0x03 define     0x03 ; adds alias

    define nop      0x00 ; Do nothing
    define hlt      0x01 ; STOP

    define print    0x02 ; Write to console
    define jmp      0x04 ; Jump to pos
    define cmp      0x05 ; compare 2 values
    define mov      0x06 ; Move value into register

    define inc      0x07 ; Increase value in register by 1
    define dec      0x08 ; Decrease value in register by 1

    define je       0x09 ; Jump if ==
    define jne      0x0A ; Jump if !=
    define jg       0x0B ; Jump if >
    define jl       0x0C ; Jump if <
    define jge      0x0D ; Jump if >=
    define jle      0x0E ; Jump if <=

    define int      0x0F ; Do action depending on the number given

    define db       0x10 ; Create pointer
    define rst      0x11 ; Delete pointer or instruction

    define binary   0x12 ; convert int to bin and store in esp
    
    define push     0x13 ; Push item onto stack
    define pop      0x14 ; pop item from stack and store in esp

    db NEXT_FILE "cov.asm"  ; Create pointer that points to the next file to run
    
    

    int 0x1 *NEXT_FILE[]    ; Run the next file