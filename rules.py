def show_rules():

    file = open("data/rules.txt", "r")
    content = file.read()
    print(content)
    file.close()
    
    input("\nPress Enter to return to the menu...")
