import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import time
import folium
import math

MONEY_COL = ['Cost of Charity Care','Total Bad Debt Expense','Cost of Uncompensated Care',
             'Total Unreimbursed and Uncompensated Care','Total Salaries From Worksheet A','Overhead Non-Salary Costs',
             'Depreciation Cost','Total Costs','Inpatient Total Charges','Outpatient Total Charges',
             'Combined Outpatient + Inpatient Total Charges','Wage-Related Costs (Core)', 'Wage-Related Costs (RHC/FQHC)',
             'Total Salaries (adjusted)','Contract Labor','Wage Related Costs for Part - A Teaching Physicians',
             'Wage Related Costs for Interns and Residents','Cash on Hand and in Banks',
             'Temporary Investments','Notes Receivable','Accounts Receivable','Less: Allowances for Uncollectible Notes and Accounts Receivable'
            ,'Inventory','Prepaid Expenses','Other Current Assets','Total Current Assets','Total Fixed Assets',
             'Investments','Other Assets','Total Other Assets','Total Assets','Accounts Payable',"Salaries, Wages, and Fees Payable",
             'Payroll Taxes Payable','Notes and Loans Payable (Short Term)','Deferred Income','Other Current Liabilities',
             'Total Current Liabilities','Mortgage Payable','Notes Payable','Unsecured Loans','Other Long Term Liabilities',
             'Total Long Term Liabilities','Total Liabilities','General Fund Balance','Total Fund Balances','Total Liabilities and Fund Balances',
             'Managed Care Simulated Payments','Total IME Payment','Inpatient Revenue','Outpatient Revenue','Gross Revenue',
             'Net Patient Revenue','Less Total Operating Expense','Net Income from Service to Patients','Total Other Income',
             'Total Income','Total Other Expenses', 'Net Income','Net Revenue from Medicaid','Medicaid Charges']

    # # mapping the hospitals
    # map = folium.Map(location=[landldf.Lat.mean(), landldf.Long.mean()],
    #                  zoom_start=14, control_scale=True)
    #
    # for index, location_info in landldf.iterrows():
    #     folium.Marker([location_info["Lat"], location_info["Long"]], popup=location_info["Hospital Name"]).add_to(map)
    # # saving the map to this file, just open it when you run
    # map.save("mapElla.html")

def format_mon(df):
    for index, row in df.iterrows():
        for col in MONEY_COL:
            if type(row[col]) == str:
                row[col] = row[col].replace(',','')
                df[col][index] = float(row[col][1:])
            else:
                df[col][index] = 0

    return df

def net_income_mapping(df):
    abs_incomes = []
    signs = []
    for index, row in df.iterrows():
        abs_incomes.append(abs(df['Net Income'][index]))
        if df['Net Income'][index] < 0:
            signs.append('-')
        else:
            signs.append('+')

    df['Absolute Net Income'] = abs_incomes
    df['Sign Net Income'] = signs
    return df
def main():
    # saving as csv
    df = pd.read_csv('Hospital_Cost_Report_2019.csv')
    f2 = pd.read_csv('hospitals.csv')

    drop_col = [
        'rpt_rec_num',
        'Provider CCN',
        'Medicare CBSA Number',
        'CCN Facility Type',
        'Provider Type',
        'Type of Control',
        'Fiscal Year Begin Date',
        'Fiscal Year End Date',
        'Number of Interns and Residents (FTE)',
        'Total Days Title V',
        'Total Days Title XVIII',
        'Total Days Title XIX',
        'Total Discharges Title V',
        'Total Discharges Title XVIII',
        'Total Discharges Title XIX',
        'Total Days Title V + Total for all Subproviders',
        'Total Days Title XVIII + Total for all Subproviders',
        'Total Days Title XIX + Total for all Subproviders',
        'Total Discharges Title V + Total for all Subproviders',
        'Total Discharges Title XVIII + Total for all Subproviders',
        'Total Discharges Title XIX + Total for all Subproviders',
        'Hospital Total Days Title V For Adults &amp; Peds',
        'Hospital Total Days Title XVIII For Adults &amp; Peds',
        'Hospital Total Days Title XIX For Adults &amp; Peds',
        'Hospital Total Discharges Title V For Adults &amp; Peds',
        'Hospital Total Discharges Title XVIII For Adults &amp; Peds',
        'Hospital Total Discharges Title XIX For Adults &amp; Peds',
        'Land',
        'Land Improvements',
        'Buildings',
        'Leasehold Improvements',
        'Fixed Equipment',
        'Major Movable Equipment',
        'Minor Equipment Depreciable',
        'Health Information Technology Designated Assets',
        'DRG Amounts Other Than Outlier Payments',
        'DRG amounts before October 1',
        'DRG amounts after October 1',
        'Outlier payments for discharges',
        'Disproportionate Share Adjustment',
        'Allowable DSH Percentage',
        "Less Contractual Allowance and discounts on patients' accounts",
        'Net Revenue from Stand-Alone SCHIP',
        'Stand-Alone SCHIP Charges'
    ]
    df.drop(drop_col, inplace=True, axis=1)
    # removing rows with no data
    df['Zip Code'].dropna()
    df['ADDRESS'].dropna()
    df['City'].dropna()
    df['State Code'].dropna()


    comb = df.merge(f2, how = 'left', on = 'ADDRESS')
    comb = comb[comb['LATITUDE'].notna()]

    df = format_mon(df)
    comb = format_mon(comb)
    comb = net_income_mapping(comb)

    df.to_csv('hosp_cost_report.csv')
    comb.to_csv('hosp_locs.csv')

if __name__ == '__main__':
    main()
