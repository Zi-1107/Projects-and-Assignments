#include "login_class.h"
#include "ticket_category.h"
#include "movie_class.h"

string autoID()
{
    srand(time(0));

    char num[9];

    for (int i = 0; i < 8; i++)
    {
        num[i] = (rand() % 10 + 48);
    }
    num[8] = '\0';

    return num;
}

int pay_decision()
{
    //DISPLAYS CHOICES FOR SELECTION
    cout << "\n\n-----[Please Select Payment method]-----" << endl;
    cout << setfill('.');
    cout << "|" << "1." << setw(36) << right << "Credit Card" << "|" << endl;
    cout << setfill('.');
    cout << "|" << "2." << setw(36) << right << "Debit Card" << "|" << endl;
    cout << setfill('.');
    cout << "|" << "3." << setw(36) << right << "Cash" << "|" << endl;
    cout << setfill('.');
    cout << "|" << "4." << setw(36) << right << "E-Wallet" << "|" << endl;
    cout << "----------------------------------------" << endl;

    //PROMPTS USER TO CHOOSE PAYMENT METHOD

    string choice = " ";
    int choice_int = 0;
    string errMsg = "Invalid input. Please re-enter: ";
        cout << "Enter Your Payment Method: ";
    choice_int = int_err_input(choice, errMsg);   
      
    return choice_int;
}

//PAYMENT METHOD
string payMethDec()
{
    int pay_type = 0;           //VARIABLE pay_type WILL RECEIVE RETURN VALUE FROM FUNCTION pay_decision()
    string pay_dis = " ";       //pay_dis IS USED TO DISPLAY IN THE TICKET
    pay_type = pay_decision();
    switch (pay_type) 
    {
    case 1:
        pay_dis = "Credit Card";
        break;
    case 2:
        pay_dis = "Debit Card";
        break;
    case 3:
        pay_dis = "Cash";
        break;
    case 4:
        pay_dis = "E-wallet";
    }
    return pay_dis;
}


string rtc()
{
    time_t timestamp = time(NULL);
    struct tm datetime = *localtime(&timestamp);

    char output[50];

    strftime(output, 50, "%d/%m/%Y", &datetime);

    return output;
}


void invoice(int ticketNum[], string category[], movie_class& movie, cust_class cust)
{
    string date = rtc();
    int adultTicketNum = 0;
    int childTicketNum = 0;
    int seniorTicketNum = 0;
    int totalTicketNum = 0;
    
    for (int i = 0; i < 3; i++)
    {
        if (category[i] == "adult") 
        {
            adultTicketNum = ticketNum[i];
        }
        else if (category[i] == "children") 
        {
            childTicketNum = ticketNum[i];
        }
        else
        {
            seniorTicketNum = ticketNum[i];
        }
    }

    totalTicketNum = adultTicketNum + childTicketNum + seniorTicketNum;
    double adultCatePrice = movie.cost_adult * adultTicketNum;
    double childCatePrice = movie.cost_kid * childTicketNum;
    double seniorCatePrice = movie.cost_senior * seniorTicketNum;
    double subtotal = adultCatePrice + childCatePrice + seniorCatePrice;
    double discountAmount = 0.0;
    double taxPayable = 0.0;
    double grandTotal = 0.0;

    if (cust.cust_mem_log == 1)
    {
        discountAmount = subtotal * 0.1;
        subtotal -= discountAmount;
    }

    taxPayable = subtotal * 0.06;
    grandTotal = subtotal + taxPayable;
    movie.grandtotal = grandTotal;

    cout << "\n\n";
    cout << "---------------------------------------------------" << endl;
    cout << "                     TGV Cinemas                   " << endl;
    cout << "                  Tel: 017-4315465                 " << endl;
    cout << "---------------------------------------------------" << endl;
    cout << setfill(' ') << setw(13) << left << "Invoice ID: " << autoID() << setw(30) << right << date << endl;
    cout << left << setw(25) << "Items" << right << setw(27) << "Price (RM)" << endl;
    cout << fixed << setprecision(2);
    cout << setw(15) << left << "1. Adult Ticket " << "(RM " << movie.cost_adult << " x " << adultTicketNum << ") " << setw(20) << right << adultCatePrice << endl;
    cout << setw(15) << left << "2. Child Ticket " <<  "(RM " << movie.cost_kid << " x " << childTicketNum << ") " << setw(20) << right << childCatePrice << endl;
    cout << setw(15) << left << "3. Senior Ticket " << "(RM " << movie.cost_senior << " x " << seniorTicketNum << ")" << setw(20) << right << seniorCatePrice << endl;
    cout << setw(52) << right << "--------" << endl;
    cout << setw(33) << left << "Subtotal" << setw(18) << right << subtotal << endl;
    cout << setw(33) << left << "Discount" << setw(11) << right << "-" << setw(7) << right << discountAmount << endl;
    cout << setw(33) << left << "Tax(6%)" << setw(11) << right << "+" << setw(7) << right << taxPayable << endl;
    cout << setw(52) << right << "--------" << endl;
    cout << setw(23) << left << "Total Ticket Number: " << totalTicketNum << endl;
    cout << setw(33) << left << "Total Payable: " << setw(18) << right << grandTotal << endl;
    cout << "---------------------------------------------------" << endl;
    
}

double payAmount(double grandTotal) 
{
    double pay_amount = 0.0;
    cout << "\nEnter Payment Amount: " << endl;
    cin >> pay_amount;
    
    while(pay_amount < grandTotal)
    {
        cin >> pay_amount;
        if(cin.fail())
        {
            cin.ignore(1000,'\n');
            cout << "Invalid input. Please re-enter: " << endl;
        }
        else
        {
            cin.ignore(1000,'\n');
            cout << "Invalid Payment Amount. Please re-enter: "<< endl;
        }
    }
    return pay_amount;
}


void receipt(double grandTotal, string movieTitle, string time, movie_class movie)
{
    string pay_dis = payMethDec();
    double pay_amount = payAmount(movie.grandtotal);
    double change = pay_amount - grandTotal;
    cout << "\n\n";
    cout << "---------------------------------------------" << endl;
    cout << "                   RECEIPT                   " << endl;
    cout << "---------------------------------------------" << endl;
    cout << fixed << setprecision(2);
    cout << setfill(' ');
    cout << setw(15) << left << "Movie Title" << right << setw(2) << ":" << setw(28) << movieTitle << endl;
    cout << setw(15) << left << "Time" << right << setw(2) << ":" << setw(28) << time << endl;
    cout << setw(15) << left << "Price(RM)" << right << setw(2) << ":" << setw(28) << grandTotal << endl;
    cout << setw(15) << left << "Payment Method" << right << setw(2) << ":" << setw(28) << pay_dis << endl;
    cout << "\n";
    cout << setw(15) << left << "Payment Amount" << right << setw(2) << ":" << setw(28) << pay_amount << endl;
    cout << setw(15) << left << "Change" << right << setw(2) << ":" << setw(28) << change << endl;
    cout << "---------------------------------------------" << endl;
}
