import pymongo
from typing import List, Dict, Any
##### Application State used to control main loop #####

app_state = True

uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(uri)
database = client["ContactBook"]
collection = database["TheContact"]

##### Read and Return collection documents ##### 
def read_index():
   return list(collection.find())

def main_saving(fname,lname,phone,email):
   ##### Stripping input for waste characters #####
   fn = fname.strip()
   ln = lname.strip()
   ph = phone.strip()
   em = email.strip() if email and email.strip else None 

   ##### Find index to be used for indexing #####
   if not read_index():
      last_id = 1
   else:
      last_id = read_index()[-1]['the_id'] + 1

   if not fn or not ln:
           print("First and last name are required.")
           return None
   doc = {
        "the_id": last_id,
        "first_name": fn,
        "last_name": ln,
        "phone": ph,
        "email": em,
    }
   collection.insert_one(doc)
   print("\nContact added successfully !")

##### Print main menu options #####
def main_menu():
   print("""\nWelcome to contact book!
   1.Add new contact
   2.List added contacts
   3.Remove contact by id
   4.Exit""")

def delete_by_id(del_id):
   collection.delete_one({'the_id':del_id})
   print("Contact Deleted Succesfully !")

def print_contacts(contacts: List[Dict[str, Any]]) -> None:
    if not contacts:
        print("No contacts found.")
        return
    for c in contacts:
        print(
            f"ID: {c['the_id']}\nFirst name: {c['first_name']}\nLast name: {c['last_name']}\n"
            f"Phone: {c['phone']}\nEmail: {c.get('email')}\n" + ("-" * 32)
        )

while app_state:
   main_menu()
   user_choice = int(input("Choose an option: "))
   if user_choice == 1:
      fname_input = input("Enter the first name :")
      lname_input = input("Enter the last name :")
      phone_input = input("Enter associated phone number: ")
      email_input = input("Enter their email (if any): ")
      main_saving(fname_input,lname_input,phone_input,email_input)
   elif user_choice == 2:
      contacts = read_index()
      print_contacts(contacts)      
      input("Press Enter to continue...")

   elif user_choice == 3:
      try:
         del_input = int(input("Enter an id to delete: "))
         delete_by_id(del_input)
         continue
      except ValueError:
         print("Please enter a valid number")
      
   elif user_choice == 4:
      app_state = False

