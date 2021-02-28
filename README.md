# nba_forecast

This service builds an ML model to predict the winner of upcoming NBA games. The frontend can be found at [www.betterthanguessing.com](https://www.betterthanguessing.com)

It broadly consists of the following parts:
 
 - an AWS EC2 instance
 - a Docker container
 - some webscrapers to collect NBA game data
 - a cloud database
 - a machine learning model (logistic regression stacked on top of a Naive Bayes classifier)
 - HTML templates
 - an S3 bucket

To run the service you can cd into the `src` folder and run the following:
 
 - `./docker_build.sh`
 
Note that you'll need to have environment variables set in order to run this service. Set them however you like, the current setup assumes you have a `env_variables.sh` script that can be run from the same directory level as `docker_build.sh`

To push changes to your EC2 instance run `./service_deploy.sh` from the top-level directory.

To manually push website updates, run `./s3_push.sh`

If you want to make any changes to the cronjob you can just modify the `scheduling.cron` file and redeploy to EC2.
	
To locally test changes to the website, first start a server with `python3 front_end/http_testing.py`. Open a browser and navigate to `localhost:8000` to see the page hosted locally.
