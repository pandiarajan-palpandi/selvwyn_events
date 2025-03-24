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

#properties for collecting user inputs - hence making the values globally accessible
user_inputs = {
    'customer_id': 0,
    'first_name':'',
    'family_name': '',
    'dob': date.today(),
    'email': '',
    'event_name': '',
    'tickets_to_buy': 0,
    'option': '1',
    'tickets_to_buy': 0,
}


def list_all_customers():
    """
    Lists customer details.
    This is an example of how to produce basic output."""
    format_str = "{: <5} {: <15} {: <15} {: <14} {: <20}"  
    print('\nEXISTING CUSTOMER INFORMATION\n')
    print('----------------------------------------------------------------------------------------')          
    display_formatted_row(["ID","First Name","Family Name","Birth Date","e-Mail"],format_str)
    print('----------------------------------------------------------------------------------------')

    if len(customers) == 0:
        print('{: >50}'.format('NO CUSTOMER INFORMATION FOUND'))
        print('----------------------------------------------------------------------------------------\n')
    else:
        try:
            for customer in customers:
                id = customer[0]
                fname = customer[1]
                famname = customer[2]
                birthdate = customer[3].strftime("%d %b %Y")
                email = customer[4]
                display_formatted_row([id,fname,famname,birthdate,email],format_str)
        except:
            print('\n Exception occured! Please try again later.')

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

def list_event_details():
    """
    List the events, show all details except Customers who have purchased tickets."""

    event_name_list = []
    format_str = "{: <30} {: <15} {: <15} {: <10} {: <10}"
    print('\nEVENT DETAILS')
    print('---------------------------------------------------------------------------------------')
    display_formatted_row(["Event Name","Age Restriction","Event Date","Capacity","Tickets Sold"],format_str)
    print('---------------------------------------------------------------------------------------')

    if len(events) > 0:
        #get the event names
        event_name_list = list(events.keys())

        # sort the names alphanumerically
        event_name_list.sort()

        #access nested collection by event name as key (sorted)
        for event_name in event_name_list:
            details = events[event_name]
            display_formatted_row([event_name, details[AGE_LIMIT], details[EVENT_DATE].strftime("%d %b %Y"), details[CAPACITY], details[TICKETS_SOLD]], format_str)
        print('---------------------------------------------------------------------------------------')
    else:
        print('{: >50}'.format('NO EVENTS DATA FOUND'))
        print('---------------------------------------------------------------------------------------')
        

def buy_tickets():
    """
    Choose a customer, then a future event, the purchase can only proceed if they meet the minimum age requirement and tickets are available """
    #Below line will initiate the loop every time the function being called thus forcing the user to provide option to retry /exit function
    user_inputs["option"] = '1'
    while user_inputs["option"] == '1':
        try:
            if check_future_event_availability():
                get_customer_id()
                get_event_name()
                get_tickets_to_buy()
                book_ticket_for_customer()
                #Below conditon will check if the code is fall through or the user opted to exit the function (option - 2)
                if user_inputs["option"] == '1':
                    reset_user_inputs()
                    get_options()
                else:
                    break
            else:
                print('\nNo future events with unsold tickets found!')
                break
        except:
            print('\nException occured! Please try again later.')
            break
    #This should reset input fields before exiting the function
    reset_user_inputs()


def add_new_customer():
    """
    Add a new customer to the customer list."""
    #Below line will initiate the loop every time the function being called thus forcing the user to provide option to retry /exit function
    user_inputs["option"] = '1'
    while user_inputs["option"] == '1':
        try:
            print('\nNEW CUSTOMER FORM')
            get_first_name()
            get_family_name()
            get_dob()
            get_email()
            save_customer()
            #Below conditon will check if the code is fall through or the user opted to exit the function (option - 2)
            if user_inputs["option"] == '1':
                reset_user_inputs()
                get_options()
            else:
                break
        except:
            print('\nException occured! Please try again later.')
            break
    #This should reset input fields before exiting the function
    reset_user_inputs()

def check_future_event_availability():
    foundFutureEvent = False
    sorted_events = dict(sorted(events.items(), key=lambda event: event[1]['event_date'], reverse = True))
    for details in sorted_events.values():
        tickets_available = int(details[CAPACITY]) - int(details[TICKETS_SOLD])
        if tickets_available > 0 and details[EVENT_DATE] > date.today():
            foundFutureEvent = True
            break
    return foundFutureEvent

