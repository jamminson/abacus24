from requests.auth import HTTPBasicAuth
import requests
import json
import csv
import pandas as pd
import numpy as np
from secret import *

def get_member_list():
    # saves all current members to abacus_members_list.json
    url = "https://eactivities.union.ic.ac.uk/API/CSP/203/reports/members?year=23-24"

    response = requests.get(url, auth=HTTPBasicAuth('', api_key))
    data = response.json()
    with open("abacus_members_list", "w") as json_file:
        json.dump(data, json_file, indent=4)
        print("Data has been written to abacus_members_list.json")

def check_member(fname, lname):
    with open("abacus_members_list") as json_file:
        data = json.load(json_file)
        for i in data:
            if (fname == i['FirstName']) and (lname == i['Surname']):
                return True
        
        return False
    
def export_emails():
     # prints all emails of full_members as newline separated string.
     s = ""
     with open("abacus_members_list") as json_file:
        data = json.load(json_file)
        for i in data:
            s += i['Email'] + '\n'

        print(s)

def products_per_year(year):
    start_year = year - 2000
    url_suffix = "{s_year}-{e_year}".format(s_year=start_year, e_year=start_year+1)
    url = "https://eactivities.union.ic.ac.uk/API/CSP/203/reports/products?year=" + url_suffix
    response = requests.get(url, auth=HTTPBasicAuth('', API_KEY))
    data = response.json()
    file_name = "products_{s_year}-{e_year}".format(s_year = start_year, e_year = start_year+1)
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)
        print("Data has been written to {fname}.json".format(fname=file_name))

def members_per_year(year):
    start_year = year - 2000
    url_suffix = "{s_year}-{e_year}".format(s_year=start_year, e_year=start_year+1)
    url = "https://eactivities.union.ic.ac.uk/API/CSP/203/reports/members?year=" + url_suffix
    response = requests.get(url, auth=HTTPBasicAuth('', API_KEY))
    data = response.json()
    print("Number Members: {}\n".format(len(data)))
    file_name = "members_{s_year}-{e_year}.csv".format(s_year = start_year, e_year = start_year+1)
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    # with open(file_name, "w") as json_file:
    #     json.dump(data, json_file, indent=4)
    #     print("Data has been written to {fname}.json".format(fname=file_name))


def get_online_sales(year):
    # Calculates membership income from given year.
    # Assumes only product is the membership income of 5 pounds
    MEMBERSHIP_PRICE = 5
    start_year = year - 2000
    url_suffix = "{s_year}-{e_year}".format(s_year=start_year, e_year=start_year+1)
    url = "https://eactivities.union.ic.ac.uk/API/CSP/203/reports/onlinesales?year=" + url_suffix

    response = requests.get(url, auth=HTTPBasicAuth('', api_key))
    data = response.json()
    file_name = "online_sales_{s_year}-{e_year}".format(s_year = start_year, e_year = start_year+1)
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)
        print("Data has been written to {fname}.json".format(fname=file_name))
    # with open("online_sales_list", "w") as json_file:
    #     json.dump(data, json_file, indent=4)
    #     print("Data has been written to online_sales_list.json")
    # print(len(data))
    # print("£" + str(len(data) * MEMBERSHIP_PRICE))
MEMBERSHIP_FEE = 5
def print_membership_income_range(start_year, end_year):
    current = start_year - 2000
    for current in range(start_year, end_year):
        sales_fname = "online_sales_{s_year}-{e_year}".format(s_year = current - 2000, e_year = current - 1999)
        members_fname = "members_{s_year}-{e_year}".format(s_year = current - 2000, e_year = current - 1999)
        if current >= 2020:
            with open(sales_fname, 'r') as event_list:
                income_data = json.load(event_list)
        
        with open(members_fname, 'r') as member_list:
            member_data = json.load(member_list)

        if current >= 2020:
            num_sales = len(income_data)
        else:
            num_sales = "NA"
        
        num_members = len(member_data)
        print("\n")
        print("---------------")
        print("Membership income data for: {s_year}-{e_year}\n".format(s_year=current, e_year = current+1))
        print("Num Members:\t{num_members}".format(num_members=num_members))
        print("Num online sales:\t{num_sales}\n".format(num_sales = num_sales))
        print("Total Membership income:\t{membership_income}\n".format(membership_income =num_members* MEMBERSHIP_FEE))


