# Springer Books

To run this locally, you can use docker. Just run the following to start a docker container and install all dependencies:

![](/resources/terminalizer.gif)


```bash
$ docker run --rm -it -v $(pwd):/home python:3.7 /bin/bash
$ cd /home
$ pip install -r requirements.txt
$ python generate.py
```

Now, if you open the generated **index.html** you should be able to see the homepage: 

![](/resources/homepage.png)