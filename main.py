from csv import writer, reader
import csv
from tabulate import tabulate
from os import path

class CSVFile():
    def __init__(self, fileName, headers):
        self.fileName = fileName
        self.headers = headers
        fileExists = path.exists(fileName)
        if not fileExists:
            self.file = open(fileName, 'w+', newline='')
            csvFile = writer(self.file)
            csvFile.writerow(self.headers)
            self.file.close()
        self.file = open(fileName, 'a+', newline='')

    def __del__(self):
        self.file.close()

    def reader(self):
        self.file.seek(0)
        iter = reader(self.file)
        self.file.seek(0)
        data=[]
        for i in iter:
            data.append(i)
        return data

    def records(self):
        data = self.reader()
        if len(data) != 0:
            data.pop(0)
        return data

    def writer(self):
        return writer(self.file)

    def update(self, records):
        self.file.close()
        newFile = open(self.fileName, 'w', newline='')
        writer = csv.writer(newFile)
        writer.writerow(self.headers)
        writer.writerows(records)
        newFile.close()
        self.file = open(self.fileName, 'r+', newline='')

    def appendRecord(self, record):
        self.file.seek(0, 2)
        self.writer().writerow(record)

    def is_empty(self):
        records = self.records()
        return len(records) == 0

    def tabulate(self):
        recordsWithHeader = self.reader()
        return tabulate(recordsWithHeader, headers="firstrow", tablefmt='grid')


#################  I N P U T   P A T I E N T #####################


class IP():
    def __init__(self):
        IPHead = [
            "S No", "Patient", "Hospital No", "Doctor", "Room No", "DOA",
            "Treatment", "Billing"
        ]
        self.file = CSVFile('IP.csv', IPHead)

    def hospitalNumberExists(self, record):
        records = self.file.records()
        for i in records:
            if i[0] == record[0]:
                return True
        return False

    def get_data(self,withSerialNumber=True):  # add serial no as option
        print("\nEnter the details of the patient")

        if (withSerialNumber):
            serial_no = input("Enter Serial No : ")
        else:
            serial_no = -1
        patient_name = input("Enter Patient name : ")
        hospital_no = input("Enter Hospital no : ")
        dr_name = input("Enter Dr Name : ")
        room_no = input("Enter Room No : ")
        doa = input("Enter the Date of Admission : ")  # Date of Admission
        treatment = input("Enter treatment : ")
        billing = input("Billing : ")

        data = [serial_no, patient_name, hospital_no, dr_name, room_no, doa, treatment, billing]
        return data

    def insert(self):  #storing IP data
        data = self.get_data()
        if not self.hospitalNumberExists(data):
            self.file.appendRecord(data)
            print("New patient record has been added.")
        else:
            print("Hospital Number already exists")

    def storeData(self):
        self.insert()

    def display(self):
        if (self.file.is_empty()):
            print("Sorry, No Records Found.")
            return
        print(self.file.tabulate())

    def search_by_hospital_no(self,hosp_no):  # Serial Number
        records = self.file.records()
        for i in records:
            if hosp_no == i[2]:
                return i
        return None
		
    def search_by_name(self,name):
        records = self.file.records()
        for i in records:
            if name == i[1]:
                return i
        return None

    def modify(self):  #modify the entire record on the basis of serial number
        se_no = input("Enter Serial Number to modify: ")
        found = False
        new_rec = []
        records = self.file.records()
        for i in records:
            if i[0] == se_no:
                print("Current Record:", i)
                data = self.get_data(withSerialNumber=False)
                data[0] = i[0]
                i = data
                found = True
            new_rec.append(i)

        if not found :
            print("Serial No not found")
        else:
            self.file.update(new_rec)
            print("Patient data has been updated")

    def delete(self):  #delete a record
        se_no = input("Enter the Hospital Number to delete: ")
        found = False
        new_rec = []
        records = self.file.records()

        for i in records:
            if i[2] == se_no:
                found = True
                continue
            new_rec.append(i)

        if not found :
            print("Hospital Number not found.")
        else:
            self.file.update(new_rec)
            print("Patient record deleted.")


    def menu(self):
        print("\n\tIP RECORDS")
        
        while (True):
            print("\n1. Add a patient \n2. Display all patients \n3. Search By Hospital No \n4. Modify a patient record \n5. Delete a patient record \n6. Search By patient name \n0. Back to Menu")
            
            ch = int(input("Enter choice "))
            if ch == 1:
                self.insert()
                
            elif ch == 2:
                self.display()
                
            elif ch == 3:
                sno_id=input("Enter the Hospital No. to search: ")
                res=self.search_by_hospital_no(sno_id)
                if(res is not None):
                    print(res)
                else:
                    print("Hospital not found")
                    
            elif ch == 4:
                self.modify()
                
            elif ch == 5:
                self.delete()
                
            elif ch == 6:
                patient_name = input("Enter the patient Name: ")
                res = self.search_by_name(patient_name)
                if(res is not None):
                    print(res)
                else:
                    print("Patient not found")
            elif ch == 0:
                return
            else:
               print("Invalid Choice")

