#!/bin/bash
mvn clean install || { echo 'mvn clean install failed' ; exit 1 ; }
cd ./target
tar -xzf tp2-simu-java-1.0-SNAPSHOT-bin.tar.gz
chmod u+x tp2-simu-java-1.0-SNAPSHOT/*.sh
cd ..
