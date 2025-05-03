function checkPriceChanges() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet1");
  const data = sheet.getDataRange().getValues();

  // Loop through each row of the data (starting from row 2, index 1)
  for (let i = 1; i < data.length; i++) {
    const [sku, product, brand, basePrice, currency, inventory, lastPrice] = data[i];
    
    // Check if the price has changed
    if (basePrice !== lastPrice) {
      // Get user email based on SKU (or logic based on brand, location, etc.)
      const userEmail = getUserEmail(sku); // Simple placeholder

      // Calculate new price (+10% markup)
      const newPrice = basePrice * 1.1;

      // Send email with price update
      sendPriceEmail(userEmail, sku, product, brand, basePrice, newPrice, currency);

      // Update the last price and last updated columns in the sheet
      sheet.getRange(i + 1, 6).setValue(basePrice); // Update Last Price
      sheet.getRange(i + 1, 7).setValue(new Date()); // Update Last Updated
    }
  }
}

function sendPriceEmail(email, sku, product, brand, basePrice, finalPrice, currency) {
  const subject = `📦 Price Update for ${product} (${brand}) [${sku}]`;
  const body = `Hello,

The base price for ${product} by ${brand} (SKU: ${sku}) has changed.
Base Price: ${currency} ${basePrice}
Your Price (+10%): ${currency} ${finalPrice.toFixed(2)}

Thanks,
Your Shop Bot`;

  // Send the email using Gmail service
  MailApp.sendEmail(email, subject, body);
}

function getUserEmail(sku) {
  // Placeholder function to map SKU to user email
  // In a real setup, you could map this via another sheet or database
  return "user@gmail.com"; // Change to dynamic email lookup if needed
}
