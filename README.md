# hostname_server
A small service that generates unique hostnames and makes them accessible via REST API.
This Python script opens a port on the local machine and waits for REST API calls. Depending on the call, it will return a unique hostname.

Inspired by [hostgen](https://github.com/Spreadcat/hostgen) and rewritten to meet my needs using Flask, SQLAlchemy, and PostgreSQL to be run within Docker containers.

# Author

*   Nikita Fomin
    

