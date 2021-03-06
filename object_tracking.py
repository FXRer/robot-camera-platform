import argparse
import time

import cv2
import imutils
from imutils.video import VideoStream

import config
from communication.Serial import Serial
from navigation import config_navigation
from navigation.ObjectFollower import ObjectFollower
from navigation.RobotSerialCommandsConverter import RobotSerialCommandsConverter
from navigation.ObjectDetectorFactory import ObjectDetectorFactory
from navigation.ImageDebug import ImageDebug


# configure argument parser
parser = argparse.ArgumentParser(description='Robot configuration')
parser.add_argument(
    'detector_type', action='store',
    help='Select detector type available types: colored-object, specific-face. For '
         'specific face an --extra-cfg is required with an image path containing the face file to be followed'
)
parser.add_argument(
    '--extra_cfg', dest='extra_cfg', action='store',
    help='Extra parameter for detector_type'
)
parser.add_argument('--show-video', dest='video', action='store_true', help='shows images on GUI')
parser.set_defaults(feature=False)
args = parser.parse_args()

serial = Serial(config.serial)  #configure serial
serial.connect()
detector = ObjectDetectorFactory.get(args.detector_type, args.extra_cfg)
object_follower = ObjectFollower(detector, RobotSerialCommandsConverter(), config_navigation.object_size_threshold)
image_debug = ImageDebug((0, 255, 255), 2)

frame_provider = VideoStream(usePiCamera=True, resolution=(1024, 768)).start()
time.sleep(2.0)


while not cv2.waitKey(30) & 0xFF == ord('q'):
    frame = frame_provider.read()
    # image is resised by with with some amount in px for better performance
    frame = imutils.resize(frame, width=config_navigation.resize_image_by_width)
    frame = imutils.rotate(frame, config_navigation.rotate_camera_by)
    object_follower.process(frame)
    if object_follower.has_command():
        command = object_follower.get_command()
        serial.send(object_follower.get_command().encode())
        print('Motor command: {0}'.format(command))
        image_debug.draw_guidelines(frame, object_follower.center, object_follower.radius)
    if args.video:
        cv2.imshow('frame', frame)

frame_provider.stop()