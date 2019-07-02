#!/usr/bin/bash
docker run -v "$(pwd)":/app -it -p 5000:5000 treemaps:beta
