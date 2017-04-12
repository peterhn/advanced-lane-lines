'''
Module for calibrating camera
'''
import glob
import os
import pickle
import cv2
import numpy as np

class CameraOptimizer():
    '''
    Helper to calibrate camera
    '''
    OUTPUT_IMAGES_PATH = 'output_images/'
    def load_coeff(self):
        images = glob.glob('test_images/test*.jpg')

        pickle_path = self.OUTPUT_IMAGES_PATH + 'dist_pickle.p'
        if not os.path.isfile(pickle_path):
            checkered_images = glob.glob('camera_cal/calibration*.jpg')
            # optimize camera base on camera calibration images
            camera_optimizer = CameraOptimizer()
            objpoints, imgpoints = camera_optimizer.extract_objpoints(checkered_images)
            img = cv2.imread(checkered_images[0])
            img_size = (img.shape[1], img.shape[0])
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
            dist_pickle = {}
            dist_pickle['mtx'] = mtx
            dist_pickle['dist'] = dist
            print('Serializing mtx and dist...')
            with open(pickle_path, 'wb') as out:
                pickle.dump(dist_pickle, out, protocol=pickle.HIGHEST_PROTOCOL)

    def extract_objpoints(self, images):
        '''
        Calibrates a camera
        '''
        objp = np.zeros((6*9, 3), np.float32)
        objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

        objpoints = []
        imgpoints = []

        for idx, fname in enumerate(images):
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

            # If found, add object points, image points
            if ret:
                objpoints.append(objp)
                imgpoints.append(corners)

                # Draw and display the corners
                # cv2.drawChessboardCorners(img, (9, 6), corners, ret)
                # write_name = 'corners_found'+str(idx)+'.jpg'
                # cv2.imwrite(write_name, img)
                # cv2.imshow('img', img)
                # cv2.waitKey(500)
        return (objpoints, imgpoints)