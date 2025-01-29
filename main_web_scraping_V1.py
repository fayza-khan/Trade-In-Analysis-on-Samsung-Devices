# import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from datetime import datetime
import pandas as pd
import time


class WebScraper:
    def __init__(self, purchase_device_model, selected_model):
        """
        Class to extract the trade-in details for a mobile phone against 2 brands (Samsung and Apple)
        Parameters: purchase_device_model (str): The device model to be selected
                  : selected_model (str): The specific model to be selected 
        """
        self.purchase_device_model = purchase_device_model
        self.selected_model = selected_model
        self.data = []
        self.brands = ['Samsung','Apple']
        self.driver = None

    def wait_and_click(self, xpath, timeout=20):
        """
        Utility function to wait for an element to be clickable and clicks it
        Parameters: xpath (str): The XPath of the element to be clicked.
                  : timeout (int): Maximum time to wait for the element to be clickable.
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        except Exception as e:
            print(f"Error identified as : {e}")
            
        
    def constant_starting_steps(self, brand):
        """
        Utility function to perform the constant starting steps
        Parameters: brand (str): The brand name ('Samsung' or 'Apple')
        """
        brands_xpath = {'Samsung': "https://prod-cdn.northladder.com/brand/1683051338736.png",
                        'Apple': "https://prod-cdn.northladder.com/brand/1613997248411.jpeg"}
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            self.driver.get("https://www.samsungtradein.ae/ae-en/#start-evaluation")

            self.wait_and_click('//span[text()="Mobile Phones"]') # click on mobile phones
            self.wait_and_click(f"//span[text()='{self.purchase_device_model}']") # click on the purchase device model
            self.wait_and_click(f"//span[text()='{self.selected_model}']") # click on the selected model
            element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "custom-category-item")))
            self.driver.execute_script("arguments[0].click();", element) # click on the mobile phone option for trade-in
            # select brand - Samsung or Apple
            image_src = brands_xpath[brand]
            print(f"Extracting details for {brand}")
            time.sleep(3)  
            image_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//img[@src='{image_src}']"))
            )
            self.driver.execute_script("arguments[0].click();", image_element)
            
        except Exception as e:
            print(f"Error identified as while clicking {brand}: {e}")

    def get_elements(self, class_name, element_type):
        """
        Utility function to retrieve elements by class name and logs their count.
        Parameters: class_name (str): The class name of the elements to be retrieved.
                  : element_type (str): The type of elements being retrieved (e.g., 'series', 'model').
        Output: elements (list): List of WebElement objects if found, else None.
        """
        try:
            time.sleep(3)
            elements = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
            )
            print(f"Count of total {element_type}: {len(elements)}")
            return elements
        except Exception as e:
            print(f"Error identified while clicking {element_type} as : {e}")
            return None
        
    def select_series(self):
        """
        Utility function to select series elements
        """
        return self.get_elements("custom-model-item", "series")

    def select_subseries(self):
        """
        Utility function to select subseries elements
        """
        return self.get_elements("custom-dynamic-tile-item", "subseries")

    def select_model(self):
        """
        Utility function to select model elements
        """

        return self.get_elements("custom-dynamic-tile-item", "model")

    def select_storage(self):
        """
        Utility function to select storage elements
        """
        return self.get_elements("custom-dynamic-tile-item", "storage")

    def select_condition(self):
        """
        Utility function to select condition elements
        """
        return self.get_elements("custom-store-drop-off-item", "condition")


    """
    Logic for iterating to scrape every detail
    1. USE trackers (series_tracker, storage_tracker, condition_tracker, etc.) to keep track of the current position in each selection
    2. It iterates through series, storage, and condition options.
    3. After each selection, it retrieves the price and appends the data to a list.
    4. It then resets the selections to continue with the next combination.

    REASON for doing: Because the URL does not get change irrespective of selecting or unselecting anything however the landing page html changes
    """

    def scrape_apple_details(self, brand='Apple'):
        """
        Utility function to select elements for Apple
        """
        series_tracker = 0
        for series_element in self.select_series():
            if series_tracker == len(self.select_series()): break
            series_element = self.select_series()[series_tracker]
            series_text = series_element.text
            self.driver.execute_script("arguments[0].click();", series_element)
            storage_tracker = 0
            for storage_element in self.select_storage():
                if storage_tracker == len(self.select_storage()): break
                storage_element = self.select_storage()[storage_tracker]
                storage_text = storage_element.text
                self.driver.execute_script("arguments[0].click();", storage_element)
                condition_tracker = 0
                for condition_element in self.select_condition():
                    if condition_tracker == len(self.select_condition()): break
                    condition_element = self.select_condition()[condition_tracker]
                    condition_text = condition_element.text
                    self.driver.execute_script("arguments[0].click();", condition_element)
                    price_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='md:nl-widget-text-right']"))
                    )
                    price = price_element.text

                    self.data.append([
                        datetime.now().strftime("%d/%m/%Y"),
                        1,
                        "Apple",
                        "Apple",
                        series_text,
                        storage_text,
                        condition_text,
                        price
                    ])
                    self.constant_starting_steps(brand)
                    condition_tracker += 1
                    series_element = self.select_series()[series_tracker]
                    self.driver.execute_script("arguments[0].click();", series_element)
                    storage_element = self.select_storage()[storage_tracker]
                    self.driver.execute_script("arguments[0].click();", storage_element)
                self.constant_starting_steps(brand)
                storage_tracker += 1
                series_element = self.select_series()[series_tracker]
                self.driver.execute_script("arguments[0].click();", series_element)
            self.constant_starting_steps(brand)
            series_tracker += 1
            
    def scrape_samsung_details(self, brand='Samsung'):
        """
        Utility function to select elements for Samsung
        """
        series_tracker = 0
        for series_element in self.select_series():
            if series_tracker == len(self.select_series()): break
            series_element = self.select_series()[series_tracker]
            series_text = series_element.text
            self.driver.execute_script("arguments[0].click();", series_element)
            
            subseries_tracker = 0
            for subseries_element in self.select_subseries():
                if subseries_tracker == len(self.select_subseries()): break
                subseries_element = self.select_subseries()[subseries_tracker]
                subseries_text = subseries_element.text
                self.driver.execute_script("arguments[0].click();", subseries_element)
                
                model_tracker = 0
                for model_element in self.select_model():
                    if model_tracker == len(self.select_model()): break
                    model_element = self.select_model()[model_tracker]
                    model_text = model_element.text
                    self.driver.execute_script("arguments[0].click();", model_element)
                    
                    storage_tracker = 0
                    for storage_element in self.select_storage():
                        if storage_tracker == len(self.select_storage()): break
                        storage_element = self.select_storage()[storage_tracker]
                        storage_text = storage_element.text
                        self.driver.execute_script("arguments[0].click();", storage_element)
                        
                        condition_tracker = 0
                        for condition_element in self.select_condition():
                            if condition_tracker == len(self.select_condition()): break
                            condition_element = self.select_condition()[condition_tracker]
                            condition_text = condition_element.text
                            self.driver.execute_script("arguments[0].click();", condition_element)
                            
                            price_element = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='md:nl-widget-text-right']"))
                            )
                            price = price_element.text

                            self.data.append([
                                datetime.now().strftime("%d/%m/%Y"),
                                0,
                                series_text,
                                subseries_text,
                                model_text,
                                storage_text,
                                condition_text,
                                price
                            ])
                            print(self.data)
                            
                            self.constant_starting_steps(brand)
                            condition_tracker += 1
                            
                            # Reset selections
                            series_element = self.select_series()[series_tracker]
                            self.driver.execute_script("arguments[0].click();", series_element)
                            subseries_element = self.select_subseries()[subseries_tracker]
                            self.driver.execute_script("arguments[0].click();", subseries_element)
                            model_element = self.select_model()[model_tracker]
                            self.driver.execute_script("arguments[0].click();", model_element)
                            storage_element = self.select_storage()[storage_tracker]
                            self.driver.execute_script("arguments[0].click();", storage_element)
                        
                        self.constant_starting_steps(brand)
                        storage_tracker += 1
                        
                        # Reset selections
                        series_element = self.select_series()[series_tracker]
                        self.driver.execute_script("arguments[0].click();", series_element)
                        subseries_element = self.select_subseries()[subseries_tracker]
                        self.driver.execute_script("arguments[0].click();", subseries_element)
                        model_element = self.select_model()[model_tracker]
                        self.driver.execute_script("arguments[0].click();", model_element)
                    
                    self.constant_starting_steps(brand)
                    model_tracker += 1
                    
                    # Reset selections
                    series_element = self.select_series()[series_tracker]
                    self.driver.execute_script("arguments[0].click();", series_element)
                    subseries_element = self.select_subseries()[subseries_tracker]
                    self.driver.execute_script("arguments[0].click();", subseries_element)
                
                self.constant_starting_steps(brand)
                subseries_tracker += 1
                
                # Reset selections
                series_element = self.select_series()[series_tracker]
                self.driver.execute_script("arguments[0].click();", series_element)
            
            self.constant_starting_steps(brand)
            series_tracker += 1


    def web_scraping_brand_level(self, brand):
        """
        Utility function to scrape phone details at the brand level based on series, model, and conditions.
        Parameter: brand (str): The brand name ('Samsung' or 'Apple')
        """
        try:
            if brand == "Samsung" and self.driver is not None:
                self.scrape_samsung_details(brand)
            elif brand == "Apple" and self.driver is not None:
                self.scrape_apple_details(brand)
        except Exception as e:
            print(f"Error faced: {e}")            
    
    def main(self):
        """
        Main function to initiate the scraping process and save data to Excel.
        """
        for brand in self.brands:
            print(f"Start scraping for {brand} brand")
            # hit the constant steps
            self.constant_starting_steps(brand)
            # hit the series step        
            self.web_scraping_brand_level(brand)
        if len(self.data) != 0:
            df = pd.DataFrame(self.data, columns=['Date', 'Brand', 'Series nm', 'Series', 'Model', 'Storage', 'Condition', 'Price (in AED)'])
            df.to_excel(f"Scraped_Phone_Details_{datetime.now().strftime("%d-%m-%Y")}.xlsx", engine='openpyxl', index=False)


if __name__ == "__main__":
    purchase_device_model = "Galaxy Z Fold4 5G | Flip4 5G" # input for purchase device model
    selected_model = "Galaxy Z Fold4 5G" # input for selected model
    web_scraper = WebScraper(purchase_device_model, selected_model)
    web_scraper.main()