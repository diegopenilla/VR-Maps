# CC-VR Project



## How it works
1. The user presses the button and speaks into the mic.
2. The Pi records the audio and sends to Speech Services (Azure) to convert to text.
3. The returned text is send by the Pi to the application backend.
4. The backend looks up the text in Google and takes a picture of the website.
5. The backend dynamically changes the output shown in the frontend, updating what the user sees in the VR environment.

## Tech Stack

### Software
- **AFrame**: a VR Framework by Mozilla
- **Docker**: software with server configurations:
    - Frontend
    - Backend 
- Azure Cloud:
  - Cognitive Services Azure
    - Speech Services: for speech to text
    - Computer Vision: for picture analysis
### Hardware: 
  - Raspberry Pi 3b+ 
    - Audio Shield
    - Microphone
    - Camera 
    - Powerbank + Adapter
  - VR Cardboard Headset
  - AWS EC2 instances: Linux AMI for frontend and backend

## Future Ideas
- Apply a language model (such as LUIS) to recognize intents from recognized texts, allowing different behaviors for the applicatione 