import pandas as pd
from faker import Faker

# Initialize Faker
fake = Faker()


# Define a function to generate a fake customer
def generate_fake_customer():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "rating": str(
            fake.random_int(min=1, max=5)
        ),  # Rating as an integer from 1 to 5
    }


# Generate a list of fake customers (200 records)
customers = [generate_fake_customer() for _ in range(200)]

# Create a DataFrame from the generated customers
df = pd.DataFrame(customers)

# Print the first few records of the DataFrame
print(df.head())

# Optionally, save to a CSV file
df.to_csv("data/customers.csv", index=False)

# Show DataFrame size
print(f"DataFrame size: {df.shape}")
