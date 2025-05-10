# scripts/generate_treaty_samples.py

import os
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Resolve path to ../data/treaty_samples
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(script_dir), "data", "treaty_samples")
os.makedirs(data_dir, exist_ok=True)

# Treaty components
treaty_types = ["Quota Share", "Excess of Loss", "Stop Loss", "Aggregate XL"]
territories = ["Worldwide", "North America", "Europe", "Asia", "Africa"]
exclusions = ["War", "Nuclear", "Terrorism", "Pandemic", "Cyber"]

# Generate 10 treaty files
for i in range(1, 11):
    treaty_text = f"""
Reinsurance Treaty Agreement #{i}

Type: {random.choice(treaty_types)}
Retention: ${random.randint(1, 5)}M per occurrence
Limit: ${random.randint(10, 50)}M per occurrence
Reinstatements: {random.randint(0, 2)} automatic at 100% additional premium
Territory: {random.choice(territories)}
Exclusions: {', '.join(random.sample(exclusions, k=2))}
Effective Date: {fake.date_between(start_date='-2y', end_date='today')}
Ceding Commission: {random.randint(20, 35)}%
Cedent: {fake.company()}
Reinsurer: {fake.company()}
""".strip()

    file_path = os.path.join(data_dir, f"treaty_sample_{i}.txt")
    with open(file_path, "w") as f:
        f.write(treaty_text)

print(f"✅ Successfully created 10 treaty samples in: {data_dir}")

