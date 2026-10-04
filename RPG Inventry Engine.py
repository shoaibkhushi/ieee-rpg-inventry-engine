import csv
import os

#item class
class Item:
    def __init__(self,name,item_type,value,rarity):
        self.name = name
        self.item_type = item_type
        self.value = value
        self.rarity = rarity
    def get_detail(self):
        return (
            f"{self.name} | "
            f"Type: {self.item_type} | "
            f"Value: {self.value} | "
            f"Rarity: {self.rarity}"
            )
    def __str__(self):
        return self.get_detail()
class Weapon(Item):
    def __init__(self, name, item_type, value, rarity,attack_power): 
        super().__init__(name, item_type, value, rarity)  
        self.attack_power = attack_power
    def get_detail(self):
        return (
            f"{self.name} | "
            f"Type: {self.item_type} | "
            f"Value: {self.value} | "
            f"Rarity: {self.rarity} | "
            f"Attac_Power: {self.attack_power}"
        )

class Potion(Item):
    def __init__(self, name, item_type, value, rarity,heal_amount):
        super().__init__(name, item_type, value, rarity)
        self.heal_amount = heal_amount

    def get_detail(self):
        return (
            f"{self.name} | "
            f"Type: {self.item_type} | "
            f"Value: {self.value} | "
            f"Rarity: {self.rarity} | "
            f"Heal_Amount: {self.heal_amount}"
        )
class Armor(Item):
    def __init__(self, name, item_type, value, rarity,defence_rating):
        super().__init__(name, item_type, value, rarity)
        self.defence_rating = defence_rating

    def get_detail(self):
        return (
            f"{self.name} | "
            f"Type: {self.item_type} | "
            f"Value: {self.value} | "
            f"Rarity: {self.rarity} | "
            f"Defence_Rating: {self.defence_rating}"
        )
def load_items(filename):
    items = []  
    skipped = 0
    print("Loading Items...")
    print("-"*60)

    file = None
    try:
        file = open(filename,"r",newline="",encoding="utf-8-sig") 
        reader = csv.DictReader(file)
        for line_number, row in enumerate(reader, start=2): 
            try: 
                if not row.get("name") or not row.get("type"):
                    raise ValueError("Missing Name or type")
                name = row["name"].strip()
                item_type = row["type"].strip()
                value = int(row["value"].strip()) 
                rarity = row["rarity"].strip()

                #extra value
                extra = int(row["extra"])
                #child object create
                if item_type.lower() == "weapon":
                    item = Weapon(
                        name,
                        item_type,
                        value,
                        rarity,
                        extra
                    )
                elif item_type.lower() == "potion":
                    item = Potion(
                        name,
                        item_type,
                        value,
                        rarity,
                        extra
                    )
                elif item_type.lower() == "armor":
                    item = Armor(  
                        name,
                        item_type,
                        value,
                        rarity,
                        extra
                    )
                else:
                    #item class 
                    item = Item(  
                        name,
                        item_type,
                        value,
                        rarity
                    )
                items.append(item)  
                print(f"Loaded: {name}")
            except (ValueError,TypeError,AttributeError) as error:
                skipped += 1
                print(
                    f"Skipped invalid row {line_number}: "
                    f"{row.get('name','Unknown')}"
                    f"{error}"
                )
    except FileNotFoundError:
        print(f"Error: File '{filename} was not found.'")
    except OSError as error:
        print(f"File Error: {error}")
    finally:
        if file is not None:
            file.close()
        print("-"*60)
        print(f"Valid item Loaded: {len(items)}") 
        print(f"Invalid Items Skipped: {skipped}")
    return items 
