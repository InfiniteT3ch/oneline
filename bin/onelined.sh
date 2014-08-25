#!/bin/sh
##############################################################
# run or stop oneline's daemon
##############################################################

if [ ${1} == "--start" ]; then
	echo "Starting oneline server (c) 2014 Nadir Hamid"
	python ../server.py &
	fpid=$!
	python ../updater.py &
	pid=$(cat ./oneline.pid.txt)
	if [ -f ./oneline.pid.txt ]; then
		echo $fpid >> oneline.pid.txt
		echo $! >> oneline.pid.txt 
		echo "It worked. now accepting connections on 127.0.0.1:9000"
	else
		echo $fpid >> oneline.pid.txt
		echo $! >> oneline.pid.txt 
		echo "Oneline is already running. Please close to restart with --restart option"
	fi
fi

if [ ${1} == "--stop" ]; then
	echo "Stopping oneline server"
	pid=$(cat ./oneline.pid.txt)
	kill ${pid} &
	pid=$(cat ../socket/oneline.pid.txt)
	kill ${pid} &
	rm ./oneline.pid.txt
	rm ../socket/oneline.pid.txt
	echo "All connections to oneline have closed. Come again :("
fi

if [ ${1} == "--restart" ]; then
	echo "Restarting oneline server"
	pid=$(cat ./oneline.pid.txt)
	kill ${pid} &	
	pid=$(cat ../socket/oneline.pid.txt)
	kill ${pid} &
	rm ./oneline.pid.txt
	rm ../socket/oneline.pid.txt

	python ../server.py &
	fpid = $!
	python ../updater.py &

	echo $fpid >> oneline.pid.txt 	
	echo $! >> oneline.pid.txt 
	echo "Oneline has restarted. now accepting connections on 127.0.0.1:9000"
fi

if [ ${1} == "--help" ]; then
	echo "Hello, welcome to Oneline."
	echo "below are my options: "
	echo " "
	echo "--start starts a oneline connection on port 9000 and host 127.0.0.1"
	echo "--stop stop any running connection"
	echo "--restart restart oneline"
	echo "--repair fix any oneline files "
fi