# Docker Cookbook - PDF

## Running Images and Containers

- Getting terminal session within a container (interactively)
```bash
# interactive terminal session
docker run -t -i ubuntu:14.04 /bin/bash 
```
- Checking 
```bash
# all containers
docker ps
# see the stopped conatianers
docker ps -a 
```
- Run container in **detached mode**: to run it as a service in the background.
  - Create a simple HTTP server in python 2.7. This maps the directory structure to HTTP requests. 
```bash
docker run -d -p 1234:1234 python:2.7 python -m SimpleHTTPServer 1234
# note the container ID and connect to it using exec and run a command
# z.B docker exec -ti container_id ls
docker exec -ti container_id /bin/bash
# z.B check the installed packages in the container
docker exec -ti container_id apt list --installed
```
## Create Stop and Kill Containers

Using `run` creates a container automatically with docker run. You can also use `create` once staged you will need to initialize it using `start`. 

```bash
docker create -P --expose=1234 python:2.7 python -m SimpleHTTPServer 1234
# find id of container
docker ps -a
# start server
docker start container_id
# kill the server SIGKILL
docker kill container_id
# stop it after a grace period SIGTERM
docker stop container_id
# remove container forever
docker rm container_id
```
- Remove a lot of stopped containers
```bash
docker rm $(docker ps -a -q)
```

## Building a Docker Image with Dockerfile
A Dockerfile is a text fiel that describes the steps that Docker needs to take to prepare an image --including installing packages, creating directories and defining environment variables, among other things. 

- Create image based on busybox image:
  - defining an environment variable
*Dockerfile*
```bash
FROM busybox
ENV foo=bar
```
Now run the image and see that the environment variable is defined.
```bash
# make iamge called busybox
docker build -t busybox
# grab the environment variable that you defined 
docker run busybox env | grep foo
```
## Run WordPress Blog using Two Linked Containers
You start two containers, one running WordPress the other is the MySQL database. **The two containers are linked using the `--link` option of Docker CLI. 
- Pull the latest image for MySQL and Wordpress. Gets the image in your computer.
  
```bash
docker pull wordpress:latest
docker pull mysql:latest
```

- Start a MySQL container, give it a name via the `--name` option and set the `MYSQL_ROOT_PASSWORD` via an environmenrt variable.
- Run a WordPress container based on the wordpress image. It will be linked using the `--link` option, **Docker will automatically set up the networking so that the ports exposed by the MySQL container are reachable inside the WordPress container**.

```bash
docker run --name mysqlwp -e MYSQL_ROOT_PASSWORD=wordpressdocker -d mysql
docker run --name wordpress --link mysqlwp:mysql -p 80:80 -d wordpress
```

- This is not working properly and is FAR from best practice. Use **Docker Compose** to do this instead:
**docker-compose.yml**.
    - Use your IP address to set this up properly.
```
# Web and Mysql are the names of the containers. 
web:
  image: wordpress
  links:
    - mysql
  environment:
    - WORDPRESS_DB_PASSWORD=password
  ports:
    - "10.123.73.61:8080:80"
  
mysql:
  image: mysql:5.7
  environment:
    - MYSQL_ROOT_PASSWORD=password
    - MYSQL_DATABASE=wordpress
```
## Backing up a DataBase for Persistency

You are running MySQL image to provide a database service, you need to back it up for data persistency. 

- Two main concepts:
  - You can execute a command line in a container running in the background
  - You can **mount a host volume ( a storage area in your filesystem) into the container**
  
We will see how to:

 - Mount a volume from the Docker host into the MySQL container.
- Use the docker exec command to call `mysqldump`
  
  -  writes info as SQL statements to standardoutput. You can then save the outputfile.

Parting from the two running containers of sql and wordpress:
- If you stop the containers, the data in the database is still accessible. If you remove the containers all the data will be lost.
- If you see the image of **mysql** you see a reference to VOLUME */var/lib/mysql*. **When you start an image you can bind mount a host directory to this mount point inside the container**.

