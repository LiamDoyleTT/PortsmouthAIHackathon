
import csv

def is_vip(user_id):
    """
    Function for checking whether or not a user is a VIP based on their user ID

    Args: 
        user_id: The user ID str to check
    
    Returns:
        vip_status: A True/False boolean value indicating if the user is a VIP
    """

    csv_path = 'VIP.csv'
    try:
        with open(csv_path, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            print("Data")
            for row in reader:
                print(row)
                if row['UserID'].strip() == user_id and row['VIP'].strip()=='YES':
                    return True
        return False  # User ID not found
    except Exception as e:
        print(f"Error reading file: {e}")
        return False


