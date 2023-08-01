# LazyLights
LazyLights is a home automation project developed using Raspberry Pi 4 model B that allows you to control your home appliances in three different ways: through a web interface, using hand gestures, and using a specific external keyboard. The appliances are connected to the Raspberry Pi using a relay circuit.

## Raspberry Pi Circuit:
<p>
<img src="https://github.com/BlurryFace04/LazyLights/assets/64888928/6cdca357-bf3d-403e-a836-5f66841bf46c" width="49%" height="49%" />
<img src="https://github.com/BlurryFace04/LazyLights/assets/64888928/009b9a30-80bf-4e08-b838-03c92f31509c" width="49%" height="49%" />
<p>

## Demonstration Video
A demonstration video showing the working of the LazyLights project can be found [here](https://www.loom.com/share/fbee2d600988498793cb7d160198f58c?sid=c427d217-d654-443a-b4fa-3e4481d0208e). This video provides a comprehensive overview of how the system operates and how it can be used to control home appliances using a web interface, hand gestures, and a specific external keyboard.

## Features
### Web Interface Control
The web interface control is implemented using Flask. A web server is set up on the Raspberry Pi, and it hosts a web page with buttons for each appliance. When a button is clicked, a request is sent to the server to control the corresponding appliance. The server then triggers the corresponding relay in the relay circuit connected to the Raspberry Pi, which in turn controls the specific appliance.

![web-interface](https://github.com/BlurryFace04/LazyLights/assets/64888928/f4c4514a-170c-4f5d-ae79-b22166f52a34)

### Hand Gesture Control
The hand gesture control is implemented using MediaPipe and OpenCV. The system captures video input from the webcam and processes it to recognize specific hand gestures. When a recognized gesture is detected, a request is sent to the server to control a specific appliance. The server then triggers the corresponding relay in the relay circuit connected to the Raspberry Pi, which in turn controls the specific appliance.

![gesture](https://github.com/BlurryFace04/LazyLights/assets/64888928/75c51c72-593c-4aa5-93da-fd5937c2d71a)

### External Keyboard Control
The external keyboard control is implemented using AutoHotkey. It is configured to listen for specific key presses exclusively on a designated external keyboard, which is used as a macro for controlling the appliances. This setup ensures that your main keyboard's functionality remains unaffected. Upon detecting a key press on the external keyboard, it sends a POST request with a JSON payload to the server API, triggering the control of a specific appliance. The server then triggers the corresponding relay in the relay circuit connected to the Raspberry Pi, which in turn controls the specific appliance. This feature provides a cool and unique way to manage your appliances, especially when the external keyboard is dedicated to this purpose.

## Code
### Server
The server is built using Flask in Python and runs on a Raspberry Pi 4 model B. It receives requests from the gesture recognition code and controls the GPIO pins of the Raspberry Pi to control the appliances. The appliances are connected to the Raspberry Pi using a relay circuit. This setup allows for the direct control of appliances based on the input from the gesture recognition or the web interface.

### Gesture Recognition
The gesture recognition is implemented using OpenCV and MediaPipe in Python. The code captures video from the webcam and processes it to recognize specific hand gestures. When a gesture is recognized, it sends a request to the server to control a specific appliance. This allows for a seamless and intuitive user experience, where simple hand gestures can control various home appliances.

### Web Interface
The web interface is built using HTML and JavaScript. It provides a user-friendly interface that allows you to control the appliances by clicking on buttons. This interface communicates with the Flask server on the Raspberry Pi, sending commands to control the appliances based on user input.

### External Keyboard Control
The external keyboard control is implemented using AutoHotkey. It listens for specific key presses on a specific external keyboard, which is used as a macro. The keypresses on the main keyboard are not affected. When a key is pressed on the external keyboard, it sends a POST request with a JSON payload to the server API to control a specific appliance. This feature allows for a quick and easy way to control appliances without needing to interact with the web interface or use hand gestures.
