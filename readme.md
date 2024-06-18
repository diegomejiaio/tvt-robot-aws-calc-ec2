# Robot EC2 Pricing

This project automates the process of calculating the cost of AWS EC2 instances using Playwright and Python.

## Demo (spanish)

[![Ver video de Loom](https://cdn.loom.com/sessions/thumbnails/1ecaba2f486740248db39099a01459d2-with-play.gif)](https://www.loom.com/share/1ecaba2f486740248db39099a01459d2)

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
   git clone https://github.com/diegomejiaio/tvt-robot-aws-calc-ec2
   ```
3. Navigate to the project directory:
   ```bash
   cd tvt-robot-aws-calc-ec2
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
7. Modify template file ```./pricing-ec2.xlsx``` and save
8. Run pytest
   ```bash
   pytest test_ec2_aws_calc.py
   ```
9.  Review traces
   ```bash
   playwright show-trace logs/trace.zip
   ```

## Usage
1. Use `pricing-ec2.xlsx` as template
2. Define you own excel
3. Use `config.txt` to define your data source
4. Run `pytest test_ec2_aws_calc.py`

## Process
1. Import necessary libraries (asyncio, playwright, pandas).
2. Define an asynchronous main function.
3. Within the main function, do the following:
   1. Read 'pricing-ec2.xlsx' as a pandas dataframe.
   2. Launch a new Chromium browser instance using playwright.
   3. Start tracing with screenshots, snapshots, and sources.
   4. Open a new page and set the viewport size.
   5. Navigate to the AWS calculator page.
   6. Change the estimation name.
   7. For each row in the dataframe, add an EC2 service:
      1. Search for EC2.
      2. Define the EC2 instance name.
      3. Select the region.
      4. Select the operating system.
      5. Select the instance type.
      6. Select the payment type.
      7. Select the reservation term.
      8. Select the payment option.
      9. Define the EBS storage amount.
      10. Select the snapshot frequency.
      11. Define the amount changed per snapshot.
      12. Save and add the service.
   8. View the summary of the estimate.
   9. Share the estimate.
   10. Agree and continue.
   11. Wait for 5 seconds.
   12. Copy the public link of the estimate.
   13. Stop tracing and save the trace to 'logs/trace.zip'.
   14. Pause the execution.
4. Run the main function using asyncio.
