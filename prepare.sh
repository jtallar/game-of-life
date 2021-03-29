#!/bin/bash
mvn clean install || { echo 'mvn clean install failed' ; exit 1 ; }
mkdir -p out
cd ./target
tar -xzf tp2-simu-1.0-bin.tar.gz
chmod u+x tp2-simu-1.0/*.sh
cd ..
