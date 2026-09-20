#pragma once
#include "header.h"

int int_err_input(string int_str, string err_msg);
void ticketCategoryMenu();
int ticketChoice();
bool quitMenuf(int cateNum);
string ticketCategory(int cateNum);
bool wantOtherCategory();
int ticketNumf(string category);
double unitPricef(int cateNum);
double catePricef(double unitPrice, int ticketNum);


// DECLARE STRUCTS AND CONSTANTS START --
struct BookingInfo 
{
    // struct for storing current booking info
    // lasts only for current session

    string movie_name;
    string date;
    string time;
    bool quitBookingMenu;
    int ticket_amount;
    vector<pair<string, string>> seat_store;  // Store seat information as a list
};

struct TicketInfo 
{
    // struct for storing ticket info
    // lasts only for current session

    tuple<int, string, double> TicketCategoryNums[3]; // [(3, adult, 18.90), (2, child, 12.60)]
    bool quitCategoryMenu;
    bool is_member; // true false
    int total_ticket_amount;
    double grandTotal;
};
// -- DECLARE STRUCTS AND CONSTANTS END