def extract_event_payments():
    csv_file_path = 'example.csv'
    json_file_path = 'example_event_list.json'
    cols = ['Date', 'Time', 'Name', 'Amount', 'Description']

    data = []
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            filtered_row = {key: row[key] for key in cols if key in row}
            data.append(filtered_row)

    with open(json_file_path, mode='w') as json_file:
        json.dump(data, json_file, indent=4)





def check_payment():
    MEMBER_EVENT_FEE = 20.00
    NON_MEMBER_EVENT_FEE = 25.00
    EVENT_NAME = 'tenten'
    correct_payment = 'correct.csv'
    incorrect_payment = 'incorrect.csv'

    member_list_path = 'abacus_members_list'
    event_list_path = 'example_event_list'
    with open(event_list_path, 'r') as event_list:
        event_list_data = json.load(event_list)
    
    with open(member_list_path, 'r') as member_list:
        member_data = json.load(member_list)

    correctly_paid = []
    incorrectly_paid = []
    
    for i in event_list_data:
        ref = i['Description']
        ref = str(ref)
        # sanitisation of ref should be here.
        print(ref)
        ref = ref.split()
        event_name = ref[0].lower()

        event_name_check = event_name == EVENT_NAME
        
        member_name_check = False
        empty_short_code = False
        if len(ref) >= 2:
            member_login = ref[1].lower()
            for member in member_data:
                if member_login == member['Login']:
                    member_name_check = True
        
        else:
            empty_short_code = True
        
        member_fee_paid_correct = member_name_check and (float(i['Amount']) == MEMBER_EVENT_FEE)
        non_member_fee_paid_correct = not(member_name_check) and (float(i['Amount']) == NON_MEMBER_EVENT_FEE)
        correct_amount_check = member_fee_paid_correct or non_member_fee_paid_correct



        if correct_amount_check and event_name_check and not(empty_short_code):
            correctly_paid.append({
                "name": i['Name'],
                "member": member_name_check,
                "amount": i['Amount'],
            })
        else:
            incorrectly_paid.append({
                "name": i['Name'],
                "member": member_name_check,
                "amount": i['Amount'],
            })

        # Open the CSV file in write mode
        with open(correct_payment, mode='w', newline='') as csv_file:
            if len(correctly_paid) > 0:
                # Get the column names from the first dictionary
                fieldnames = correctly_paid[0].keys()
                
                # Create a DictWriter object
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                # Write the header (column names)
                writer.writeheader()
                
                # Write the data rows
                writer.writerows(correctly_paid)

        
        with open(incorrect_payment, mode='w', newline='') as csv_file:
            # Get the column names from the first dictionary
            if len(incorrectly_paid) > 0:
                fieldnames = incorrectly_paid[0].keys()
                
                # Create a DictWriter object
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                # Write the header (column names)
                writer.writeheader()
                
                # Write the data rows
                writer.writerows(incorrectly_paid)

        # check reference. could make the second one be CID / imperial email.
        # check if in member_list using name or description CID
        # check whether the right amount has been paid
        # print to correctly paid list, print to incorrectly paid list. 


def filter_for_fresher():
    fresher_csv = "1010_fresher.csv"
    non_fresher_csv = "1010_non_fresher.csv"
    signups = '1010 - fulllist_cleaned.csv'

    freshers = []
    non_freshers = []
    
    with open(signups, 'r') as everyone:
        csv_reader = csv.DictReader(everyone)
        data = list(csv_reader)

        for row in data:
            raw_sortcode = row['Imperial shortcode\n(i.e. the bit that comes before the @ on your ic.ac.uk email)']
            #process
            sortcode = raw_sortcode.lower()
            year = sortcode[-2:]
            if year == "24":
                freshers.append(row)
            else:
                non_freshers.append(row)
            


    with open(fresher_csv, mode='w', newline='') as csv_file:
            if len(freshers) > 0:
                # Get the column names from the first dictionary
                fieldnames = freshers[0].keys()
                
                # Create a DictWriter object
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                # Write the header (column names)
                writer.writeheader()
                
                # Write the data rows
                writer.writerows(freshers)
    
    with open(non_fresher_csv, mode='w', newline='') as csv_file:
        if len(non_freshers) > 0:
            # Get the column names from the first dictionary
            fieldnames = freshers[0].keys()
            
            # Create a DictWriter object
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            # Write the header (column names)
            writer.writeheader()
            
            # Write the data rows
            writer.writerows(non_freshers)               

