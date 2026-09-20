/*Library*/
#include "header.h"
#include "login_class.h"

/*Customer Login*/
void cust_member(cust_class& cust)
{
    //Local Variables
    char owned = ' ';
    string memID = "";
    bool flag = 0;

    //Check whether the input is valid
    while (isspace(owned) || isdigit(owned))
    {
        cout << "\nDo you have a membership ID? (Y/N): ";
        cin.get(owned);
        cin.ignore(100, '\n');
    }

    while (flag == 0)
    {
        //When the customer is membership
        if (tolower(owned) == 'y')
        {
            cout << "Enter your membership ID: ";
            getline(cin, memID);

            if (memID.empty())
            {
                cout << "Invalid Input. Please re-enter again." << endl;
            }
            else
            {
                flag = 1;
            }
            
        }
        //When customer not a membership
        else if (tolower(owned) == 'n')
        {
            cout << "Alright! Proceed to Customer Menu." << endl;
            break;
        }
        else
        {
            cout << "Invalid Input. Please re-enter again." << endl;
        }
    }

    if (flag == 1)
    {
        for (int i = 0; i < 3; i++)
        {
            if (memID == cust.cust_memID[i][0])
            {
                cust.cust_mem_log = 1;
                cout << "\nWelcome, " << cust.cust_memID[i][1] << "!" << endl;
                break;
            }
        }
    }

}

/*Admin Login*/
void admin_login(admin_class& admin)
{
    //Local Variables
    string inputname = "";
    string inputpass = "";
    bool success = 0;
    int log_count = 0; //For counting tried purpose

    while (inputname.empty() || inputpass.empty() || success == 0)
    {

        cout << "\nEnter Your Username: ";
        getline(cin, inputname);
        cout << "Enter Your PIN number: ";
        getline(cin, inputpass);

        //Check if input is empty
        if (inputname.empty() || inputpass.empty())
        {
            cout << "Please enter your username and password." << endl;
            log_count++;
        }
        else
        {
            //Check if name and password from user is correct
            if (inputname == admin.realname && inputpass == admin.realpass)
            {
                success = 1;
                admin.username = inputname;
                admin.userpass = inputpass;
            }
            else
            {
                cout << "Incorrect username or password. Please try again." << endl;
                log_count++;
            }
        }

        //If tried more than 3 times, the system automatically pause for 20 seconds
        if (log_count == 3)
        {
            cout << "You have exceeded the maximum number of login attempts. Please try again after 20 seconds." << endl;

            for (int timer = 20; timer > 0; timer--)
            {
                this_thread::sleep_for(chrono::seconds(1));
                if (timer % 5 == 0)
                {
                    cout << "Remaining time: " << timer << "seconds" << endl;
                }
            }
            log_count = 0;
        }
    }
}

/*Admin Menu*/
void admin_menu(admin_class& admin)
{
    //local Variables
    char choice = ' ';
    bool skip = 0;

    cout << "\nAdministrator Menu" << endl;
    cout << setfill('*') << setw(50) << "\n";
    cout << "\n";
    cout << "1. Movie List" << endl;
    cout << "2. Sales Status" << endl;
    cout << "3. Modify Movie" << endl;
    cout << "0. Exit" << endl;

    while (skip == 0)
    {
        cout << "\nEnter Your Choice: ";
        cin.get(choice);
        cin.ignore(100, '\n');

        if (isspace(choice) || isalpha(choice))
        {
            cout << "Invalid choice. Please try again." << endl;
        }
        else if (isdigit(choice))
        {
            switch (choice) 
            {
            case '1':
                admin.ad_choice = 1;
                skip = 1;
                break;
            case '2':
                admin.ad_choice = 2;
                skip = 1;
                break;
            case '3':
                admin.ad_choice = 3;
                skip = 1;
                break;
            case '0':
                admin.ad_choice = 0;
                skip = 1;
                break;
            default:
                cout << "Invalid choice. Please try again." << endl;
                break;
            }
        }
    }
}