#################  O U T P U T   P A T I E N T ##################################
class OP():
    def __init__(self):
        OPHead = ["Serial No", "Hospital No", "New/Renewal", "Patient", "Gender","Address", "Fee","Doctor Name"]
        self.file = CSVFile('OP.csv', OPHead)

    def hospitalNumberExists(self, record):
        records = self.file.records()
        for i in records:
            if i[0] == record[0]:
                return True
        return False

    def get_data(self,withSerialNumber=True):
        print("Enter the details of the patient: ")

        if (withSerialNumber):
            serial_no = input("Enter Serial No : ")
        else:
            serial_no = -1
        hospital_no = input("Enter Hospital no : ")
        new_or_renewal = input("Enter if New or Renewal[N/R] : ")
        patient_name = input("Enter Patient name : ")
        gender = input("Enter gender [M/F] : ")
        address = input("Enter address : ")
        fee = input("Enter the Fee : ")
        dr_name = input("Enter Doctor Name : ")

        data = [serial_no, hospital_no, new_or_renewal, patient_name, gender, address, fee, dr_name]
        return data

    def insert(self):
        data = self.get_data()
        if not self.hospitalNumberExists(data):
            self.file.appendRecord(data)
            print("Patient Record has been added.")
        else:
            print("Hospital Number already exists.")
    
    def storeData(self):
        self.insert()

    def display(self):
        if (self.file.is_empty()):
            print("Sorry, No patient records Found.")
            return
        print(self.file.tabulate())

    def search_by_hospital_no(self,hosp_no):  #search by Serial number and search by Patient name
        records = self.file.records()
        for i in records:
            if hosp_no== i[1]:
	            return i
        return None
                
    def search_by_name(self,name):
        records = self.file.records()
        for i in records:
            if name == i[3]:
                return i
        return None
        
    def modify(self):  #modify the entire record on the basis of serial number
        hos_no = input("Enter the hospital Number: ")
        print(hos_no)
        found =False
        new_rec=[]
        records = self.file.records()
        for i in records:
            if i[1] == hos_no:
                print("Current Records: ",i)
                data = self.get_data(withSerialNumber=False)
                data[0] = i[0]
                i=data
                found=True
            new_rec.append(i)

        if not found :
            print("The Hospital No is Invalid")
        else:
            self.file.update(new_rec)


    def delete(self):
        hosp_no = input("Enter Hospital Number to delete: ")
        new_rec = []
        found=False
        records = self.file.records()

        for i in records:
            if i[1] ==hosp_no:
                found = True
                continue
            new_rec.append(i)

        if not found :
            print("Not Found :(")
        else:
            self.file.update(new_rec)
            print("Deleted Successfully !")
    
    def menu(self):
        print("\n\tOP RECORDS")
        while True:
            print("\n1. Add a patient \n2. Display all patients \n3. Search By Hospital No \n4. Modify a patient record \n5. Delete a patient record \n6. Search By patient name \n0. Back to Menu")
           
            ch  = int(input("Enter your choice: "))
            
            if ch == 1:  #insertion of op record
                self.insert()
                
            elif ch == 2:  #display all op records
                self.display()
                
            elif ch == 3:  #search for specified op record
                hospital_no=input("Enter the hospital no to search: ")
                res=self.search_by_hospital_no(hospital_no)
                if(res is not None):
                    print(res)
                else:
                    print("Serial No not found!")
                    
            elif ch == 4:  #modify specified op record
                self.modify()
                
            elif ch == 5:  #delete specified op record
                self.delete()	
                
            elif ch == 6:
                patient_name = input("Enter the patient name: ")
                res=self.search_by_name(patient_name)
                if(res is not None):
                    print(res)
                else:
                    print("Name not found!")
                    
            elif ch == 0:
                break
                
            else:
                print("\n Invalid input")
                
################################################################################

