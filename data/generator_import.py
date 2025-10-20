"""
Simple IESO Generators Import Script
Imports data into the ieso_generators table
"""

import pandas as pd
from sqlalchemy import create_engine

# Database connection - UPDATE THIS WITH YOUR DATABASE INFO
DATABASE_URL = "postgresql://postgres:pass@localhost:5432/ieso"
# For SQLite: DATABASE_URL = "sqlite:///ieso_generators.db"

# Read the Excel file
gens = pd.read_excel(
    "./IESO-Active-Contracted-Generation-List.xlsx",
    sheet_name="Contract Data",
    header=2
)

# Rename columns to match the database table
gens.columns = [
    'agreement_type',
    'capacity_mw',
    'facility_name',
    'supplier_name',
    'status',
    'operational_term_years',
    'commercial_operation_date',
    'operation_start_date',
    'operation_end_date',
    'fuel_group',
    'technology',
    'fuel_type',
    'connection_type',
    'city_town',
    'municipality',
    'ieso_zone',
    'planning_region',
    'unused_column'
]

# Drop the unused column
gens = gens.drop('unused_column', axis=1)

# Add data as of date
gens['data_as_of_date'] = pd.to_datetime('2025-06-30')

# Clean data types
gens['capacity_mw'] = pd.to_numeric(gens['capacity_mw'], errors='coerce')
gens['operational_term_years'] = pd.to_numeric(gens['operational_term_years'], errors='coerce')

# Convert dates
date_cols = ['commercial_operation_date', 'operation_start_date', 'operation_end_date']
for col in date_cols:
    gens[col] = pd.to_datetime(gens[col], errors='coerce')

# Preview
print("Data preview:")
print(gens.head())
print(f"\nTotal generators: {len(gens)}")
print(f"Total capacity: {gens['capacity_mw'].sum():,.1f} MW")

# Connect to database and import
engine = create_engine(DATABASE_URL)
gens.to_sql('ieso_generators', engine, if_exists='append', index=False)

print(f"\n✅ Successfully imported {len(gens)} generators!")