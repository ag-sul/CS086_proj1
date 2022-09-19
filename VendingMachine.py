def space(n):
    spaces = ""
    for i in range(0, n):
        spaces = spaces + " "
    return spaces

class VendingMachine:
    history = ""
    items = []
    balance = 0
    def __init__(self):
        self.balance = 0
    
    def getBalance(self):
        return "$" + "{:.2f}".format(self.balance)
    
    def addItem(self, item):
        itemFound = False
        itemIndex = 0
        for i in self.items:
            if i.name.upper() == item.name.upper() and i.cost == item.cost:
                itemFound = True
                itemIndex = self.items.index(i)
                break
        if itemFound:
            self.items[itemIndex].inventory = self.items[itemIndex].inventory + item.inventory
        else:
            self.items.append(item)
    
    def vendItemByName(self, name, money):
        for item in self.items:
            if item.name.upper() == name.upper():
                if item.cost <= money:
                    if item.inventory > 0:
                        item.inventory = item.inventory - 1
                        self.balance = self.balance + item.cost
                        return money - item.cost
                    else:
                        print("Item out of stock.")
                        raise Exception
                else:
                    print("Insufficient funds.")
                    raise Exception
        print("Item not found: " + name)
        raise Exception



    def printInventory(self):
        names = []
        maxName = 4
        ids = []
        maxId = 2
        prices = []
        maxPrice = 5
        quantities = []
        maxQuantity = 9
        
        for item in self.items:
            currentName = item.name
            names.append(currentName)
            if len(currentName) > maxName:
                maxName = len(currentName)
                
            currentId = str(self.items.index(item))
            ids.append(currentId)
            if len(currentId) > maxId:
                maxId = len(currentId)
                
            currentPrice = "$" + "{:.2f}".format(item.cost)
            prices.append(currentPrice)
            if len(currentPrice) > maxPrice:
                maxPrice = len(currentPrice)
                
            currentInv = str(item.inventory)
            quantities.append(currentInv)
            if len(currentInv) > maxQuantity:
                maxQuantity = len(currentInv)
        
        print("Item" + space(maxName - 4) + "    ID" + space(maxId - 2) + "    Price" + space(maxPrice - 5) + "    Inventory" + space(maxQuantity - 9))
        
        for i in range(0, len(names)):
            print(names[i] + space(maxName - len(names[i]) + 4) + ids[i] + space(maxId - len(ids[i]) + 4) + prices[i] + space(maxPrice - len(prices[i]) + 4) + quantities[i] + space(maxQuantity - len(quantities[i]) + 4))
        
class Item:
    cost = 0
    inventory = 0
    name = ""
    
    def __init__(self, name, inventory, cost):
        self.cost = cost
        self. inventory = inventory
        self.name = name

class Money:
    pennies = 0
    nickels = 0
    dimes = 0
    quarters = 0
    ones = 0
    
    def __init__(self, *args):
        if len(args) == 1:
            amount = args[0]
            self.dollars = int(amount)
            amount = amount - 1 * self.dollars
            self.quarters = int(amount/0.25)
            amount = amount - 0.25 * self.quarters
            self.dimes = int(amount/0.1)
            amount = amount - 0.1 * self.dimes
            self.nickels = int(amount/0.05)
            amount = amount - 0.05 * self.nickels
            self.pennies = int(amount/0.01)
            amount = amount - 0.01 * self.pennies
        if len(args) == 5:
            self.pennies = args[4]
            self.nickels = args[3]
            self.dimes = args[2]
            self.quarters = args[1]
            self.dollars = args[0]
        
    def getAmount(self):
        return self.pennies * 0.01 + self.nickels * 0.05 + self.dimes * 0.1 + self.quarters * 0.25 + self.dollars

    def toString(self):
        output = ""
        if self.dollars > 0:
            output = output + str(self.dollars) + " Dollars, "
        if self.quarters > 0:
            output = output + str(self.quarters) + " Quarters, "
        if self.dimes > 0:
            output = output + str(self.dimes) + " Dimes, "
        if self.nickels > 0:
            output = output + str(self.nickels) + " Nickels, "
        if self.pennies > 0:
            output = output + str(self.pennies) + " Pennies"
        
        output = output.replace("1 Dollars", "1 Dollar")
        output = output.replace("1 Quarters", "1 Quarter")
        output = output.replace("1 Dimes", "1 Dime")
        output = output.replace("1 Nickels", "1 Nickel")
        output = output.replace("1 Pennies", "1 Penny")

        output = output.removesuffix(", ")
        output = " and ".join(output.rsplit(", ", 1))

        return output          
    
class Parser:
    def parse(self, cmd):
        if cmd.upper() == "BALANCE":
            print(str(vm.getBalance()))
        elif cmd.upper() == "HISTORY":
            print(str(vm.history))
        elif cmd.upper() == "INVENTORY":
            vm.printInventory()
        elif cmd.upper().startswith("ADD ITEM"):
            try:
                cmdList = cmd.split(" ")
                name = ""
                index = 2
                while (not cmdList[index].isnumeric()):
                    name = name + " " + cmdList[index]
                    index = index + 1
                qty = int(cmdList[index])
                price = float(cmdList[index+1].strip("$"))
                vm.addItem(Item(name.strip(" "), qty, price))
            except Exception as e:
                print("Error adding item. Correct syntax is:\nadd item <str> <int> <float>")
        elif cmd.upper().startswith("BUY ITEM"):
            try:
                cmdList = cmd.split(" ")
                name = ""
                index = 2
                while (not cmdList[index].isnumeric()):
                    name = name + " " + cmdList[index]
                    index = index + 1
                dollars = int(cmdList[index])
                quarters = int(cmdList[index+1])
                dimes = int(cmdList[index+2])
                nickels = int(cmdList[index+3])
                pennies = int(cmdList[index+4])
                money = Money(dollars, quarters, dimes, nickels, pennies)
                change = Money(vm.vendItemByName(name.strip(" "), money.getAmount()))
                print("Vending: " + name.strip(" "))
                print("Change: ${:.2f}".format(change.getAmount()) + "    (" + change.toString() + ")")
                vm.history = vm.history + "\n" + cmd
            except Exception as e:
                print(str(e))
                print("Error buying item. Correct syntax is:\nbuy item <str> <int> <int> <int> <int> <int>")
        elif cmd.upper() == "HELP":
            print("Command                         Example                     Description\n\n" + 
                "balance                         balance                     shows the balance\n" +
                "history                         history                     prints list of transactions\n" +
                "inventory                       inventory                   prints available items with name and ID\n" +
                "add item <str> <int> <float>    add item chips 2 $1.00      add an item name qty price\n" +
                "buy item <str> {5}<int>         buy item chips 1 2 2 4 3    buys an item with # dollars, quarters, dimes, nickels,\n" +
                "                                                            pennies. It also shows change given and the remaining\n" +
                "                                                            balance with currency distribution. For change, the machine\n" +
                "                                                            uses the largest denominator of currency that is available.\n" +
                "help                            help                        display help menu with these commands\n" +
                "exit                            exit                        exit the vending machine")
        elif cmd.upper() == "EXIT":
            print("Goodbye.")
            exit(0)
        else:
            print("Unknown command: " + cmd)


#MAIN
vm = VendingMachine()

p = Parser()
while (True):
    p.parse(input(">"))