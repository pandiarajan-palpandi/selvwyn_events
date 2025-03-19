# ============== SELWYN EVENT TICKETING SYSTEM ==============
# Student Name: Pandiarajan Palpandi
# Student ID : 1167810
# ================================================================
import re
from datetime import date,datetime,timedelta     # datetime module is required for working with dates

# Make the variables and function in set_data.py available in this code (without needing 'set_data.' prefix)
from set_data import customers,events,unique_id,display_formatted_row   

#Below are the collection keys to access event informaton
AGE_LIMIT = 'age_restriction'
EVENT_DATE = 'event_date'
CAPACITY = 'capacity'
TICKETS_SOLD = 'tickets_sold'
CUSTOMERS = 'customers'

# regex patterns
DATE_FORMAT = '%d/%m/%Y'
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def list_all_customers():
    """
    Lists customer details.
    This is an example of how to produce basic output."""
    format_str = "{: <5} {: <15} {: <15} {: <14} {: <20}"  
    print('----------------------------------------------------------------------------------------')          # Use the same format_str for column headers and rows to ensure consistent spacing. 
    display_formatted_row(["ID","First Name","Family Name","Birth Date","e-Mail"],format_str)
    print('----------------------------------------------------------------------------------------')
    # Use the display_formatted_row() function to display the column headers with consistent spacing
    for customer in customers:
        id = customer[0]
        fname = customer[1]
        famname = customer[2]
        birthdate = customer[3].strftime("%d %b %Y")
        email = customer[4]

        display_formatted_row([id,fname,famname,birthdate,email],format_str)     # Use the display_formatted_row() function to display each row with consistent spacing

def list_customers_and_tickets():
    """
    Lists Customer details (including birth date), and the events they have purchased tickets to attend."""
    format_str_1 = "{: <5} {: <15} {: <15} {: <14} {: <20}"  
    format_str_2 = "{: <30} {: <15} {: <15} {: <10}"
    print('\nCUSTOMER AND THIER BOOKING DETAILS')
   
    #sorting customers by family name and then first name using lambda function
    sorted_customers = sorted(customers, key = lambda x:(x[2], x[1]))
    
    for customer in sorted_customers:
        eventBooked = False
        id = customer[0]
        fname = customer[1]
        famname = customer[2]
        birthdate = customer[3].strftime("%d %b %Y")
        email = customer[4]
        print('---------------------------------------------------------------------------')
        display_formatted_row(["ID","First Name","Family Name","Birth Date","e-Mail"],format_str_1)
        print('---------------------------------------------------------------------------')
        display_formatted_row([id,fname,famname,birthdate,email],format_str_1)
        #get the event names
        event_name_list = list(events.keys())

        # sort the names alphanumerically
        event_name_list.sort()

        #access nested collection by event name as key (sorted)
       

        print('\n---------------------------------------------------------------------------------------')
        display_formatted_row(["Event Name","Age Restriction","Event Date","Tickets Bought"],format_str_2)
        print('---------------------------------------------------------------------------------------')
        for event_name in event_name_list:
            details = events[event_name]
            customer_and_tickets = details['customers']
            for ct in customer_and_tickets:
                if ct[0] == id:
                     eventBooked = True
                     display_formatted_row([event_name, details[AGE_LIMIT], details[EVENT_DATE].strftime("%d %b %Y"), ct[1]], format_str_2)
        if eventBooked == False:
            print('{: >50}'.format('NO EVENTS BOOKED'))
        print('---------------------------------------------------------------------------------------\n')

        
    input("\nPress Enter to continue.")

def list_event_details():
    """
    List the events, show all details except Customers who have purchased tickets."""

    event_name_list = []
    format_str = "{: <30} {: <15} {: <15} {: <10} {: <10}"
    print('---------------------------------------------------------------------------------------')
    display_formatted_row(["Event Name","Age Restriction","Event Date","Capacity","Tickets Sold"],format_str)     # Use the display_formatted_row() function to display the column headers with consistent spacing
    print('---------------------------------------------------------------------------------------')

    #get the event names
    event_name_list = list(events.keys())

    # sort the names alphanumerically
    event_name_list.sort()

    #access nested collection by event name as key (sorted)
    for event_name in event_name_list:
        details = events[event_name]
        display_formatted_row([event_name, details[AGE_LIMIT], details[EVENT_DATE].strftime("%d %b %Y"), details[CAPACITY], details[TICKETS_SOLD]], format_str)
    print('---------------------------------------------------------------------------------------')
    
    input("\nPress Enter to continue.")

def buy_tickets():
    """
    Choose a customer, then a future event, the purchase can only proceed if they meet the minimum age requirement and tickets are available """
    valid_id = False
    print('\nEXISTING CUSTOMER INFORMATION\n')
    list_all_customers()
    customers_ids = list(zip(*customers))[0]
    while valid_id == False:
        customer_id = input('\nPlease provide the customer\'s id that you are buying tickets for: ')
        try: 
            customers_ids.index(customer_id)
            valid_id = True
        except:
            print('Invalid input, Please try again!')
            valid_id = False






