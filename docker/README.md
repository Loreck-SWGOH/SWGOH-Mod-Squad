# Docker Containers

This directory contains the files needed to set-up a Docker container.

## Prerequisites

* Download and install [Docker
  Desktop](https://docs.docker.com/get-docker/) on your laptop.  If
  you have a previous installation, perform an update to make sure you
  stay on the latest version.

* You should have some command-line interface running on your laptop.
  For Mac/Linux, this is the Terminal program, and for Windows, this
  can be the PowerShell.  We will call this your "host shell".

* Pick a directory where you have all your course-related stuff, e.g.,
  `~/316` (for Mac/Linux) or `C:\316` (for Windows).  We will call
  this directory your "course directory (on laptop)".  WARNING: We do
  NOT recommend putting this directory in cloud storage ---
  permissions on such files may be messed up and you may have trouble
  running programs that depend on having specific permissions.

* Download and unzip the [316 container repository source
  code](https://gitlab.oit.duke.edu/compsci316/316-container/-/archive/main/316-container-main.zip)
  inside your course directory on laptop.  Name (or rename) that
  subdirectory `container`.  We will call this subdirectory your
  "container subdirectory (on laptop)".  If it's set up correctly, you
  should be able to find the file with path
  `container/docker-compose.yaml` relative to your course directory.

  - Alternatively, if you already have `git` installed on your laptop,
    you can simply clone the [316 container
    repository](https://gitlab.oit.duke.edu/compsci316/316-container).
    Doing `git pull` from within this container subdirectory on your
    laptop will get you the latest source files.

## Getting started

* Make a copy of the file `env-template.txt` in the container subdirectory and
  name it `.env`; then edit the fields to your liking.  The following commands
  assume you are using Mac/Linux:
  ```
  cd ~/316/container/
  cp env-template.txt .env
  nano .env
  ```
  For all subsequent steps, we assume that Docker Desktop is up and
  running, and you are executing commands in your host shell with your
  working directory being the container subdirectory (where
  `docker-compose.yaml` resides).

* Use the following to prepare for launching containers the first time:
  ```
  docker compose build
  ```
  This will take quite some time, as it involves downloading various
  software and setting things up, but you only have to run this once.

* In our default setup, we assume that for convenience, you will want
  to access your entire course directory from within your container as
  well.  Hence, before we launch the containers, open Settings for
  Docker Desktop, go to Resources -> File Sharing, and add your course
  directory (one level above the container directory) to the list (to
  be "bind mounted").

* To start the containers for the first time, 
  ```
  docker compose up -d
  ```

## Using containers

For the following, assume that Docker Desktop is up and running, and
you are executing commands in your host shell with your working
directory being the container subdirectory (where
`docker-compose.yaml` resides).

* To start/stop running the containers, use:
  ```
  docker compose start
  docker compose stop
  ```

* While the containers are running, to log into your container running Ubuntu, type:
  ```
  docker compose exec -it ubuntu bash --login
  ```
  You will be within what we would call your "course shell."  WARNING:
  Don't forget the `--login` switch; without it, your environment
  won't be properly initialized.

  Once you are in, you can also access your entire course directory on
  the host through `~/shared/` in your container.  You will have full
  read-write access.  WARNING: Files outside this directory reside
  ONLY within your container; unless you back them up in a different
  way, don't expect them to be around forever!

  HINT: When everything is command-line, sometimes it is hard to tell
  whether you are inside your host shell, your course shell, or
  even some command-line interface running within your course
  shell.  Pay attention to the command-line prompt, and make sure you
  issue the right commands in the right environment.

## Advanced usage

* To see what services are running by Docker:
  ```
  docker compose ps
  ```
  To debug some service (e.g., `postgres` database), you can see its
  log using the following command:
  ```
  docker compose logs --tail 50 --timestamps postgres
  ```
  To keep monitoring, just add the `--follow` flag:
  ```
  docker compose logs --tail 50 --follow --timestamps postgres
  ```

* If you need a clean restart, you can destroy the containers and its
  associated volumes using:
  ```
  docker compose down -v
  ```
  WARNING: This will wipe out whatever you have outside `~/shared` in
  your container, including things like databases you created in your
  containers, etc.  But sometimes it may be necessary in order to
  correct some configuration issues.

* Docker caches build steps in order speed up the build process, but
  occasionally, you run into issues where a clean rebuild is better.
  In that case, use:
  ```
  docker compose --progress plain build --no-cache
  ```
  The `--progress plain` flag allows you to see the entire output from
  the build process.

* Over time, Docker make use a lot of space with its container images,
  caches, volumes, etc.  You can see how much space Docker is using
  overall, and you reclaim a lot of space assuming that you don't need
  any of the volumes either:
  ```
  docker system df
  docker builder prune -a
  ```
