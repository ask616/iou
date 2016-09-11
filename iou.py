import json
import os.path
import sys

"""
{
    total_owed: [
        {
            "name": "kevin",
            "amount": 13.13
        },...
    ],
    transaction_history: [
        {
            "name": "kevin",
            "amount": 135.13,
            "memo": "a;kdfa;sdgasgd"
        },...
    ]
}
"""
data_file_name = ".iou.data.json"

def initDataFile():
    data = { "total_owed": [], "transaction_history": [] }
    with open(data_file_name, 'w') as data_file:
        json.dump(data, data_file)

    return data

def getDataFile():
    if not os.path.exists("./" + data_file_name):
        return initDataFile()
    
    with open(data_file_name) as data_file:
        data = json.load(data_file)
        return data

def writeDataFile(data):
    with open(data_file_name, 'w') as data_file:
        json.dump(data, data_file)

def recalculateAllTotals(transaction_history, transaction_totals):
    total_owed = map(lambda t: { "name": t[0], "amount": t[1] }, transaction_totals.items())
    print("Data recalculated, proceeding...")
    return { total_owed: total_owed, transaction_history: transaction_history }

def verifyData(data_file):
    transaction_totals = {}
    
    for transaction in data_file["transaction_history"]:
        if transaction["name"] in transaction_totals:
            transaction_totals[transaction["name"]] += transaction["amount"]
        else:
            transaction_totals[transaction["name"]] = transaction["amount"]
   
    for total in data_file["total_owed"]:
        if not total["amount"] == transaction_totals[total["name"]]:
            print("Corrupted data detected, recalculating...")
            return recalculateAllTotals(data_file["transaction_history"], transaction_totals)
  
    return data_file
 
def new_transaction(data):
    transaction_info = input("Enter transaction details: ")   

    user_owed = not transaction_info[0].lower() == "i"
   
    if user_owed:
        # does not start with "I owe"
        if not "owes me" in transaction_info or not "$" in transaction_info or not "for" in transaction_info:
            print("Invalid input, please try again.")
            return data
        name = transaction_info.split("owes me")[0].strip().title()
        amount = transaction_info.split("$")[1].split("for")[0].strip()
        memo = transaction_info.split("for")[1].strip()

    else:
        # starts with "I owe"
        if not "I owe" in transaction_info or not "$" in transaction_info or not "for" in transaction_info:
            print("Invalid input, please try again.")
            return data

        transaction_rest = transaction_info.split("I owe")[1].strip()
        name = transaction_rest.split("$")[0].strip().title()
        amount = transaction_rest.split("$")[1].split("for")[0].strip()
        memo = transaction_rest.split("for")[1].strip()

    try:
        amount = float(amount) if user_owed else -1 * float(amount)
    except:
        print("There was an error, please try again.")
        return data
    
    new_transaction = { "name": name, "amount": amount, "memo": memo }
    data["transaction_history"].insert(0, new_transaction)

    total_entry = [entry for entry in data["total_owed"] if entry["name"].lower() == name.lower()]

    if len(total_entry):
        total_entry[0]["amount"] += amount
    else:
        new_total = { "name": name, "amount": amount }
        data["total_owed"].insert(0, new_total)
    
    return data

def get_totals(data, args):
    if not len(args):
        for summary in data["total_owed"]:
            if summary["amount"] > 0:
                print(summary["name"] + " owes you $" + str(summary["amount"]))
            elif summary["amount"] < 0:
                print("You owe " + summary["name"] + " $" + str(abs(summary["amount"])))
    else:
        name_search = " ".join(args).strip()
        for summary in data["total_owed"]:
            if name_search.lower() == summary["name"].lower():
                if summary["amount"] > 0:
                    print(summary["name"] + " owes you $" + str(summary["amount"]))
                elif summary["amount"] < 0:
                    print("You owe " + summary["name"] + " $" + str(abs(summary["amount"])))
                else:
                    print("You don't owe " + summary["name"] + " anything")
                return None
        print(args[0] + " was not found.")
        return None

def get_history(data, args):
    if not len(args):
        for transaction in data["transaction_history"]:
            if transaction["amount"] > 0:
                print(transaction["name"] + " owed you $" + str(transaction["amount"]) + " for " + transaction["memo"])
            elif transaction["amount"] < 0:
                print("You owed " + transaction["name"] + " $" + str(abs(transaction["amount"])) + " for " + transaction["memo"])
    else:
        name_search = " ".join(args).strip()
        for transaction in data["transaction_history"]:
            if name_search.lower() == transaction["name"].lower():
                if transaction["amount"] > 0:
                    print(transaction["name"] + " owed you $" + str(transaction["amount"]) + " for " + transaction["memo"])
                elif transaction["amount"] < 0:
                    print("You owed " + transaction["name"] + " $" + str(abs(transaction["amount"])) + " for " + transaction["memo"])

def controller(args):
    data_file = getDataFile()
    data_file = verifyData(data_file)

    if args[0] == "new":
        data_file = new_transaction(data_file)
        writeDataFile(data_file)
    elif args[0] == "summary":
        get_totals(data_file, args[1:])
    elif args[0] == "history":
        get_history(data_file, args[1:])
    else:
        print("Sorry, command was unrecognized. Try again?")

if __name__ == "__main__":
    controller(sys.argv[1:])
