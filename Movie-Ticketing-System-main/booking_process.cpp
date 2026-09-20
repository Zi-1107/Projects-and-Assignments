#include "booking_process.h"
#include "login_class.h"

TicketInfo CompleteTicketBuyingProcess(cust_class& cust)
{
    TicketInfo main_store;

    int complete = 0;
    tuple<int, string, double> LocalTicketCategoryNums[3];
    int cateNum = 0, ticketNum = 0, totalticketnumber = 0, indexing = 0;
    double unitPrice = 0.0, catePrice = 0.0, discount = 1.0, totalPrice = 0.0, grandTotal = 0.0;
    string category = " ";
    bool quitMenu = false, wantOtherCate = true;

    //loop only if user want to choose other category
    while (wantOtherCate) 
    {
        ticketCategoryMenu();									//display menu 
        cateNum = ticketChoice();								//category choice
        quitMenu = quitMenuf(cateNum);
        if (quitMenu && indexing == 0) 
        {
            main_store.quitCategoryMenu = true;
            break;
        }
        else if (quitMenu) 
        {
            main_store.quitCategoryMenu = false;
            complete = 1;
            break;												//immediately exit the loop if want to quit menu
        }
        else 
        {
            main_store.quitCategoryMenu = false;
            category = ticketCategory(cateNum);						//assign category (adult, children, senior)
            unitPrice = unitPricef(cateNum);						//assign unitPrice according to category
            ticketNum = ticketNumf(category);		                //ticket number of the category chosen

            totalticketnumber += ticketNum;

            catePrice = catePricef(unitPrice, ticketNum);			//calculate total price for one category
            totalPrice += catePrice;								//calculate total price for every category chosen

            LocalTicketCategoryNums[indexing] = make_tuple(ticketNum, category, catePrice);

            //user allowed to choose other category 
            wantOtherCate = wantOtherCategory();
            if (!wantOtherCate) 
            {
                complete = 1;
                break;
            }
        }
        indexing += 1;
    }
    
    if (complete == 1)
    {
        main_store.total_ticket_amount = totalticketnumber;
        for (int i = 0; i < 3; ++i) 
        {
            main_store.TicketCategoryNums[i] = LocalTicketCategoryNums[i];
        }
        bool is_member = cust.cust_mem_log;                              //true false
        main_store.is_member = is_member;

        if (is_member == true)
        {
            discount = 0.9;
        }

        grandTotal = totalPrice * discount;
        main_store.grandTotal = grandTotal;

        return main_store;
    }
    else 
    {
        return main_store;
    }
}

BookingInfo booking_main(Movie movie_list[10], int ticket_amount)
{
    BookingInfo main_store;
    string date, time;
    vector<pair<string, string>> seat_store;

    // Print list of movies
    cout << "\nAvailable Movies:" << endl;
    for (size_t i = 0; i < 10; ++i) 
    {
        cout << i + 1 << ". " << movie_list[i].name << endl;
    }

    int selected_movie_idx = 0;
    while (true) 
    {
        // while loop to check valid input for selected_movie_idx
        cout << "Enter a number to select a movie, 0 or letter to exit: ";
        cin >> selected_movie_idx;

        if (cin.fail()) 
        {  // Check for invalid input (e.g., letters)
            main_store.quitBookingMenu = true;
            cout << "\n===== Exiting booking menu =====\n" << endl;
            break;
        }
        else if (selected_movie_idx == 0) 
        {
            main_store.quitBookingMenu = true;
            cout << "\n===== Exiting booking menu =====\n" << endl;
            break;
        }
        else if (selected_movie_idx >= 1 && selected_movie_idx <= 10) 
        {
            Movie selected_movie = movie_list[selected_movie_idx - 1];
            main_store.quitBookingMenu = false;

            for (int i = 0; i < ticket_amount; ++i) 
            {
                string movie_name;
                pair<string, string> seat_n;
                tie(date, time, seat_n, movie_name) = selected_movie.booking(date, time, ticket_amount);

                // to check if seat for this movie at this date and time is fully booked
                // if so, we restart the while loop
                if (movie_name.empty()) 
                {
                    continue;
                }

                seat_store.push_back(seat_n);

                // declare inside cus local for loop variables
                main_store.movie_name = movie_name;
                main_store.date = date;
                main_store.time = time;
            }

            main_store.ticket_amount = ticket_amount; //amount of tickets for this session only
            main_store.seat_store = seat_store; //store of booked seats for this session only

            return { main_store };

        }
        else 
        {
            cout << "Invalid selection. Please try again." << endl;
        }
    }
    // maybe we can declare defualt values for main_store   
    return { main_store }; // Default return if exiting, so struc main_store is empty
}