def calculate_ticket_number():
    input_sheet = "1010_fresher.csv"
    with open(input_sheet, 'r') as input_sheet:
        csv_reader = csv.DictReader(input_sheet)
        data = list(csv_reader)

        count = 0
        for row in data:
            count += int(row["No. standard tickets \n£15 (member)\n£20 (non-member)"])
            # count += int(row["No. VIP tickets\n£20 (member)\n£25 (non-member)"])
        
        print(count)

def write_csv_file(filename, data):
        with open(filename, mode='w', newline='') as csv_file:
            if len(data) > 0:
                # Get the column names from the first dictionary
                fieldnames = data[0].keys()
                
                # Create a DictWriter object
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                # Write the header (column names)
                writer.writeheader()
                
                # Write the data rows
                writer.writerows(data)    

def split_vip_standard_release():
    input_sheet = "1010 - second_release_fulllist.csv"
    vip_csv = "1010_vip.csv"
    standard_csv = "1010_standard.csv"
    TOTAL_VIP = 24
    vip = []
    standard = []
    with open(input_sheet, 'r') as input_sheet:
        csv_reader = csv.DictReader(input_sheet)
        data = list(csv_reader)
    
    for row in data:
        if TOTAL_VIP <= 0:
            # if run out of VIP
            standard.append(row)
        else:
            vip_ticket_no = int(row["No. VIP tickets\n£20 (member)\n£25 (non-member)"])
            if vip_ticket_no > 0:
                TOTAL_VIP -= vip_ticket_no
                if TOTAL_VIP < 0:
                    standard.append(row)
                vip.append(row)
            else:
                standard.append(row)
    
    write_csv_file(vip_csv, vip)
    write_csv_file(standard_csv, standard) 

def standard_release():
    input_sheet = "1010_standard_fulllist.csv"
    standard_csv = "1010_standard.csv"
    fail_csv = "1010_fail.csv"
    TOTAL_STANDARD = 150
    standard = []
    fail = []

    with open(input_sheet, 'r') as input_sheet:
        csv_reader = csv.DictReader(input_sheet)
        data = list(csv_reader)
    
    for row in data:
        if TOTAL_STANDARD <= 0:
            fail.append(row)
        else:
            standard_ticket_no = int(row["No. standard tickets \n£15 (member)\n£20 (non-member)"])
            if standard_ticket_no == 0:
                standard_ticket_no = int(row["No. VIP tickets\n£20 (member)\n£25 (non-member)"])
                row["No. standard tickets \n£15 (member)\n£20 (non-member)"] = standard_ticket_no 
                row["No. VIP tickets\n£20 (member)\n£25 (non-member)"] = 0
            TOTAL_STANDARD -= standard_ticket_no
            if TOTAL_STANDARD < 0:
                row["No. standard tickets \n£15 (member)\n£20 (non-member)"] = TOTAL_STANDARD + standard_ticket_no
            standard.append(row)
    
    write_csv_file(standard_csv, standard)
    write_csv_file(fail_csv, fail)
    # could write here for all people without tickets.


def calculate_payment_amounts():
    # get member status.
    # figure out correct payment amount

    with open("members_24-25.csv", 'r') as empty_payers:
        member_data = csv.load(empty_payers)
    
    member_sortcodes = [entry["Login"] for entry in member_data]

    input_sheet = "1010 - payers.csv"
    df = pd.read_csv(input_sheet)

    #clean payer sortcodes.
    df["Sortcode"] = df["Sortcode"].apply( lambda x: x.lower())
    df["Member_Status"] = df["Sortcode"].apply( lambda x: True if x in member_sortcodes else False )


    def calculate_payment(row):
        if row["Member_Status"]:
            STANDARD_TICKET = 15
            VIP_TICKET = 20
        else:
            STANDARD_TICKET = 20
            VIP_TICKET = 25

        return int(row["Standard"]) * STANDARD_TICKET + int(row["Vip"]) * VIP_TICKET

    df["Amount_Expected"] = df.apply(calculate_payment, axis=1)
    df.to_csv("payer_expected_amounts.csv", index=False)

