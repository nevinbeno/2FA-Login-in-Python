GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PINK='\033[1;35m'
YELLOW='\033[0;33m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
ORANGE='\033[38;5;214m'
No_Color='\033[0m'

import hashlib
import bcrypt
import sqlite3
import pyotp
import qrcode
from qrcode.console_scripts import main
import re
import datetime
import time
from typing import Optional
import sys

connection_to_main_database = sqlite3.connect("main_database.db")
cursor_main = connection_to_main_database.cursor()
cursor_main.execute("""
            CREATE TABLE IF NOT EXISTS main_table (
                       Sl_no INTEGER PRIMARY KEY, 
                       Username VARCHAR(255) NOT NULL, 
                       Mobile_Number VARCHAR(10) NOT NULL, 
                       Password VARCHAR(255) NOT NULL)
                """)
connection_to_main_database.commit()
connection_to_main_database.close()

connection_to_key = sqlite3.connect("keys.db")
cursor_key = connection_to_key.cursor()
cursor_key.execute("""
            CREATE TABLE IF NOT EXISTS key_table (
                        Sl_no INTEGER PRIMARY KEY, 
                        Mobile_Number VARCHAR(255) NOT NULL, 
                        Key VARCHAR(255) NOT NULL)
                 """)
connection_to_key.commit()
connection_to_key.close()

connection_to_tracker = sqlite3.connect("login_tracker.db")
cursor_tracker = connection_to_tracker.cursor()
cursor_tracker.execute("""
            CREATE TABLE IF NOT EXISTS tracker (
                    Sl_no INTEGER PRIMARY KEY, 
                    Username VARCHAR(255) NOT NULL,
                    Login_Date VARCHAR(15) NOT NULL,
                    Login_Time VARCHAR(255) NOT NULL,
                    Day VARCHAR(10) NOT NULL,
                    Login_Status VARCHAR(10) NOT NULL,
                    Description VARCHAR(255) NOT NULL
                    )
                 """)
connection_to_tracker.commit()
connection_to_tracker.close()


