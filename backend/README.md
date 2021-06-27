# Container Status backend

### List all containers

URL +
`GET /containers`

**Response**

- `200 OK` on success

```json

[
    {"containerid": "8fd6356dd918", 
    "name": "test container 1", 
    "status": "exited", 
    "node": "Node_1", 
    "timestamp": "2021-06-27 18:20:04.638700"
    },

    {"containerid": "0f3b8820ed65", 
    "name": "test container 2", 
    "status": "running", 
    "node": "Node_1", 
    "timestamp": "2021-06-27 18:20:04.638700"
    }   
]

```


### adding a new container

**Definition**

`POST /container`

**Arguments**

- `"containerid":string` Container ID from docker
- `"name":string` a user friedly name of the container
- `"status":string` Status of the container Up or down or pause ....
- `"node":string` docker node where the container is running on 
- `"timestamp":string`something like last seen ;)

if the container is already available this data will be just overwritten


**Response**

- `201 Created` on success

```json
{"containerid": "8fd6356dd918", 
    "name": "test container 1", 
    "status": "exited", 
    "node": "Node_1", 
    "timestamp": "2021-06-27 18:20:04.638700"
}
```


## Delete all container from a single node
this function will be used every time, when the worker client sends his feedback to the backend. 
A very simple way to make sure, only currently available containers on this node are represented in the dockerstats backend.
There might be a more sophisticated way to do inside the backend. But this is just a quick and dirty approach to implement it.
**Definition**

`DELETE /nodes/<node>`

**Response**

- `200` list af all deleted containers