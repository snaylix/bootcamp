# Download Metabase.jar with wget
wget wget https://downloads.metabase.com/v0.35.3/metabase.jar

# We need Java to launch the application
# Download Java directly from the Amazon Linux Repository
sudo yum install java-1.8.0

# Launch it
java -jar metabase.jar

# We need to make sure that when we log out / disconnect from the AWS machine, the Metabase server is still running in the background.
screen
# Screen, or GNU Screen, is a terminal multiplexer. In other words, it means that you can start a screen ‘session’ and then open any number of windows (virtual terminals) inside that session. Processes running in Screen will continue to run when their window is not visible even if you get disconnected.

# This will launch a Metabase server on port 3000 by default. We need to redirect default Metabase port (:3000) to the public HTTP port (:80)
sudo java -jar -DMB_JETTY_PORT=80 metabase.jar
