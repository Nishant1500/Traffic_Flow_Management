# Traffic Flow Management with AI

![image](https://github.com/Nishant1500/Traffic_Flow_Management/assets/53296643/ea54de61-2a49-4491-b02d-2b1cb47d5a6e)

## Overview

This repository contains the base code for a Traffic Flow Management system that utilizes artificial intelligence to detect vehicle density, calculate time durations for each lane, and control traffic lights using a microcontroller. The vehicle detection is performed on Google Colab, and the data is then transmitted to the microcontroller through websockets. This project, developed as a part of a school project, incorporates Supervision for vehicle counting in specific zones within each lane. Additionally, the system features a frontend built with Flowbite UI, JQuery, and Socket.io, hosted on `localhost:3000`. The project serves a Socket.io server on port `3000` for the frontend and a WebSocket server on port `4000` for communication with the microcontroller. The microcontroller uses Mike Causer's TM1637 driver to display relevant information on an LED display.

## Features

- **Vehicle Density Detection:** The system employs AI-based algorithms to detect and analyze vehicle density in each lane, with vehicle detection performed on Google Colab.

- **Zone-based Vehicle Counting:** Supervision is integrated to count the number of vehicles in specific zones within each lane, providing detailed information for traffic analysis.

- **Time Duration Calculation:** Based on real-time vehicle density data, the system calculates optimal time durations for traffic lights at each intersection.

- **Microcontroller Integration:** The traffic lights are controlled by a microcontroller, which receives the calculated time durations from the AI system through websockets and adjusts the traffic signal accordingly. The microcontroller uses Mike Causer's TM1637 driver to display relevant information on an LED display.

- **Frontend with Flowbite UI:** The user interface is built using Flowbite UI, JQuery, and Socket.io, accessible at `localhost:3000`.
    <details>
      <summary>View preview</summary>
      <img src="https://github.com/Nishant1500/Traffic_Flow_Management/assets/53296643/7f41d370-b252-4f68-80ce-57d8a238f509"/>
      <h3>Different Combinations of Light turned on:</h3>
      <img src="https://github.com/Nishant1500/Traffic_Flow_Management/assets/53296643/14308aac-6d28-408a-a499-2a2d369ca7de"/>

    </details>


- **📡 Communications:**
  - Webcame < -- > Cloud < -- > Websocket Server

- **Dependencies:**
  - [Ultralytics](https://github.com/ultralytics/ultralytics): Used for vehicle detection and analysis.
  - [Python-SocketIO](https://python-socketio.readthedocs.io/): Facilitates communication between the AI system, microcontroller, and frontend.
  - [Flask](https://flask.palletsprojects.com/): Utilized for serving the frontend and hosting the Socket.io server.
  - [Eventlet](http://eventlet.net/): Enables WebSocket communication between the AI system and the microcontroller.
  - [Supervision](https://github.com/roboflow/supervision): Used for vehicle counting in specific zones.

## Prerequisites

- Python 3.x **< 3.12**
- Microcontroller with MicroPython (e.g. Raspberry Pi Pico, Arduino) and Mike Causer's tm1637.py uploaded
- Google Colab Project (for vehicle detection in the base code)
- Flowbite UI, JQuery
- Socket.io

## Setup Instructions

1. Clone the repository (local):

   ```bash
   git clone https://github.com/Nishant1500/Traffic_Flow_Management.git
   ```
2. Upload Notebook file to Google Colab:
  Upload Enhanced_Traffic_Management.ipynb of /Cloud/ directory.
  > File: [Enhanced_Traffic_Management.ipynb](/Cloud/Enhanced_Traffic_Management.ipynb)

4. Install dependencies (local):

   ```bash
   pip install ultralytics python-socketio Flask eventlet
   ```

   Install dependencies (cloud):
   Run the cells and it will install them.

5. Connect the microcontroller and upload the micropython firmware, and Mike Causer's TM1637 driver > tm1636.py.

6. Run the main program:

   ```bash
   python index.py
   ```

7. Access the frontend at `localhost:3000` to monitor and interact with the traffic flow.

8. Run the vehicle detection on Google Colab and it pass the detections to the microcontroller through websockets.

## License

This project is licensed under the Creative Commons Zero v1.0 Universal License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Supervision for enhancing vehicle counting accuracy in specific zones.
- Flowbite UI, JQuery, and Socket.io for the interactive frontend.
- Mike Causer's TM1637 driver for displaying information on the LED display.
- Ultralytics, Python-SocketIO, Flask, and Eventlet for efficient communication and web serving.

Feel free to reach out with any questions or feedback. Happy coding!
