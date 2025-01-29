# Samsung & Apple Trade-In Price Scraper & Dashboard

## Overview
This project is designed to extract mobile phone trade-in details, including pricing and device conditions, from the **Samsung Trade-In UAE** website. It automates data extraction, cleans the scraped data, and visualizes key insights through a **Power BI dashboard**.

## Features
For a given input purchase device series and model, we follow these steps:

### **1. Web Scraping**
- Extracts trade-in data for **Samsung** and **Apple** devices.
- Captures details including **series, model, storage options, and condition-based trade-in prices**.
- Uses **Selenium** to interact with dropdowns, buttons, and webpage elements.
- Implements **error handling** for missing elements or changing webpage structures.

### **2. Data Cleaning & Storage**
- Ensures **structured and formatted data** for easy analysis.
- Cleans raw scraped data, removing inconsistencies and duplicates.
- Stores cleaned data into an **Excel file** for further processing.

### **3. Power BI Dashboard for Analysis**
A **Power BI dashboard** was developed to visualize trade-in prices, trends, and insights effectively. Key components include:
- **Top Trade-In Models:** Displays the most traded models with the highest trade-in value.
- **Average Trade-In Prices by Condition:** Shows price variations based on condition (**Flawless, Average, Broken**).
- **Average Trade-In Prices by Series:** Compares price differences across Apple and Samsung devices.
- **Trade-In Prices by Model:** Breakdown of trade-in prices across different device models.
- **Interactive Filters:** Select between Apple, Samsung S22, and S23 series for dynamic insights.

## Dependencies
### **Python Libraries Used:**
1. **Selenium** - Automates webpage interactions.
2. **Pandas** - Processes and structures scraped data.
3. **Datetime** - Handles timestamping for dataset tracking.
4. **Logging** - Captures logs for debugging and monitoring.
5. **Openpyxl** - Enables Excel file operations.

### **Browser Driver Requirement:**
- **ChromeDriver** must be installed to match the version of **Google Chrome**.
- Ensure the driver is in the system **PATH** for seamless execution.

## Setup Instructions
### **1. Install Dependencies**
```sh
pip install selenium pandas openpyxl
```

### **2. Download and Configure ChromeDriver**
a. Install **ChromeDriver** matching your **Google Chrome** version.
b. Add the downloaded **ChromeDriver** to your system's **PATH**.

### **3. Run the Script**
```sh
python samsung_trade_in_price_scraper.py
```

## Output
The script generates an **Excel file** titled:
```
Scraped_Phone_Details_<date>.xlsx
```

### **Columns in the Output File:**
- **Date**: Date of scraping.
- **Brand**: Samsung or Apple.
- **Series Name**: Device series name.
- **Model**: Device model.
- **Storage**: Storage capacity.
- **Condition**: Device condition (Flawless, Average, Broken).
- **Price**: Trade-in price.

## Scope for Improvements
### **1. Advanced Scraping Enhancements**
- **Proxy Support**: Use rotating proxies to prevent IP bans.
- **User-Agent Rotation**: Simulate different browsers to bypass detection.
- **Dynamic Brand Addition**: Allow flexible addition of new brands via configuration.

### **2. Robust Error Handling**
- Improve handling of **TimeoutException, StaleElementReferenceException**, and **NoSuchElementException**.
- Implement **retry mechanisms** for handling network failures.

### **3. Enhanced Data Analytics & Modeling**
- Perform **exploratory data analysis (EDA)** on the cleaned dataset.
- Build **predictive models** to estimate future trade-in values.
- Generate **Power BI reports** dynamically based on new datasets.

## Conclusion
This project automates the extraction of trade-in prices, refines the data, and visualizes insights through a **Power BI dashboard**. It provides valuable insights into device trade-in values across different conditions and models, aiding users in making informed decisions.

For future improvements, additional automation, error handling, and predictive analytics can further enhance its capabilities.

