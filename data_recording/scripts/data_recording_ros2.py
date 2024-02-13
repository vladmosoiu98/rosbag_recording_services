#!/usr/bin/env python3
import os
import subprocess
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class DataRecorder(Node):
    def __init__(self):
        super().__init__('data_recording')
        self.start_recording_service = self.create_service(Trigger, '/data_recording/start_recording', self.start_recording)
        self.stop_recording_service = self.create_service(Trigger, '/data_recording/stop_recording', self.stop_recording)
        self.toggle_recording_service = self.create_service(Trigger, '/data_recording/toggle_recording', self.toggle_recording)

        self.process = None
        self.recording = False

        self.output_directory = self.get_parameter('/data_recording/output_directory').get_parameter_value().string_value
        if not self.output_directory:
            self.output_directory = '~/rosbag/'

        self.topics = self.get_parameter('/data_recording/topics').get_parameter_value().string_array_value
        if not self.topics:
            self.get_logger().error('No Topics Specified.')

        self.command = ['ros2', 'bag', 'record', '-e'] + self.topics + ['__name:=data_recording_myrecorder']

        self.get_logger().info('Data Recorder Started')

    def toggle_recording(self, req, res):
        if self.recording:
            return self.stop_recording(req, res)
        else:
            return self.start_recording(req, res)

    def start_recording(self, req, res):
        if self.recording:
            self.get_logger().error('Already Recording')
            res.success = False
            res.message = 'Already Recording'
            return res

        self.process = subprocess.Popen(self.command, cwd=self.output_directory)
        self.recording = True
        self.get_logger().info('Started recorder, PID %s' % self.process.pid)
        res.success = True
        res.message = 'Started recorder, PID %s' % self.process.pid
        return res

    def stop_recording(self, req, res):
        if not self.recording:
            self.get_logger().error('Not Recording')
            res.success = False
            res.message = 'Not Recording'
            return res

        self.process.terminate()
        self.process = None
        self.recording = False

        self.get_logger().info('Stopped Recording')
        res.success = True
        res.message = 'Stopped Recording'
        return res


def main(args=None):
    rclpy.init(args=args)
    data_recorder = DataRecorder()
    rclpy.spin(data_recorder)

if __name__ == "__main__":
    main()