# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
import  parinya
from pupan.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
import os
import datetime
from pathlib import Path
import arrow
from flask_cors import CORS
import base64
# filesPath = r"/var/www/html/image/"
from parinya import YOLOv3
from parinya import LINE
# criticalTime = arrow.now().shift(hours=+7).shift(days=-1)
yolo = YOLOv3('coco.names','yolov3-tiny.cfg','yolov3-tiny.weights')
line = LINE('IlxhXDiH1r1avlZkK8n5vMGpwsKZLkHee5gL3Im9yUm')
base64_message = None
# for item in Path(filesPath).glob('*'):
#     if item.is_file():
#         print (str(item.absolute()))
#         itemTime = arrow.get(item.stat().st_mtime)
#           # if itemTime < criticalTime:
#           #   #remove it
#           # pass




# for filename in os.listdir(path):
#     print(filen ame)
#     # if os.stat(os.path.join(path, filename)).st_mtime < now - 7 * 86400:
#     if os.path.getmtime(os.path.join(path, filename)) < now - 7 * 86400:
#         if os.path.isfile(os.path.join(path, filename)):
#             #print(filename)
#             os.remove(os.path.join(path, filename))


# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)


CORS(app)
cors = CORS(app, resources={
    
    r"/*":{
        "origins":"*"
        
        }
    })



# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()


time.sleep(2.0)




def delete1():
        
        path = r"/var/www/html/image/"
        now = time.time()
        items = os.listdir("/var/www/html/image/")
        newlist = []
        for names in items:
                if names.endswith(".png"):
                        os.remove(path+'/'+names)

@app.route("/")
def home_page():
    return Response(dumps({
        'content': 'Allow Access Origin'
        }), mimetype='text/json')

@app.route("/del")
def delete():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(delete1(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/camera")
def index():
    # return the rendered template
    return render_template("index.html")
def generate1():
    return str(datetime.datetime.now())
    #cv2.imwrite('/var/www/html/image/'+str(datetime.datetime.now())+'.png', outputFrame)
@app.route("/pic")
def pic():
    return str(base64_message)

@app.route("/cap")
def capture():
    # return the response generated along with the specific media
    # type (mime type)
    date1= str(datetime.datetime.now())
    cv2.imwrite('/var/www/html/image/'+str(date1)+'.png', outputFrame)
    with open('/var/www/html/image/'+str(date1)+'.png', 'rb') as binary_file:
    	binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
   
    base64_message = base64_encoded_data.decode('utf-8')
    print(base64_message)
    #with open('/var/www/html/image/'+str(date1)+'.png', "rb") as img_file:
        #my_string = base64.b64encode(img_file.read())
        #print(my_string)
    
    
       #mimetype = "multipart/x-mixed-replace; boundary=frame")

def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock
    

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0) 
         yolo.detect(frame, draw=False)
         yolo.detect(frame)
         obj = yolo.detect(frame, draw=False)
         for A in obj:
             labal, left, top, width , height = A
             if (labal[0]=='p' and labal[3] == "s"):
                 print(labal)
                 time.sleep(5)
#                 line.sendimage(frame[:, :, ::-1])
                 date1= str(datetime.datetime.now())
                 cv2.imwrite('/var/www/html/image/'+str(date1)+'.png', frame)
                 # cv2.imwrite('/var/www/html/image/'+str(date1)+'.png', outputFrame)
                 with open('/var/www/html/image/'+str(date1)+'.png', 'rb') as binary_file:
                 binary_file_data = binary_file.read()
                 global base64_message
                 base64_encoded_data = base64.b64encode(binary_file_data)
                 base64_message = base64_encoded_data.decode('utf-8')
#                 print(base64_message)
                #with open('/var/www/html/image/'+str(date1)+'.png', "rb") as img_file:
                    #my_string = base64.b64encode(img_file.read())
                    #print(my_string)
                
        
        



        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        #cv2.imwrite('/home/pupan/Documents/'+str(datetime.datetime.now())+'.png', outputFrame)
        
        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        

        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)

            # cehck to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                    (0, 0, 255), 2)
        
        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    
    
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
        help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
        help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
        threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()
