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

### To Do Short Term
1. Retrieve GUI generated data from Neo4j, add positions to tree/level structures (split 360 degrees conveniently).
2. Make floating text in Aframe `<scene>` look towards the user.
3. Decide wether or not to store graph scripts in firebase to persist data (use Neo4j to store url for files)
4. Add images.
5. Generate images with text inside them. 

### To Do Medium Term
1. Define what we need to have running for a Minimum Viable Product.
2. How we want to continue with the design elements
3. Host a web page explaining what it does (for business side)
4. explore pitching and funding oppertunities in berlin

# Local Development

## Start VR Server
```bash
cd
source flaskenv/bin/activate
cd /Users/diego/Desktop/Workspace/Code/VR-Map/
bash run_docker.sh
```

## Start Database
