# TreeMaps

## FreshTech

### Intro
Clone the fresh tech:
```bash
git clone git@github.com:diegopenilla/VR-Maps.git
```
Enter fresh tech and docker up:
```bash
cd VR-Maps
docker-compose up 
```

## Create Database from Python Instructions
```bash
python3 database.py 
```
## Need to save Cypher Scripts also into a Folder => function that writes in Neo4j

### Endpoints 
- Flask App: `http://0.0.0.0:5000`
- Neo4j: `http://0.0.0.0:7474`

### To Do
1. Retrieve GUI generated data from Neo4j, add positions to tree/level structures (split 360 degrees conveniently).
2. Make floating text in Aframe `<scene>` look towards the user.
3. Decide wether or not to store graph scripts in firebase to persist data (use Neo4j to store url for files)
4. Add images.
5. Generate images with text inside them. 


# Local Development

## Start VR Server
```bash
cd
source flaskenv/bin/activate
cd /Users/diego/Desktop/Workspace/Code/VR-Map/
bash run_docker.sh
```

## Start Database