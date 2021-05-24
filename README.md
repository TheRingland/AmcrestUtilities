# AmcrestUtilities

Some handy little scripts I wrote for my Amcrest Cameras. Will probably work on Dahua brand as well. 

1. cameraconfigbackups.py - Bypasses the nasty config encryption and extracts all the current settings into a JSON file. Just add your IP's to the CAMERA_IP list and set your credentials. I'm sure it could use a lot more love, but not today.

2. cameradaylight.py - Uses the Sunrise-Sunset API to find the current Dusk and Dawn times, then programs the Day/Night schedule on the cameras in the list accordingly. The API has limits, so I only hit it once a day to be nice. 

- LAT/LNG = Camera Latitude and Longitude to 6 decimals as a String.
- DELTA = Amount of time to add to Sunrise and subtract from Sunset for "Day" mode
- CAMERA_IP = List of Camera IP's
- CAMERA_USER = Admin username of Camera
- CAMERA_PASS = Admin Password of Camera


Many thanks to the team at https://sunrise-sunset.org/api . 
