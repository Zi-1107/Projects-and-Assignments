#ifndef LOGIN_CLASS_H
#define LOGIN_CLASS_H

#include "header.h"

class admin_class
{
    public:
        string username = "";
        string userpass = "";
        int ad_choice = 0;
        const string realname = "admin";
        const string realpass = "pass";
};

class cust_class
{
   public:
        const string cust_memID[3][2] = {
                {"012345678901","Laurence"},
                {"456789098768","Daryl"},
                {"987654321098","Cindy"}
        };
        bool cust_mem_log = 0; //For After Member Discount Usage

        string record[1][5] = {
               {"Movie","Date","Time","Category","Seat"}
        };
};

#endif
