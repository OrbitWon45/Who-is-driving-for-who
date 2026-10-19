# This imports the datetime, csv, and decimal modules. It also imports remove from the os module for the Driver class.
from datetime import date
import csv
import sys
from os import remove
from decimal import *


# This module holds the Driver class with all the methods to preform the tasks on the command list
# and the methods to delete, create, read, and write to the driver and drivers files.
class Driver:
    # The init method is used to create an instance that brings all the self varaibles back to their
    # original state and value.
    def __init__(self):
        self.file_name = ''
        self.today = date.today()
        self.str_today = self.today.strftime('%m-%d-%Y')
        self.date_from = ''
        self.date_to = ''
        self.ppg = Decimal(0)
        self.total = Decimal(0)
        self.miles = Decimal(0)
        self.mpg = Decimal(0)
        self.hours = Decimal(0)
        self.fill_up_total = Decimal(0)

    # This method exits the program before errors are created, or to handle errors.
    def exit_program(self):
        print('terminating Program.')
        sys.exit(self)

    # This method reads the drivers file, and driver's file and appends the files to a list of dictionaries.
    def read_driver_files(self, name):
        self.file_name = name
        try:
            driver_files_dicts = []
            with open(self.file_name + '.csv', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    driver_files_dicts.append(row)
            return driver_files_dicts
        except FileNotFoundError:
            print(f'Could not find {self.file_name}\'s file. Please try again')
            self.exit_program()
        except Exception as e:
            print(type(e), e)
            self.exit_program()

    # This method writes new statistics (i.e.. workday stats, and fill-ups) to an existing driver's file. This method
    # is also used to create a new driver's file.
    def write_driver_files(self, stats, name):
        self.file_name = name
        try:
            with open(self.file_name + '.csv', 'w', newline='') as file:
                fieldnames = ['Date', 'Fill_up', 'Price_per_gal', 'Gas_spent', 'Net_total']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(stats)
        except Exception as e:
            print(type(e), e)
            print('Failed to write to file. Please try again.')
            self.exit_program()

    # This method adds new drivers to the list of drivers in the drivers file.
    def write_drivers_file(self, stat):
        try:
            with open('drivers.csv', 'w', newline='') as file:
                fieldnames = ['Driver']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(stat)
        except Exception as e:
            print(type(e), e)
            print('Failed to write to file. Please try again.')
            self.exit_program()

    # This method takes the drivers file list of dictionaries and appends the driver's names to a list.
    def get_drivers_list(self):
        list_of_dicts = self.read_driver_files('drivers')
        drivers_list = []
        for d in list_of_dicts:
            drivers_list.append(d['Driver'])
        return drivers_list

    # This method gets the last price per gallon (PPG) in an existing driver's file and returns it alone.
    def get_price_per_gal(self, name):
        list_of_file_dicts = self.read_driver_files(name)
        ppg_list = []
        ppg_index = ''
        for d in list_of_file_dicts:
            if d['Price_per_gal'] != '0':
                ppg_list.append(d['Price_per_gal'])
            ppg_index = ppg_list[-1]
        self.ppg = Decimal(ppg_index)
        return self.ppg

    # This method lets you choose your driver's file.
    def choose_driver(self):
        print()
        name = input('Please enter the driver\'s name: ')
        drivers_list = self.get_drivers_list()
        if name not in drivers_list:
            print()
            print('Driver not found, please add driver and try again')
            print()
            print('Drivers list')
            for d in drivers_list:
                print(d)
            self.exit_program()
        else:
            print('Driver found!')
            name = name.lower()
            return name

    # This method adds a new driver to the drivers list and creates a new file for the new driver.
    def add_new_driver(self):
        i = 0
        dict_of_drivers = self.read_driver_files('drivers')
        drivers_list = self.get_drivers_list()
        print()
        new_driver = input('Enter name of new driver: ')
        if new_driver not in drivers_list:
            while i < 1:
                try:
                    self.ppg = Decimal(input('Enter the price per gallon (PPG)'
                                             ' of gas on your last fill-up please (Must be a number!): '))
                    i += 1
                except InvalidOperation as e:
                    print()
                    print('Price per gallon of last Fill-up Must be numerical.: ', e)
                    print()
            dict_of_drivers.append({'Driver': new_driver})
            self.write_drivers_file(dict_of_drivers)
            name = new_driver.lower()
            driver_stats = [{'Date': self.str_today, 'Fill_up': 0,
                             'Price_per_gal': self.ppg, 'Gas_spent': 0, 'Net_total': 0}]
            self.write_driver_files(driver_stats, name)
            print()
            print('Driver successfully add!')
        else:
            print()
            print('Driver name already taken. Check drivers list and try again.')
            print()
            print('Drivers list')
            for d in drivers_list:
                print(d)

    # This method lets you add workday statistics to an existing driver's file. It also outputs the total earned,
    # net earned, gas spent, rate per hour of the net total, and hours working on the app to the user.
    def add_workday_stats(self):
        name = self.choose_driver()
        driver_stats = self.read_driver_files(name)
        self.ppg = self.get_price_per_gal(name)
        i = 0
        while i < 1:
            try:
                self.total = Decimal(input('What was the total you made today? (You must enter a number): '))
                self.miles = Decimal(
                    input('How many miles did you drive while on the app? (You must enter a number!): '))
                self.mpg = Decimal(
                    input('How many miles per gallon (MPG) did the ride get today? (You must enter a number!): '))
                self.hours = Decimal(
                    input('How many hours did you devote to the app today? (You must enter a number!): '))
            except InvalidOperation as e:
                print()
                print('Your answers MUST be numerical.: ', e)
                print()
                continue
            print()
            commit = str(input('Last chance, are you happy with all your answers? (yes or no): '))
            print()
            if 'n' in commit.lower():
                continue
            else:
                i += 1
        ppm = self.ppg / self.mpg
        gas_spent = Decimal(str(ppm * self.miles)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        net_total = self.total - gas_spent
        rate_per_hour = net_total / self.hours
        rate_per_hour_quantized = Decimal(str(rate_per_hour)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        print()
        print(self.str_today)
        print(f'For {self.total} dollars made, your net total is: {net_total}!')
        print(f'You spent {gas_spent} dollars in gas on the app today.')
        print(f'You made: {rate_per_hour_quantized} an hour for {self.hours} hours on the app!')
        driver_stats.append({'Date': self.str_today, 'Fill_up': 0,
                             'Price_per_gal': self.ppg, 'Gas_spent': gas_spent, 'Net_total': net_total})
        new_stats = driver_stats
        self.write_driver_files(new_stats, name)
        print()
        print('Your workday stats have been added to file!')

    # This method adds a new fill-up total and the new price per gallon (PPG) to an existing driver's file.
    def fill_up(self):
        i = 0
        name = self.choose_driver()
        driver_file = self.read_driver_files(name)
        while i < 1:
            try:
                self.fill_up_total = Decimal(input('How much was the total of fill-up? (You must enter a number): '))
                self.ppg = Decimal(input('How much was the price per gallon (PPG)? (You must enter a number): '))
            except InvalidOperation as e:
                print()
                print('Your answers all MUST be numerical.: ', e)
                print()
                continue
            print()
            commit = str(input('Last chance, are you happy with all your answers? (yes or no): '))
            print()
            if 'n' in commit.lower():
                continue
            else:
                i += 1
        driver_file.append({'Date': self.str_today, 'Fill_up': self.fill_up_total,
                            'Price_per_gal': self.ppg, 'Gas_spent': 0, 'Net_total': 0})
        new_stats = driver_file
        self.write_driver_files(new_stats, name)
        print('Fill up has been  added to file!')

    # This method takes an existing driver's file. Lists all the driver's, net totals, their dates,
    # the sum of those net totals, and the sum of the gas spent totals between chosen dates and outputs
    # those statistics to the user.
    def get_money_earned(self):
        name = self.choose_driver()
        list_of_dicts = self.read_driver_files(name)
        totals_list = []
        sum_of_totals = Decimal(0)
        i = 0
        while i < 1:
            self.date_from = str(input('Choose date FROM (Use this format: mm-dd-yyyy): '))
            self.date_to = str(input('Choose date TO (Use this format: mm-dd-yyyy): '))
            if '-' not in self.date_from or '-' not in self.date_to:
                print()
                print('Dates must be in mm-dd-yyyy format, try again.')
                print()
                continue
            else:
                print()
                commit = str(input('Last chance, are you happy with your dates? (yes or no): '))
                print()
                if 'n' in commit.lower():
                    continue
                else:
                    i += 1
        for d in list_of_dicts:
            if d['Date'] >= self.date_from and d['Date'] <= self.date_to and d['Net_total'] != '0':
                totals_list.append([d['Date'], d['Net_total']])
                total = Decimal(d['Net_total'])
                sum_of_totals += total
        print()
        print('Date        Net Totals')
        for l in totals_list:
            print(f'{l[0]}: {Decimal(l[1])}')
        print()
        print(f'The sum of all the net totals between from: '
              f'{self.date_from} and to: {self.date_to} dates is: {sum_of_totals}.')

    # This method takes an existing driver's file. Lists all the driver's fill-up totals,
    # and the sum of those totals between chosen dates and outputs those statistics to the user.
    def get_fill_ups(self):
        name = self.choose_driver()
        list_of_dicts = self.read_driver_files(name)
        totals_list = []
        sum_of_totals = Decimal(0)
        sum_of_gas_spent = Decimal(0)
        i = 0
        while i < 1:
            self.date_from = str(input('Choose date FROM (Use this format: mm-dd-yyyy): '))
            self.date_to = str(input('Choose date TO (Use this format: mm-dd-yyyy): '))
            if '-' not in self.date_from or '-' not in self.date_to:
                print()
                print('Dates Must be in mm-dd-yyyy format, try again.')
                print()
                continue
            else:
                print()
                commit = str(input('Last chance, are you happy with your dates? (yes or no): '))
                print()
            if 'n' in commit.lower():
                continue
            else:
                i += 1
        for d in list_of_dicts:
            gas_spent = Decimal(d['Gas_spent'])
            sum_of_gas_spent += gas_spent
            if d['Date'] >= self.date_from and d['Date'] <= self.date_to and d['Fill_up'] != '0':
                totals_list.append([d['Date'], d['Fill_up']])
                total = Decimal(d['Fill_up'])
                sum_of_totals += total
        print()
        print('Date        fill-up totals')
        for l in totals_list:
            print(f'{l[0]}: {Decimal(l[1])}')
        print()
        print(f'The sum of all your fill-ups between from: '
              f'{self.date_from} and to: {self.date_to} dates is: {sum_of_totals}.')
        print(f'You spent {sum_of_gas_spent} dollars on gas working on the app between these dates.')

    # This method removes a known driver from the drivers list and removes the driver's existing file.
    # It deletes the driver from the program.
    def delete_driver(self):
        file_name_title = str(input('What is the name of the driver you want to delete?: '))
        file_name = file_name_title.lower()
        drivers_list_of_dicts = self.read_driver_files('drivers')
        drivers_list = self.get_drivers_list()
        if file_name_title in drivers_list:
            for i, d in enumerate(drivers_list_of_dicts, start=0):
                if d['Driver'] == file_name_title:
                    drivers_list_of_dicts.pop(i)
                    self.write_drivers_file(drivers_list_of_dicts)
                    remove(file_name + '.csv')
                    print()
                    print('Driver deleted!')
        else:
            print()
            print('Driver not found. Check Drivers list and try again.')
            print()
            print('Drivers list')
            for d in drivers_list:
                print(d)






