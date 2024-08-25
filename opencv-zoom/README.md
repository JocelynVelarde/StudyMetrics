# OpenCV-Zoom

Detects people faces if there awake or sleepy using a custom YOLOv8 model. 




## About

Since Python is not really a good option for running Computer Vision, we used C++ with a couple of libraries.

This tool uses the following:

- OpenCV with CUDA implementation
- CUDA 11.7
- cudNN 8
- TensorRT 10.0.1.6
- TensorRT API from https://github.com/cyrusbehr/tensorrt-cpp-api

The main thing to change was the config behind the COCOS.yaml object inside the original libraries from Ultralytics and being able to record live with the object detection on-going (it was really a pain to do it, but we got it working...)


## Deployment

**This tool was tested and coded on Ubuntu 20.04 LTS,** but if you got knowledge in ``CMakeLists``, just change the direction of the tools mentioned.

Before trying this tool first make sure to have installed all the tools mentioned and a C++ compiler ``g++/gcc ``.

### Extras installed
- NVIDIA Codecs
- Media Support (ffmpeg, gstreamer…)
- Camera Support
- 

```bash
  mkdir build
  cd build
  cmake ..

  make -j
```

To run with your camera just write:

```bash
  ./detect_object_video --model /path/to/your/onnx/model.onnx --input 0
```




