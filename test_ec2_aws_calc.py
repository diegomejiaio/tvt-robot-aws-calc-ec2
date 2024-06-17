import asyncio
from playwright.async_api import async_playwright, expect
import pandas as pd

async def main():
    async with async_playwright() as p:
        # read excel first row as header
        excel = pd.read_excel('pricing-ec2.xlsx', header=0)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()
        await page.set_viewport_size({"width": 1600, "height": 800})
        await page.goto('https://calculator.aws/#/estimate')
        # Change estimation name
        await page.get_by_role("link", name="Edit My Estimate").click()
        await page.get_by_placeholder("Enter Name").click()
        await page.get_by_placeholder("Enter Name").fill("My new estimation")
        await page.get_by_label("Save", exact=True).click()
        await page.get_by_label("Add service").first.click()
        for _, row in excel.iterrows():
            await page.get_by_placeholder("Search for a service").click()
            await page.get_by_placeholder("Search for a service").fill("ec2")
            await page.get_by_label("Configure Amazon EC2").click()
            await page.get_by_placeholder("Enter a description for your estimate").click()
            # Add EC2 instance name
            await page.get_by_placeholder("Enter a description for your estimate").fill(row['instance_name'])
            await page.get_by_placeholder("Enter a description for your estimate").press("Enter")
            await page.get_by_label("Choose a Region").click()
            # select region
            await page.get_by_role("combobox").fill(row['region'])
            await page.get_by_text(str(row['region']), exact=True).click()
            # select operating system
            match row.ope_system:
                case "Windows":
                    await page.get_by_label("Operating system").click()
                    await page.get_by_role("option", name="Windows Server", exact=True).click()
                    await page.get_by_label("Operating system").press("Escape")
                case "Linux":
                    pass
            # select instance type
            await page.get_by_placeholder("Search by instance name or filter by keyword").click()
            await page.get_by_placeholder("Search by instance name or filter by keyword").fill(row['instance_family'])
            await page.get_by_role("table", name="EC2 selection").get_by_label("").check()
            await page.get_by_role("button", name="Other purchasing options").click()
            match row.payment_type:
                case "On-Demand":
                    await page.get_by_label("On-Demand", exact=True).check()
                    await page.get_by_label("Usage", exact=True).click()
                    await page.get_by_label("Usage", exact=True).fill(str(row['monthly_usage']))
                case "Compute Savings Plans":
                    match row.reserved_years:
                        case 1:
                            await page.locator("[id=\"compute-savings-1\\ Year\"]").check()
                        case 3:
                            await page.locator("[id=\"compute-savings-3\\ Year\"]").check()
                    match row.payment_option:
                        case "No Upfront":
                            await page.locator("#compute-savings-None").check()
                        case "Partial Upfront":
                            await page.locator("#compute-savings-Partial").check()
                        case "All Upfront":
                            await page.locator("#compute-savings-All").check()
                case "EC2 Instance Savings Plans":
                    await page.get_by_text("EC2 Instance Savings PlansGet deeper discount when you only need one instance fa").click()
                    # Get the radio button element
                    radio_button = page.get_by_label("EC2 Instance Savings Plans")

                    # Click the radio button if it's not already checked
                    if not await radio_button.is_checked():
                        await radio_button.click()
                    match row.reserved_years:
                        case 1:
                            await page.locator("[id=\"instance-savings-1\\ Year\"]").check()
                        case 3:
                            await page.locator("[id=\"instance-savings-3\\ Year\"]").check()
                    match row.payment_option:
                        case "No Upfront":
                            await page.locator("#instance-savings-None").check()
                        case "Partial Upfront":
                            await page.locator("#instance-savings-Partial").check()
                        case "All Upfront":
                            await page.locator("#instance-savings-All").check()
                case "Convertible Reserved Instances":
                    await page.get_by_label("Convertible Reserved Instances", exact=True).check()
                    match row.reserved_years:
                        case 1:
                            await page.locator("[id=\"convertible-1\\ Year\"]").check()
                        case 3:
                            await page.locator("[id=\"convertible-3\\ Year\"]").check()
                    match row.payment_option:
                        case "No Upfront":
                            await page.locator("#convertible-None").check()
                        case "Partial Upfront":
                            await page.locator("#convertible-Partial").check()
                        case "All Upfront":
                            await page.locator("#convertible-All").check()
                case "Standard Reserved Instances":
                    await page.get_by_label("Standard Reserved Instances").check()
                    match row.reserved_years:
                        case 1:
                            await page.locator("[id=\"standard-1\\ Year\"]").check()
                        case 3:
                            await page.locator("[id=\"standard-3\\ Year\"]").check()
                    match row.payment_option:
                        case "No Upfront":
                            await page.locator("#standard-None").check()
                        case "Partial Upfront":
                            await page.locator("#standard-Partial").check()
                        case "All Upfront":
                            await page.locator("#standard-All").check()
                case _:
                    await page.get_by_label("Standard Reserved Instances").check()
            # select term type
            await page.get_by_role("button", name="Amazon Elastic Block Store (EBS) - optional Amazon Elastic Block Store (EBS) Info").click()
            await page.get_by_label("Storage amount Value").click()
            # select storage amount
            await page.get_by_label("Storage amount Value").fill(str(row['ebs_storage']))
            await page.get_by_label("Snapshot Frequency").click()
            # select snapshot frequency
            await page.get_by_role("option", name=str(row['snapshot_freq']),exact=True).click()
            await page.get_by_label("Amount changed per snapshot Value").click()
            # select amount changed per snapshot
            await page.get_by_label("Amount changed per snapshot Value").fill(str(row['snapshot_storage']))
            # next row 
            await page.get_by_role("button", name="Save and add service").click()
            # verify if the service was added
            assert await page.get_by_text('Successfully added Amazon EC2 estimate.').is_visible()
        await page.get_by_role("button", name="View summary").click()

        await page.click('text="Share"')
        await page.click('text="Agree and continue"')

        # Wait 5 seconds
        await page.wait_for_timeout(5000)
        # Copy public link
        link = await page.get_by_role("button", name="Copy public link").click()
        await context.tracing.stop(path="logs/trace.zip")
        await page.pause()
        # browser.close()

asyncio.run(main())