```bash
docker exec container_id mysqldump --all-databases --password=password > wordpress.backup
```




__________ 
# Using Docker - PDF

```bash
docker run test/cowsay-dockerfile /usr/gamers/cowsay "Moo"
```

The `ENTRYPOINT` specifies an executable that is used to handle any arguments passed to `docker run` z.B:

```bash
ENTRYPOINT ["/usr/games/cowsay"]
```

Now we can just do this:

```bash
docker build -t test/cowsay-dockerfile .
docker run test/cowsay-dockerfile "Moo"
```

More customized way:
- Create a script called *entrypoint.sh*
```bash
#!/bin/bash
if [$# -eq 0]; then
  /usr/games/fortune | /usr/games/cowsay
else
  /usr/games/cosway "$@"
fi
```

- Pipe input from fortune into cowsay if its called with no arguments, otherwise it calls cowsay with the given arguments.

```
FROM debian
RUN apt-get update && apt-get install -y cowsay fortune
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
```

### Pushing to your repo

```bash
docker build -t diegopenilla/myimage:mytag .
docker push diegopenilla/myimage:mytag
```

## Managing Data with Volumes and Data Containers

How do we persist and backup our data?
- Docker provides volumes, are files/directories already mounted on the host and not part of the normal union system.
- Can be shared with other containers and all changes will be made directly to the host filesystem.

```
  VOLUME/data
```

and 

```
docker run -v /data test/webserver
```

- By default, the directory will be mounted on the **host inside your Docker installation directory (/var/lib/docker)**.
   
## Ways of using Volumes
There are three ways to initialize Volumes:

1. We can declare a volume at runtime with the -v flag:
```bash
docker run -it --name container-test -h CONTAINER -v /data debian /bin/bash
```

**This will make the directory /data inside the container into a volume. Any files the image held inside the /data directory will be copied to the volume.**

You can find out where the volume lives on the host by:
```bash
docker inspect -f {{.Mounts}} container-test
```

In this case the volume /data/ in the container is simply a link to the directory /var/lib/docker/volumes/5cad../data on the host.

- If you add a file into the directory **you should immediately be able to see it from the container**.

2. Using a Dockerfile:


## Sharing Data
```bash
docker run -v /home/adrian/data:/data debian ls /data
```
The -v HOST_DIR:CONTAINER_DIR syntax is very useful for sharing files between the host and one or more containers. 

You can also share data bewteen containers by using --volumes-from CONTAINER with docker run z.B we create a new contaienr that has access to the volumes from the ontainer in our previous example:

```bash
docker run -it -h NEWCONTAINER --volumes-from container-test debian /bin/bash
```

**It’s important to note that this works whether or not the container holding the vol‐ umes (container-test in this case) is currently running.** 

## Create a docker container mounting an image from the host
```bash
docker run -it --name container-test3 -h CONTAINER -v /Users/diego/DockerVolumes:/data debian /bin/bash
```

```
docker run -v name:/path/in/container ...
```

## Weird Stuff
- This was giving me access to the Docker host:
```bash
screen
/Users/diego/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
```

- After specifying the volume of a named image:
```bash
docker run -it --name container-test3 -h CONTAINER -v /Users/diego/DockerVolumes:/data debian /bin/bash
```

- The previous command no longer enters the docker host but shows the folder where I left. 


### Common Docker Commands

#### Docker Boolean Flags

In most unix command line tools, you will find flags don't have any value such as -l in ls -l. Since these flags are either set or not set, Docker considers these to be **boolean flags**. But you can have **default true and default false** flags. 

- Specifying a flag without argument sets it to true. A default true flag is not unset by an argument with a value **the only way a default true flag can be unset is by setting it to false `-f=false`**. 

z.B In this case is a default false, we specify it to true:
```bash
docker run --read-only=true
```

### The run Command

`--rm`: removes the container when it exits 
`-e` `--env`: sets environment variables inside container

