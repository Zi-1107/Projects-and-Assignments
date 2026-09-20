#include "header.h"
#include "ticket_category.h"
#include "login_class.h"

int int_err_input(string int_str, string err_msg)
{
    bool cdt = false;						//condition set to false
    int real_int = 0;						//the variable to stored the integer converted from string
    while (!cdt) 
    {							
        getline(cin >> ws, int_str);		//accept user input and stored it as a string

        //assume the input is valid
        cdt = true;

        //check if every character is a digit
        for (char c : int_str) 
        {
            if (!isdigit(c)) 
            {
                //note that negative integer is consider as not an integer in this case as '-' sign is not a digit, same goes to decimal number
                //this only works for positive integer only (pure digit)
                cdt = false;	//if any character is not a digit, set condition to false
                break;			
            }
        }
        if (!cdt) 
        {
            cout << err_msg;
        }
        else 
        {
            return real_int = stoi(int_str);		//retrun the input if it was truly a positive integer
        }
    }
    return 0;
}

void ticketCategoryMenu() 
{
    //menu for ticket category
    cout << " " << "Choose your ticket category:\n";
    cout << " " << setw(54) << setfill('_') << "\n" << setfill(' ');
    cout << " " << "|" << setw(23) << "CATEGORY" << right << setw(17) << "|" << setw(10) << "PRICE(RM)" << setw(2) << "|" << endl;
    cout << " " << "|" << setw(40) << setfill('_') << "|" << setw(12) << setfill('_') << "|" << setfill(' ') << endl;
    cout << " " << setw(40) << left << "| 1 | Adult" << right << "|" << setw(8) << right << "22.50" << setw(4) << "|" << endl;
    cout << " " << setw(40) << left << "| 2 | Children (< 18 years old)" << right << "|" << setw(8) << right << "13.50" << setw(4) << "|" << endl;
    cout << " " << setw(40) << left << "| 3 | Senior (>= 60 years old)" << right << "|" << setw(8) << right << "10.50" << setw(4) << "|" << endl;
    cout << " " << "|___|" << setw(36) << setfill('_') << "|" << setw(12) << setfill('_') << "|" << setfill(' ') << endl;
    cout << " " << setw(52) << left << "| 4 | Quit this menu" << right << "|" << endl;
    cout << " " << "|___|" << setw(48) << setfill('_') << "|" << setfill(' ') << endl;
    cout << setw(56) << setfill('=') << " " << setfill(' ') << endl;
    cout << " " << "Your choice (Enter 1/2/3/4): ";
}

int ticketChoice() 
{
    string cateNum = " ", cateErrMsg = " Your choice is invalid. Pls try again (1/2/3/4): ";
    int cateNum_int = 0;

    while (cateNum_int < 1 || cateNum_int > 4) 
    {
        cateNum_int = int_err_input(cateNum, cateErrMsg);
        if (cateNum_int < 1 || cateNum_int > 4) 
        {		
            //if user input is not 1,2,3,4 but other integer 
            cout << cateErrMsg;
        }
    }
    return cateNum_int;
}

bool quitMenuf(int cateNum) 
{
    //quit menu if user enter 4
    bool quitMenu = false;
    if (cateNum == 4) 
    {
        quitMenu = true;
        cout << "\n ===== You have quit the menu =====\n";
    }
    return quitMenu;
}

string ticketCategory(int cateNum) 
{
    //assign category according to user choice
    string category = " ";
    switch (cateNum) 
    {
    case 1:
        category = "adult";
        break;
    case 2:
        category = "children";
        break;
    case 3:
        category = "senior";
        break;
    default:
        break;
    }
    return category;
}

bool wantOtherCategory() 
{
    bool otherCate = false, cdt = false;
    string input = " ";
    cout << " Would you like to purchase other category?\n" << " 'y' for yes OR 'n' for no: ";
    //ask user whether want to buy other category or not

    while (!cdt) 
    {
        cin >> input;
        if (input == "y" || input == "Y") 
        {
            cdt = true;
            otherCate = true;				//set true if want to buy other category
        }
        else if (input == "n" || input == "N") 
        {
            cdt = true;
            otherCate = false;				//set false if dont want to buy other category
        }
        else 
        {
            cout << " Please enter 'y' or 'n' only: ";		//ask user enter again if not y or n
        }
    }
    return otherCate;
}

int ticketNumf(string category) 
{
    string ticketNum = " ", ticketErrMsg = " Please enter a positive integer for the ticket number you would like to purchase: ";
    int ticketNum_int = 0;
    bool ticketCond = false;

    cout << "\n How many " << category << " tickets would you like to purchase?" << "\n Enter a number: ";
    //ask user how many tickets to buy

    while (!ticketCond) 
    {
        ticketNum_int = int_err_input(ticketNum, ticketErrMsg);

        if (ticketNum_int == 0) 
        {
            //tell user they cannot purchase 0 ticket
            cout << " You cannot choose 0 ticket. Please enter again: ";
        }
        else 
        {
            //user succesfully purchase their ticket
            ticketCond = true;
            cout << "\n ========== You have successfully selected " << ticketNum_int << " tickets for the " << category << " category ==========\n\n";
        }
    }
    return ticketNum_int;
}

double unitPricef(int cateNum) 
{
    //assign unitPrice according to the category chosen 
    double unitPrice = 0.0;
    switch (cateNum) 
    {
    case 1:
        unitPrice = 22.50;		//adult price
        break;
    case 2:
        unitPrice = 13.50;		//children price
        break;
    case 3:
        unitPrice = 10.50;		//seniot price
        break;
    }
    return unitPrice;
}

double catePricef(double unitPrice, int ticketNum) 
{
    double catePrice = 0.0;
    catePrice = unitPrice * ticketNum;		//calculate the total price for one category chosen by user
    return catePrice;
}

