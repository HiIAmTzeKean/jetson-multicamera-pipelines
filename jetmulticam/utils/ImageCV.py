from PIL import Image
import io
import cv2
import numpy as np

class ImageCV:
    def __init__(self, gstSample):
        self._imageBuffer = self.getImageBuffer(gstSample)
        self._image = Image.open(io.BytesIO(self._imageBuffer))
        self._imageCV = None
        self.toOpenCV()

    def getImageBuffer(self,gstSample):
        if gstSample is None:
            return None
        
        # get buffer from the Gst.sample object
        buf = gstSample.get_buffer()
        buf2 = buf.extract_dup(0, buf.get_size())
        return buf2
    
    def toOpenCV(self):
        imageStream = io.BytesIO(self._imageBuffer)
        self._imageCV = cv2.imdecode(np.frombuffer(imageStream.read(), np.uint8), -1)
        # print(type(self._imageCV))
    
    def showCVImage(self):
        if (self._imageCV is None):
            raise Exception("Image CV not created")
        cv2.imshow("image", self._imageCV)
        cv2.waitKey(0)

    def showPillowImage(self):
        self._image.show()
    
    def getCVImage(self):
        return self._imageCV

from typing import List
class ImageStitcher():
    def __init__(self,imageCVArray:List[ImageCV], size:int=2) -> None:
        self._size = size
        self._mode = cv2.Stitcher_PANORAMA
        self._imageArray = list()
        for item in imageCVArray:
            self._imageArray.append(item.getCVImage())
        self._result = None
        
    def stitch(self):
        try:
            stitchy = cv2.createStitcher(self._mode)
            (status, self._result) = stitchy.stitch(self._imageArray)
            if (status == 0):
                # all okay here
                pass
            elif (status == 1):
                # cv2.imshow("image1", self._imageArray[0])
                # cv2.waitKey(0)
                # cv2.imshow("image2", self._imageArray[1])
                # cv2.waitKey(0)
                raise Exception("Error stitching: Not enough keypoints")
            elif (status == 2):
                raise Exception("Error stitching: Homography fail")
        except Exception as e:
            print(e)
            raise e
    
    def showImage(self):
        if (self._result == None):
            self.stitch()
        cv2.imshow("image1", self._imageArray[0])
        cv2.imshow("image2", self._imageArray[1])
        cv2.imshow("output", self._result)
        cv2.waitKey(100)