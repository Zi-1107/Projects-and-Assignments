#include <iostream>
#include <string>
#include <iomanip>
#include <cstdlib>
#include <cctype>
#include <algorithm>
#include <sstream>
using namespace std;

const int MAX_QTY = 20;
const int MAX_ITEMS = 5;

bool isDigit(const string& str) {
    if (str.empty()) return false;
    for (char const &c : str) {
        if (!isdigit(c)) return false;
    }
    return true;
}

string trim(const string& str) {
    size_t first = str.find_first_not_of(" \t\r\n");
    if (first == string::npos) return "";
    size_t last = str.find_last_not_of(" \t\r\n");
    return str.substr(first, (last - first + 1));
}

string toUpper(string str) {
    for (size_t i = 0; i < str.length(); ++i) {
        str[i] = toupper(str[i]);
    }
    return str;
}

class Stock {
public:
    string itemName;
    int quantity;
    double price;

    Stock(string name = "", int qty = 0, double prc = 0.00) {
        itemName = name;
        quantity = qty;
        price = prc;
    }

    char getSymbol() const {
        if (!itemName.empty()) {
            return toupper(itemName[0]);
        }
        return ' ';
    }
};

class VendingUi {
private:
    Stock stockList[MAX_ITEMS];
    string username;
    string password;

public:
    
    VendingUi(Stock inputList[MAX_ITEMS] = nullptr) {
        username = "admin";
        password = "1234";

        if (inputList != nullptr) {
            for (int i = 0; i < MAX_ITEMS; ++i) {
                stockList[i] = inputList[i];
            }
        } else {
            for (int i = 0; i < MAX_ITEMS; ++i) {
                stockList[i] = Stock("", 0, 0);
            }
        }
    }

    bool checkEmpty() {
        for (int i = 0; i < MAX_ITEMS; ++i) {
            if (stockList[i].itemName != "") {
                return false;
            }
        }
        return true;
    }

    int getActiveSlots(int activeSlotsArray[MAX_ITEMS]) {
        int count = 0;
        for (int i = 0; i < MAX_ITEMS; ++i) {
            if (!stockList[i].itemName.empty()) {
                activeSlotsArray[count] = i + 1;
                count++;
            }
        }
        return count; 
    }

    string checkN() {
        int activeSlots[MAX_ITEMS];
        int count = getActiveSlots(activeSlots);

        if (count == 0) {
            return "()";
        }

        string result = "(";
        for (int i = 0; i < count; ++i) {
            result += to_string(activeSlots[i]);
            if (i < count - 1) {
                result += ", ";
            }
        }
        result += ")";
        return result;
    }

    void printStock() {
        cout << "\n--- Stock Levels ---\n";
        for (int i = 0; i < MAX_ITEMS; ++i) {
            if (!stockList[i].itemName.empty()) {
                cout << "[" << (i + 1) << "] Item Name: " << stockList[i].itemName 
                     << ", Quantity: " << stockList[i].quantity << "\n";
            }
        }
    }

    void printPrice() {
        cout << "\n--- Price List ---\n";
        for (int i = 0; i < MAX_ITEMS; ++i) {
            if (!stockList[i].itemName.empty()) {
                cout << "[" << (i + 1) << "] Item Name: " << stockList[i].itemName 
                     << ", Price: $" << fixed << setprecision(2) << stockList[i].price << "\n";
            }
        }
    }

    void printAll() {
        cout << "\n--- Detailed Inventory Summary ---\n";
        for (int i = 0; i < MAX_ITEMS; ++i) {
            string name = !stockList[i].itemName.empty() ? stockList[i].itemName : "[EMPTY SLOT]";
            cout << "[" << (i + 1) << "] Slot " << (i + 1) << " -> Name: " << name 
                 << ", Price: $" << fixed << setprecision(2) << stockList[i].price 
                 << ", Quantity: " << stockList[i].quantity << "\n";
        }
    }

    void checkAll() {
        system("cls");
        int activeItems = 0;
        int totalQuantity = 0;

        for (int i = 0; i < MAX_ITEMS; ++i) {
            if (!stockList[i].itemName.empty()) {
                activeItems++;
                totalQuantity += stockList[i].quantity;
            }
        }

        bool needsRefill = totalQuantity < (activeItems * 2);

        cout << "\n--- Machine Diagnostic Check ---\n";
        cout << "Active Menu Slots: " << activeItems << "\n";
        cout << "Total Physical Items in Stock: " << totalQuantity << "\n";
        cout << "Status: " << (needsRefill ? "\u26A0\uFE0F REFILL ADVISED" : "STOCK OKAY") << "\n";
    }

