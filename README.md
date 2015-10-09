# ExpertMind (formerly COMP9323)

[![Join the chat at https://gitter.im/solki/COMP9323](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/solki/COMP9323?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
project of comp9323

*I love md!*
*Hey, guys. Seems no way to modify the name of this project. Why not create a new one?*

# ExpertMind REST Service ("the service" in the following contents) Deployment, Startup and Usage
Before deploy and use ExpertMind REST Service codes on your computer, please make sure that you have Python 2.7 and PIP installed. Use [SetupTools](https://pypi.python.org/pypi/setuptools) to setup and manage package index of python is highly recommended here.
- 1. Deployment
  - Pull from branch *expertmind_services_hansmong* to your computer
  - Use PIP to install Django framework  
      ```pip install Django # see https://docs.djangoproject.com/en/1.8/topics/install/#installing-official-release```
  - Use PIP to install Django REST framework support  
      ```pip install djangorestframework```  
      ```pip install markdown```  
      ```pip install django-filter # see http://www.django-rest-framework.org/#installation```
- 2. Startup
  - Go into the root folder of *the service* in a Terminal or &#42;nix shell environment
  - In the Terminal or &#42;nix shell environment, type the following command:  
      ```python manage.py runserver```  
  - In a browser, type *http://localhost:8000/expertmind_services/* to test if the services have been started up successfully.
- 3. Usage
  - a. Node operation
    - Create a new node by the following  
    *POST /expertmind_service/create_new_node/*  
      with the JSON body like  
      {  
        "nodeDisplay": "This is a test Node name",  
        "nodeDescription": "This is a test Node description"  
      }
    - Add a child node to an existed node  
    *POST /expertmind_service/add_child_node/*  
      with the JSON body like  
      {  
        "nodeDisplay": "this is a test child node name",  
        "nodeDescription": "this is a test child node description",  
        "nodeParents"0: [  
          {"_id": "someParentId"}  
        ]  
      }  
    *Note: in current version of the services, only one parent for each node will be taken into consideration. That means if you pass a JSON body with multiple nodeParents, the services will take the first parent as the parent of the child node to be added.*
    - Get information of a Node by its ID  
      *GET /expertmind_service/get_node_by_id/[node_id]*  
      If a node is successfully retrieved, the response will generally be  
      {  
        "result": "success",  
        "data":  
        {  
          "nodeDisplay": "name",  
          "nodeDescription": "description",  
          "nodeTags": [  
            { "_id": "someId" },  
            { "_id": "otherId" }  
          ],  
          "nodeParents": [
            { "_id": "aParent" }  
          ],  
          "nodeChildren": [  
            { "_id": "child1" },  
            { "_id": "child2" }  
          ],  
          "nodeVotes": [
            { "_id": "goodVote3329" },  
            { "_id": "badVote10641" }  
          ],  
          "nodeStatus": "1",  
          "nodeCreateAt": "2015-09-29 13:42:51"  
        }  
      }
    - Get information of descendant nodes of a Node by its ID  
      *GET /expertmind_service/get_descendant_nodes/[node_id]*  
      If a node is successfully retrieved, the response will generally be  
      {  
        "result": "success",  
        "data": [  
        {  
          "nodeDisplay": "name",  
          "nodeDescription": "description",  
          "nodeTags": [  
            { "_id": "someId" },  
            { "_id": "otherId" }  
          ],  
          "nodeParents": [  
            { "_id": "aParent" }  
          ],  
          "nodeChildren": [  
            { "_id": "child1" },  
            { "_id": "child2" }  
          ],  
          "nodeVotes": [  
            { "_id": "goodVote3329" },  
            { "_id": "badVote10641" }  
          ],  
          "nodeStatus": "1",  
          "nodeCreateAt": "2015-09-29 13:42:51"  
        }]  
      }  
      *Note: in this case the response will contain a list of descendant node information.*
    - Get information of children nodes of a Node by its ID  
      *GET /expertmind_service/get_child_nodes/[node_id]*  
      {  
        "result": "success",  
        "data": [  
        {  
          "nodeDisplay": "name",  
          "nodeDescription": "description",  
          "nodeTags": [  
            { "_id": "someId" },  
            { "_id": "otherId" }  
          ],  
          "nodeParents": [  
            { "_id": "aParent" }  
          ],  
          "nodeChildren": [  
            { "_id": "child1" },  
            { "_id": "child2" }  
          ],  
          "nodeVotes": [  
            { "_id": "goodVote3329" },  
            { "_id": "badVote10641" }  
          ],  
          "nodeStatus": "1",  
          "nodeCreateAt": "2015-09-29 13:42:51"  
        }]  
      }  
      *Note: in this case the response will contain a list of chidren node information.*
