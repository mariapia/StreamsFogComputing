# StreamsFogComputing

# Running
The project can be executed using the scripts in the folder.

1. **build_dockers.sh** - it builds three different types of docker images, one for each type of nodes in the architecture (EdgeNode, Fognode, CloudNode)
2. **run_cloud.sh** - it runs the instance for the cloud.
3. **run_fog.sh** - it runs an instance for the FogNode. It accepts:
    * the name of the image.
4. **run_edge.sh** - it runs an instance for the EdgeNode. It accepts:
    * the name of the the edge device
    * the path of the text that has to be analyzed
    * the number of lines of the text that will be analyzed
5. **stop_dockers.sh** - it stops all the dockers whose names are given as parameters
6. **remove_dockers.sh** - it deletes all the docker instances whose names are given as parameters.
