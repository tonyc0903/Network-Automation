# NetworkAutomation
In the process of practicing network automation with Python and other technologies

This repository contain scripts for my network automation journey

Helpful tips for me along the way (will update with tips daily):

`group_vars` - this folder contains a routers.yml for automating and inheriting variables at group level

`host_vars` - this folder contains yml files for each specific device which allows you to configure them with specific configurations. (Note that the yml file name in the host_var folder must match the hosts stated in the hosts.yml (in this case I saved the hosts in a yml or the original INI )

`ansible-doc ios_command` - This command privides an offline version of documentation of all the tasks associated with the modulename (substitute with name) 
