#ifndef MOVIE_CLASS_H
#define MOVIE_CLASS_H

#include "header.h"
#include "ticket_category.h"

// MOVIE CLASS DEFINITION
class Movie 
{
public:
    // declare variables 
    array<string, 10> alphabs = { "A", "B", "C", "D", "E", "F", "G", "H", "I", "J" };
    array<string, 10> list_nums = { "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" };
    string name;
    string length;
    string genre;
    string language;
    vector<string> dates;
    vector<string> time;
    map<string, map<string, vector<pair<string, string>>>> booking_data;

    // Constructor to initialize the movie with details, def  __init__. 
    Movie(string name, string length, string genre, string language, vector<string> dates, vector<string> times)
        : name(name), length(length), genre(genre), language(language), dates(dates), time(times) {
        booking_data = initialize_booking(dates, times);
    }

    // Initialize booking data with available dates and times
    // Nested Map, Ex.
    // main_dict = { 
    //     date = {
    //         time = {
    //             []
    //         }
    //     }
    // }
    map<string, map<string, vector<pair<string, string>>>> initialize_booking(vector<string> dates, vector<string> times) {
        map<string, map<string, vector<pair<string, string>>>> main_dict;
        for (string date : dates) 
        {
            map<string, vector<pair<string, string>>> plc_dict;
            for (string time : times) 
            {
                plc_dict[time] = vector<pair<string, string>>();  // Initialize empty seat vector for each time
            }
            main_dict[date] = plc_dict;
        }
        return main_dict;
    }

    // Print movie information
    void print_info() 
    {
        cout << "Movie name: " << name << endl;
        cout << "Movie length: " << length << endl;
        cout << "Movie genre: " << genre << endl;
        cout << "Movie language: " << language << endl;
    }

    // Input for date selection with validation
    string in_date() 
    {
        cout << "This is the available dates: ";
        // for date in dates, looping throught one at a time. Think of indexing
        for (string date : dates) 
        {
            cout << date << ", ";
        }
        cout << endl;

        string chosen_date;
        while (true) 
        {
            cout << "Enter a valid date: ";
            cin >> chosen_date;
            // find(start of range, end of range, variable to be found)
            // If found return variable, else return end of range
            if (find(dates.begin(), dates.end(), chosen_date) != dates.end()) 
            {
                return chosen_date;
            }
            cout << "Invalid date, please try again." << endl;
        }
    }

    // Input for time selection with validation
    string in_time() 
    {
        cout << "This is the available times: ";
        // for time in times, looping throught one at a time. Think of indexing
        for (string t : time) 
        {
            cout << t << ", ";
        }
        cout << endl;

        string chosen_time;
        while (true) 
        {
            cout << "Enter a valid time: ";
            cin >> chosen_time;
            // find(start of range, end of range, variable to be found)
            // If found return variable, else return end of range
            if (find(time.begin(), time.end(), chosen_time) != time.end()) 
            {
                return chosen_time;
            }
            cout << "Invalid time, please try again." << endl;
        }
    }

    // Return booked seats for a given date and time
    vector<pair<string, string>>& return_seats(string date, string time) 
    {
        // dictionary is called with keys
        // Key : Value
        // Nested Dictionary is called with two or more keys
        return booking_data[date][time]; // returns seats vector 
    }

    // Show available and booked seats
    void show_seats(const vector<pair<string, string>>& booked_seats) 
    {
        cout << "   1   2   3   4   5   6   7   8   9   10" << endl; // hard coded, can use setw

        for (string letter : alphabs) 
        {
            cout << letter << " ";
            for (string col : list_nums) 
            {
                // find(start of range, end of range, variable to be found)
                // If found return variable, else return end of range
                // make_pair(letter, col) makes a pair which is what our booked_seats var type is. It just combines it into a tuple / pair
                if (find(booked_seats.begin(), booked_seats.end(), make_pair(letter, col)) != booked_seats.end()) 
                {
                    cout << "|XX|"; // occupied
                }
                else 
                {
                    cout << "|  |"; // unoccupied
                }
            }
            cout << endl;
        }
    }

