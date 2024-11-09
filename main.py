import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
import time

# Telegram bot configuration
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your bot token
CHAT_ID = "YOUR_CHAT_ID"  # Replace with your chat ID
bot = Bot(token=TELEGRAM_TOKEN)

# Google Sheets configuration
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("telegram-bot-441211-141a516bc81f.json", scope)
client = gspread.authorize(creds)

# Access the spreadsheet
spreadsheet = client.open("Accbox Spotify Accounts")  # Replace with your spreadsheet name

def main():
    while True:
        check_expired_accounts()  # Your function to check and alert on expired accounts
        time.sleep(3600)  # Wait for 1 hour (3600 seconds)
def check_expired_accounts():
    # Loop through each worksheet in the spreadsheet
    for worksheet in spreadsheet.worksheets():
        data = worksheet.get_all_records()  # Get all rows in the current sheet
        
        # Check each row for expiration
        expired_accounts = []
        for row in data:
            # Convert "Remaining days" to an integer, default to a high number if conversion fails
            try:
                remaining_days = int(row.get("Remaning days", 1))
            except ValueError:
                continue  # Skip rows where "Remaining days" is not a valid number
            
            # Check if the account is expired
            if remaining_days <= 0:
                expired_accounts.append(row)
        
        # Send alert for each expired account
        if expired_accounts:
            message = f"Expired accounts in sheet '{worksheet.title}':\n"
            for account in expired_accounts:
                message += f"\nEmail: {account['Email']}\nPlan: {account['Plan']}\nExpired {abs(remaining_days)} days ago\n"
            bot.send_message(chat_id=CHAT_ID, text=message)

# Run the function to check for expired accounts
main()
