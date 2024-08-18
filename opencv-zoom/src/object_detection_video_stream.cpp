#include "cmd_line_util.h"
#include "yolov8.h"
#include <opencv2/cudaimgproc.hpp>
#include <opencv2/videoio.hpp>  // Para cv::VideoWriter
#include <filesystem>           // Para manejo de rutas y directorios

// Runs object detection on video stream then displays annotated results.
int main(int argc, char *argv[]) {
    YoloV8Config config;
    std::string onnxModelPath;
    std::string inputVideo;

    // Parse the command line arguments
    if (!parseArgumentsVideo(argc, argv, config, onnxModelPath, inputVideo)) {
        std::cerr << "Error parsing command line arguments." << std::endl;
        return -1;
    }

    // Create the YoloV8 engine
    YoloV8 yoloV8(onnxModelPath, config);

    // Initialize the video stream
    cv::VideoCapture cap;

    // Open video capture
    try {
        cap.open(std::stoi(inputVideo));
    } catch (const std::exception &e) {
        cap.open(inputVideo);
    }

    // Check if the capture is opened
    if (!cap.isOpened()) {
        std::cerr << "Unable to open video capture with input '" << inputVideo << "'." << std::endl;
        return -1;
    }

    // Try to use HD resolution (or closest resolution)
    auto resW = cap.get(cv::CAP_PROP_FRAME_WIDTH);
    auto resH = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
    std::cout << "Original video resolution: (" << resW << "x" << resH << ")" << std::endl;
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 1280);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 720);
    resW = cap.get(cv::CAP_PROP_FRAME_WIDTH);
    resH = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
    std::cout << "New video resolution: (" << resW << "x" << resH << ")" << std::endl;

    // Define the output video file path
    std::string outputPath = "/home/rob/Documents/recordings/recorded_video.mp4";
    std::filesystem::create_directories(std::filesystem::path(outputPath).parent_path()); // Crear el directorio si no existe

    // Initialize VideoWriter
    cv::VideoWriter writer;
    writer.open(outputPath, cv::VideoWriter::fourcc('M', 'J', 'P', 'G'), 30, cv::Size(resW, resH), true);
    
    if (!writer.isOpened()) {
        std::cerr << "Unable to open video writer for output path '" << outputPath << "'." << std::endl;
        return -1;
    }

    while (true) {
        // Grab frame
        cv::Mat img;
        cap >> img;

        if (img.empty()) {
            std::cerr << "Unable to decode image from video stream." << std::endl;
            break;
        }

        // Run inference
        const auto objects = yoloV8.detectObjects(img);

        // Draw the bounding boxes on the image
        yoloV8.drawObjectLabels(img, objects);

        // Write the frame to the video file
        writer.write(img);

        // Display the results
        cv::imshow("Object Detection", img);
        if (cv::waitKey(1) >= 0)
            break;
    }

    // Release resources
    cap.release();
    writer.release();
    cv::destroyAllWindows();

    return 0;
}
