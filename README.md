# ROSBag Recording Services
This is a simple ROS2 package that allows starting and stopping rosbag2 recordings via service calls, which is useful for performing repeated data collection.

>**Disclaimer:**  
This package is still using the CLI command for recording ros2 bags, which is not the most efficient way to do it. The package will be updated to use the rosbag2 API when it becomes available.

## Config
The config for the recording is in config/config.yaml.\
Configure the output directory for the rosbag files and topics to be recorded.\
Rosbag files are saved with the current date and time as a filename. [**might change this**]

## Launching
```
ros2 launch data_recording data_recording.launch.py
```

## Services Available
The package creates three services, which can be called with a `std_srvs.srv.TriggerRequest` message:
* /data\_recording/start\_recording
* /data\_recording/stop\_recording
* /data\_recording/toggle\_recording
