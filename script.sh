#!/bin/bash

while read postcode
do
    echo $postcode
    url=$"http://finddrivinginstructor.direct.gov.uk/DSAFindNearestWebApp/findNearest.form?pageNumber=1&postcode=$postcode"
    content=$(curl -silent -L $url)
    echo ${#content}
    if ${#content} < 9000
    	then
    	echo "foo"
   	fi
done < $1
