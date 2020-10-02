# NoSQLInjection
The project contain NoSQL authentication bypass and NoSQL Injection automation script.


# NoSQL Authentication Bypass 
## How to run 

### Usage

```
NoSQLAuthBypass.py [-h] [-u URL] [-d Data] [-w wordlist] [-p Proxy] [-v] [-Lo Logout-Identifier]
```

### Example

```
NoSQLAuthBypass.py -u http://example.com/login -w filepath -Lo "Logout identifier"
```

### Arguments
| Arguments        | Description           |
| ------------- |:-------------:|
|  -h, --help            |show this help message and exit|
|  -u URL, --url URL     |Target URL (e.g. "http://www.example.com/login")|
|  -d Data, --data Data  |Data string to be sent through POST|
|  -w wordlist, --wordlist |wordlist Path to the wordlist|
|  -p Proxy, --proxy |Use a proxy to connect to the target URL (e.g. "127.0.0.1:8080")|
|  -v, --verbose         |verbose mode|
|  -Lo Logout-Identifier, --LogoutIdentifier |String identifier from logged out page|

# NoSQL Injection 
## How to run 

### Usage

```
NoSQLInjection.py [-h] [-u URL] [-d Data] [-w Wordlist] [-U Username] [-p Proxy] [-v] [-Lo Logout-Identifier] [-t Threads]
```

### Example

```
NoSQLInjection.py -u http://example.com/login -Lo "Logout identifier" -u username -t 50
```

### Arguments
| Arguments        | Description           |
| ------------- |:-------------:|
|  -h, --help            |show this help message and exit|
|  -u URL, --url URL     |Target URL (e.g. "http://www.example.com/login")|
|  -d Data, --data Data  |Data string to be sent through POST|
|  -w wordlist, --wordlist |wordlist Path to the wordlist|
|  -p Proxy, --proxy |Use a proxy to connect to the target URL (e.g. "127.0.0.1:8080")|
|  -v, --verbose         |verbose mode|
|  -Lo Logout-Identifier, --LogoutIdentifier |String identifier from logged out page|
