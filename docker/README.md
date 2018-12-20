# Instructions for using Docker with pdia
Last updated on August 17, 2018.
```
Jason Xie
Princeton, NJ
```

Docker is not compatible with versions of Windows before Windows 10.

## Table of contents
1. [Installing and setting up Docker](#setup)
2. [Running pdia/docked-jupyter](#run)
3. [Troubleshooting and FAQ](#help)


## Installing and setting up Docker <a name="setup"></a>

1. Create a Docker Hub account at the following
```
https://hub.docker.com
```
2. Download Docker Community Edition for free from the following
```
https://www.docker.com/community-edition
```
3. Install Docker on your computer. This requires administrator access.

  If you are using Windows 10, you will need to restart your computer in order to setup HyperV.

4. Open Docker and login using the credentials you used to setup your Docker Hub account.


## Running pdia/docked-jupyter <a name="run"></a>

1. You can find a file to run Jupyter in the *docker/* folder. This will be **pdj-mac.command** on Mac or **pdj-windows.bat** on Windows.

  The first time you run this file, a security prompt may appear warning you that the file is unverified. Ignore the warning and allow the file to run. You can inspect the code yourself by opening the file using the text editor of your choice.

  Running this file will open a terminal window, which will prompt you to specify which version of pdia you would like to work with.

  Once you have made your choice, it will automatically pull the latest version of the appropriate image from Docker Hub, set up a new instance of Jupyter, and open it in your default browser.

2. Jupyter opens onto a home directory with a *work/* subfolder. The *work/* subfolder is linked to the folder from which you ran pdj-starter. **Anything that you don't save into _work/_ will be destroyed when you end this container.**

3. Return to the terminal window and press any key to close the process and clean up the container.

4. You can run pdj-mac or pdj-windows from any folder that Docker has permission to access by dragging it into the folder of choice and opening it. If there is a problem, check Docker preferences or settings and make sure that Docker has access to the drive in question.

5. When you are using Docker on a Windows computer shared with multiple users, **make sure to quit Docker and then sign out before leaving the computer for an extended period of time.** This gets in front of a bug related to how Windows computers hibernate, which at times may force us to restart the computer to make Docker start working again.


## Troubleshooting <a name="help"></a>

### Docker

If Docker will not open, check to make sure that your account is in docker-users and it is not running on any other account.

If Docker is using more or less CPU than expected, change the Settings (or Preferences in Mac) under the Advanced tab from the Docker icon. By default, Docker will be limited to 2 cores.

### Using pdj-mac or pdj-windows

If the program fails with an HTTP error, restart your machine and try again.

If the program fails with a big error message concerned with enchant, make sure you have the latest version of requirements.txt and setup.py

If the program fails with an input/output error, quit Docker, sign out of your account, and sign back in.

If Jupyter does open but asks for a password, input the token **pdia**. If this fails, restart the computer and try again.

If Jupyter is ever empty, your folder is not mounted properly. Go to Docker and reset the file sharing permissions. You should be able to see pdj-mac or pdj-windows at least.

## FAQ

### What is Docker?

Docker is a tool that creates identical disposable environments to work inside from anything that can run Docker. No matter what the host machine is like or how many programs and libraries have or haven't been installed on it, as long as it can run Docker, you can use the host machine to run as many virtual computers with exactly the environments you need as you want for as long as you like, and destroy them all once you are done.

### How do I see what's inside these installers?

On Mac, you can view the code from any text editor at least as powerful as TextEdit; I work in Atom.
On Windows, you can view the code from any text editor at least as powerful as Notepad; I work in Notepad++.

### How do I save a _ file?

A Dockerfile can be created by saving a text document as "Dockerfile" including quotation marks with no extension on Windows.

A .dockerignore file can be created by saving a text document as .dockerfile. with both periods and no extension on Windows.

A .command file may not be executable by any user until you run the following
```
chmod 777 example.command
```
