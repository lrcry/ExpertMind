from django.test import TestCase
from dao.nodes import Nodes

# Create your tests here.

input = {
    'nodeDisplay': 'just for test',
    'nodeDescription': 'Third node for Nodes Class',
    'nodeTags': [],
    'nodeParents': [],
    'nodeChildren': [],
    'nodeVotes': [
        {
            "_id": "100000000"
        }
    ],
    'nodeStatus': 1
}

return_node = Nodes().create(input['nodeDisplay'], input['nodeDescription'], input['nodeTags'], input['nodeParents'],
                             input['nodeChildren'], input['nodeVotes'], input['nodeStatus'])

if "key" in return_node:
    for key in return_node:
        print key, ": ", return_node[key]