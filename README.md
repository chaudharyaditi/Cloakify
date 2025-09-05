# Cloakify 🔮
a python + opencv + flask project that makes a red, blue or green cloak disappear in real time using your webcam!

## setup
1. clone this repo and open the folder in your terminal or VS code.  
2. install the required dependencies:  
   ```bash
   pip install flask opencv-python numpy
   ```
### usage
1. choose which cloak you're using (this could be a shirt, blanket, towel etc that is the same color as the option you chose)
2. step out of frame for a few seconds; the program will capture the background.
3. step back in with your cloak on. anywhere the cloak appears will now show the background instead.

#### features
- real-time video processing
- color detection in hsv color space
- background replacement for invisibility effect

note: running this program will need to access your webcam
