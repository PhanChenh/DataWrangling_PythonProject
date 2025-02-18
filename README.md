# Project Title: Data Wrangling Project - Securities Upload for Strong Oak Security Management

## Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Objective](#objective)
- [Analysis Approach](#analysis-approach)
- [Association Rule Metrics](#Association-Rule-Metrics)
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
- [attributes.data](Data/attributes.data)
- [exchange.data](Data/exchange.data)
- [stock.data](Data/stock.data)
- [strong_oak_security_master.csv](Data/strong_oak_security_master.csv)

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

# How to run code

1. Ensure all required datasets are stored in the /data directory.
2. Install dependencies: pip install pandas numpy.
3. Run the Python script that processes the data:
```python
python process_securities.py
```
- The output CSV files will be saved in the specified directory.

## Technologies Used
- Programming Language: Python
- Libraries: pandas, numpy
- File Formats: csv, .data
- Data Cleaning & Transformation: Pandas DataFrame operations

## Results & Visualizations
- Summary statistics of securities uploaded.
- Distribution of valid vs. invalid securities.
- Breakdown of missing data before and after processing.

## Recommendation
- Automate the validation process to improve efficiency.
- Implement a robust error-handling mechanism for invalid securities.
- Maintain a historical record of uploaded securities for future reference.

------------

## Project Overview, Background & Objectives:

Dataset: attributes.data, exchange.data, stock.data, and strong_oak_security_master.csv

As a data engineer at a small company called Euler, and you work with financial data. Primarily you are involved in maintaining lists of securities for clients, where securities trade on Stock Exchanges. One of your clients, "Strong Oak Security Management" has realised they need to outsource their security management, and they admit that their data is quite the mess. At Euler you have a platform to manage securites, so your job is to take their list of securities, and load it into Euler's proprietary security management platform.

This load is a multi-step process, firstly identifying valid securites, then uploading attributes for these, and then answering questions provided by the client. Securities may not be valid for numerous reasons such as no longer being traded on an exchange, and we are unable to load these securities. Ensure you read through this full document, including the notes section before beginning, and understand the requirements for each section.

## Loading Securities into the platform 

To load the securities into the platform you need the following identifiers:
`MIC, QUEUESIP, Symbol, RequestId` where one of `QUEUESIP` or `Symbol` must be populated. It is important to include `MIC` as part of the identifiers, as the same security listed on different exchanges may return different results when querying data vendors.
Each of these will be assigned an `EulerId`, which should be an iterator starting at 1, that is the first security uploaded will be 1, the second 2, and the *n*th security designated n.
An example csv upload file would be:

```csv
EulerId,MIC,QUEUESIP,Symbol,RequestId
1,XNYS,0x5f4120,ABB,654
2,XNAS,,BGT,2045
```

We want to maximise the number of securities we can upload from the clients "Security Master" (located in `data/strong_oak_security_master.csv`), but we cannot upload a security without one of `QUEUESIP` or `Symbol`. i.e., `QUEUESIP` may be null as long as a `Symbol` is provided.

* The client wants to minimise the number of null values in `QUEUESIP` and `Symbol`.

* Provide us with your generated upload in a csv format, named `{firstName}_{lastName}_section1.csv`.

* Files required: `stock.data`, `exchange.data`, `strong_oak_security_master.csv`.

### Notes

Consider the following (without needing to communicate these in your response):

* What are some issues you encountered in this process and how did you overcome them?
* How many merges did your solution require?
* Did you find many false positive matches that you had to filter out?

## Uploading Attributes

Next, relevant attributes need to be uploaded. For explicitness, the platform requires these to be uploaded in *long format*. The exact format to be uploaded requires 3 columns: `EulerId, AttributeName, AttributeValue`. There should be no null values in the `AttributeValue` column. An example csv upload considering a subset of the attributes would be:

```csv
EulerId,AttributeName,AttributeValue
1,Asset Class,International Equity
1,Inception Date,2010-08-09
1,Return Since Inception,0.0664140167
2,Asset Class,International Equity
2,Return Since Inception,-0.0746303434
```

The attributes the client want are "Asset Class", "Inception Date", "Exchange Name", "Exchange Location", "Security Name", "Strong Oak Identifier", and "Return Since Inception".
This data should be sourced from the several `.data` files, and the `EulerId` should correspond to the values generated from the first response.

* Exchange location should be given as the combination of Exchange Country and City (i.e. `{country} - {city}`).

* Provide us with your generated upload in a csv format, named `{firstName}_{lastName}_section2.csv`.

* Files required: `attributes.data`, `exchange.data`, `{firstName}_{lastName}_section1.csv` (or just use the outputted data from section 1)

## Notes and Comments

* We recommend using any pandas however you should prioritise correctness of your responses over utilising pandas.
* RequestId is a unique value that is used to match to the data vendor (the supplier of this data, where data is collected from on a daily basis to maintain the securities)
* Each row in the Stock List is a single security, and will have a unique QUEUESIP and Symbol
* Ticker and Symbol are the same thing
* Ensure that code is well commented, and use docstrings where appropriate
* Code cleanliness will be considered. It should be clear where the solution to section 1 ends and section 2 begins for example.
* All data required is provided in `/data` however, you are welcome to access the internet to better understand the data set.
* QUEUESIP is a made up identifier.
