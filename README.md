# THacks2Stopcam
Project for THacks 2 - detect how many cars stop at a 4-way intersection using OpenCV

It's always annoying to see cars that don't stop at intersections when they are suppposed to, especially when it is close to a school or little children. My partner and I thought it would be cool to count how many cars stopped at a certain intersection - and show people how safe or not safe it was.

We used some footage of cars going by a four-way intersection and detecting whether or not they stopped (footage is not uploaded).

Initially we were going to use HAAR cascades to detect the cars in the frame - we didn't have enough time to train a CNN (and it wouldn't have been fast enough to demo realtime on our laptops.)
However, we didn't find a HAAR cascade that suited our needs (we were looking at the cars from the side, not from the front - which is how many of the cascades available had been trained).

So we decided to detect the cars in the frame using absolute value differences in the frames - which were first converted to grayscale -  (pixels which changed from frame to frame would have have their values increased to 256, and those that didn't would become 0)

Then we used the built-in OpenCV function to find contours in the image (which is now just the car in black and white), and determined its area. If it was greater than a threshold, then it would be considered a car.

We calculated its speed, and determined if the car stopped. If it didn't, we would add to the fileSystem.txt a binary value (0 for not stopped, 1 for stopped)

Then we served it to a webpage using Flask.

We learned a lot about detecting the speed of a moving object, as well as how to use Flask to serve specific information. Finding an alternative to HAAR cascades was also a highlight :)
