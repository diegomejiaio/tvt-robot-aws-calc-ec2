# Robot EC2 Pricing

This project automates the process of calculating the cost of AWS EC2 instances using Playwright and Python.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Support

### Payment types

- On-Demand
- Convertible Reserved Instances
- Standard Reserved Instances
- Compute Savings Plans
- EC2 Instance Savings Plans

### OS

- Linux
- Windows
## Installation

1. Install [Playwright](https://playwright.dev/python/docs/intro)
2. Clone the repository:
   ```bash
   git clone {}
   ```
3. Navigate to the project directory:
   ```bash
   cd yourrepository
   ```
4. Create a virtual environment:
   ```bash
   python -m venv env
   ```
5. Activate the virtual environment:
   - For Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - For macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
6. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
7. Run pytest
   ```bash
   pytest test_ec2_aws_calc.py
   ```


## Functional steps

1. Read pricing-ec2.xlsx as dataframe
2. Open the browser https://calculator.aws/#/estimate
3. Change estimation name
4. For each ec2 instance add service
   1. Seach EC2
   2. Define EC2 name (texbox)
   3. Define region (dropdown)
   4. Define os (dropdown)
   5. Define number of instances (textbox)
   6. Seach instance type (textbox)
   7. Select instance type (radiobutton)
   8. Select payment type (radiobutton)
   9. Select reservation term (radiobutton)
   10. Select payment option
   11. Clic EBS
   12. Define storage amount in GB
   13. Select Snapshot frencuency
   14. Define changed per snapshot in GB
   15. Clic in Save and add service
   16. Step 1 for next row
5.  Clic in View summary
6.  Clic in Share
7.  Clic in Agree an continue
8.  Wait 5 seconds
9.  Clic in Copy public link
10. Print public link
11. Finish process without closing screen