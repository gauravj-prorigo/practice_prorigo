def serac_by_word(word):
    data = True
    line_no = 1
    with open("Pratice.txt", "r") as f:
        while data:
            data = f.readline()
            if word in data:
                return line_no
            line_no += 1
        
        return -1        

result = serac_by_word("pythons")
print(result)
