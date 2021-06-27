import os
import shelve
import markdown

# Import the framework
from flask import Flask, g
import flask_restful
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Create the API
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("docker_stats.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():

    # README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        content = markdown_file.read()

        # Convert it to HTML
        return markdown.markdown(content)

#get all container with all values 
#URL might be http://127.0.0.1:5000/containers
class ContainerList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())
        

        container = []

        for key in keys:
            container.append(shelf[key])

        #return {'message': 'Success', 'data': container}, 200
        return container, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('containerid', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('status', required=True)
        parser.add_argument('node', required=True)
        parser.add_argument('timestamp', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['containerid']] = args

        return {'message': 'DockerContainer registered', 'data': args}, 201


###Nodes
#get a container list (only Container IDs from a single node
#and delete all container from a single node 
#example URL 
#http://127.0.0.1:5000/nodes/Node_1
class NodeList(Resource):
    def get(self, fromnode): # fromnode = <string:fromnode>
        shelf = get_db()
        keys = list(shelf.keys())
        container = []
        container_from_node = []

        for key in keys:
            container.append(shelf[key])

        for item in container:
            if fromnode in item.values():
                container_from_node.append((item['containerid']))

        return container_from_node, 200

    def delete(self, fromnode):
        shelf = get_db()
        keys = list(shelf.keys())
        container = []
        container_from_node = []
        print("fromnode: ", fromnode)

        for key in keys:
            container.append(shelf[key])

        for item in container:
            #print(item)
            if fromnode in item.values():
                #print("bbbb")
                container_from_node.append((item['containerid']))
                containerid = item['containerid']
                del shelf[containerid]
                                
        return container_from_node, 200


#get a single container 
#http://127.0.0.1:5000/8fd6356dd918
class Container(Resource):
    def get(self, containerid):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (containerid in shelf):
            return {'message': 'Container not found', 'data': {}}, 404

        return {'message': 'Container found', 'data': shelf[containerid]}, 200

    def delete(self, containerid):
        shelf = get_db()

        # If the key does not exist return 404
        if not (containerid in shelf):
            return {'message': 'Container not found', 'data': {}}, 404

        del shelf[containerid]
        return '', 204


api.add_resource(ContainerList, '/containers')
api.add_resource(Container, '/container/<string:containerid>')
#####
api.add_resource(NodeList, '/nodes/<string:fromnode>') #delete request - delets all containers for this node