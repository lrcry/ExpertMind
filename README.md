# ExpertMind (formerly COMP9323)  

ExpertMind is a project for identifying how to get experts from the Internet by crowdsourcing the ideas and show them in a mindmap.  

[![Join the chat at https://gitter.im/solki/COMP9323](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/solki/COMP9323?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
project of comp9323

## Deployment

You may deploy this application using either Docker or manual methods, but using Docker is recommended, because you don't need to worry about the installation of Python and its dependencies, it will run in a sandbox environment, and it can be easily removed.

### Deploy with Docker (Recommended)

1. Install Docker in the machine for deployment.

   See Docker installation documentation for [Linux](https://docs.docker.com/linux/started/), [Mac](https://docs.docker.com/mac/started), or [Windows](https://docs.docker.com/windows/started).

2. Run `sudo docker build -t expert-mind .` in the source root folder. (don’t forget the `.` period)

   You may run `sudo docker images` to check if the image has been built successfully.

3. Run `sudo docker run -d -p "80:8000" expert-mind` to start the server.

   Here we map the `80` port in the host machine to the `8000` port in the Docker container. In your real environment, you may need to change `80` to an available port.

   You may run `sudo docker ps` to check if the server is running.

4. Open `http://localhost` in your browser. If you are using other ports rather than `80`, you should append it to the end of this url.

5. If you want to stop it, firstly get the container id using `sudo docker ps`, and then run `sudo docker stop CONTAINER_ID` to stop it.

6. If you want to remove the image, run `sudo docker rmi -f expert-mind`.


### Manual Deployment

If you don't want to use Docker as described above, you can deploy it manually in the following way.

Before deploy and use ExpertMind REST Service codes on your computer, please make sure that you have Python 2.7 and PIP installed. Use [SetupTools](https://pypi.python.org/pypi/setuptools) to setup and manage package index of python is highly recommended here.

  - Use PIP to install Django framework

      ```shell
      pip install Django
      ```

      See [Django installation documentation](https://docs.djangoproject.com/en/1.8/topics/install/#installing-official-release).
  - Use PIP to install Django REST framework support  
      ```shell
      pip install djangorestframework
      pip install markdown
      pip install django-filter
      ```
      See [Django REST frameworkd installation documentation](http://www.django-rest-framework.org/#installation)


  - Use PIP to install orchestrate mongodb service support  
      ```shell
      pip install porc
      ```
  - Startup
      - Go into the root folder of *the service* in a Terminal or &#42;nix shell environment
      - In the Terminal or &#42;nix shell environment, type the following command:
          ```shell
          python manage.py runserver
          ```
      - In a browser, type *http://localhost:8000/* to test if the services have been started up successfully.

## API Specification
   - Nodes: see [Nodes Resource REST API](https://github.com/lrcry/ExpertMind/wiki/Nodes-Resource-REST-API)
   - Events: see [Events Resource REST API](https://github.com/lrcry/ExpertMind/wiki/REST-API-description-of-Events-resource)
   
