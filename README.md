# Record checker

***

### This application check if the record has characters that are not encoded in UTF-8 format.
- If a char from the record it's not UTF-8 encoded, the application will log an error message

### After you run this program it will create one log file with two messages

| logging info               | logging error                       |
|----------------------------|-------------------------------------|
| This record can be process | This record contains bad characters |

# Logging requirements
***
## What has to be logged
- Severity and timestamp of Google Standard
- Logger Name (derived from your project) e.g. "Name" in Python 
- Global Use Case (e.g. "DDO")
- Component (e.g. "Dataflow") 
- Thread (what thread caused the error; e.g. "ThreadName" in Python)
- FileName (Coding file)
- Function Name (where the logging happened) 
- Line (in which line the logging happened) 
- URL 
- Message 
# Security
## Personal information
- Personally identifiable data. While there are some obviously sensitive things like Social Security Number, combinations of data (like first name + date of birth or last name + zip code) or user generated data (like an email or user name, e.g. BillGates@hotmail.com) can also leak information.
- Health Data
- Financial Data (like credit card numbers)
- Passwords
- IP addresses may be considered sensitive, especially when in combination with personally identifiable data.
## Tips for sensitive data
- Compartmentalize Sensitive Data 
   - When you work with sensitive data, you should minimize which parts of the system work with that data. For example, it might be tempting to use a SSN or an email address as a unique identifier for a person. If you do that, though, many different parts of the system (database tables, API endpoints, etc) will process and store the sensitive field. A better approach is to isolate the sensitive field and only use it when absolutely necessary.
- Keep Sensitive Data Out of URLs
   - don’t use the sensitive field as a unique identifier. For the endpoint urls, use these external ids instead
   - Do NOT log personal information
#
***
## How is logged

- Take the "logging handler" and change the output to JSON
- Create a general "formatter" for Logging that can be reused by all teams (structured as JSON Logging)
