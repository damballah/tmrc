# tmrc
#### Tor Middle Relay Creator v0.1

**Tested on Debian 12.**

Concept:

- Automatic installation of Tor
- Automatic configuration of a middle node
- Automatic installation of the monitoring tool NYX


<br>
Requirements:

All updates must be made :
```sh
sudo apt update
sudo apt upgrade
```

<br>
Instructions:

- Clone the following git with the command:
```sh
git clone https://github.com/damballah/tmrc 
```

- Then, go to the folder : tmrc and run the python file like this :
```sh
python3 tmrc.py
```

- Then, follow the instructions (only 4), then let the script do its thing. 

At the end, it will indicate that the monitoring [NYX] for your Middle Tor node is ready, 

all you have to do is type : 
```sh
nyx
```
to run it. 

Then, after 3-5 hours, you can go to the 
site: https://metrics.torproject.org/rs.html to see your node working. 
(Sometimes, more than 5 hours are needed to see your node appear in the list).

#### Enjoy ;)