class Inventory:
    def __init__(self):
        self.item = []  
    def add_item(self,item):
        self.item.append(item)
        print(f"\n {item.name} addd to inventry..")
    #remove item
    def remove_item(self, name):
        for item in self.item:
            if item.name.lower() == name.lower():
                self.item.remove(item)
                print(f"\n {item.name} removed from inventry..")
                return
        print("\n Item Not Found!")
    #all item show
    def show_all(self):
        if not self.item:
            print("Inventry is empty.")
            return
        print("\n=========== INVENTRY ===========")
        for number,item in enumerate(self.item,start=1): 
            print(f"{number}. {item.get_detail()}")
   #search item
    def search_by_name(self, name): 
        result = [
            item for item in self.item
            if name.lower() in item.name.lower()
        ] 
        if result:
            print("\n ====== Search Results =======")
            for item in result:
                print(item.get_detail())
        else:
            print("No item found..")
    def filter_by_type(self,item_type):
        results = [
            item for item in self.item 
            if item.item_type.lower() == item_type.lower()
        ]

        if results:
            print(f"\n========== {item_type.upper()} ITEMS ==========")
            for item in results:
                print(item.get_detail())
        else:
            print("\nNo items found for this type.")
    #filter rarity
    def filter_by_rarity(self,rarity):
        results = [
            item for item in self.item
            if item.rarity.lower() == rarity.lower()
        ]
        if results:
            print(f"\n========== {rarity.upper()} ITEMS ==========")
            for item in results:
                print(item.get_detail())  
        else:
            print("\nNo items found for this rarity.")
    #total fold
    def total_gold_value(self):
        total = sum(item.value for item in self.item)
        print("\n========== INVENTORY VALUE ==========")
        print(f"Total Gold Value: {total} gold")
        return total
    #unique category
    def unique_categories(self):
        categories = {
            item.item_type
            for item in self.item
        }
        print("\n========== UNIQUE CATEGORIES ==========")
        for category in sorted(categories):
            print(f"- {category}")
        return categories
    #nested dict
    def inventory_by_category(self):

        categorized = {}

        for item in self.item: 

            category = item.item_type

            if category not in categorized:
                categorized[category] = {
                    "count": 0,
                    "items": []
                }
            categorized[category]["count"] += 1
            categorized[category]["items"].append(
                item.name
            )
        print("\n========== INVENTORY BY CATEGORY ==========")
        for category, data in categorized.items():  
            print(f"\n{category}")
            print(f"Count: {data['count']}")

            for item_name in data["items"]:
                print(f"  - {item_name}")
        return categorized
def find_item_by_name(all_item, name):

   for item in all_item:

    if item.name.lower() == name.lower():
        return item

   return None
#main menu
def main():
    print("=" * 60)
    print("             RPG INVENTRY ENGINE           ")
    print("=" * 60)
    all_item = load_items("items.csv")  
    inventory = Inventory()  
    for item in all_item:
        inventory.add_item(item)  
    while True:
      print("="*60)
      print("              MAIN MENU            ")
      print("="*60)
      print("1:Show All Items")
      print("2:Add Item")
      print("3:Remove Item")
      print("4:Search Item by Name")
      print("5:Filter by Type")
      print("6:Filter by Rarity")
      print("7:Calculate Total Gold Value")
      print("8:Show Unique Categories")
      print("9:Show Inventory by Category")
      print("10:Exit")
      choice = input("\nEnter your choice: ").strip() 

      if choice == "1":
          inventory.show_all()  
      elif choice == "2":
          name = input("Enter Item Name to add: ").strip()
          item = find_item_by_name(all_item,name)
          if item:
              inventory.add_item(item) 
          else:
              print("This item does not exist in the item database.")
      elif choice == "3":
        name = input("Enter item name to remove: ").strip()
        inventory.remove_item(name)  
      elif choice == "4":
          name = input("Enter Item name to search: ").strip()
          inventory.search_by_name(name)  
      elif choice == "5":
          item_type = input("Enter Type (Weapon/Potion/Armor/Magic): ").strip()
          inventory.filter_by_type(item_type) 
      elif choice == "6":
          rarity = input("Enter Rarity (Common/Rare/Epic/Lendary): ").strip()
          inventory.filter_by_rarity(rarity) 
      elif choice == "7":
          inventory.total_gold_value() 
      elif choice == "8":
          inventory.unique_categories() 
      elif choice == "9":
          inventory.inventory_by_category() 
      elif choice == "10":
          print("Thanks you for using RPG Inventry Engine!")
          break 
      else:
          print("Invalid Choice.Please Select Correct Choice..")             
if __name__ == "__main__":
    main()