    void printVendingMachine() {
        if (checkEmpty()) {
            cout << "VENDING MACHINE IS EMPTY\n";
            return;
        }

        system("cls");
        int dividerLen = 0;
        string namesRow = "";
        string valuesRow = "";
        
        char initialsRowSymbols[MAX_ITEMS];
        int initialsRowQuantities[MAX_ITEMS];
        int dynamicActiveCount = 0;
        int colWidth = 14;

        for (int i = 0; i < MAX_ITEMS; ++i) {
            if (!stockList[i].itemName.empty()) {
                ostringstream nameOss, priceOss;
                nameOss << left << setw(colWidth) << stockList[i].itemName;
                namesRow += nameOss.str();

                priceOss << "$" << left << setw(colWidth - 1) << fixed << setprecision(2) << stockList[i].price;
                valuesRow += priceOss.str();

                initialsRowSymbols[dynamicActiveCount] = stockList[i].getSymbol();
                initialsRowQuantities[dynamicActiveCount] = stockList[i].quantity;
                dynamicActiveCount++;

                dividerLen += colWidth;
            }
        }

        cout << "\t" << namesRow << "\n";
        cout << "\t" << valuesRow << "\n";
        cout << "\t" << string(dividerLen, '-') << "\n";

        int maxRows = 1;
        for (int i = 0; i < dynamicActiveCount; ++i) {
            if (initialsRowQuantities[i] > maxRows) {
                maxRows = initialsRowQuantities[i];
            }
        }

        for (int rowIdx = 0; rowIdx < maxRows; ++rowIdx) {
            string rowOutput = "";
            for (int i = 0; i < dynamicActiveCount; ++i) {
                char initial = initialsRowSymbols[i];
                int quantity = initialsRowQuantities[i];

                ostringstream cellOss;
                if (quantity == 0) {
                    if (rowIdx == 0) {
                        cellOss << left << setw(colWidth) << "<SOLD OUT>";
                    } else {
                        cellOss << left << setw(colWidth) << "";
                    }
                } else if (rowIdx < quantity) {
                    string symStr(1, initial);
                    cellOss << left << setw(colWidth) << symStr;
                } else {
                    cellOss << left << setw(colWidth) << "";
                }
                rowOutput += cellOss.str();
            }

            if (!trim(rowOutput).empty()) {
                cout << "\t" << rowOutput << "\n";
            }
        }
    }

    void buyMenu() {
        if (checkEmpty()) {
            cout << "No items available to purchase.\n";
            cout << "\nPress Enter to return...";
            cin.get();
            return;
        }

        int validSlots[MAX_ITEMS];
        int totalValid = getActiveSlots(validSlots);

        cout << "Please Select Your Drink \n" << checkN() << ": ";
        string rawAns;
        getline(cin, rawAns);
        rawAns = trim(rawAns);

        bool isValidChoice = false;
        int ans = -1;
        if (isDigit(rawAns)) {
            ans = stoi(rawAns);
            for (int i = 0; i < totalValid; ++i) {
                if (validSlots[i] == ans) {
                    isValidChoice = true;
                    break;
                }
            }
        }

        if (!isValidChoice) {
            cout << "Invalid selection.\n";
            cout << "\nPress Enter to return...";
            cin.get();
            return;
        }

        Stock& selectedItem = stockList[ans - 1];

        if (selectedItem.quantity == 0) {
            cout << "<SOLD OUT>\n";
        } else {
            cout << "Please Enter Your Payment - " << fixed << setprecision(2) << selectedItem.price << ": ";
            string amtInput;
            getline(cin, amtInput);
            amtInput = trim(amtInput);

            try {
                size_t parsedChars;
                double amt = stod(amtInput, &parsedChars);
                // Validation parsing to simulate Python's implicit float breakdown error handling
                if (parsedChars != amtInput.length()) throw invalid_argument("Extra chars");

                if (amt >= selectedItem.price) {
                    cout << "Your Change is $" << fixed << setprecision(2) << (amt - selectedItem.price) << "\n";
                    selectedItem.quantity -= 1;
                    cout << "Thank You, Come Back Again!\n";
                } else {
                    cout << "Insufficient Payment Given \nTransaction Canceled\n";
                }
            } catch (...) {
                cout << "Invalid money input format. Transaction Canceled.\n";
            }
        }

        cout << "\nPress Enter to continue...";
        cin.get();
    }

