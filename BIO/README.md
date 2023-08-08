# LWFR

LWFR is live video face recognition app. It is school project for Biometric Systems class for academic year 2022/2023.
Documentation is xkubik32.pdf.

This program is using pre trained face detection and face recognition models from [Deepface framework](https://github.com/serengil/deepface).

```
.
├── README.md                   
├── requirements.txt                    # Python requirements
├── face_recognition.py                 # Main functionality for live video face recognition
├── main.py                             # Main module for program
├── settings.py                         # Variables used in another packages
├── utils.py                            # Helping functions
└──
``` 

## Project setup instructions
### Installation:
```bash
# Install python interpreter in version at least 3.8.
# Install all necessary python requirements from requirements.txt:
pip install -r requirements.txt

# !!!YOU NEED TO HAVE SUPPORT FOR AVX INSTRUCTIONS OTHERWISE TENSORFLOW WILL BE FAILING WITH SEGMENTATION FAULT!!!

# Add all images you want to recognize to `database` folder.
# Setup everything necessary in `settings.py` and run program.
```

### Running:
```bash
python main.py
```

Now the program is recognizing faces from your default webcam. But you can change it to any stored file and external web cam that you want.

## Author
- [Jakub Kubík](https://github.com/Jakub-Kubik)