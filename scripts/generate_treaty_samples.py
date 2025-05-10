# scripts/generate_treaty_samples.py

import os
import random
from faker import Faker

def generate_treaties(n=10, output_dir="data/treaty_samples"):
    os.makedirs(output_dir, exist_ok=True)
    fake = Faker()

    types = ["Quota Share", "Excess of Loss", "Stop Loss", "Aggregate XL"]
    territories = ["Worldwide", "North America", "Europe", "Asia", "Africa"]
    exclusions = ["War", "Nuclear", "Terrorism", "Pandemic", "Cyber"]

    for i in range(1, n + 1):
        text = f"""
Reinsurance Treaty Agreement #{i}

Type: {random.choice(types)}
Retention: ${random.randint(1, 5)}M per occurrence
Limit: ${random.randint(10, 50)}M per occurrence
Reinstatements: {random.randint(0, 2)} automatic
Territory: {random.choice(territories)}
Exclusions: {', '.join(random.sample(exclusions, k=2))}
Effective Date: {fake.date_between(start_date='-2y', end_date='today')}
Ceding Commission: {random.randint(20, 35)}%
Cedent: {fake.company()}
Reinsurer: {fake.company()}
""".strip()

        path = os.path.join(output_dir, f"treaty_sample_{i}.txt")
        with open(path, "w") as f:
            f.write(text)

    print(f"✅ Created {n} treaty samples → {output_dir}")

if __name__ == "__main__":
    generate_treaties()
