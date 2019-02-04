# airtable-cfc-content-review
Pull data from AirTable and then format it into a PHP array for compatibility with our IBM website.

This project uses the AirTable Python Wrapper - https://github.com/gtalarico/airtable-python-wrapper

# Notes

- For any record, if `Asset Type` has more than one item in it, this program will ONLY choose the first item. If you want to change the category that a topic appears in, change the first item in `Asset Type` in AirTable.

# How-to's

To add a table:
1. Add the table name to the list in `line 7`.
1. Create a list in the `# Create defaultdict structures` section by copying and pasting an existing list under the other variables and changing the variable name.
1. Find this code in the `# Place data from the table in the correct list` section, copy it, and add it after the last `elif` statement.
```python
elif table is 'Disaster Domain':
  disaster_domain_records_list[asset_type].append(topic_list)
```
  1. Change `Disaster Domain` to your table name you added in Step 1.
  1. Change `disaster_domain_records_list` to the variable name you made in Step 2.
1. Find this code in `line 149`, copy it, and add it after the last `createPHPpage(...)` entry
```python
createPHPpage(technical_domain_records_list, '_technical-content')`
```
  1. Change `technical_domain_records_list` to your variable name you made in Step 2.
  1. Change `_technical-content` to the name of the file you want to generate.
  
To delete a table and associated code:
1. Remove the corresponding table name in the list in `line 7`.
1. Remove the corresponding variable under the `# Create defaultdict structures` section.
1. Remove the corresponding code in the `# Place data from the table in the correct list` section.
1. Remove the corresponding code at the end of the file that calls the `createPHPpage` method.
