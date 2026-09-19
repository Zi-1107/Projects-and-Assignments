#include <iostream>
#include <string>
#include "Container.cpp"

using namespace std;

int main() {
    Container<string> cart(5);
    string item;

    cout << "Online Shopping Cart" << endl;

    // Add items to the container
    cart.addItem("Laptop");
    cart.addItem("Wireless Mouse");
    cart.addItem("USB-C Cable");
    cart.addItem("Mechanical Keyboard");

    cart.print();
    cout << "\nCurrent items in cart: " << cart.getLength() << "\n\n";

    // Use searchItem to check for a specific product
    cout << "What item are you searching for? ";
    getline(cin, item);
    cout << "\nChecking for " << item << "..." << endl;
    if (cart.searchItem(item)) {
        cout << "Item is in your cart." << endl;
    }
    else {
        cout << "Item not found." << endl;
    }

    //Use removeItem to remove from container
    cout << "\nWhat item do you want to remove? ";
    getline(cin, item);
    cout << "\nRemoving " << item<< "from cart..." << endl;
    cart.removeItem(item);

    //Change from laptop to desktop
    string item2;
    cout << "\nWhat item do you want to remove? ";
    getline(cin, item);
    cout << "What item do you want to change to? ";
    getline(cin, item2);
    cart.updateItem(item, item2);

    cart.print();

    // print and clear
    cout << "\n\nProceeding to Checkout..." << endl;
    cout << "Payment successful" << endl;
    cart.print();

    cout << "\nThank you for shopping\n\n" << endl;

    return 0;
}