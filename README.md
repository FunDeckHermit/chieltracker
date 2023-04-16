# Chiel Tracker
[Tracking my friend](https://hiruventure.nl/) during his roadtrip through Japan

Made using:
 * [locationsharinglib](https://github.com/costastf/locationsharinglib) for Google Location sharing data
 * [gpxpy](https://github.com/tkrajina/gpxpy) for building/parsing .gpx files
 * [srtm4](https://github.com/centreborelli/srtm4) for getting elevation data from coordinates
 * [gpx.studio](https://github.com/gpxstudio/gpxstudio.github.io) for displaying the map and overlaying the gpx tracks

# Installation
Make a virtual environment and get the requirements above. Serve the .gpx and index.html file using Caddy and Bob's your uncle. I use a simple cron tab entry to poll for new location data.