    void adminInventory() {
        system("cls");
        cout << "Password: ";
        string inputPass;
        getline(cin, inputPass);

        if (inputPass == password) {
            while (true) {
                system("cls");
                cout << "\n--- Inventory Administration ---\n";
                cout << "\n[1] Refill Stock\n";
                cout << "[2] Reset Stock (Empty out all items)\n";
                cout << "[3] Update Price\n";
                cout << "[4] Change/Create Item\n";
                cout << "[5] Delete Item\n";
                cout << "[6] Check All\n";
                cout << "[B] Back to Main Menu\n";
                cout << "Enter Option: ";

                string choice;
                getline(cin, choice);
                choice = toUpper(trim(choice));

                if (choice == "1") {
                    refillStock();
                } else if (choice == "2") {
                    resetStock();
                } else if (choice == "3") {
                    updatePrice();
                } else if (choice == "4") {
                    changeItem();
                } else if (choice == "5") {
                    deleteItem();
                } else if (choice == "6") {
                    checkAll();
                    cout << "\nPress Enter to continue...";
                    cin.get();
                } else if (choice == "B") {
                    break;
                } else {
                    cout << "\nInvalid Option. Please try again.\n";
                    cout << "\nPress Enter to continue...";
                    cin.get();
                }
            }
        }
    }

    void refillStock() {
        system("cls");
        printStock();
        int validSlots[MAX_ITEMS];
        int totalValid = getActiveSlots(validSlots);

        string promptN = checkN();
        string estr = ", ALL)";
        // Replicating Python slice replacement: check_n()[:-1] + estr
        string complexPrompt = promptN.substr(0, promptN.length() - 1) + estr;

        cout << "What Item would you like to refill \n" << complexPrompt << ": ";
        string ans;
        getline(cin, ans);
        ans = toUpper(trim(ans));

        if (ans == "ALL") {
            for (int i = 0; i < MAX_ITEMS; ++i) {
                if (!stockList[i].itemName.empty()) {
                    stockList[i].quantity = MAX_QTY;
                }
            }
            cout << "All active items refilled!\n";
        } else if (isDigit(ans)) {
            int selectedIdx = stoi(ans);
            bool isValid = false;
            for (int i = 0; i < totalValid; ++i) {
                if (validSlots[i] == selectedIdx) {
                    isValid = true;
                    break;
                }
            }

            if (isValid) {
                stockList[selectedIdx - 1].quantity = MAX_QTY;
                cout << stockList[selectedIdx - 1].itemName << " refilled!\n";
            } else {
                cout << "Invalid input.\n";
            }
        } else {
            cout << "Invalid input.\n";
        }
        cout << "\nPress Enter to continue...";
        cin.get();
    }

    void resetStock() {
        cout << "Reset All Stock to 0? Y/N: ";
        string ans;
        getline(cin, ans);
        ans = toUpper(trim(ans));

        if (ans == "Y") {
            for (int i = 0; i < MAX_ITEMS; ++i) {
                stockList[i].quantity = 0;
            }
            cout << "All Stock quantities are now 0.\n";
        } else {
            cout << "Process Canceled.\n";
        }
        cout << "\nPress Enter to continue...";
        cin.get();
    }

    void updatePrice() {
        system("cls");
        printPrice();
        int validSlots[MAX_ITEMS];
        int totalValid = getActiveSlots(validSlots);

        cout << "What Item's price would you like to change \n" << checkN() << ": ";
        string rawAns;
        getline(cin, rawAns);
        rawAns = trim(rawAns);

        bool isValidChoice = false;
        int ans = -1;
        if (isDigit(rawAns)) {
            ans = stoi(rawAns);
            for (int i = 0; i < totalValid; ++i) {
                if (validSlots[i] == ans) {
                    isValidChoice = true;
                    break;
                }
            }
        }

        if (isValidChoice) {
            int idx = ans - 1;
            cout << "New Price: ";
            string priceInput;
            getline(cin, priceInput);
            priceInput = trim(priceInput);

            try {
                size_t parsedChars;
                double newPrice = stod(priceInput, &parsedChars);
                if (parsedChars != priceInput.length()) throw invalid_argument("Parsing offset error");
                stockList[idx].price = newPrice;
                cout << "Price updated successfully!\n";
            } catch (...) {
                cout << "Invalid amount format.\n";
            }
        } else {
            cout << "Invalid input.\n";
        }
        cout << "\nPress Enter to continue...";
        cin.get();
    }

