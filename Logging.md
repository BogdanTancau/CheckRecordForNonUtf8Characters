
# Logging requirements (Master Data)
***
## What can be logged
- Logger Name
- Severity 
- Timestamp
- Global Use Case (e.g. "DDO")
- Component (e.g. "Dataflow") 
- Thread (what thread caused the error; e.g. "ThreadName" in Python)
- FileName (Coding file)
- Function Name (where the logging happened) 
- URL 
- Message
- some application exceptions should be logged
- application events should be logged
- some application states should be logged
- the logging specifies which specific records and fields the user accessed and what the user did with the data. For example in the case of adjusting data, both the content before the change and after the change should be recorded
- the logging also includes information about read-only actions on highly confidential data
- the logging specifies which specific records and fields the user accessed and what the user did with the data. For example in the case of adjusting data, both the content before the change and after the change should be recorded
- the logging also includes information about read-only actions on highly confidential data
## Which events to logged
- Input validation failures(unacceptable encodings)
- Output validation failures
- Application errors and system events e.g. syntax and runtime errors, connectivity problems, performance issues, third party service error messages, file system errors, file upload virus detection, configuration changes
- Data changes
- Sequencing failure
## The application logs must record "when, where, who and what" for each event.


### When
- Log date and time (international format)
- Event date and time - the event timestamp may be different to the time of logging e.g. server logging where the client application is hosted on remote device that is only periodically or intermittently online
- Interaction identifier Note A
### Where
- Application identifier e.g. name and version
- Application address e.g. cluster/hostname or server IPv4 or IPv6 address and port number, workstation identity, local device identifier
- Service e.g. name and protocol
- Geolocation
- Window/form/page e.g. entry point URL and HTTP method for a web application, dialogue box name
- Code location e.g. script name, module name
### Who (human or machine user)
- Source address e.g. user's device/machine identifier, user's IP address, cell/RF tower ID, mobile telephone number
- User identity (if authenticated or otherwise known) e.g. user database table primary key value, user name, license number
###What
- Type of event: info, notice, warning, error, critical, alert, emergency.
- Severity of event  
- Security relevant event flag (if the logs contain non-security event data too)
- Description
- Default should not be used

| 100 | Debug     | Debug or trace information.                                                         |
|-----|-----------|-------------------------------------------------------------------------------------|
| 100 | Debug     | Debug or trace information.                                                         |
| 200 | Info      | Routine information, such as ongoing status or performance.                         |
| 300 | Notice    | Normal but significant events such as start up, shut down, or configuration change. |
| 400 | Warning   | Warning events might cause problem.                                                 |
| 500 | Error     | Error events are likely to cause problem                                            |
| 600 | Critical  | Critical events cause more severe problems or outage.                               |
| 700 | Alert     | A person must take action immediately.                                              |
| 800 | Emergency | One or more system are unusable.                                                    |

## Security
- IMPORTANT: do not allow elevation of privilege to the sensitive information. Logging of the real data may be not needed for developers. If such, obfuscation of real protected data must be enforced
- Activity logging that contains real protected data should be protected in the same way as the data itself. 
## How is logged
- Take the "logging handler" and change the output to JSON
- Create a general "formatter" for Logging that can be reused by all teams (structured as JSON Logging)
- You can find more details  in [CRA_DDO Logger and Logging documentation](https://atos365.sharepoint.com/sites/CRA-DDO/_layouts/15/Doc.aspx?sourcedoc={060d1175-b962-4f41-939f-7325a7175a30}&action=edit&wd=target%28Plattform%20Ops%2FOverview%20Platform%20Ops.one%7C4e89b199-6c1b-486b-8a4e-ff645bc551dd%2FLOGGER%20and%20LOGGING%20-%20Plattform%20Ops%20Requirements%20to%20functional%20Teams%7C8aa05a3c-ee01-4ab4-9baa-a4dbe0071ce5%2F%29)

#### If you need a deep understanding of  the logging process please check these resources:
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying
- https://docs.python.org/3/library/logging.html#logrecord-attributes
- https://www.compact.nl/articles/forensic-logging-requirements/
- https://dzone.com/articles/application-logging-what-when
- https://www.dataset.com/blog/the-10-commandments-of-logging/
