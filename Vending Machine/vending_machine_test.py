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
        # Ensure we always match exactly MAX_ITEMS
        if stock_list:
            self.stock_list = stock_list
        else:
            self.stock_list = [Stock("", 0, 0) for _ in range(MAX_ITEMS)]
        self.username = "admin"
        self.password = "1234"

    def check_empty(self):
        for item in self.stock_list:
            if item.item_name != "":
                return False
        return True

    def get_active_slots(self):
        """Returns a list of 1-based indices that actually contain items."""
        return [i + 1 for i, stock in enumerate(self.stock_list) if stock.item_name]

    def check_n(self):
        slots = self.get_active_slots()
        if not slots:
            return "()"
        return "(" + ", ".join(map(str, slots)) + ")"
    
    def print_stock(self):
        print("\n--- Stock Levels ---")
        for i, stock in enumerate(self.stock_list):
            if stock.item_name:
                print(f"[{i+1}] Item Name: {stock.item_name}, Quantity: {stock.quantity}")

    def print_price(self):
        print("\n--- Price List ---")
        for i, stock in enumerate(self.stock_list):
            if stock.item_name:
                print(f"[{i+1}] Item Name: {stock.item_name}, Price: ${stock.price:.2f}")

    def print_all(self):
        print("\n--- Detailed Inventory Summary ---")
        for i, stock in enumerate(self.stock_list):
            name = stock.item_name if stock.item_name else "[EMPTY SLOT]"
            print(f"[{i+1}] Slot {i+1} -> Name: {name}, Price: ${stock.price:.2f}, Quantity: {stock.quantity}")

    def check_all(self):
        sys("cls")
        active_items = 0
        total_quantity = 0
        
        for stock in self.stock_list:
            if stock.item_name:
                active_items += 1
                total_quantity += stock.quantity
                
        needs_refill = total_quantity < (active_items * 2)
        
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
        col_width = 14

        for stock in self.stock_list:
            if stock.item_name:
                names_row += f"{stock.item_name:<{col_width}}"
                values_row += f"${stock.price:<{col_width-1}.2f}"
                initials_row.append((stock.symbol, stock.quantity))
                divider_len += col_width
                
        print(f"\t{names_row}")
        print(f"\t{values_row}")
        print("\t" + "-" * divider_len)

        max_rows = max([qty for _, qty in initials_row] + [1])
        
        for row_idx in range(max_rows):
            row_output = ""
            for initial, quantity in initials_row:
                if quantity == 0:
                    if row_idx == 0:
                        row_output += f"{'<SOLD OUT>':<{col_width}}"
                    else:
                        row_output += f"{'':<{col_width}}"
                elif row_idx < quantity:
                    row_output += f"{initial:<{col_width}}"
                else:
                    row_output += f"{'':<{col_width}}"
            
            if row_output.strip():
                print(f"\t{row_output}")

    def buy_menu(self):
        if self.check_empty():
            print("No items available to purchase.")
            input("\nPress Enter to return...")
            return

        valid_slots = self.get_active_slots()
        raw_ans = input(f"Please Select Your Drink \n{self.check_n()}: ").strip()
        
        if not raw_ans.isdigit() or int(raw_ans) not in valid_slots:
            print("Invalid selection.")
            input("\nPress Enter to return...")
            return

        ans = int(raw_ans)
        selected_item = self.stock_list[ans - 1]

        if selected_item.quantity == 0:
            print("<SOLD OUT>")
        else:
            try:
                amt = float(input(f"Please Enter Your Payment - {selected_item.price:.2f}: ").strip())
                if amt >= selected_item.price:
                    print(f"Your Change is ${amt - selected_item.price:.2f}")
                    selected_item.quantity -= 1
                    print("Thank You, Come Back Again!")
                else:
                    print("Insufficient Payment Given \nTransaction Canceled")
            except ValueError:
                print("Invalid money input format. Transaction Canceled.")
                
        input("\nPress Enter to continue...")

    def admin_inventory(self): 
        sys('cls')
        if input("Password: ") == self.password:
            while True:
                sys('cls')
                print("\n--- Inventory Administration ---")
                print("\n[1] Refill Stock")
                print("[2] Reset Stock (Empty out all items)")
                print("[3] Update Price")
                print("[4] Change/Create Item")
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
                    input("\nPress Enter to continue...")
                elif choice == "B":
                    break
                else:
                    print("\nInvalid Option. Please try again.")
                    input("\nPress Enter to continue...")

    def refill_stock(self): 
        sys('cls')
        self.print_stock()
        valid_slots = self.get_active_slots()
        
        estr = ", ALL)"
        ans = input(f"What Item would you like to refill \n{self.check_n()[:-1] + estr}: ").strip().upper()
        
        if ans == "ALL":
            for i in self.stock_list:
                if i.item_name:
                    i.quantity = MAX_QTY
            print("All active items refilled!")
        elif ans.isdigit() and int(ans) in valid_slots:
            self.stock_list[int(ans)-1].quantity = MAX_QTY
            print(f"{self.stock_list[int(ans)-1].item_name} refilled!")
        else:
            print("Invalid input.")
        input("\nPress Enter to continue...")

    def reset_stock(self):
        ans = input("Reset All Stock to 0? Y/N: ").strip().upper()
        if ans == "Y":
            for i in self.stock_list:
                i.quantity = 0
            print("All Stock quantities are now 0.")
        else:
            print("Process Canceled.")
        input("\nPress Enter to continue...")

    def update_price(self): 
        sys('cls')
        self.print_price()
        valid_slots = self.get_active_slots()

        raw_ans = input(f"What Item's price would you like to change \n{self.check_n()}: ").strip()
        if raw_ans.isdigit() and int(raw_ans) in valid_slots:
            idx = int(raw_ans) - 1
            try:
                new_price = float(input("New Price: "))
                self.stock_list[idx].price = new_price
                print("Price updated successfully!")
            except ValueError:
                print("Invalid amount format.")
        else:
            print("Invalid input.")
        input("\nPress Enter to continue...")

    def change_item(self): 
        sys('cls')
        self.print_all()

        raw_ans = input(f"Enter slot number (1-{MAX_ITEMS}) to modify/create: ").strip()
        if raw_ans.isdigit() and (1 <= int(raw_ans) <= MAX_ITEMS):
            idx = int(raw_ans) - 1
            print("Press Enter to keep the previous values unchanged\n")
            item = self.stock_list[idx]

            name_input = input(f"Name ({item.item_name if item.item_name else 'None'}): ").strip()
            if name_input:
                item.item_name = name_input

            qty_input = input(f"Quantity ({item.quantity}): ").strip()
            if qty_input.isdigit():
                item.quantity = min(int(qty_input), MAX_QTY)

            price_input = input(f"Price ({item.price}): ").strip()
            if price_input:
                try:
                    item.price = float(price_input)
                except ValueError:
                    print("Invalid price layout ignored.")
            print("Slot updated configuration successfully!")
        else:
            print("Invalid slot input.")
        input("\nPress Enter to continue...")

    def delete_item(self): 
        sys('cls')
        self.print_stock()
        valid_slots = self.get_active_slots()

        raw_ans = input(f"What Item would you like to delete \n{self.check_n()}: ").strip()
        if raw_ans.isdigit() and int(raw_ans) in valid_slots:
            idx = int(raw_ans) - 1
            print(f"Deleted: {self.stock_list[idx].item_name}")
            self.stock_list[idx] = Stock("", 0, 0)
        else:
            print("Invalid selection.")
        input("\nPress Enter to continue...")
       

def main():
    stock_list = []
    stock_item = [("Milo", 10, 1.50), ("Coke", 0, 2.50), ("A&W", 2, 3.50), ("100+", 4, 4.50), ("", 0, 0.00)]
    
    for i in stock_item:
        stock_list.append(Stock(i[0], i[1], i[2]))
        
    # Ensure pool stays capped to structural MAX constraints
    while len(stock_list) < MAX_ITEMS:
        stock_list.append(Stock("", 0, 0))

    vending_machine = Vending_Ui(stock_list=stock_list) 

    while True:
        sys('cls')
        print("\n=== Vending Machine ===")
        print("1 [ Purchase Items ]")
        print("2 [ Inventory-Admin ]")
        print("3 [ Exit ]")
        
        option = input("Enter Option: ").strip()
        
        if option == "1":
            vending_machine.print_vending_machine()
            vending_machine.buy_menu()
        elif option == "2":
            vending_machine.admin_inventory()
        elif option == "3":
            print("\nThank you for using the Vending Machine. Goodbye!")
            break
        else:
            print("\nInvalid Option. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()