# WhisperTRT

This project optimizes [OpenAI Whisper](https://github.com/openai/whisper) with [NVIDIA TensorRT](https://developer.nvidia.com/tensorrt#:~:text=NVIDIA%20TensorRT%2DLLM%20is%20an,on%20the%20NVIDIA%20AI%20platform.) and implements the [Wyoming Protocol](https://www.home-assistant.io/integrations/wyoming/) for Home Assistant integration..

When executing the ``base.en`` model on NVIDIA Jetson Orin Nano, WhisperTRT runs **~3x faster** while consuming only **~60%** the memory compared with PyTorch.

By default, this uses the tiny.en model.

WhisperTRT roughly mimics the API of the original Whisper model, making it easy to use. The Wyoming goodies are based off [wyoming-faster-whisper](https://github.com/rhasspy/wyoming-faster-whisper) with minimal tweaks to use WhisperTRT instead of faster-whisper.

While WhisperTRT was originally built for and tested on the Jetson Orin Nano, this project was built in Docker on an x86 Ubuntu 24.04 VM with a 4070 Ti.

Check out the [performance](#performance) and [usage](#usage) details below!


## Performance

All benchmarks are generated by calling ``profile_backends.py``,
processing a 20 second audio clip.

### Execution Time

Execution time in seconds to transcribe 20 seconds of speech on Jetson Orin Nano. See [profile_backends.py](profile_backends.py) for details.


|     | whisper (Jetson) | faster_whisper (Jetson) | whisper_trt (Jetson) | whisper (4070 Ti) | faster_whisper (4070 Ti) | whisper_trt (4070 Ti) |
|-------|---------|--------------------|--------|---------|--------------------|--------|
| tiny.en | 1.74 sec | 0.85 sec | **0.64 sec** | 0.40 sec|--------------------|--------|
| base.en | 2.55 sec | Unavailable | **0.86 sec** | 0.71 sec |--------------------|--------|


### Memory Consumption

Memory consumption to transcribe 20 seconds of speech on Jetson Orin Nano. See [profile_backends.py](profile_backends.py) for details.

|     | whisper (Jetson) | faster_whisper (Jetson) | whisper_trt (Jetson) | whisper (4070 Ti) | faster_whisper (4070 Ti) | whisper_trt (4070 Ti) |
|-------|---------|--------------------|--------|---------|--------------------|--------|
| tiny.en | 569 MB | **404 MB** | 488 MB | 672 MB |--------------------|--------|
| base.en | 666 MB |  Unavailable | **439 MB** | 726 MB |--------------------|--------|

## Usage

### Docker
1. Clone the GitHub repo.
2. Navigate into the directory.
3. Run ``docker compose up -d``.


## See also:
- [torch2trt](https://github.com/NVIDIA-AI-IOT/torch2trt) - Used to convert PyTorch model to TensorRT and perform inference.
- [NanoLLM](https://github.com/dusty-nv/NanoLLM) - Large Language Models targeting NVIDIA Jetson.  Perfect for combining with ASR!
