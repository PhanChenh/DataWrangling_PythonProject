# Project Title: Data Wrangling Project - Securities Upload for Strong Oak Security Management

## Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Objective](#objective)
- [Analysis Approach](#analysis-approach)
- [Key Findings](#key-findings)
- [How to run code](#how-to-run-code)
- [Technologies Used](#technologies-used)
- [Results](#results)
- [Recommendation](#recommendation)
- [Contact](#contact)

## Overview

Strong Oak Security Management has outsourced their security management to Euler, a financial data platform. Euler’s data engineering team is responsible for loading, processing, and validating security data from Strong Oak’s security master file.

## Dataset

The project uses the following datasets:
- [attributes.data](Data/attributes.data): Includes various security attributes.
- [exchange.data](Data/exchange.data): Provides exchange details like name and location.
- [stock.data](Data/stock.data): Contains stock-related information, possibly including Symbol and QUEUESIP.
- [strong_oak_security_master.csv](Data/strong_oak_security_master.csv): Contains the raw list of securities.

These datasets contain information about securities, attributes, and exchanges, necessary for the validation and upload process.

## Objective
The primary goal of this project is to clean, validate, and transform the security data to fit Euler’s proprietary security management platform. The process involves:
1. Identifying and filtering valid securities.
2. Uploading attributes in the required format.
3. Minimizing missing data where possible.

## Analysis Approach
1. Loading Securities into the Platform:
- Extract relevant security identifiers: MIC, QUEUESIP, Symbol, RequestId.
- Assign a unique EulerId to each security.
- Ensure at least one of QUEUESIP or Symbol is populated.
- Minimize null values in QUEUESIP and Symbol.
- Save the cleaned securities data in {firstName}_{lastName}_section1.csv.

2. Uploading Attributes:

- Extract security attributes from multiple sources.
- Convert data to a long format with columns: EulerId, AttributeName, AttributeValue.
- Ensure no null values exist in AttributeValue.
- Save the attributes dataset in {firstName}_{lastName}_section2.csv.

**Noted:** For detail steps, please view [detail file](Detail_Steps_README.md)

## Key Findings

- Some securities in the master file were invalid due to missing identifiers or being inactive.
- Merging data from multiple sources introduced inconsistencies that needed filtering.
- Some false-positive matches were identified and removed.
- The exchange.data file provided necessary location data for exchange names.

## How to run code

1. Ensure all required datasets are stored in the /data directory.
2. Install dependencies: pip install pandas os pathlib.
3. Run the Python script that processes the data:
```
python firstName_lastName_data_solutions.py
```
- The output csv files will be saved in the specified directory.

## Technologies Used
- Programming Language: Python
- Libraries: pandas, os, pathlib
- File Formats: csv, .data
- Data Cleaning & Transformation: Pandas DataFrame operations

## Results
- Breakdown of missing data before and after processing.

![before](https://github.com/user-attachments/assets/e6db559f-a352-4ccd-af85-5d4ae5e56b63)

Figure 1: Validation and Breakdown Before Processing

There are presence of missing data in stock (RequestId, Symbol, QUEUESIP, MIC), strong_oak_security_master (Ticker, QUEUESIP, Strong Oak Identifier), and attributes data (Asset Class, Inception Date, Return Since Inception).

![after](https://github.com/user-attachments/assets/ed082976-9a04-44ff-ac98-ebfe65ae7702)

Figure 2: Validation and Breakdown After Processing

- No missing values for certain columns (e.g., EulerId, MIC).
- No duplicate EulerId or RequestId after processing.
- No invalid MIC values, indicating that only valid MICs are in the dataset.
- No issues with Exchange Location format or invalid AttributeName.

## Recommendation
- Automate the validation process to improve efficiency.
- Implement a robust error-handling mechanism for invalid securities.
- Maintain a historical record of uploaded securities for future reference.

## Contact

📧 Email: pearriperri@gmail.com

🔗 [LinkedIn](https://www.linkedin.com/in/phan-chenh-6a7ba127a/) | Portfolio
