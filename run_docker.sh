#!/usr/bin/bash
docker run -d -v $(pwd)/app -p 5000:5000 treemaps2:beta
