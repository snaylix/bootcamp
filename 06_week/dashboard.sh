# Download Metabase.jar with wget
wget https://downloads.metabase.com/v0.35.3/metabase.jar

# We need Java to launch the application
# Download Java directly from the Amazon Linux Repository
sudo yum install java-1.8.0

# Kill everything that tries to access port 80, to make sure that it's free
sudo kill -9 $(sudo lsof -t -i:80)

# This will launch a Metabase server on port 3000 by default. We need to redirect default Metabase port (:3000) to the public HTTP port (:80)
# We need to make sure that when we log out / disconnect from the AWS machine, the Metabase server is still running in the background.
sudo nohup java -jar -DMB_JETTY_PORT=80 metabase.jar &
