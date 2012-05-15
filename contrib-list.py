import urllib
import re
import csv
import time

def findname(string):
    comma = re.compile(',')
    splits = string.split()
    if comma.search(string) == None:
        lastname = splits[0]
        firstname = splits[1]
    else:
        lastname = splits[0][:-1]
        firstname = splits[1]
    return lastname, firstname

def readwrite(origfile, newfile):
    urlln = 'http://www.elections.il.gov/CampaignDisclosure/ContributionsSearchByAllContributions.aspx?ddlContributionType=All+Types&ddlLastOnlyNameSearchType=Starts+with&txtLastOnlyName='
    urlfn = '&ddlFirstNameSearchType=Starts+with&txtFirstName='
    urlend = '&ddlAddressSearchType=Starts+with&txtAddress=&ddlCitySearchType=Starts+with&txtCity=&ddlState=&txtZip=&txtZipThru=&ddlOccupationSearchType=Starts+with&txtOccupation=&ddlEmployerSearchType=Starts+with&txtEmployer=&txtAmount=&txtAmountThru=&txtRcvDate=&txtRcvDateThru=&ddlOrderBy=Last+or+Only+Name+-+A+to+Z&ddlVendorLastOnlyName=Starts+with&txtVendorLastOnlyName=&ddlVendorFirstName=Starts+with&txtVendorFirstName=&ddlVendorAddress=Starts+with&txtVendorAddress=&ddlVendorCity=Starts+with&txtVendorCity=&ddlVendorState=&txtVendorZip=&txtVendorZipThru=&ddlPurpose=Starts+with&txtPurpose='

    with open(origfile, 'rb') as f:
        reader = csv.reader(f, delimiter='\n')
        for row in reader:
            name = row[0]
            lastname =  findname(name)[0]
            firstname =  findname(name)[1]
            try:
                page = urllib.urlopen(urlln+lastname+urlfn+firstname+urlend)
                html = page.read()
                pattern = re.compile('<span id="ctl00_ContentPlaceHolder1_lblTotals">Your search found ([0-9]*) receipts')
                if re.search(pattern, html).group(1) == '0':
                    pass
                else:
                    with open(newfile, 'ab') as n:
                        writer = csv.writer(n, delimiter='\n')
                        writer.writerow([name])
            except IOError:
                time.sleep(5)
