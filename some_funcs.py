def read_password(filename):
    with open(filename, 'r') as f:
        password = f.read()
    return password


#print(read_password('spiders/file.txt'))