class Register:
    """This class will save the name, and other details of a new login user."""
    def __init__(self, name : str, mobile_number : str, password : str) -> None:
        self.name = name
        self.mobile_number = mobile_number
        self.secured_mobile_number = self._hash_mobile_number(mobile_number)
        self.password = self._hash_password(password)
        self.key = pyotp.random_base32()

    def _hash_password(self : object, password : str) -> str:
        """This function will hash the password using bcrypt method"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def _hash_mobile_number(self : object, mobile_number : str) -> str:
        """This function hashes using the sha256 method"""
        return hashlib.sha256(mobile_number.encode()).hexdigest()

class Current_Date_and_Time:
    """A class for setting the date and time details, one of the core class in the program, to avoid confusions and redundencies
        Automatically gets the current time, as when needed.
    """
    def __init__(self)-> None:
        current_date = datetime.date.today()
        self.date = current_date.strftime("%Y-%m-%d")
        current_time = datetime.datetime.now()
        self.time = current_time.strftime("%I:%M:%S  %p")
        self.day = current_date.strftime("%A")

def hide_cursor() -> None:
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor() -> None:
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def animation_spin_wheel() -> None:
    hide_cursor()
    list_symbol = ['_', '\\', '|', '/', '.']
    for _ in range(3):
        for i in list_symbol:
            print(f"{YELLOW + i + No_Color}" + "\r", end="")
            time.sleep(0.05)

def animation_dot() -> None:
    hide_cursor()
    list_symbol = ['   ', '.  ', '.. ', '...']
    for _ in range(3):
        for i in list_symbol:
            print(f"{YELLOW}Loading {i + No_Color}\r", end="")
            time.sleep(0.10)
    show_cursor()

def countdown() -> None:
    limit = 30
    for i in range (limit,0,-1):
        print(f"Please retry in " + f"{YELLOW + str(i) + No_Color}" + " seconds \r", end="")
        time.sleep(1)
    print(f"{PINK}Session expired !{No_Color}                                          ")

def fail() -> None:
    print(f"{YELLOW}Initializing..{No_Color}\r", end="")
    time.sleep(0.5)
    print(f"{YELLOW}Processing your Request..{No_Color}\r", end="")
    time.sleep(0.40)
    print(f"{YELLOW}Authenticating Credentials..{No_Color}\r", end="")
    time.sleep(0.50)
    print(f"{YELLOW}Verifying TOTP..                 {No_Color}\r", end="")
    time.sleep(1)
    print(f"{YELLOW}Potential TOTP mis - match detected              {No_Color}\r", end="")
    time.sleep(1)

def success() -> None:
    print(f"{YELLOW}Initializing..{No_Color}\r", end="")
    time.sleep(1)
    print(f"{YELLOW}Processing your Request..{No_Color}\r", end="")
    time.sleep(0.50)
    print(f"{YELLOW}Authenticating Credentials..{No_Color}\r", end="")
    time.sleep(0.30)
    print(f"{YELLOW}Verifying Account Details..   {No_Color}\r", end="")
    time.sleep(0.40)
    print(f"{YELLOW}Encrypting Data..              {No_Color}\r", end="")
    time.sleep(0.20)
    print(f"{YELLOW}Contacting the server..{No_Color}\r", end="")
    time.sleep(0.30)
    print(f"{YELLOW}Syncing..                   {No_Color}\r", end="")
    time.sleep(0.47)
    print(f"{YELLOW}Validating the connection..{No_Color}\r", end="")
    time.sleep(0.30)
    print(f"{YELLOW}Securing..                      {No_Color}\r", end="")
    time.sleep(0.20)
    print(f"{YELLOW}Finalizing..{No_Color}\r", end="")
    time.sleep(0.40)
    print(f"{YELLOW}Executing..                   {No_Color}\r", end="")
    time.sleep(1.25)

def get_username(mobile_number : str) -> str:
    """To get the username, as it is not a global variable, and needs at multiple places, hence to avoid redundency"""
    connection_to_main_database = sqlite3.connect("main_database.db")
    cursor_main = connection_to_main_database.cursor()
    query_for_name = "SELECT Username FROM main_table WHERE Mobile_Number = ?"
    cursor_main.execute(query_for_name, (mobile_number, ))
    username = cursor_main.fetchone()
    connection_to_main_database.close()
    return username[0]

def login_permission() -> bool:
    """Asks for login permission for the sers who already have an account."""
    user_login_permission = input(f"Would you like to login ({GREEN}Yes{No_Color} / {RED}No{No_Color}) :")
    if (user_login_permission.lower() == "yes"):
        return True
    else:
        return False

def display_and_enquire() -> str:
    """Displays the various states, and enquires user about their account
        The user_answer.lower() will turn the user entered text to lower case, 
        so that the check in the other functions become case insensitive
    """
    print(f"=============================================================\n")
    print(f"{'Sl_no':>20}{'Desription':>20}{'Please enter':>20}\n")
    print(f"{1:>20}{WHITE + '  Yes, I have one' + No_Color:>34}{GREEN + 'Yes' + No_Color:>23}")
    print(f"{2:>20}{WHITE + '  No, I don\'t' + No_Color:>31}{RED + 'No' + No_Color:>25}")
    print(f"{3:>20}{WHITE + '  I don\'t remember' + No_Color:>34}{BLUE + 'Help' + No_Color:>24}")
    user_answer = input(f"\nDo you have an account ? ({GREEN}Yes{No_Color} / {RED}No{No_Color} / {BLUE}Help{No_Color}) : ")
    return user_answer.lower()

def validate_name(name : str) -> bool:
    """Name validation. Prevents invalid names, like the ones containing digits, or white spaces"""
    if (re.fullmatch(r"^[A-Za-z]+\.? ?( [A-Z]\.)*( [A-Za-z]+)*$", name)):
        return True
    else:
        return False

def validate_phone(mobile_number : str) -> bool:
    """Regex implementation..Check if mobile number is 10 digits and starts with 6-9. If yes, returns True, else False"""
    if(re.fullmatch(r"^[6-9][0-9]{9}$", mobile_number)):
        return True
    else:
        return False
    
def validate_password(password : str) -> bool:
    """A basic password validation, just to ensure that the field is not empty"""
    if re.fullmatch(r"^\S+$", password):
        return True
    else:
        return False

def check_if_registered(mobile_number : str) -> bool:
    """Checks whether the mobile number is had already been registered, or not, hence, preventing any missue."""
    connection_to_main_database = sqlite3.connect("main_database.db")
    cursor_main = connection_to_main_database.cursor()
    query = "SELECT * FROM main_table WHERE Mobile_Number = ?"
    cursor_main.execute(query, (mobile_number,)) # mobile_number be passed as a tuple
    result = cursor_main.fetchone()
    connection_to_main_database.close()
    if result == None:
        return False
    else:
        return True

def get_mobile_number() -> tuple[str, bool]:
    """To get the mobile number. This operation is needed at multiple places, hence made as a function. 
        Every user will have at most 3 attempts to type mobile number. If the third attempt also fails, then the function returns False
        The function returns two things, the number(if valid) and then the status, which indicates the validity of the number. """
    """In such cases, when the funntion returns multiple things, we use tuple representation for the 'type hints' """
    for i in range (3):
        ph_no = input("Enter your mobile number : ")
        if (validate_phone(ph_no)):
            return ph_no, True
        else:
            animation_spin_wheel()
            print(f"{ORANGE}WARNING{No_Color} ; {PINK}Invalid Mobile Number.{No_Color} Please enter a valid mobile number. You have {YELLOW}{2 - i}{No_Color} more chances remaining.")
            show_cursor()
            continue
    print(f"\n{RED}ERROR{No_Color} : {ORANGE}You have reached maximum attempt of entering mobile number.{No_Color} Please re-try again.")
    show_cursor()
    return "Invalid", False

def check_for_password(mobile_number : str, password : str) -> bool:
    """Connects to the suitable database, and validate it"""
    connection_to_main_database = sqlite3.connect("main_database.db")
    cursor_main = connection_to_main_database.cursor()
    query = "SELECT Password FROM main_table WHERE Mobile_Number = ?"
    cursor_main.execute(query, (mobile_number, ))
    result = cursor_main.fetchone() # the result will be a tuple, of the form (username, password in hasged form)
    stored_password = result[0]
    connection_to_main_database.close()
    if (bcrypt.checkpw(password.encode(), stored_password.encode())):
        return True
    else:
        return False

def get_password(mobile_number : str) -> bool:
    """Similar method as that of mobile numbers"""
    for i in range(3):
        password = input("Enter your password : ")
        animation_spin_wheel()
        if (check_for_password(mobile_number, password)):
            show_cursor()
            return True
        else:
            print(f"{ORANGE}WARNING{No_Color} ; {PINK}Incorrect password{No_Color} ; Try again.")
            show_cursor()
            continue
    username = get_username(mobile_number)
    present = Current_Date_and_Time()
    save_to_tracker(username, present.date, present.time, present.day, "Failed", "User enters wrong password thrice consecutively")
    print(f"{RED}ERROR{No_Color} : {ORANGE}Password entry limit exceeded.{No_Color} Account temporarily freezed.\n")
    hide_cursor()
    countdown()
    show_cursor()
    return False

def get_Details() -> Optional[Register]: 
    """The 'Optional' is used bcs, to indicate that, the function may return a Register object, or else, it will return None"""
    for i in range(3):
        name = input("Enter your name : ")
        if validate_name(name):
            break
        else:
            print(f"{ORANGE}WARNING !{No_Color}Invalid name. Please enter a valid one. You have {YELLOW}{2-i}{No_Color} more chances left. ")
            if i == 2:
                return None
    mobile_number, state = get_mobile_number()
    if not state:
        return None
    is_already_registered = check_if_registered(mobile_number)
    if is_already_registered:
        animation_spin_wheel()
        print(f"{ORANGE}WARNING{No_Color} ; You already have an account here.. You cannot register again with this mobile number.")
        show_cursor()
        return None
    for i in range(3):
        password = input("Enter your password (You may have letters, numbers, or symbols, but no whitespaces): ")
        if validate_password(password):
            break
        else:
            print(f"{ORANGE}WARNING !{No_Color}Invalid password. Please enter a valid one. You have {YELLOW}{2-i}{No_Color} more chances left. ")
            if i == 2:
                return None
    return Register(name, mobile_number, password)

def save_to_tracker(username : str, current_date : str, time : str, day : str, status : str, desc : str) -> None:
    """To save the attempts to the tracker database"""
    connection_to_tracker = sqlite3.connect("login_tracker.db")
    cursor_tracker = connection_to_tracker.cursor()
    cursor_tracker.execute("INSERT INTO tracker (Username, Login_Date, Login_Time, Day, Login_Status, Description) VALUES (?, ?, ?, ?, ?, ?)", (username, current_date, time, day, status, desc))
    connection_to_tracker.commit()
    connection_to_tracker.close()

def New_Registration() -> bool:
    user = get_Details()
    if user is None:
        return False
    connection_to_main_database = sqlite3.connect("main_database.db")
    cursor_main = connection_to_main_database.cursor()
    cursor_main.execute("INSERT INTO main_table (Username, Mobile_Number, Password) VALUES (?, ?, ?)", (user.name, user.mobile_number, user.password))
    connection_to_main_database.commit()
    connection_to_main_database.close()

    connection_to_key = sqlite3.connect("keys.db")
    cursor_key = connection_to_key.cursor()
    cursor_key.execute("INSERT INTO key_table (Mobile_Number, Key) VALUES (?, ?)", (user.secured_mobile_number, user.key))
    connection_to_key.commit()
    connection_to_key.close()

    present = Current_Date_and_Time()
    save_to_tracker(user.name, present.date, present.time, present.day, "---", "User Registration")
    
    print(f"{CYAN}Account succesfully created.{No_Color}")
    return True

def generate_QRCode_and_Validate(mobile_number : str) -> None:
    connection_to_key = sqlite3.connect("keys.db")
    cursor_key = connection_to_key.cursor()
    query_for_key = "SELECT Key FROM key_table WHERE Mobile_Number = ?"
    cursor_key.execute(query_for_key, (hashlib.sha256(mobile_number.encode()).hexdigest(), ))
    key = cursor_key.fetchone()
    connection_to_key.close()

    username = get_username(mobile_number)

    uri = pyotp.totp.TOTP(key[0]).provisioning_uri(name = f"Greetings {username}", issuer_name="Nevin Beno")
    qr = qrcode.QRCode(
                    version = 1,
                    box_size=1,
                    border=1
                      )
    qr.add_data(uri)
    qr.make()
    animation_dot()
    qr.print_ascii(tty=True)

    otp = pyotp.TOTP(key[0])
    user_input_otp = input(f"Enter the OTP: ")
    present = Current_Date_and_Time()
    animation_spin_wheel()
    show_cursor()
    if (otp.verify(user_input_otp)):
        hide_cursor()
        save_to_tracker(username, present.date, present.time, present.day, "Succes", "User successfully logged in")
        success()
        print(f"{GREEN}Login Successful. {No_Color}Welcome {username} !")
        show_cursor()
    else:
        save_to_tracker(username, present.date, present.time, present.day, "Failed", "Invalid TOTP entered by the user")
        hide_cursor()
        fail()
        print(f"{RED}ERROR{No_Color} : {ORANGE}TOTP verification failed.{No_Color} Account temporarily freezed.\n")
        countdown()
        show_cursor()
        exit()

def login() -> bool:
    if not login_permission():
        return False
    print("\n")
    mobile_number, state = get_mobile_number()
    if not state:
        return False
    is_already_registered = check_if_registered(mobile_number)
    if not is_already_registered:
        print(f"{ORANGE}WARNING{No_Color} ; {PINK}You do not have an account here. {No_Color}Please register first, and then login.")
        return False
    state = get_password(mobile_number)
    if not state:
        return False
    generate_QRCode_and_Validate(mobile_number)
    return True
    
if __name__ == "__main__":

    while (True):
        user_type = display_and_enquire()
        if(user_type == "no"):
            succesful_registration = New_Registration()
        elif(user_type == "yes"):
            user_login = login()
        elif(user_type == "help"):
            mobile_number, valid = get_mobile_number()
            if valid:
                is_already_registered = check_if_registered(mobile_number)
                if is_already_registered:
                    print(f"{BLUE}You have an account here.{No_Color}")
                else:
                    print(f"{PINK}You do not have an account here.{No_Color}")
        else:
            print(f"{RED}ERROR{No_Color} : {ORANGE}Invalid input{No_Color} ; Please enter one, as given in the table.")
    
        control = input(f"\nEnter {YELLOW}Exit{No_Color} to exit the program, or just hit the {YELLOW}Enter Key{No_Color} to continue.")
        if (control.lower() == "exit"):
            break
        else:
            print("\n\n")
            continue