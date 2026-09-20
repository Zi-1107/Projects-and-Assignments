#pragma once
#include "header.h"
#include "ticket_category.h"
#include "movie_class.h"
#include "login_class.h"

TicketInfo CompleteTicketBuyingProcess(cust_class& cust);
BookingInfo booking_main(Movie movie_list[10], int ticket_amount);
