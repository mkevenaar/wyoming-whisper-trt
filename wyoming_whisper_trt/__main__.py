#!/usr/bin/env python3
import argparse
import asyncio
import logging
import re
from functools import partial

import whisper_trt
from whisper.tokenizer import Tokenizer
from whisper_trt import ModelDimensions, AudioEncoderTRT, TextDecoderTRT
from wyoming.info import AsrModel, AsrProgram, Attribution, Info
from wyoming.server import AsyncServer

from . import __version__
from .handler import WhisperTrtEventHandler

_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        required=True,
        help="Name of whisper model to use",
        nargs='?',
        const="tiny"
    )
    parser.add_argument("--uri", required=True, help="unix:// or tcp://")
    parser.add_argument(
        "--data-dir",
        required=True,
        action="append",
        help="Data directory to check for downloaded models",
    )
    parser.add_argument(
        "--download-dir",
        help="Directory to download models into (default: first data dir)",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Device to use for inference (default: cpu)",
    )
    parser.add_argument(
        "--language",
        help="Default language to set for transcription",
    )
    parser.add_argument(
        "--compute-type",
        default="default",
        help="Compute type (float16, int8, etc.)",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--initial-prompt",
        help="Optional text to provide as a prompt for the first window",
    )
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    parser.add_argument(
        "--log-format", default=logging.BASIC_FORMAT, help="Format for log messages"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Print version and exit",
    )
    args = parser.parse_args()

    if not args.download_dir:
        # Download to first data dir by default
        args.download_dir = args.data_dir[0]

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO, format=args.log_format
    )
    _LOGGER.debug(args)

    model_name = args.model
    match = re.match(r"^(tiny|base|small|medium)", args.model)
    if match:
        # Original models re-uploaded to huggingface
        model_size = match.group(1)
        model_name = f"{model_size}"
        args.model = f"whisper-{model_name}"

    if args.language == "auto":
        # Whisper does not understand "auto"
        args.language = None

    wyoming_info = Info(
        asr=[
            AsrProgram(
                name="whisper-trt",
                description="OpenAI Whisper with TensorRT",
                attribution=Attribution(
                    name="NVIDIA-AI-IOT",
                    url="https://github.com/NVIDIA-AI-IOT/whisper_trt",
                ),
                installed=True,
                version=__version__,
                models=[
                    AsrModel(
                        name=model_name,
                        description=model_name,
                        attribution=Attribution(
                            name="OpenAI",
                            url="https://huggingface.co/OpenAI",
                        ),
                        installed=True,
                        languages=tokenizer.LANGUAGE_CODES,  # Access languages from the tokenizer
                        version=whisper_trt.__version__,
                    )
                ],
            )
        ],
    )

    # Load model
    _LOGGER.debug("Loading %s", args.model)
    # Initialize the Tokenizer
    # Assuming you have a way to get encoding and num_languages, replace '...' with actual values
    encoding = ...  # Obtain the correct encoding instance (not a string)
    num_languages = ...  # Set the number of languages supported

    tokenizer = Tokenizer(encoding=encoding, num_languages=num_languages)

    # Initialize ModelDimensions
    dims = ModelDimensions(
        n_text_ctx=...,
        n_audio_ctx=...,
        n_mels=...,
        # Other necessary dimensions
    )

    # Initialize AudioEncoderTRT
    encoder = AudioEncoderTRT(
        # Add necessary initialization parameters here
    )

    # Initialize TextDecoderTRT
    decoder = TextDecoderTRT(
        # Add necessary initialization parameters here
    )
    
    whisper_model = whisper_trt.WhisperTRT(
        dims=dims,
        encoder=encoder,
        decoder=decoder,
        tokenizer=tokenizer
    )

    server = AsyncServer.from_uri(args.uri)
    _LOGGER.info("Ready")
    model_lock = asyncio.Lock()
    await server.run(
        partial(
            WhisperTrtEventHandler,
            wyoming_info,
            args,
            whisper_model,
            model_lock,
            initial_prompt=args.initial_prompt,
        )
    )

# -----------------------------------------------------------------------------

def run() -> None:
    asyncio.run(main())

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
