/*Library*/
#include "header.h"

/*File Include*/
#include "login.h"
#include "login_class.h"
#include "booking_process.h"
#include "ticket_category.h"
#include "movie_class.h"
#include "admin_function.h"

string autoID();
int pay_decision();
string payMethDec();
string rtc();
void invoice(int ticketnum[], string category[], movie_class& movie, cust_class cust);
void receipt(double grandTotal, string movieTitle, string time, movie_class movie);
double payAmount(double grandTotal);

string LOGO = R"(
 _____  ___           ___ _                                
/__   \/ _ \/\   /\  / __(_)_ __   ___ _ __ ___   __ _ ___ 
  / /\/ /_\/\ \ / / / /  | | '_ \ / _ \ '_ ` _ \ / _` / __|
 / / / /_\\  \ V / / /___| | | | |  __/ | | | | | (_| \__ \
 \/  \____/   \_/  \____/|_|_| |_|\___|_| |_| |_|\__,_|___/

)";

int main()
{
  //Class Variable
  admin_class admin;
  movie_class movie;
  cust_class cust;
  TicketInfo ticket_store;
  BookingInfo booking_store;

  // declare movies in array list to loop through 
  Movie movie_list[10] = {
    Movie("The Godfather", "2hr", "Drama", "English", {"1", "2", "3", "4"}, {"12:30", "1:30", "2:00", "3:45"}),
    Movie("Titanic", "2hr", "Romance", "English", {"1", "2", "3", "4"}, {"12:30", "1:30", "2:00", "3:45"}),
    Movie("Inception", "1hr", "Sci-Fi", "English", {"1", "2", "3", "4"}, {"12:30", "1:30", "2:00", "3:45"}),
    Movie("The Dark Knight", "2hr", "Action", "English", {"1", "2", "3", "4"}, {"12:30", "1:30", "2:00", "3:45"}),
    Movie("Parasite", "2hr", "Drama", "English", {"1", "2", "3", "4"}, {"12:30", "1:30", "2:00", "3:45"}),
    Movie("Forrest Gump", "2hr 40min", "Romance", "English", {"1", "2", "3", "4"}, {"12:30", "1:30", "2:00", "3:45"}),
    Movie("Avengers: Endgame", "3h", "Action", "English", {"1", "2", "3", "4"}, {"12:30", "1:30", "2:00", "3:45"}),
    Movie("The Exorcist", "2hr", "Horror", "English", {"1", "2", "3", "4"}, {"12:30", "1:30", "2:00", "3:45"}),
    Movie("A Nightmare on Elm Street", "2hr", "Horror", "English", {"1", "2", "3", "4"}, {"12:30", "1:30", "2:00", "3:45"}),
    Movie("Hereditary", "2hr", "Sci-Fi", "Drama", {"1", "2", "3", "4"}, {"12:30", "1:30", "2:00", "3:45"})
  };

  
  //Local Variable
  char choice = ' ';
  bool retry = 1;

  cout << "--------------------------------------\n";
  cout << LOGO << endl;
  cout << "--------------------------------------\n";
  cout << "\n======== Welcome to the TGVCinemas Booking System ========\n";
  
  while (isspace(choice) || retry == 1) 
  {
    cout << "\nPlease select your role:" << endl;
    cout << "1. Administrator" << endl;
    cout << "2. Customer" << endl;
    cout << "0. Exit Program" << endl;
    cout << "Enter your choice: ";
    cin.get(choice);
    cin.ignore(100,'\n');

    //Validate user input
    if (isalpha(choice) || isspace(choice))
    {
      retry = 1;
      cout << "Invalid choice. Please try again." << endl;
    }
    else if (isdigit(choice))
    {
      retry = 0;
      if (choice == '1')
      {
          admin_login(admin);

          checkpoint1:
          admin_menu(admin);

          if (admin.ad_choice != 0)
          {
            switch(admin.ad_choice)
            {
                case 1:
                   ad_mvlist(movie);
                   break;
                case 2:
                   ad_salesreport(movie);
                   break;
                case 3:
                   ad_mfymovie(movie);
                   break;
            }
            goto checkpoint1;
          }
          else 
          {
            retry = 1;
            admin.username = "";
            admin.userpass = "";
            break;
          }
      }
      else if (choice == '2')
      {
          cust_member(cust);

          ticket_store = CompleteTicketBuyingProcess(cust);

          if (!ticket_store.quitCategoryMenu)
          {
              booking_store = booking_main(movie_list, ticket_store.total_ticket_amount);
          }

          if (!booking_store.quitBookingMenu)
          {       
              vector<pair<string, string>> seat_store = booking_store.seat_store;
              cout << "\nBooking Summary:\nMovie: " << booking_store.movie_name << "\nDate: " << booking_store.date << "\nTime: " << booking_store.time
                  << "\nNumber of Tickets: " << booking_store.ticket_amount << "\nSeat(s): ";
              for (auto seat : seat_store)
              {
                  cout << seat.first << seat.second << " ";
              }
              cout << endl;
           
              string is_member = ticket_store.is_member ? "Yes" : "No";    //the yes or no string to be displayed based on whether the customer is member or not
              cout << "\nTicket Summary:\nMember: " << is_member << "\nNumber of Tickets: " << ticket_store.total_ticket_amount
                  << "\nGrand Total: " << ticket_store.grandTotal << endl;
              for (int i = 0; i < 3; ++i)
              {
                      cout << "(" << get<0>(ticket_store.TicketCategoryNums[i]) << ", "
                      << get<1>(ticket_store.TicketCategoryNums[i]) << ", "
                      << get<2>(ticket_store.TicketCategoryNums[i]) << ")" << std::endl;
              }
          }

          int ticketnum[3];
          string category[3];
          double catePrice[3];

          for (int i = 0; i < 3; i++)  
          {
            ticketnum[i] = get<0>(ticket_store. TicketCategoryNums[i]);  
            category[i] = get<1>(ticket_store.TicketCategoryNums[i]); 
            catePrice[i] = get<2>(ticket_store.TicketCategoryNums[i]);
          }
          
            invoice(ticketnum, category, movie, cust);
            receipt(movie.grandtotal, booking_store.movie_name, booking_store.time, movie);
      }
      else if (choice == '0')
      {
         break;
      }
      else
      {
         cout << "Invalid choice. Please try again." << endl;
         retry = 1;
      }
    }
  }
  cout << "\n=============== THANK YOU for using the TGVCINEMAS system ===============";
  cout << "\n=========================== HAVE A NICE DAY! ===========================\n";
  return 0;  
}



