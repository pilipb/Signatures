# Signatures Repo

The idea is to produce a standalone executable, or plugin for documents that allows the writing of a signature using the webcam and drawing with a finger.

## How to use

Run drawWithFinger.py or fingerSign.py

darw with finger allows you draw with colours and gives you more controls, finger sign allows only signatures.
    
    ```
    python drawWithFinger.py
    ```
    
    ```
    python fingerSign.py
    ```


Draw with index finger, turn off pen by closing fist, turn on pen by opening fist.

When done press 'q' or cmd + q to quit.
press 's' to save the image to the downloads folder.


### Note

In trying to develop a packaged app / executable, an error was found with mediapipe dependencies in `pyinstaller` meaning that this was unsuccessful.

 
