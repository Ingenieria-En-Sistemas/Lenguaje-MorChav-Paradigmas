from scanner import Scanner

def main():
    s = Scanner("not (true and false) ")
    tokens = s.scanAll()
    print(tokens)

if __name__ == '__main__':
    main()