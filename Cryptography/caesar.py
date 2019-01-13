alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
input_str = raw_input("Enter message in UPPERCASE: ")
input_shift = raw_input("Shift value, default 3: ")
shift_value = int(input_shift) if len(input_shift) > 0 else 3

input_len = len(input_str)
output_str = ""

for i in range(input_len):
    char = input_str[i]
    pos = alpha.find(char)
    newpos = (pos + shift_value)%26
    print i, char, pos, newpos,
    output_str += alpha[newpos]

print "Encrypted message: ", output_str

    
