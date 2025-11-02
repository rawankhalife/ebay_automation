# eBay Tech Deals — Exploratory Data Analysis (EDA) Report

## **1. Methodology**
The dataset was collected using a custom Selenium-based scraper that extracted real-time tech deals from eBay.  
After cleaning the raw CSV file to handle missing and inconsistent values, a comprehensive **Exploratory Data Analysis (EDA)** was performed using Python (Pandas, Matplotlib).  

The main steps included:
- **Data Cleaning:** Removed placeholder rows (e.g., “N/A”), normalized price values, converted timestamps, and filled missing fields.
- **Time Analysis:** Grouped deals by hour to identify scraping time distribution.
- **Price & Discount Analysis:** Visualized the distribution of prices, discounts, and price relationships.
- **Shipping Analysis:** Analyzed frequency of shipping options.
- **Text Analysis:** Extracted brand/product keywords from titles.
- **Discount Ranking:** Identified the top 5 deals with the highest discount percentages.

---

## **2. Key Findings**

### **a. Time Series**
All entries initially had the same timestamp (hour 17) due to a timestamp placement error in the scraper.  
This issue was corrected by generating timestamps within the scraping loop, ensuring accurate time-based trends in future runs.

### **b. Price and Discount Patterns**
- Product prices are **highly right-skewed**, with most items priced under **\$500** and only a few reaching **\$4000**.  
- The **boxplot** confirmed multiple high-value outliers representing premium products.  
- The **scatter plot** between `original_price` and `price` showed a **strong positive correlation**, meaning higher original prices generally lead to higher sale prices.
- The **discount percentage distribution** revealed two major groups: items with minimal discounts and another group offering deep discounts between **40–70%**.

### **c. Shipping Information**
- “**Shipping info unavailable**” appeared in the majority of listings, likely due to incomplete or dynamically loaded data.  
- Only a small subset of listings included detailed shipping information such as *Free Standard Shipping* or *eBay International Shipping*.

### **d. Keyword Frequency**
- **Apple** dominated the listings, followed by **Samsung**, confirming the prevalence of mobile and accessory-related deals.  
- Other keywords like *Laptop* and *Tablet* appeared less often, while *Gimbal* was rare.  
- This indicates a dataset biased toward **portable consumer electronics**.

### **e. Price Difference**
- The majority of discounts were under **\$200**, indicating modest savings across most deals.  
- A few high-value items had discounts exceeding **\$1000**, typically premium Apple products.

### **f. Top 5 Highest Discounts**
| Rank | Product | Original ($) | Discounted ($) | Discount % |
|------|----------|---------------|----------------|-------------|
| 1 | Apple MacBook Pro 16" (2019) | 2399.00 | 389.99 | 83.74% |
| 2 | Arlo Pro 4 Camera Kit | 499.99 | 113.99 | 77.20% |
| 3 | Proscan 10.1" Tablet/DVD Combo | 139.99 | 37.99 | 72.86% |
| 4 | Sony WH-CH720N Headphones | 149.99 | 49.99 | 66.67% |
| 5 | Apple iPad Pro 5 (2021) | 1099.00 | 426.40 | 61.20% |

---

## **3. Challenges Faced**
- **Timestamp issue:** All records initially had the same hour due to static timestamp assignment.  
- **Incomplete shipping data:** Many listings lacked clear shipping details, reducing analysis accuracy.  
- **Inconsistent text structure:** Titles varied in formatting, making keyword extraction and standardization challenging.  
- **Dynamic webpage content:** Some eBay listings load elements with JavaScript, limiting Selenium’s initial scrape coverage.

---

## **4. Potential Improvements**
- Automate scraping at **regular intervals** to build a time-based trend dataset.  
- Implement **advanced text cleaning and NLP** to categorize product titles more accurately.  
- Improve scraping logic to extract structured shipping and seller information.  
- Expand keyword detection to include **more tech categories** (e.g., monitor, console, smartwatch).  
- Integrate visualization dashboards (e.g., Plotly or Power BI) for interactive insights.

---

## **5. Conclusion**
The analysis revealed that eBay tech deals are dominated by **Apple and Samsung products**, most of which are **affordable accessories or refurbished devices** with moderate to significant discounts.  
Although the dataset provides useful insights into pricing and discount behaviors, improving data completeness and temporal diversity will enable deeper, more reliable trend analysis in future runs.

