from cvDarts.perception import DartThrownWatcher

# Defines a list of devices which
webcam_device_ids = [1]
watcher = DartThrownWatcher(webcam_device_ids)

print(watcher.is_new_dart_recognized())