######################### P H A R M A C Y  #####################################
class Pharmacy():
    def __init__(self):
        PharmHead = ["S No","Bill","Patient", "Hospital No", "List of Medicines","Quantity"]
		
        self.file = CSVFile('Pharmacy.csv', PharmHead)

    def billNumberExists(self, record):
        records = self.file.records()
        for i in records:
            if i[5] == record[5]:
                return True
        return False
      
    def get_data(self,withSerialNumber=True):  # add serial no as option
        print("\nEnter the details of PHARMACY: ")

        if (withSerialNumber):
            serial_no = input("Enter S.no : ")
        else:
            serial_no = -1
        patient_name = input("Enter Patient name : ")
        hospital_no = input("Enter Hospital no : ")
        bill_no = input("Enter The bill No : ")  # Date of Admission

        medicines = ""
        medicine_quantities = ""

        while(True):
            med = input("Enter name of the medicine: ")
            med_quan = input("Enter the quantity : ")
            medicines = medicines+' '+med
            medicine_quantities = medicine_quantities+' '+med_quan
            ch= input("Do you want to continue (y/n)?")
            if ch=='n' or ch=='n' :
                break     
        data = [serial_no,bill_no, patient_name, hospital_no, medicines,medicine_quantities]
        return data

    def insert(self):
        data = self.get_data()
        if not self.billNumberExists(data):
            self.file.appendRecord(data)
            print("New pharmacy bill has been added.")
        else:
            print("The bill number already exists")

    def storeData(self):
        self.insert()

    def display(self):
        if(self.file.is_empty()):
            print("Sorry, No Records Found.")
            return
        print(self.file.tabulate())

    def search_by_hospital_no(self,hosp_no):  #search by Serial number and search by Patient name
        records = self.file.records()
        for i in records:
            if hosp_no == i[3]:
            	return i
        return None

    def search_by_name(self, name):
        records = self.file.records()
        for i in records:
            if name == i[2]:
                return i
        return None

    def search_by_bill_no(self,bill_no):
        records = self.file.records()
        for i in records:
            if bill_no == i[1]:
                return i
        return None

    def delete(self):
       bill_no = input("Enter Bill No. to delete: ")
       new_rec = []
       found = False
       records = self.file.records()

       for i in records:
        if i[1] == bill_no:
            found = True
            continue
        new_rec.append(i)

       if not found:
            print("Hospital No not found")
       else:
            self.file.update(new_rec)
            print("Record deleted successfully!")

    def menu(self):
        print("\n\tPHARMACY RECORDS")
        
        while True:
                print(
                    "\n1. Add a new bill \n2. Display all bills \n3. Search by Hospital no \n4. Delete \n5. Search by Patient name \n6. Search by Bill No \n0. Back to Menu"
                )
                ch = int(input("Enter your choice: "))
            
                if ch == 1:  #insertion of Pharmacy record
                    self.insert()
                    
                elif ch == 2:  #display all Pharmacy records
                    self.display()
                    
                elif ch == 3:  #search for specified Pharmacy record
                    sno_id = input("Enter the hospital no to search: ")
                    res = self.search_by_hospital_no(sno_id)
                    if (res is not None):
                        print(res)
                    else:
                        print("Hospital No not found!")
                        
                elif ch == 4:  #delete specified Pharmacy record
                    self.delete()
                    
                elif ch == 5:
                    patient_name = input("Enter the patient name: ")
                    res = self.search_by_name(patient_name)
                    if(res is not None):
                        print(res)
                    else:
                        print("Patient not found!")
					
                elif ch== 6:
                    bill_no = input("Enter the bill No. :")
                    res = self.search_by_bill_no(bill_no)
                    if(res is not None):
                        print(res)
                    else:
                        print("Bill No. not found!")
                elif ch == 0:
                    break
                else:
                    print("\n Invalid input")

###############################################################################

################################# Finance #####################################


class Finance():

    def __init__(self):
        financeHead = ["Date", "Mode of Payment", "Total Amount"]
        self.file = CSVFile('Finance.csv', financeHead)

    def get_data(self,withSerialNumber=True): 
        print("\nEnter the Finance details: ")
        payment_modes = ["Cash","Card","Insurance"]
        date = input("Enter the date: ")  
        mode_of_payment = int(input("Enter mode of payment :\n1. Cash\n2. Card\n3. Insurance\n"))
    
        total = input("Enter the total amount: ")
        data =[date, payment_modes[mode_of_payment-1], total]

        return data
        
    def insert(self):
        data=self.get_data()
        self.file.appendRecord(data)
        print("New record has been added \n")


    def storeData(self):
        self.insert()   

    def display(self):
        if (self.file.is_empty()):
            print("Sorry, No Records Found.")
            return
        print(self.file.tabulate())
    
    def menu(self):
        print("\n\tFINANCIAL RECORDS")
        while True:
                
                print("\n1. Add a new payment record \n2. Display all payment records  \n0. Back to Menu")
                ch4 = int(input("\nEnter your choice: "))
                if ch4 == 1: 
                    self.storeData()
                elif ch4 == 2:
                    self.display()
                elif ch4 == 0:
                    break
                else:
                    print("\n Invalid input")

        



###############################################################################
#menu

def main():
    print("****************************************************************************")
    print("*                                                                          *")
    print("*                   Welcome to Hospital Software Management                *")
    print("*                                                                          *")
    print("****************************************************************************")

    _IP = IP()
    _OP = OP()
    _PHARMACY = Pharmacy()
    _FINANCE = Finance()

    while True:
        print(
            "\n 1. IP \t 2. OP \t 3. Pharmacy \t 4. Finance \n  \n \t Press 5 to Exit\n"
        )
        ch = int(input("Enter your choice : "))
      
        if ch == 1:
            _IP.menu()
        elif ch == 2:
            _OP.menu()
        elif ch == 3:
            _PHARMACY.menu()
        elif ch == 4: 
            _FINANCE.menu()
        elif ch == 5:
            break
        else:
            print("\n Invalid input at the end")

    print("\n\t\tThank you")


main()
