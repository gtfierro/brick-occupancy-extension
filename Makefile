upload: index.html
	scp index.html webserver:/opt/occupancy-extension/

all.ttl: *.ttl
	python combine.py

index.html: all.ttl
	pylode -i all.ttl -o index.html -f html -c true

