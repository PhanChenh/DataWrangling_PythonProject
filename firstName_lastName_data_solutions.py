import os
import pathlib

import pandas 

"""You are welcome to use this structure as a starting point, or you can start from scratch.

The prefixed `get_` methods should not need any adjustment to read in the data.
Your solutions should be mostly contained within the prefixed `generate_` methods, and the `data_investigation()`

"""

# --- Fill in your details here ---
FIRST_NAME = "Phan"
LAST_NAME = "Chenh"

# Gets current path
CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = os.path.join(CURRENT_DIR, "data")


def get_exchange_data():
    exchange_data = pandas.read_csv(
        os.path.join(DATA_DIR, "exchange.data"),
        delimiter="|",
    )
    return exchange_data


def get_stock_list():
    stock_list = pandas.read_csv(os.path.join(DATA_DIR, "stock.data"))
    return stock_list


def get_security_master():
    security_master = pandas.read_csv(
        os.path.join(DATA_DIR, "strong_oak_security_master.csv")
    )
    return security_master


def get_attributes():
    attributes = pandas.read_csv(os.path.join(DATA_DIR, "attributes.data"))
    return attributes


def generate_security_upload(
    security_master, full_stock_data, exchange_data
) -> pandas.DataFrame:
    """
    Generates the security upload DataFrame by merging and filtering relevant securities data.
    
    Inputs:
    - security_master: DataFrame containing security master data.
    - full_stock_data: DataFrame containing stock list data.
    - exchange_data: DataFrame containing exchange data.

    Function do: 
    - Merge tables (left)
    - Filter valid securities (either QUEUESIP or Symbol must be populated)
    - Check MIC valid - not null (It is important to include `MIC` as part of the identifiers, as the same security listed on different exchanges may return different results when querying data vendors)
    - Handle duplicate (RequestId is a unique value that is used to match to the data vendor)
    - Assign `EulerId`
    
    Output:
    - security_upload: DataFrame with columns [EulerId, MIC, QUEUESIP, Symbol, RequestId]
    
    """

    # Merge security master with stock data
    merged_data = pandas.merge(security_master, full_stock_data, on='QUEUESIP', how='outer')
    
    # Merge with exchange data to check MIC valid
    merged_data2 = pandas.merge(merged_data, exchange_data, on='MIC', how='outer')

    # Filter valid securities (either QUEUESIP or Symbol must be populated)
    valid_securities = merged_data2[
        (merged_data2['QUEUESIP'].notna()) | (merged_data2['Symbol'].notna())
    ]

    # Filter out rows where MIC is NaN to get valid MIC
    filtered_MIC = valid_securities.dropna(subset=['MIC'])

    # Handle or remove duplicates (keeping the first occurrence)
    filtered_data = filtered_MIC.drop_duplicates(subset=['RequestId'], keep='first')

    # Assign EulerId (as an iterator starting at 1)
    valid_data = filtered_data.reset_index(drop=True)
    valid_data['EulerId'] = valid_data.index + 1

    # Select and reorder columns for the final upload
    security_upload = valid_data[['EulerId', 'MIC', 'QUEUESIP', 'Symbol', 'RequestId']]

    return security_upload



def generate_attribute_upload(
    security_upload, attribute_data, exchange_data
) -> pandas.DataFrame:
    """
    Generates the relevant attributes upload DataFrame by merging and filtering relevant data.
    
    Inputs:
    - security_upload: Dataframe from above
    - attribute_data: DataFrame containing attributes data.
    - exchange_data: DataFrame containing exchange data.

    Function do: 
    - Merge tables (inner)
    - `EulerId` should correspond to the values generated from the first response.
    - Exchange location should be given as the combination of Exchange Country and City (i.e. `{country} - {city}`).
    - Change 'name' column in exchange table to Exchange Name
    - The attributes the client want are "Asset Class", "Inception Date", "Exchange Name", "Exchange Location", "Security Name", "Strong Oak Identifier", and "Return Since Inception"
    - the platform requires these to be uploaded in *long format*.
    - no null values in the `AttributeValue` column

    Output:
    - attribute_upload: DataFrame with columns [EulerId, AttributeName, AttributeValue]
    """

    # Merge attributes with securities to link attributes with EulerId
    attr_securities = pandas.merge(attribute_data, security_upload, on='RequestId', how='inner')

    # Merge with exchange data to get exchange information
    attr_securities2 = pandas.merge(attr_securities, exchange_data, on='MIC', how='inner')

    # Create Exchange Location attribute by combining domicile and city
    attr_securities2['Exchange Location'] = attr_securities2['domicile'] + ' - ' + attr_securities2['city']

    # Create DataFrame for Exchange Name attribute
    attr_securities2['Exchange Name'] = attr_securities2['name']

    # Filter only the required attributes
    required_attributes = ["Asset Class", "Inception Date", "Exchange Name", "Exchange Location", "Security Name", "Return Since Inception"]

    # Create the long format DataFrame
    long_format = pandas.melt(
        attr_securities2,
        id_vars=['EulerId'],
        value_vars=required_attributes,
        var_name='AttributeName',
        value_name='AttributeValue'
    )

    # Drop rows with null values in 'AttributeValue'
    attribute_upload = long_format.dropna(subset=['AttributeValue'])

    # Sort by 'EulerId' 
    attribute_upload = attribute_upload.sort_values(by='EulerId')
    
    # Reset index
    attribute_upload = attribute_upload.reset_index(drop=True)

    return attribute_upload


