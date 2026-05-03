# Claims Processing System (Python)
   
    When the system is run for the first time, it makes a request to the FDA open data API and downloads the 
    available NDC dataset. This initial step may take a few seconds longer than subsequent runs. The downloaded 
    NDC data is normalized into the 11-digit (5-4-2) format and stored locally along with a timestamp. The cached 
    data remains valid for 24 hours.
    
    After loading the NDC data, the system reads the input CSV file and performs validation on each claim. Once 
    the data passes all validation rules, it is checked against the cached NDC dataset to ensure it exists in the FDA directory.
    
    On subsequent runs, the system is faster because it reuses the cached NDC data and avoids calling the FDA API 
    again. If the cached data expires (after 24 hours), the system automatically refreshes it by making a new API call. 
    This ensures the data remains up to date while minimizing unnecessary external requests

## Features
    •	CSV-based batch processing
    •	Field-level validation (member, NDC, dates, etc.)
    •	NDC validation using FDA directory
    •	Business rule validation (quantity, days supply)
    •	Copay calculation (commercial, medicare, medicaid)
    •	Output results as structured JSON
    •	Unit tests across all layers
    •	NDC cache with 24-hour refresh logic

## Project Work Flow Diagram Miro Link
    https://miro.com/app/board/uXjVHfP7Zk0=/?moveToWidget=3458764668805690142&cot=14
    
![img.png](img.png)

 
## How It Works
    CSV Input
       ↓
    BatchReader → InputParser → Normalizer
       ↓
    ClaimValidationService (data validation + NDC check)
       ↓
    QuantityRuleService (business rules)
       ↓
    CopayRuleService (calculate copay)
       ↓
    ResultBuilder
       ↓
    OutputWriter → JSON Output
 
## Running the Application 
    Run the processor script:
    python3 -m claims_processing.main sample/input_claims.csv sample/output.json
    
## Running the Tests
    python3 -m unittest discover -s tests -p "test_*.py" -v

    Run specific module:
    python3 -m unittest discover -s tests/<folder_name> -p "test_*.py"
 
## NDC Directory Handling
    •	The system downloads FDA NDC data on first run
    •	Cached in:
       directory/ndc_cache.json
    •	Cache expires after 24 hours
    •	Automatically refreshed when expired

# Business Rules
## Validation Rules
    •	member_id must be exactly 10 digits
    •	NDC must be in 5-4-2 format and exist in FDA directory
    •	date_of_service must be valid and not in future
    •	quantity > 0
    •	days_supply between 1–90
    •	drug_cost > 0
    •	plan_type ∈ {commercial, medicare, medicaid}

## Copay Rules
    Plan Type	Rule
    Commercial	20% (min $10, max $100)
    Medicare	$15 if NDC starts with 0, else $5
    Medicaid	$0

## Testing Coverage
    •	Data layer (reader, parser, normalizer, writer)
    •	Services (validation, copay, rules)
    •	Processor (orchestration)
    •	NDC (downloader, cache, client)

## Tech Stack
    •	Python 3.13
    •	unittest (testing)
    •	Standard libraries (csv, json, datetime, logging)