```bash
docker run -e var1=val -e var2="val 2" debian env
```
```
>> HOME=/root
>> var1=val
>> var2=val 2
...
```

-`h`, `--host`: sets container unix host name to `NAME`.

```bash
docker run -h "myhost" debian hostname
```
```
>> myhost
```

- `-v`, `--volume`: to mount file storage from the OS into the container

- `--volumes-from`: **mounts volumes from the specified container**. 

- `--expose`: identifies port or range as being used in the container but does not open the port. **Only makes sense in association with `-P` when linking containers.

- `--link`: sets up a private network interface to the specified container. 

- `-p`, `--publish`: publishes a port on the container, making it accesible from the host. If the host port is not defined a random high-numbered port would be chosen, which can be covered by using `docker port`.

- `-P`, `--publish-all`: publish all exposed ports on the container to the host. 

- `w`, `--workdir`

- `--entrypoint`: sets the entry point for the container to the given argument, **overriding any ENTRYPOINT instruction in the Dockerfile**.

## Managing Containers

To manage containers during their lifecycle:

`docker attach [OPTIONS] container`

The `attach` allows the suer to view or interact with the main process inside the container z.B:

```bash
ID=$(docker run -d debian sh -c "while true; do echo 'tick'; sleep 1; done;")
docker attach $ID
```

- `docker create`: creates a container from an image but does not start it. Takes most of the same arguments as `run`.
- `docker cp`: copies files and directories between container and host
- `docker exec`: runs a command inside a container. 
```bash
ID=$(docker run -d debian sh -c "while true; do sleep 1; done;")
docker exec $ID echo "Hello"
```

Where the `$ID` is the container ID!.

- `docker kill`: sends a `SIGKILL` to kill container immediately. 
- `docker pause`: suspend processes in the given container.
- `docker restart`: restarts one or more containers. 
- `docker rm`: removes one or more containers. 

### Container Info
- `docker diff`: show changes made to the containers filesystem compared to the image it was launched from.
- `docker events`: prints real time events from the daemon.
- `docker inspect`: detailed info about containers or images. Covering network settings and volume mappings.
- `docker logs`: **everything that has been written to STDERR or STDOUT inside the container**.
- `docker port`: show list of ports mappings for given container. to discover the assigned ports
```bash
ID=$(docker run -P -d redis)
docker port $ID
>> 0.0.0.0:32768
```
- `docker ps`: high level info about current containers. 
- `docker top` : info about running processes in given container. 

## Dealing with Docker Images

`docker build`: builds an image from Dockerfile.
`docker commit`: creates an image from the specified container. 
- `docker export`: **exports the contents of the container's filesystem as a tar archive on STDOUT. THe resulting archive can be loaded with `docker import`. Only filesystem is imported, not metadata about ports, CMD, ENTRYPOINT, Volumes etc.
- `docker history`: info about the layers of the image
- `docker images`
- `docker import`: creates an image from an archive file containing a filesystem, such as that created by `docker export`.
- `docker load`: loads a repository from a tar achive via STDIN. Repo may contain several images and tags. Images include history and metadata. Suitable archive files are created by `docker save`.
- `docker rmi`
- `docker save`: saveds the named images or repositories to a tar archive, which is streamed to STDOUT. Use `-o` to write to a file:
```bash
docker save -o /tmp/redis.tar redis:latestimage
docker rmi redis:latestimage
docker load -i /tmp/redis.tar
docker images redis
```

-`docker tag`: associates a repository and a tag with an image. 
```bash
docker tag image:latest diegopenilla/image:newtag
```
- Adds the image:latest to the diegopenilla repo using a newtag. 

## Using the Registry

- `docker login`: register with or log in to, the registry server. If no registry is specified it is assumed it is the DockerHub. 
- `docker logout`: logs out from registry.
- `docker pull`: downloads an image from a registry. If no tag is given, gets the :latest one availabe.
- `docker push`: pushes an image or repository to the registry.
- `docker search`: prints a lsit of public respo on the docker hub matching the searched term.

