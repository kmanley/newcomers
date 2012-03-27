import sys, csv, datetime


def main(filename):
    addresses = {} # address -> [firstname1, lastname1, renewal date1, firstname2, lastname2, renewal date2]
    unique_names = {} # address -> {}
    writer = csv.writer(open(r"newcomers_mailing_list_%s.csv" % str(datetime.date.today()), "wb"))
    writer.writerow(("Name", "Address", "City", "State", "Zip", "Renewal Date"))
    reader = csv.DictReader(open(filename, 'rb'))
    for row in reader:
        row["Address"] = row["Address"].title()
        key = row["First name"].strip() + row["Last name"].strip()
        if unique_names.setdefault(row["Address"], {}).get(key):
            pass
        else:
            addresses.setdefault(row["Address"], []).extend((row["First name"], 
                                                             row["Last name"], 
                                                             row["Renewal due"]))
            unique_names[row["Address"]][key] = 1
    keys = addresses.keys()
    keys.sort()
    for key in keys:
        #if key.strip():
        #    continue
        if len(addresses[key]) == 3:
            fname, lname, rdate = addresses[key]
            row = ["%s %s" % (fname, lname), key, "Ridgefield", "CT", '="06877"', rdate]
            print row
            writer.writerow(row)
        elif len(addresses[key]) == 6:
            fname1, lname1, rdate, fname2, lname2, unused = addresses[key]
            if lname1 == lname2:
                name = "%s & %s %s" % (fname1, fname2, lname1)
            else:
                name = "%s %s & %s %s" % (fname1, lname1, fname2, lname2)
            row = [name, key, "Ridgefield", "CT", '="06877"', rdate]
            print row
            writer.writerow(row)
            
if len(sys.argv) != 2:
    print ("usage: newcomers_generate_list.py <csv_filename>")
    sys.exit(1)
main(sys.argv[1])