def check_correctly_paid():
 
    event_payment_path = 'payer_expected_amounts.csv'
    bank_statement_path = '1010 - payments_cleaned_9_10.csv'

    event_payment_data = pd.read_csv(event_payment_path)
    bank_payment_data = pd.read_csv(bank_statement_path)

    # get sortcode row for bank payment data.
    bank_payment_data["Sortcode"] = bank_payment_data["Description"].apply(lambda x: x.split()[1].lower())

    sortcode_to_amount_paid = dict(zip(bank_payment_data["Sortcode"], bank_payment_data["Amount"]))
    event_payment_data["Amount_Paid"] = event_payment_data["Sortcode"].map(sortcode_to_amount_paid)
    event_payment_data["Amount_Paid"] = event_payment_data["Amount_Paid"].fillna("0")

    # bank_payment_data.drop(["Transaction ID", "Date", "Time", "Type", "Name", "Emoji", "Category", "Currency", "Local amount", "Local currency", "Notes and #tags", "Address", "Receipt", "Category split", "Money Out", "Money In"], axis=1)
    # bank_event_merged = pd.merge(bank_payment_data, event_payment_data, on="Sortcode")

    def correctly_paid(row):
        return row["Amount_Expected"] == row["Amount_Paid"]
    
    event_payment_data["Correctly_Paid"] = event_payment_data.apply(correctly_paid, axis=1)
    event_payment_data.to_csv("payments_checked_third.csv", index=False)

# members_per_year(2024)


def fresher_dinner():
    fresher_dinner_path = 'fresher_dinner_raw.csv'
    fresher_dinner_data = pd.read_csv(fresher_dinner_path)
    
    members = pd.read_csv("members_24-25.csv")
    members_sortcode = members[['Login']]

    dinner_signups = pd.DataFrame(columns=['Full Name', 'Shortcode', 'Is_Member', 'Amount_Expected', 'Amount_Paid', 'Correctly_Paid'])

    i = 0

    for row in fresher_dinner_data.itertuples():
        print("THis is i: {}".format(i))
        full_name = row[2]
        shortcode = row[3].lower()
        is_fresher = row[4] == "Year 1"
        
        print(is_fresher)
        is_member = bool(members_sortcode.isin([shortcode]).any())
        print(is_member)
        
        if is_fresher and is_member:
            amount_expected = 20
        elif is_fresher and not is_member:
            amount_expected = 25
        else:
            amount_expected = 30

        amount_paid = "NULL"
        correctly_paid = "NULL"
        dinner_signups.loc[i] = [full_name, shortcode, is_member, amount_expected, amount_paid, correctly_paid]
        i += 1
    
    dinner_signups.to_csv("dinner_signups_first_release.csv", index=False)

# Define a function to classify based on age and salary
def classify_ticket(row):
    if (row['IsMember'] == True) & (row['Ticket_Type'] == "1 Standard"):
        return 25.0
    elif (row['IsMember'] == True) & (row['Ticket_Type'] == "1 VIP"):
        return 35.0
    elif (row['IsMember'] == False) & (row['Ticket_Type'] == "1 Standard"):
        return 25.0
    else:
        return 35.0

def process_payments(event_code):
    payments = pd.read_csv("payments.csv")   
    payments = payments[['Name', 'Description', 'Money In']]
    payments[['Shortcode', 'Event']] = payments['Description'].str.split(' ', 1, expand=True)
    # print all payments to check for exceptions
    payments.to_csv("./{}_payments_all.csv".format(event_code), index=False)
    payments = payments[(payments['Event'] == event_code)]
    payments.to_csv("./{}_payments_processed.csv".format(event_code), index=False)

def process_members():
    members_per_year(2024)
    members = pd.read_csv("members_24-25.csv")
    members = members[['Login']]
    members['Shortcode'] = members['Login'].str.lower()
    members.to_csv("./members_processed.csv", index=False)


