import sys
def hide_cursor() -> None:
    """When this function is called, the cursor is hidden"""
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor() -> None:
    """When this function is called, the cursor will be visible"""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()
# sample demo :
if __name__ == "__main__":
    name = input("Now you see cursor, enter your name :")
    hide_cursor()
    name2 = input("Now you son't see the cursor, enter your name : ")
    input("Press enter to show the cursor.")
    show_cursor()