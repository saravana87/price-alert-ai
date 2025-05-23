# Price Alert AI

📺 Watch demo on YouTube:  
https://youtu.be/YctOyy0DB28

A simple price update and alert system using **Google Sheets** and **Google Apps Script**. The script detects changes in product prices and sends email alerts to users when the price changes, with a **10% markup** applied to your internal price.

## Features

- Monitors price changes in Google Sheets.
- Sends email alerts when prices change.
- Applies a **10% markup** to your internal price.
- Handles different **currencies**.

## Setup

1. Create a Google Sheet with columns for `SKU`, `Product`, `Brand`, `Base Price`, `Currency`, `Inventory`, `Last Price`, and `Last Updated`.
2. Paste the provided Apps Script code into the Google Sheets script editor.
3. Set up a time-driven trigger to check for price changes periodically.
4. Ensure email notifications are configured.

## Development

- **Platform**: Google Sheets + Google Apps Script

## License

MIT License