    void changeItem() {
        system("cls");
        printAll();

        cout << "Enter slot number (1-" << MAX_ITEMS << ") to modify/create: ";
        string rawAns;
        getline(cin, rawAns);
        rawAns = trim(rawAns);

        if (isDigit(rawAns) && stoi(rawAns) >= 1 && stoi(rawAns) <= MAX_ITEMS) {
            int idx = stoi(rawAns) - 1;
            cout << "Press Enter to keep the previous values unchanged\n\n";
            Stock& item = stockList[idx];

            cout << "Name (" << (!item.itemName.empty() ? item.itemName : "None") << "): ";
            string nameInput;
            getline(cin, nameInput);
            nameInput = trim(nameInput);
            if (!nameInput.empty()) {
                item.itemName = nameInput;
            }

            cout << "Quantity (" << item.quantity << "): ";
            string qtyInput;
            getline(cin, qtyInput);
            qtyInput = trim(qtyInput);
            if (isDigit(qtyInput)) {
                item.quantity = min(stoi(qtyInput), MAX_QTY);
            }

            cout << "Price (" << item.price << "): ";
            string priceInput;
            getline(cin, priceInput);
            priceInput = trim(priceInput);
            if (!priceInput.empty()) {
                try {
                    size_t parsedChars;
                    double parsedPrice = stod(priceInput, &parsedChars);
                    if (parsedChars != priceInput.length()) throw invalid_argument("Parsing error");
                    item.price = parsedPrice;
                } catch (...) {
                    cout << "Invalid price layout ignored.\n";
                }
            }
            cout << "Slot updated configuration successfully!\n";
        } else {
            cout << "Invalid slot input.\n";
        }
        cout << "\nPress Enter to continue...";
        cin.get();
    }

    void deleteItem() {
        system("cls");
        printStock();
        int validSlots[MAX_ITEMS];
        int totalValid = getActiveSlots(validSlots);

        cout << "What Item would you like to delete \n" << checkN() << ": ";
        string rawAns;
        getline(cin, rawAns);
        rawAns = trim(rawAns);

        bool isValidChoice = false;
        int ans = -1;
        if (isDigit(rawAns)) {
            ans = stoi(rawAns);
            for (int i = 0; i < totalValid; ++i) {
                if (validSlots[i] == ans) {
                    isValidChoice = true;
                    break;
                }
            }
        }

        if (isValidChoice) {
            int idx = ans - 1;
            cout << "Deleted: " << stockList[idx].itemName << "\n";
            stockList[idx] = Stock("", 0, 0);
        } else {
            cout << "Invalid selection.\n";
        }
        cout << "\nPress Enter to continue...";
        cin.get();
    }
};

int main() {
    Stock stockList[MAX_ITEMS];

    // Local structures simulating Python stock tuples
    string mockNames[5] = {"Milo", "Coke", "A&W", "100+", ""};
    int mockQuantities[5] = {10, 0, 2, 4, 0};
    double mockPrices[5] = {1.50, 2.50, 3.50, 4.50, 0.00};

    // Filling up our fixed array space
    for (int i = 0; i < 5 && i < MAX_ITEMS; ++i) {
        stockList[i] = Stock(mockNames[i], mockQuantities[i], mockPrices[i]);
    }

    // Checking boundaries if MAX_ITEMS layout is altered
    for (int i = 5; i < MAX_ITEMS; ++i) {
        stockList[i] = Stock("", 0, 0);
    }

    VendingUi vendingMachine(stockList);

    while (true) {
        system("cls");
        cout << "\n=== Vending Machine ===\n";
        cout << "1 [ Purchase Items ]\n";
        cout << "2 [ Inventory-Admin ]\n";
        cout << "3 [ Exit ]\n";
        cout << "Enter Option: ";

        string option;
        getline(cin, option);
        option = trim(option);

        if (option == "1") {
            vendingMachine.printVendingMachine();
            vendingMachine.buyMenu();
        } else if (option == "2") {
            vendingMachine.adminInventory();
        } else if (option == "3") {
            cout << "\nThank you for using the Vending Machine. Goodbye!\n";
            break;
        } else {
            cout << "\nInvalid Option. Please try again.\n";
            cout << "\nPress Enter to continue...";
            cin.get();
        }
    }

    return 0;
}