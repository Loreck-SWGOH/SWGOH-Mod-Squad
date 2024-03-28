# Docker Containers

This directory contains the files needed to set-up a Docker container(s) to develop your application. There are some basic tutorials on using Docker and integrating your application.

## Download and Install Files

* Identify the command-line interface (CLI) for your operating system. For Mac/Linux, this is the Terminal program. For Windows, this is the PowerShell program.  We will call this your "CLI".

* If you're using Windows, ensure that Windows Subsytem for Linux (WSL) has been [completely installed](https://learn.microsoft.com/en-us/windows/wsl/install). You may need to enable virtualization within the BIOS settings to complete the installation.

* Download (or update) Docker Desktop on your laptop by following the [installation instructions](https://docs.docker.com/get-docker/) for your operating system. If you are using a PC with an Enterprise edition, you can use the Hyper-V Docker configuration. However, this guide will assume that you are using the WSL configuration. Ensure that you can start the Docker Desktop.

* Identify a directory that will contain your Docker containers and your git repositories. We will call this directory your "project directory". We will call the container directory your "container subdirectory".
  ```
  ├── project directory
      └── container
      └── git
      ├── *
  ```
  The Docker configuration file assumes that the containers and repositories are in the same directory to allow project code access outside of the Docker instance. If you change this structure be sure to change the Docker configuration file. WARNING: It is NOT recommended putting these directories in cloud storage --- permissions on such files may be messed up and you may have trouble running programs that depend on having specific permissions.

* Download all the files in this folder into the `container` subdirectory created above. Since GitHub works on a per repo basis you may have to download the entire repo as an archive (zip, tar, etc.) and extract only the interested files. If it's set up correctly, you should be able to find the file with path `container/compose.yaml` relative to your project directory.

## Getting started

* Ensure that the Docker Desktop is running. Open your CLI and change to your container subdirectory. Add environment variables to the `.env` file if desired.

* In the CLI, from the container subdirectory, prepare the Docker containers:
  ```
  docker compose build
  ```
  This will take quite some time, as it involves downloading various software and setting things up, but you only have to run this once. When complete you should see the container image in Docker Desktop.

* The default setup assumes that you will access the development code outside the Docker instance and that the development code is located within the git subdirectory that you created above. If you make changes to the location/name of your git subdirectory, then make the appropriate changes to `compose.yml`

* In the CLI, from the container subdirectory, to start the containers for the first time, 
  ```
  docker compose up -d
  ```
  If successful, then you should see new containers in the Docker Desktop.

## Using containers

You can manage your containers from the Docker Desktop. Starting and stopping the containers can be performed via the `Containers` section in the left menu of the Docker Desktop.

* If you need to use the CLI, then from the container subdirectory you can start/stop running the containers:
  ```
  docker compose start
  docker compose stop
  ```

* While the containers are running you can log into the Ubuntu container. From the CLI, change to the container subdirectory, and type:
  ```
  docker compose exec -it ubuntu bash --login
  ```
  You will be within what we would call your "course shell."  WARNING: Don't forget the `--login` switch; without it, your environment won't be properly initialized.

  Periodically, you'll need to access your course shell using admin priviledges. In that case use:
  ```
  docker compose exec -it -u 0 ubuntu bash --login
  ```

  Once you are in, you can also access your entire course directory on the host through `~/shared/` in your container.  You will have full read-write access.  WARNING: Files outside this directory reside ONLY within your container; unless you back them up in a different way, don't expect them to be around forever!

  HINT: When everything is command-line, sometimes it is hard to tell whether you are inside your host shell, your course shell, or even some command-line interface running within your course shell.  Pay attention to the command-line prompt, and make sure you issue the right commands in the right environment.

## Advanced usage

* To see what services are running by Docker:
  ```
  docker compose ps
  ```
  To debug some service (e.g., `postgres` database), you can see its log using the following command:
  ```
  docker compose logs --tail 50 --timestamps postgres
  ```
  To keep monitoring, just add the `--follow` flag:
  ```
  docker compose logs --tail 50 --follow --timestamps postgres
  ```

* If you need a clean restart, you can destroy the containers and its associated volumes using:
  ```
  docker compose down -v
  ```
  WARNING: This will wipe out whatever you have outside `~/shared` in your container, including things like databases you created in your containers, etc.  But sometimes it may be necessary in order to correct some configuration issues.

* Docker caches build steps in order speed up the build process, but occasionally, you run into issues where a clean rebuild is better. In that case, use:
  ```
  docker compose --progress plain build --no-cache
  ```
  The `--progress plain` flag allows you to see the entire output from the build process.

* Over time, Docker make use a lot of space with its container images, caches, volumes, etc.  You can see how much space Docker is using overall, and you reclaim a lot of space assuming that you don't need any of the volumes either:
  ```
  docker system df
  docker builder prune -a
  ```