def list_future_available_events():
    """
    List all future events that have tickets available
    """
    foundFutureEvent = False
    format_str = "{: <30} {: <15} {: <15} {: <10} {: <12} {: <10}"
    print('\nFUTURE EVENT DETAILS')
    print('---------------------------------------------------------------------------------------------------------')
    display_formatted_row(["Event Name","Age Restriction","Event Date","Capacity","Tickets Sold", "Avaiable Tickets"],format_str)
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
    return foundFutureEvent     

def event_exists():
    return events.get(user_inputs["event_name"]) != None

def is_customer_allowed():
    allowed = False
    try:
        #Below line will gather all ids from the customers list from 0 index position and creates a list
        customers_ids = list(zip(*customers))[0]
        customer = customers[customers_ids.index(int(user_inputs["customer_id"]))]
        birth = customer[3]
        event_age_limit = events[user_inputs["event_name"]][AGE_LIMIT]
        if event_age_limit <= 0:
            allowed = True
            return allowed
        today = date.today()
        olderThan = date(today.year - event_age_limit, today.month, today.day)
        if birth >=  olderThan:
            allowed = False
        return allowed
    except:
        print('\nException Occured! Validation Failed.')
        return allowed

def get_options():
    selected = False
    while selected == False:
        options = ['1','2']
        print("\n==== SELECT OPTIONS FROM BELOW ===")
        # Try again option is for both repeating last action and repeat last function
        print(" 1 - Try Again")
        # Below will get the user out of current operation and show main menu
        print(" 2 - Return to Main Menu")
        selection =  input("\nPlease enter menu choice: ").strip().upper()
        if options.count(selection) > 0:
            user_inputs["option"] = selection
            selected = True
            break
        else:
            selected = False
            print('\nInvalid Selection! PLease provde valid option from the list.')

def exit_operation():
    user_inputs["option"] = ''
    reset_user_inputs()

def reset_option():
    user_inputs["option"] == '1'

def reset_user_inputs():
    user_inputs["customer_id"] = 0
    user_inputs["first_name"] = ''
    user_inputs["family_name"] = ''
    user_inputs["dob"] = date.today()
    user_inputs["email"] = ''
    user_inputs["event_name"] = ''
    user_inputs["option"] = ''
    user_inputs["tickets_to_buy"] = 0

def get_first_name():
    while user_inputs["option"] == '1':
        first_name = input('\nPlease enter first name: ').strip()
        if first_name != '':
            user_inputs["first_name"] = first_name
            reset_option()
            break
        else:
            print('\nFirst name can not be empty! Please provide a valid first name.')
            get_options()

def get_family_name():
    while user_inputs["option"] == '1':
        family_name = input('\nPlease enter family name: ').strip()
        if family_name != '':
            user_inputs["family_name"] = family_name
            reset_option()
            break
        else:
            print('\nFamily name can not be empty! Please provide a valid family name.')
            get_options()

def get_email():
    while user_inputs["option"] == '1':
        email = input('\nPlease enter email address: ').strip()
        if email != '':
            if re.match(EMAIL_PATTERN, email) is not None:
                user_inputs["email"] = email
                reset_option()
                break
            else:
                print('\nInvalid email format! Please provide a valid email address.')
                get_options()
        else:
            print('\nEmail address can not be empty! Please provide a valid email address.')
            get_options()

def get_dob():
    while user_inputs["option"] == '1':
        dob = input('\nPlease enter date of birth in (dd/mm/yyyy) format. Example 24/01/2025: ').strip()
        if dob != '':
            try:
                today = datetime.today()
                formated_date = datetime.strptime(dob, DATE_FORMAT)
                if formated_date < today:
                    if get_age(formated_date) < 110:
                        user_inputs["dob"] = date(formated_date.year, formated_date.month, formated_date.day)                        
                        break
                    else:
                        print('\nInvalid age! Customer age can not exceed 110. Please enter valid date of birth.')
                        get_options()
                else:
                    print('\nInvalid date! Date is in future. Please enter a valid date of birth')
                    get_options()
            except:
                print('\n Invalid date format! Please enter date in dd/mm/yyyy format. Example 24/01/2025')
                get_options()
        else:
            print('\nBirth date can not be empty! Please provide a valid date.')
            get_options()

