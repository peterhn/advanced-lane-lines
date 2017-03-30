'''
Module for calibrating camera
'''
import cv2

class CameraOptimizer():
    '''
    Calibrates camera
    '''
    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8, 0:6].T.reshape(-1,2)
    def calibrate_camera(self, img):
        '''
        Calibrates a camera based on image
        '''
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (8,6), None)
        img = cv2.drawChessboardCorners(img, (8,6), corners, ret)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints,\
                        imgpoints, gray.shape[::-1], None, None)



    def show_calibration(self):
        pass
undistorted = cal_undistort(img, objpoints, imgpoints)

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
f.tight_layout()
ax1.imshow(img)
ax1.set_title('Original Image', fontsize=50)
ax2.imshow(undistorted)
ax2.set_title('Undistorted Image', fontsize=50)
plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
    