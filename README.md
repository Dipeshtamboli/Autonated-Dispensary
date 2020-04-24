<blockquote><p>Automated dispensary, capable of locating and identifying the medicine on the table and can move it to a desire location automatically.</p></blockquote>



We implemented an `automated dispensary` on a small scale. It is a mechanism that can `identify` strips of medicines kept on a table on the basis of their colour and shape, and pass them to a `designated spot`. There were two major components to the project - `Training a classifier` and doing the related image processing for optimizing the process of getting the position of the object from the image and `building the CNC mechanism` to transport the object.


An additional UI was a mobile app to accept voice commands and to transmit commands to the Arduino through Bluetooth, and further to the main program. Also, this project has potential applications for `bed-ridden patients`.

Contains the codes for an Automated Dispensary system.
The system builds a classifier for images of pills, powered by retraining the final layer of MobileNet architecture.
It further contains implementations to localize the positions of certain objects in the omage through contour detection and a simple sliding window.
Further, it has code to commnicate with an Arduino-UNO to recieve orders and control stepper motors.


<button style="background-color:azure;color:white;width:200px;
height:40px;">[Link to the report](https://github.com/Dipeshtamboli/Autonated-Dispensary/blob/master/report/automated_dispensary_report.pdf)</button>

<!-- /home/dipesh/Automated--Dispensary/report/automated_dispensary_report.pdf -->

<figure class="video_container">
  <video controls="true" width="888" height="500" allowfullscreen="true" poster="https://dipeshtamboli.github.io/images/itsp/vid_thumb.png">
    <source src="https://dipeshtamboli.github.io/videos/itsp/itsp_demo_video.mp4" type="video/mp4">
    <source src="https://dipeshtamboli.github.io/videos/itsp/itsp_demo_video.ogg" type="video/ogg">
    <source src="https://dipeshtamboli.github.io/videos/itsp/itsp_demo_video.webm" type="video/webm">
  </video>
</figure>