# GET TICKETS SENT: NAME, SHORTCODE, TICKET_TYPE
# GET payments.csv
# Check ticket type format in expected amount calculation
# Check prices 
# Check Event Code
def check_payments():
    # Predefined values
    EVENT_CODE = "CC"

    # MEMBERS
    process_members()
    members = pd.read_csv("members_processed.csv")

    # PAYMENTS
    process_payments(EVENT_CODE)
    payments = pd.read_csv("{}_payments_processed.csv".format(EVENT_CODE))

    # Get sent names and shortcodes
    sent = pd.read_csv("tickets_sent.csv")
    sent['Shortcode'] = sent['Shortcode'].str.lower()

    # Check for membership
    sent["IsMember"] = sent["Shortcode"].isin(members["Shortcode"])

    # Calculate Expcted Amount
    sent['Expected Amount'] = sent.apply(classify_ticket, axis=1)

    left_join_df = pd.merge(sent, payments, on='Shortcode', how='left')
    print(left_join_df.head())

    left_join_df = left_join_df.fillna("-")

    left_join_df.to_csv("./{}_payments.csv".format(EVENT_CODE), index=False)





    


    # payments = pd.read_csv("payments.csv")
    # payments = payments[['Name', 'Description', 'Money In']]
    # payments[['Shortcode', 'Event']] = payments['Description'].str.split(' ', 1, expand=True)
    # # payments.to_csv("./splitted_payments.csv", index=False)
    # payments = payments[(payments['Event'] == "CC")]
    # payments.to_csv("./splitted_payments.csv", index=False)

    # sent = pd.read_csv("tickets_sent.csv")
    # sent["IsMember"] = sent["Shortcode"].isin(members_sortcode["Login"])
    # sent.to_csv("./splitted_payments_member.csv", index=False)

    # sent['Expected_Amount'] = '20'
    # sent.loc[(sent['IsMember'].bool()) & (sent['TICKET TYPE'] == "Standard"), 'Expected_Amount'] = 20
    # sent.loc[(sent['IsMember'].bool()) & (sent['TICKET TYPE'] == "VIP"), 'Expected_Amount'] = 25
    # sent.loc[(not(sent['IsMember'].bool())) & (sent['TICKET TYPE'] == "Standard"), 'Expected_Amount'] = 25
    # sent.loc[(not(sent['IsMember'])) & (sent['TICKET TYPE']) == "VIP", 'Expected_Amount'] = 30




    


    

    


        

    # for i in payments:
    #     ref = i['Description']
    #     ref = str(ref)
    #     # sanitisation of ref should be here.
    #     print(ref)
    #     ref = ref.split()
    #     event_name = ref[0].lower()

    #     event_name_check = event_name == EVENT_NAME
        
    #     member_name_check = False
    #     empty_short_code = False
    #     if len(ref) >= 2:
    #         member_login = ref[1].lower()
    #         for member in member_data:
    #             if member_login == member['Login']:
    #                 member_name_check = True
        
    #     else:
    #         empty_short_code = True
        
    #     member_fee_paid_correct = member_name_check and (float(i['Amount']) == MEMBER_EVENT_FEE)
    #     non_member_fee_paid_correct = not(member_name_check) and (float(i['Amount']) == NON_MEMBER_EVENT_FEE)
    #     correct_amount_check = member_fee_paid_correct or non_member_fee_paid_correct
    



check_payments()
# fresher_dinner()


# Need to check membership plus year. Calculate the expected payment amount. 
# Need to check bank statement for calculate amount paid.





            
            



# calculate_membership_income(2023)
# products_per_year(2018)
# products_per_year(2017)
# get_online_sales(2020)
# get_online_sales(2019)
# get_online_sales(2018)
# get_online_sales(2017)
# calculate_membership_income(2023)
# calculate_membership_income(2022)
# calculate_membership_income(2021)
# print_membership_income_range(2016, 2024)
# members_per_year(2019)
# members_per_year(2018)
# members_per_year(2017)
# members_per_year(2016)
# members_per_year(2023)
# filter_for_fresher()
# calculate_ticket_number()
