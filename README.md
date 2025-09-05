# Cloakify 🔮
a python + opencv project that makes a red or blue cloak disappear in real time using your webcam!

## setup
1. clone this repo and open the folder in your terminal or VS code.  
2. install the required dependencies:  
   ```bash
   pip install flask opencv-python numpy
   ```
### usage
1. choose which cloak you're using.
2. step out of frame for a few seconds; the program will capture the background.
3. step back in with your cloak on. anywhere the cloak appears will now show the background instead.
CTRL + Z in the terminal to exit

#### features
- real-time video processing
- color detection in hsv color space
- background replacement for invisibility effect

front-end UI coming soon!

note: running this program will access your webcam
