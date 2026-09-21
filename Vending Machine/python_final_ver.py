from os import system as sys
MAX_QTY = 20
MAX_ITEMS = 5

class Stock():
    def __init__(self, name, quantity, price):
        self.item_name = name if name else ""
        self.quantity = quantity if quantity else 0
        self.price = price if price else 0.00
    
    # Dynamic property so changing the name automatically fixes the symbol
    @property
    def symbol(self):
        return self.item_name[0].upper() if self.item_name else " "


class Vending_Ui():
    def __init__(self, stock_list):
        self.stock_list = stock_list if stock_list else [Stock("", 0, 0), Stock("", 0, 0), Stock("", 0, 0), Stock("", 0, 0), Stock("", 0, 0)]
        self.username = "admin"
        self.password = "1234"

    def check_empty(self):
        all_empty = True

        for i in self.stock_list:
            if i.item_name != "":  # Found an item that is NOT empty
                all_empty = False
                break  # No need to keep checking the rest
        if all_empty:
            return True

    def check_n(self):
        n = 0
        cusstr = "("
        for i in self.stock_list:
            if i.item_name != "":
                n += 1
                cusstr += f"{n}, "
        n_cusstr = cusstr[:-2]
        n_cusstr += ")"
        return (n_cusstr)
    
    def print_stock(self):
            print("\n--- Stock Levels ---")
            for stock in self.stock_list:
                if stock.item_name:
                    print(f"Item Name: {stock.item_name}, Quantity: {stock.quantity}")

    def print_price(self):
        print("\n--- Price List ---")
        for stock in self.stock_list:
            if stock.item_name:
                print(f"Item Name: {stock.item_name}, Price: ${stock.price:.2f}")

    def print_all(self):
        print("\n--- Detailed Inventory Summary ---")
        for stock in self.stock_list:
            if stock.item_name:
                print(f"Item Name: {stock.item_name}, Price: ${stock.price:.2f}, Quantity: {stock.quantity}")

    def check_all(self):
        sys("cls")
        active_items = 0
        total_quantity = 0
        
        for stock in self.stock_list:
            if stock.item_name:
                active_items += 1
                total_quantity += stock.quantity
                
        needs_refill = total_quantity < (active_items * 2) # Flag true if average stock drops under 2 units per item
        
        print(f"\n--- Machine Diagnostic Check ---")
        print(f"Active Menu Slots: {active_items}")
        print(f"Total Physical Items in Stock: {total_quantity}")
        print(f"Status: {'⚠️ REFILL ADVISED' if needs_refill else 'STOCK OKAY'}")
        
    def print_vending_machine(self):
        
        if self.check_empty():
            print("VENDING MACHINE IS EMPTY")
            return
        
        sys('cls')
        divider_len = 0
        names_row = ""
        values_row = ""
        initials_row = []
        
        # Consistent column width variable to easily adjust sizing
        col_width = 14

        for stock in self.stock_list:
            # Skip completely empty stock slots if necessary, or preserve space
            if stock.item_name:
                # FIX 1 & 2: Concat strings and move internal formatting alignment inside curly brackets
                names_row += f"{stock.item_name:<{col_width}}"
                values_row += f"{stock.price:<{col_width}.2f}"
                initials_row.append((stock.symbols, stock.quantity))
                divider_len += col_width
                
        print(f"\t{names_row}")
        print(f"\t{values_row}")
        print("\t" + "-" * divider_len)

        # 1. Determine the maximum height loop length
        max_rows = max([qty for _, qty in initials_row] + [1])
        
        # 2. Loop row by row vertically
        for row_idx in range(max_rows):
            row_output = ""
            
            for initial, quantity in initials_row:
                if quantity == 0:
                    # If empty, display <SOLD OUT> on the first row only
                    if row_idx == 0:
                        row_output += f"{'<SOLD OUT>':<{col_width}}"
                    else:
                        row_output += f"{'':<{col_width}}"
                elif row_idx < quantity:
                    # FIX 3: Match the exact column alignment widths (col_width)
                    row_output += f"{initial:<{col_width}}"
                else:
                    row_output += f"{'':<{col_width}}"
            
            # Print row if it contains items
            if row_output.strip():
                print(f"\t{row_output}")

    def buy_menu(self):

        if self.check_empty():
            return

        ans = int(input(f"Please Select Your Drink \n{self.check_n()}: ").strip())
        if str(ans) in self.check_n():
            if self.stock_list[ans-1].quantity == 0:
                print("<SOLD OUT>")
            else:
                amt = float(input(f"Please Enter Your Payment - {self.stock_list[ans-1].price}: ").strip())
                if amt > self.stock_list[ans-1].price:
                    print(f"Your Change is { amt - (self.stock_list[ans-1].price):.2f}")
                    self.stock_list[ans-1].quantity -= 1
                else:
                    print("Insufficient Payment Given \nTransection Canceled")
        else:
            print("invalid input")
        print("Thank You, Come Back Again")

    def admin_inventory(self): 
        sys('cls')
        if input("Password: ") == self.password:
            while True:
                sys('cls')
                print("\n--- Inventory Administration ---")
                
                print("\n[1] Refill Stock")
                print("[2] Reset Stock (Empty out all items)")
                print("[3] Update Price")
                print("[4] New Item")
                print("[5] Delete Item")
                print("[6] Check All")
                print("[B] Back to Main Menu")
                
                choice = input("Enter Option: ").strip().upper()
                
                if choice == "1":
                    self.refill_stock()
                elif choice == "2":
                    self.reset_stock()
                elif choice == "3":
                    self.update_price()
                elif choice == "4":
                    self.change_item()
                elif choice == "5":
                    self.delete_item()
                elif choice == "6":
                    self.check_all()
                elif choice == "B":
                    break
                else:
                    print("\nInvalid Option. Please try again.")
                
                input("\nPress Enter to continue...")

    def refill_stock(self): 
        sys('cls')
        self.print_stock()

        estr = ", ALL)"
        ans = input(f"What Item would you like to refill \n{self.check_n()[:-1] + estr}: ").strip().upper()
        if ans == "ALL":
            for i in self.stock_list:
                i.quantity = MAX_QTY
        elif str(ans) in self.check_n():
            self.stock_list[int(ans)-1].quantity = MAX_QTY
        else:
            print("invalid input")

    def reset_stock(self):
        ans = input("Reset All Stock to 0: Y/N").strip().upper()
        if ans == "Y":
            for i in self.stock_list:
                i.quantity = 0
            print("All Stock is now 0")
        elif ans == "N":
            print("Processed Canceled")
        else:
            print("invalid input")

    def update_price(self): 
        sys('cls')
        self.print_price()

        ans = int(input(f"What Item's price would you like to change \n{self.check_n()}: ").strip())
        if str(ans) in self.check_n():
            self.stock_list[int(ans)-1].price = float(input("New Price: "))
        else:
            print("invalid input")

    def change_item(self): 
        sys('cls')
        self.print_all()

        ans = int(input(f"What column's item would you like to change or create \n{self.check_n()}: ").strip())
        if str(ans) in self.check_n():
            print("Enter to keep the previous values")
            item = self.stock_list[int(ans) - 1]

            # 1. Update Name
            name_input = input(f"Name ({item.item_name}): ")
            if name_input.strip():  # Checks if the input is not just spaces or empty
                item.item_name = name_input

            # 2. Update Quantity
            qty_input = input(f"Quantity ({item.quantity}): ")
            if qty_input.strip():
                item.quantity = int(qty_input)  # Leaves it as previous value if empty

            # 3. Update Price
            price_input = input(f"Price ({item.price}): ")
            if price_input.strip():
                item.price = float(price_input)
        else:
            print("invalid input")

    def delete_item(self): 
        sys('cls')
        print("\n--- Stock Levels ---")
        for stock in self.stock_list:
            if stock.item_name:
                print(f"Item Name: {stock.item_name}")

        ans = int(input(f"What Item would you like to delete \n{self.check_n()}: ").strip())
        if str(ans) in self.check_n():
            self.stock_list[int(ans)-1] = Stock("", 0, 0)
        else:
            print("invalid input")
       
def main():
    # Max 5 items, 20 qty

    # test
    stock_list = []
    stock_item = [("Milo", 10, 1.50), ("Coke", 0, 2.50), ("A&W", 2, 3.50), ("100+", 4, 4.50), ("", 12, 5.50)]
    for i in stock_item:
        stock_list.append(Stock(i[0], i[1], i[2]))
    Vending_Machine = Vending_Ui(stock_list=stock_list) 

    while True:
        sys('cls')
        print("\nVending Machine")
        print("1 [Purchase Items ]")
        print("2 [Inventory-Admin ]")
        print("3 [Exit ]")
        
        option = input("Enter Option: ").strip()
        
        if option == "1":
            Vending_Machine.print_vending_machine()
            Vending_Machine.buy_menu()
        elif option == "2":
            Vending_Machine.admin_inventory()
        elif option == "3":
            print("\nThank you for using the Vending Machine. Goodbye!")
            break
        else:
            print("\nInvalid Option. Please try again.")

if __name__ == "__main__":
    sys('cls')
    main()