## Part II Using Docker in Development p.71

We develop a single web application that returns an unique image for a given string. We will use flask:

*Dockerfile*
```docker
FROM python:3.4

RUN pip install Flask==0.10.1
WORKDIR /app
COPY app /app

CMD ["python", "identidock.py"]
```

*Flask App*
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World\n"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

```

Now test it:
```bash
curl localhost:5000
```

- Works fine, but every time the code is changed the image needs to be rebuild and the container restarted. **We can bind mount the source code folder on the host to fix this**.

After you have removed the container:
```bash
docker run -d -p 5000:5000 -v "$(pwd)"/app:/app identidock
```

There is no way we could use this container in production, it is running the default web server only intended for development too inefficient and insecure in production.

-  Using **uWSGI instead of the default Flask webserver will provide us with a flexible containerwe can use in a range of settings**.

- We can transition the container to use uWSGI by modifying the Dockerfile:

*Dockerfile*
```bash
FROM python:3.7

RUN pip install Flask==1.0.3 uWSGI==2.0.18
WORKDIR /app
COPY app /app

CMD ["uwsgi", "--http", "0.0.0.0:5000", "--wsgi-file", "/app/identidock.py", \
"--callable", "app", "--stats", "0.0.0.0:9090"]

```

- Creates a new command to run uWSGI. We tell uWSGI to **start an http server listening on port 9090, running the app application from /app/identidock.py. It also starts a stats server on port 9191.

Now run it:
```
docker build -t identidock .
docker run -d -v "$(pwd)" -p 5000:5000 -p 9090:9090 identidock
```

```bash
curl localhost:5000
curl localhost:9090
```

- Runining `docker logs container` shows that the server is complaining about beeing run as root.
  
*Dockerfile*
```docker
FROM python:3.7
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask==1.0.3 uWSGI==2.0.18
WORKDIR /app
COPY app /app

EXPOSE 5000 9090
USER uwsgi

CMD ["uwsgi", "--http", "0.0.0.0:5000", "--wsgi-file", "/app/identidock.py", \
"--callable", "app", "--stats", "0.0.0.0:9090"]
```

- Create the uswgi user and group in a normal Unix fashion
- Expose to declare the ports accesible to the host and other containers
- Sets the user for all the following lines (including `CMD` and `ENTRYPOINT`) to be uwsgi.


The Linux kernel uses UIDs and GIDs to identify users and determine their access rights. Mapping UIDs and GIDs to identifiers is handled in userspace by the OS. 
- **always set a USER in Dockerfiles, if you don't your processes will be running as root within the container. AS UIDs are the same within the container and on the host, should an attacker manage to break the container, he will have root access to the host machine**.

Let's now try another command:
```bash
docker run -d -P --name port-test identidock
docker port port-test
```

- We don't specify the ports but let Docker handle this, its practical if you have a lot of ports that need to be exposed. 

But now another problem: **we've lost access to the development tools we had such as debugging output and live code**. 
- Ideally we want to use **the same image for production and development** and enable different features depending on where it is running. We can achieve this by using an environment variable and a simple script to switch **features according to context**.

- You run a script in the dockerfile to set up what you want!
  - If the variable ENV is set to DEV, it will run the debug webserver, otherwise it will use the production server.
  
```bash
#!/bin/bash
set -e 

if ["$ENV" = "DEV"]; then
  echo "Running Development Server"
  exec python "identidock.py"
else
  echo "Running Production Server"
  exec uwsgi --http 0.0.0.0:9090 --wsgi-file /app identidock.py --callable app --stats 0.0.0.0:9191
fi
```

*Dockerfile*
```docker
FROM python:3.7
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask==1.0.3 uWSGI==2.0.18
WORKDIR /app
COPY app /app

EXPOSE 5000 9090
USER uwsgi

CMD ["/cmd.sh"]
```

```bash
chmod +x cmd.sh
docker build -t identidock .
docker run -e "ENV-DEV" -p 5000:5000 identidock
```
Page 81.