def get_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age

def save_customer():
    if user_inputs["option"] == '1':
        format_str = "{: <5} {: <15} {: <15} {: <14} {: <20}"  
        new_customer = [int(unique_id()), user_inputs["first_name"], user_inputs["family_name"], user_inputs["dob"], user_inputs["email"]]
        customers.append(new_customer)
        print('\n----------------------------------------------------------------------------------------')   
        display_formatted_row(["ID","First Name","Family Name","Birth Date","e-Mail"],format_str)
        print('\n----------------------------------------------------------------------------------------')   
        display_formatted_row(new_customer.copy(), format_str)
        print('----------------------------------------------------------------------------------------')   
        print('\nCustomer information added successfully!' )
    

def get_customer_id():
    while user_inputs["option"] == '1':
        list_all_customers()
        customers_ids = list(zip(*customers))[0]
        customer_id = input('\nPlease provide the customer\'s id that you are buying tickets for: ').strip()
        if customer_id.isnumeric():
            customer_id_num = int(customer_id)
            if customers_ids.count(customer_id_num) > 0:
                user_inputs["customer_id"] = customer_id_num
                reset_option()
                break
            else:
                print('\nCutomer not found! Please provide a valid ID number.')
                get_options()
        else:
            print('\nInvalid Input! Please provide a valid ID number.')
            get_options()
        

def get_event_name():
    while user_inputs["option"] == '1':
        event_exists = list_future_available_events()
        if event_exists == True:
            user_inputs["event_name"] = input('\nPlease enter the event name to buy ticket: ').strip()
            if event_exists:
                if is_customer_allowed():
                    break
                else:
                    print('\nCustomer does not meet the age criteria! Hence can not book the event.')
                    get_options()
            else:
                print('\nEvent not found! Please provide a valid event name.')
                get_options()
        else:
            print('\nNo future events found! Exiting ticket booking... ')
            exit_operation()
            break



def get_tickets_to_buy():
    while user_inputs["option"] == '1':
        tickets_to_buy = input(f'\nPlease enter the number of ticket to buy (Available Tickets - {events[user_inputs["event_name"]][CAPACITY] - events[user_inputs["event_name"]][TICKETS_SOLD]}): ').strip()
        if tickets_to_buy.isnumeric():
            user_inputs["tickets_to_buy"] = int(tickets_to_buy)
            if int(events[user_inputs["event_name"]][CAPACITY]) - int(events[user_inputs["event_name"]][TICKETS_SOLD]) >= user_inputs["tickets_to_buy"]:
                break
            else:
                print('\nTickets Unavailable! Please provide a valid ticket count.')
                get_options()
        else:
            print('\nInvalid Number! Please provide a valid number.')
            get_options()


def book_ticket_for_customer():
    if user_inputs["option"] == '1':
        extra_ticket = False
        details = events[user_inputs["event_name"]]
        customer_and_tickets = details['customers']
        if len(customer_and_tickets) == 0:
            update_customer_booking(customer_and_tickets, user_inputs["tickets_to_buy"])
            return None
        for ct in customer_and_tickets:
            if ct[0] == user_inputs["customer_id"]:
                #existing customer ticket found and hence increasing the ticket count by one
                total_tickets_bought = int(ct[1]) +  user_inputs["tickets_to_buy"]
                customer_and_tickets.remove(ct)
                update_customer_booking(customer_and_tickets, total_tickets_bought)
                extra_ticket = True
                break
        if extra_ticket == False:
            # No existing tickets found for the customer and hence appending new set
            update_customer_booking(customer_and_tickets, user_inputs["tickets_to_buy"])
        print('\nTickets booked successfully!')

def update_customer_booking(customer_and_tickets, updated_count):
    customer_and_tickets.append((user_inputs["customer_id"], updated_count))
    events[user_inputs["event_name"]]['tickets_sold'] = events[user_inputs["event_name"]]['tickets_sold'] +  user_inputs["tickets_to_buy"]



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