def data_investigation(security_upload, attribute_upload):
    """
    Conducts an investigation of the data to ensure correctness and consistency.
    
    Inputs:
    - security_upload: DataFrame containing security upload data.
    - attribute_upload: DataFrame containing attribute upload data.
    
    Outputs:
    - Prints out key metrics and checks for both DataFrames to ensure they meet the expected criteria.
    """
    
    # Print summary statistics for security upload
    print("Security Upload Data Summary:")
    print("Total Records:", len(security_upload))
    print("Unique EulerIds:", security_upload['EulerId'].nunique())
    print("Unique RequestIds:", security_upload['RequestId'].nunique())
    print("Missing EulerId Values:", security_upload['EulerId'].isna().sum())
    print("Missing RequestId Values:", security_upload['RequestId'].isna().sum())
    print("\n")

    # Print summary statistics for attribute upload
    print("Attribute Upload Data Summary:")
    print("Total Records:", len(attribute_upload))
    print("Unique EulerIds:", attribute_upload['EulerId'].nunique())
    print("Unique Attribute Names:", attribute_upload['AttributeName'].nunique())
    print("Missing Attribute Values:", attribute_upload['AttributeValue'].isna().sum())
    print("\n")

    # Check for any EulerId mismatches between security upload and attribute upload
    attribute_euler_ids = set(attribute_upload['EulerId'].unique())
    security_euler_ids = set(security_upload['EulerId'].unique())
    
    missing_in_attributes = security_euler_ids - attribute_euler_ids
    missing_in_security = attribute_euler_ids - security_euler_ids
    
    if missing_in_attributes:
        print(f"EulerIds present in security upload but missing in attribute upload: {missing_in_attributes}")
    if missing_in_security:
        print(f"EulerIds present in attribute upload but missing in security upload: {missing_in_security}")
    print("\n")

    # Check for duplicates in attribute upload
    duplicate_attributes = attribute_upload[attribute_upload.duplicated(subset=['EulerId', 'AttributeName'], keep=False)]
    if not duplicate_attributes.empty:
        print("Duplicate records in attribute upload based on 'EulerId' and 'AttributeName':")
        print(duplicate_attributes)
    else:
        print("No duplicates found in attribute upload.")
    print("\n")

    # Check for any unexpected attribute names
    expected_attributes = {"Asset Class", "Inception Date", "Exchange Name", "Exchange Location", "Security Name", "Strong Oak Identifier", "Return Since Inception"}
    actual_attributes = set(attribute_upload['AttributeName'].unique())
    
    unexpected_attributes = actual_attributes - expected_attributes
    if unexpected_attributes:
        print(f"Unexpected attribute names found: {unexpected_attributes}")
    else:
        print("All attribute names are as expected.")
    print("\n")

    # Summary of missing values
    missing_values_summary = {
        'Security Upload': {
            'EulerId': security_upload['EulerId'].isna().sum(),
            'RequestId': security_upload['RequestId'].isna().sum()
        },
        'Attribute Upload': {
            'AttributeValue': attribute_upload['AttributeValue'].isna().sum()
        }
    }
    print("Summary of Missing Values:")
    for data_type, counts in missing_values_summary.items():
        print(f"{data_type}:")
        for col, count in counts.items():
            print(f"  {col}: {count} missing")
    print("\n")



def main():
    security_master = get_security_master()
    full_stock_data = get_stock_list()
    exchange_data = get_exchange_data()

    # * Loading Securities into the platform * #

    # get security data...
    security_upload = generate_security_upload(
        security_master=security_master,
        full_stock_data=full_stock_data,
        exchange_data=exchange_data,
    )

    # * Uploading Attributes * #

    attribute_data = get_attributes()

    # get attribute data...
    attribute_upload = generate_attribute_upload(
        security_upload=security_upload,
        attribute_data=attribute_data,
        exchange_data=exchange_data,
    )

    # solutions go here.

    security_upload.to_csv(
        os.path.join(CURRENT_DIR, f"{FIRST_NAME}_{LAST_NAME}_section1.csv")
    )
    attribute_upload.to_csv(
        os.path.join(CURRENT_DIR, f"{FIRST_NAME}_{LAST_NAME}_section2.csv")
    )

    data_investigation(
        security_upload=security_upload, attribute_upload=attribute_upload
    )


if __name__ == "__main__":
    main()