    // Input for seat selection with validation
    pair<string, string> in_seats(string date, string time) 
    {
        string row_alpha, col_num;
        while (true) 
        {
            cout << "Enter seat letter (A-J): ";
            cin >> row_alpha;
            transform(row_alpha.begin(), row_alpha.end(), row_alpha.begin(), ::toupper); // transform string to upper. Could use char, but I'm more comfortable with strings
            // find(start of range, end of range, variable to be found)
            // If found return variable, else return end of range
            // Our parameters are our gobals declared at the header
            if (find(alphabs.begin(), alphabs.end(), row_alpha) == alphabs.end()) 
            {
                cout << "Invalid row. Please try again." << endl;
                continue;
            }

            // Defining a list of valid numbers as strings

            cout << "Enter seat number (1-10): ";
            cin >> col_num;

            // Check if input is not in list_nums
            // find(start of range, end of range, variable to be found)
            // If found return variable, else return end of range
            // Our parameters are our gobals declared at the header
            if (find(list_nums.begin(), list_nums.end(), col_num) == list_nums.end()) 
            {
                cout << "Invalid seat number. Please try again." << endl;
                continue;
            }


            pair<string, string> seat_n = make_pair(row_alpha, col_num);
            // return_seats returns our seat vector
            if (find(return_seats(date, time).begin(), return_seats(date, time).end(), seat_n) != return_seats(date, time).end()) 
            {
                // checks for booked seat using find function
                cout << "Seat already booked. Please choose another seat." << endl;
            }
            else 
            {
                return_seats(date, time).push_back(seat_n); // append seat_n into seat vector
                cout << "\nSeat booked successfully!\n";
                show_seats(return_seats(date, time));
                return seat_n;
            }
        }
    }

    // Main booking function
    tuple<string, string, pair<string, string>, string> booking(string date, string time, int ticket_amt) 
    {
        // we check if date and time are empty, this is for booking multiple tickets
        // if false we enter date and time, if true we skip 
        // So users don't have to enter date and time multiple times
        if (date.empty() && time.empty()) 
        {
            date = in_date();
            time = in_time();
        }

        // check if the hall is full by checking len of seat vector, hard coded limit 100
        if ((return_seats(date, time).size() + ticket_amt) >= 100) 
        {
            cout << "Sorry, all seats are booked. Please try another date and time." << endl;
            return make_tuple("", "", make_pair("", ""), "");
        }

        vector<pair<string, string>>& seats = return_seats(date, time);
        show_seats(seats);
        pair<string, string> seat_n = in_seats(date, time);
        return make_tuple(date, time, seat_n, name);
    }
};

class movie_class
{
   public:
      const double cost_adult = 22.50;
      const double cost_kid = 13.50;
      const double cost_senior = 10.50;

      //Format: Code || Name || Duration || Category
      string mv_list[10][4] = {
         {"ANM2401","The Godfather","2 Hours","Drama"},
         {"APL1324","Titanic","2 Hours","Romance"},
         {"BTJ2426","Inception","1 Hours","Sci-Fi"},
         {"DNT2402","The Dark Knight","2 Hours","Action"},
         {"EOT2410","Parasite","2 Hours","Drama"},
         {"UGL2413","Forrest Gump","2 Hours","Romance"},
         {"TRF2414","Avengers: Endgame","3 Hours","Action"},
         {"DHI9792","The Exorcist","2 Hours","Horror"},
         {"MGL2427","A Nightmare on Elm Street","2 Hours","Horror"},
         {"GOF2416","Hereditary","2 hrs","Drama"}
      };

         int adult_tksold[10] = {10,20,30,40,40,30,20,10,20,30};
         int kid_tksold[10] = {40,30,20,10,10,20,30,40,40,30};
         int senior_tksold[10] = {20,30,40,30,20,10,20,30,40,40};
         double revenue[10] = {0,0,0,0,0,0,0,0,0,0};

         double grandtotal = 0.0;
};

#endif
