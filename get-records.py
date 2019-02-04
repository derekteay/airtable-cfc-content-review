from airtable import Airtable
from collections import defaultdict
import json
import sys

# List of table names we want to read from
table_names = ['Technical Domain', 'Disaster Domain', 'Healthcare Domain', 'Content since 10/29']

# Create defaultdict structures
technical_domain_records_list = defaultdict(list)
disaster_domain_records_list = defaultdict(list)
healthcare_domain_records_list = defaultdict(list)
content_since_records_list = defaultdict(list)

# Go through the data retrieved from each of the tables listed above
for table in table_names:

    # AirTable API setup - replace the values with your own
    airtable = Airtable('base-key', 'table-name', api_key='your-api-key')

    # Get only records that are in the correct Status
    records = airtable.get_all(view='Keep')

    # Process each record from AirTable
    for record in records:

        # For ease of code writing
        record = record['fields']

        # Topic might not be provided, catch this error
        try:
            topic = record['Topic']
        except KeyError:
            topic = "EMPTY"

        # Description might not be provided, catch this error
        try:
            description = record['Description']
        except KeyError:
            description = "This is a sample description"

        # Topic Category might not be provided, catch this error
        try:
            topic_category = record['Topic Category']
        except KeyError:
            topic_category = "EMPTY"

        # Asset Type might not be provided, catch this error
        try:
            asset_type = record['Asset Type']

            # If Asset Type has more than 1 entry in AirTable, it will turn into a list.
            # We're going to take only the first entry
            if type(asset_type) is list:
                asset_type = record['Asset Type'][0]
            else:
                asset_type = record['Asset Type']
        except KeyError:
            asset_type = "EMPTY"

        # URL might not be provided, catch this error
        try:
            url = record['URL']
        except KeyError:
            url = "EMPTY"

        # Create event list dictionary
        topic_list = {"table": table,
                      "topic": topic,
                      "desc": description,
                      "topic category": topic_category,
                      "asset type": asset_type,
                      "url": url}

        # DEBUG
        # print(table, topic, description, topic_category, asset_type, url)

        # Place data from the table in the correct list
        if table is 'Technical Domain':
            technical_domain_records_list[asset_type].append(topic_list)
        elif table is 'Disaster Domain':
            disaster_domain_records_list[asset_type].append(topic_list)
        elif table is 'Healthcare Domain':
            healthcare_domain_records_list[asset_type].append(topic_list)
        elif table is 'Content since 10/29':
            content_since_records_list[asset_type].append(topic_list)


# Create the PHP file
#
# list - the variable name of the list processed above
# filename - what the name of the created file should be (without the .php extension)
def createPHPpage(list, filename):
    item_counter = 1

    # Write to the filename specified
    stdout = sys.stdout
    sys.stdout = open(filename + '.php', 'w')

    print("<?php")
    print("$content = array(")

    # Get the category that the following items will be in
    for item in list:
        print("\t\"" + item + "\"", "=> array(")

        event_counter = 1

        # Get the item detail
        for details in list[item]:
            # DEBUG
            # print(str(event_counter), item2)
            # print(json.dumps(item2, indent=2))

            print("\t\tarray(")
            print("\t\t\t\"title\" => " + "\"" + details['topic'] + "\",")
            print("\t\t\t\"date\" => " + "\"" + details['desc'] + "\",")
            print("\t\t\t\"url\" => " + "\"" + details['url'] + "\",")

            # Check the list length against the counter so we know if we need a ',' or not
            if event_counter == len(list[item]):
                print("\t\t)")
            else:
                print("\t\t),")

            event_counter += 1

        # Check the list length against the counter so we know if we need a ',' or not
        if item_counter == len(list):
            print("\t)")
        else:
            print("\t),")
        item_counter += 1

    print(");")
    print("?>")

    sys.stdout = stdout

    # Read file to make sure data is good
    file_contents = open(filename + '.php', 'r')
    content = file_contents.read()
    file_contents.close()
    print('** ' + filename + ' **')
    print(content)
    print()


createPHPpage(technical_domain_records_list, '_technical-content')
createPHPpage(disaster_domain_records_list, '_disaster-content')
createPHPpage(healthcare_domain_records_list, 'healthcare-content')
createPHPpage(content_since_records_list, '_content-since-content')