def add_new_customer():
    """
    Add a new customer to the customer list."""
    try:
        format_str = "{: <5} {: <15} {: <15} {: <14} {: <20}"  
        new_form = ""
        while new_form != 'X':
            print("==== New Customer Information Form ===")
            first_name = input('Please enter first name:\n').strip()
            while (first_name == ""):
                print('Invalid input. Please try again!')
                first_name = input('Please enter first name:\n').strip()

            family_name = input('Please enter family name:\n').strip()
            while (family_name == ""):
                print('Invalid input. Please try again!')
                family_name = input('Please enter family name:\n').strip()

            valid_date = False
            while valid_date == False:
                try:
                    date_of_birth = input('Please enter date of birth in DD-MM-YYYY format:\n').strip()
                    formated_date = datetime.strptime(date_of_birth, DATE_FORMAT)
                    valid_date = True
                except:
                    print('Invalid input. Please try again!')
                    valid_date = False



            valid_email = False
            while valid_email == False:
                email_address = input('Please enter email address:\n').strip()
                valid_email = re.match(EMAIL_PATTERN, email_address) is not None
                if valid_email != True:
                    print('Invalid input. Please try again!')


            new_customer = [unique_id(), first_name, family_name, date(formated_date.year, formated_date.month, formated_date.day), email_address]
            customers.append(new_customer)
            print('\n\n')
            display_formatted_row(["ID","First Name","Family Name","Birth Date","e-Mail"],format_str)
            display_formatted_row(new_customer, format_str)
            print('\nCustomer information added successfully!' )
            new_form = input("\nPress Enter to add more or press X to return to main menu: ").strip().upper()
            if (new_form != 'X' and new_form != '' ):
                print("\n*** Invalid response, please try again.")
    except:
        print('Unable to add customer now. Please try again later.')

    # REMOVE this line once you have some function code (a function must have one line of code, so this temporary line keeps Python happy so you can run the code)

def list_future_available_events():
    """
    List all future events that have tickets available
    """
    foundFutureEvent = False
    format_str = "{: <30} {: <15} {: <15} {: <10} {: <12} {: <10}"
    print('\nFUTURE EVENT DETAILS\n')
    print('---------------------------------------------------------------------------------------------------------')
    display_formatted_row(["Event Name","Age Restriction","Event Date","Capacity","Tickets Sold", "Avaiable Tickets"],format_str)     # Use the display_formatted_row() function to display the column headers with consistent spacing
    print('---------------------------------------------------------------------------------------------------------')
    #sorting the events by event_date 
    sorted_events = dict(sorted(events.items(), key=lambda event: event[1]['event_date'], reverse = True))
    for event_name, details in sorted_events.items():
        tickets_available = int(details[CAPACITY]) - int(details[TICKETS_SOLD])
        #Listing only future events if tickets available to buy
        if tickets_available > 0 and details[EVENT_DATE] > date.today():
            display_formatted_row([event_name, details[AGE_LIMIT], details[EVENT_DATE].strftime("%d %b %Y"), details[CAPACITY], details[TICKETS_SOLD], tickets_available], format_str)
            foundFutureEvent = True
    if foundFutureEvent == False:
        print('{: >70}'.format('NO FUTURE EVENTS WITH UNSOLD TICKETS FOUND'))
    print('---------------------------------------------------------------------------------------------------------')      
    input("\nPress Enter to continue.")

def disp_menu():
    """
    Displays the menu and current date.  No parameters required.
    """
    print("==== WELCOME TO SELWYN EVENT TICKETING SYSTEM ===")
    print(" 1 - List Customers")
    print(" 2 - List Customers and their Events")
    print(" 3 - List Event Details")
    print(" 4 - Buy Tickets")
    print(" 5 - Future Events with tickets")
    print(" 6 - Add New Customer")
    print(" X - eXit (stops the program)")

# ------------ This is the main program ------------------------

# Don't change the menu numbering or function names in this menu.
# Although you can add arguments to the function calls, if you wish.
# Repeat this loop until the user enters an "X" or "x"
response = ""
while response != "X":
    disp_menu()
    # Display menu for the first time, and ask for response
    response = input("Please enter menu choice: ").upper()
    if response == "1":
        list_all_customers()
    elif response == "2":
        list_customers_and_tickets()
    elif response == "3":
        list_event_details()
    elif response == "4":
        buy_tickets()
    elif response == "5":
        list_future_available_events()
    elif response == "6":
        add_new_customer()
    elif response != "X":
        print("\n*** Invalid response, please try again (enter 1-6 or X)")

    print("")

print("\n=== Thank you for using the SELWYN EVENT TICKET SYSTEM! ===\n")

