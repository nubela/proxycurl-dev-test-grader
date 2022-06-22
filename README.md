# Proxycurl Dev Test Grader

This project exists as a grader for [Nubela's programming test](https://giki.wiki/@nubela/Startup-Life/dev-test).

## Get started by building this docker image

$ docker build -t proxycurl-test-validator .

## To test your own docker image

$ docker run -v /home/user/your-workspace/proxycurl-dev-test-grader:/opt -it your/imagename:tag /opt/socks.sock # run your own image

$ docker run -v /home/user/your-workspace/proxycurl-dev-test-grader:/root/share -it proxycurl-test-validator verify /root/share/socks.sock # run this validator