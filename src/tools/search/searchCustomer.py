from tools.registry import register_tool
import pandas as pd

@register_tool(
    name="getCustomerById",
    description="Returns a customer by their ID"
)
def getCustomerById(customer_id):
    """
    Retrieves a customer by their ID from the CSV file.

    Args:
        customer_id (int): The ID of the customer to retrieve.

    Returns:
        pandas.DataFrame: The customer data if found, otherwise an empty DataFrame.
    """
    df = pd.read_csv("C:/Users/dalex/Documents/DataSetsProjects/Insurance2026.csv", encoding="cp1252")
    # customer = df[df["Patient_Id"] == customer_id]
    # #customer = df[df["Customer_ID"] == customer_id]  # Adjust for zero-based indexing
    # customerInfo = customer.to_dict(orient="records")
    # normalize so numeric IDs and string IDs compare correctly
    patient = df[df["Patient_Id"].astype(str).str.strip() == str(customer_id)]

    if patient.empty:
        return {}

    # Patient_Id should be unique, so return a single record
    return patient.iloc[0].to_dict()
    
    #return customerInfo


    #return f"hola2{customer_id}"  # Example id: 100009

#Example id: 100009