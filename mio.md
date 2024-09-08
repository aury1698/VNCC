This repository contains code that will be used to confront the "classic" or _monolitic_ approch to software development against the more recent _serveless_ way.
The code shows a simple example of machine learning training and predictions services, using authentication and adding some fake load to pan out the execution time.

The monolitic code will be executed inside a _Kubernetes_ pod while the serverless version will be served using _OpenFaas_ .

#### Iris-server

Both the monolitic and the Openfaas functions contact a web server for authentication needs and for the storage/retrieval of the trained models.
The Dockerfile for this server follows the same structure as the others seen before, but is does not use the handle() function, instead, the whole server is implemented inside the index.py function. Here we have a Flask server which exposes GET and POST calls on different paths. This is done to show how our code could contact and interact with a remote server to host out data, since the Openfaas functions need to be _stateless_ to work correctly.
The _iris-k8s-server.yml_ is used to deploy the server inside Kubernetes and it creates a _ClusterIP_ endpoint so that the service can be contated by the whole cluster

#### OpenFaas implementation

Since OpenFaas has some default templates we can choose from, we started from the _python3_ template https://github.com/openfaas/templates/tree/master/template/python3 , which was then customized to our needs. Taking the _training function_ as an example, we have

    \
    |- iris-train.yml
    |- iris-train\
    |   |-__init__.py
    |   |-handler.py
    |   |-requirements.txt
    |- template\
        |-iris-train\
            |-Dockerfile
            |-template.yml
            |-index.py
            |-requirements.txt
            |-function\
                |-__init__.py
                |-handler.py
                |-requirements.txt

Most of the folder structure is created by using

    faas-cli new --lang iris-train iris-train

Understanding and changing the Dockerfile to fit out needs was the first step in our project.
- Inside the _python3_ template the starting image is alpine linux with python installed, this has been changed to _ubuntu_ since we are more accostumed to this OS.
- Both the templates then create a non root-user capable of executing the code.
- After copying the index.py and the requirements.txt files inside the image, pip is used to install the additional packages. To have this work inside the ubuntu enviroment we resorted to setting up a virtual enviroment and installing every dependency of our code inside of it.
- The watchdog needs to be set up to launch the _index.py_ script using the correct python inside the virtual enviroment. _fprocess_ was changed to "test/bin/python3 /home/app/index.py" and to avoid that the watchdog shuts the connection down prematurely, the write timer has been set to "write_timeout=300s"

The training code can then be put inside of the __handle()__ function inside _iris-train/handler.py_ file.
In this example the training is done over the _iris-dataset_ to show how the same structure could be replicated for a generic machine learning project.

To enable communication between the functions and the iris-server, the _openfaas_ namespace needs the correct authorization inside the cloud, which is stated inside the _openfaas-roles.yml_ file

#### Monolitic implementation

