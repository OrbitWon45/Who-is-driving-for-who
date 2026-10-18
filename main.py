# This imports the driver module.
from driver import Driver

# This is the main,py file of the program. the program will store gas-fill-up totals
# and the price per gallon for drivers the whole year round. The program will also
# tell drivers information that the delivery apps don't want drivers to know. Information
# like the net total of the total made after the price per mile has been subtracted
# from the total and the rate per hour the driver has been earning driving for the apps.
# Also, the driver will be able to see if the tax deductions compare to the gas spent working
# for the app. The driver will know what they are really earning while they invest their time and
# effort into the delivery apps.


# This function outputs the "List of Commands to the user."
def list_of_commands():
    print()
    print('List of Commands')
    print()
    print('list-drivers: - List all drivers')
    print('add-driver: - Add new driver')
    print('add-stats: - Add a workday\'s stats')
    print('money-earned: - lists net-totals of 1 or multiple days earnings and sum of totals')
    print('list-fill-ups: - Lists 1 or multiple fill-ups and sum of list')
    print('fill-up: - Add total for fill-up and price per gallon')
    print('del: - Deletes a driver')
    print('exit: - Exit program')
    print()


# This is the main function and point of entry to the program. This function lets the user choose what commands they
# want the program to preform.
def main():
    print('Who is Driving for Who: Delivery Driver Program')
    print()
    print('You must know your vehicles miles per gallon (mpg) and \n'
          'the price per gallon (ppg) of your last fill up to\n'
          'start using this program.')
    print('Raise terminal screen to the top.')
    i = 0
    # While loop over the commands till i = 1. This keeps the program going till the user is finished.
    while i < 1:
        list_of_commands()
        # This asks the user for a command.
        command = input('What would you like to do? Enter command please: ')
        dr = Driver()
        # These are the commands the user can choose.
        if command.lower() == 'list-drivers':
            list_of_drivers = dr.get_drivers_list()
            print()
            print('Drivers list')
            if len(list_of_drivers) == 0:
                print('None')
            else:
                for d in list_of_drivers:
                    print(d)
        elif command.lower() == 'add-driver':
            dr.add_new_driver()
        elif command.lower() == 'add-stats':
            dr.add_workday_stats()
        elif command.lower() == 'money-earned':
            dr.get_money_earned()
        elif command.lower() == 'list-fill-ups':
            dr.get_fill_ups()
        elif command.lower() == 'fill-up':
            dr.fill_up()
        elif command.lower() == 'del':
            dr.delete_driver()
        elif command.lower() == 'exit':
            print()
            print('Who is Driving for Who: Delivery Driver Program is closed.')
            # When the user is finished the exit code will add 1 to the i variable to end the while loop.
            i += 1
        else:
            print()
            # If the user enters an invalid command, this message is output.
            print('Not a valid command. Please refer to the menu and try again.')


if __name__ == '__main__':
    main()

print('See you later, driver in the know.')



