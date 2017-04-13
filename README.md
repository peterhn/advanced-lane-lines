# **Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./test_images/test2.jpg "Undistorted"
[image2]: ./output_images/test_undist1.jpg "Road Transformed"
[image3]: ./output_images/color_binary.png "Binary Example"
[image4]: ./output_images/perspective_transformed.png "Warp Example"
[image5]: ./output_images/warped_color_binary.png "Fit Visual"
[image6]: ./output_images/detected_lane.jpg "Output"
[video1]: ./processed_project_video.mp4 "Video"

---
### Camera Calibration

The code is contained for this step in contained in `camera_optimizer.py`.

I started the lane detection by calibrating the camera and removing distortion. This is done by preparing the "object points", which are the (x, y, z) coordinates of the chessboard corners in the world. The chessboard images were fixed on the (x, y) plane when z = 0, meaning the object points would be the same for each calibration image. So in `camera_optimizer.py`, `objp` is a replicated array of coordinates from `objpoints`, which is an array of all of the detected chessboard corners. While `imgpoints` are the pixel position of each of the corners in teh image plane with every chessboard detection.

`objpoints` and `imgpoints` were then used to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function.


### Pipeline (single images)
##### Non Distortion corrected image
![alt text][image1]

##### Distortion corrected image

![alt text][image2]

##### Color And Gradient transform
I used a combination of color and gradient thresholds to generate a binary image (`create_color_binary()` in `main.py`).  

![alt text][image3]

##### Perspective Transform

The code for my perspective transform includes a function called `warp()`. The `warp()` function takes as inputs an image (`img`) and warps the image with a hardcoded `src` and `dst` points. I chose the hardcode the source and destination points in the following manner:

```
    corners = np.float32([[190,720],[589,457],[698,457],[1145,720]])
    new_top_left=np.array([corners[0,0],0])
    new_top_right=np.array([corners[3,0],0])
    offset=[150,0]
    
    src = np.float32([corners[0],corners[1],corners[2],corners[3]])
    dst = np.float32([corners[0]+offset,new_top_left+offset,new_top_right-offset ,corners[3]-offset])    
 
```
This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 589, 457      | 340, 0        | 
| 190, 720      | 340, 720      |
| 1145, 720     | 995, 720      |
| 698, 457      | 995, 0        |

Below is an example of what the perspective transformed image looks like.

![alt text][image4]

#### Finding lane line pixels

I extracted the lane line pixels using the warped image along with color and gradient thresholding (in `find_lanes()` of `main.py`). With this warped image, I used a sliding window to find the peaks of the lane lines in the lower half of the image from a historgram. With this histogram, I added up the pixel values along each column in the image. Since the threshold image only contains either 1s or 0s, I know the lines are more apparent when there is a column full of 1s, creating a peak in the histogram, which is a starting point for lane detection within the image. Below is a sample image of what the warped image looks like:

![alt text][image5]

#### Calculating Radius of Curvature

The radius of curvature is computed upon finishing finding the lane lines in `find_lanes()` method. The method that does the computation is called `calculate_curvature_meter_radius()`. The mathematics involved is summarized in the tutorial.
For a second order polynomial f(y)=A y^2 +B y + C the radius of curvature is given by R = [(1+(2 Ay +B)^2 )^3/2]/|2A|.

#### Results of Lane Detection

Once the values of the left and right lane pixels are found from `find_lanes()`, they are mapped and warped back down to the original, undistorted image in `to_real_world_space()`, where in this method the detection drawn and returned on the original image.  Here is an example of my result on a test image:

![alt text][image6]

---

#### Final Video

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

####1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  

