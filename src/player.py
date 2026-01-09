import os
import time
import logging

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

AUDIO = os.path.join(os.path.dirname(__file__), "..", "resources", "athan.mp3")
# Audio duration in seconds (2 minutes 13 seconds)
AUDIO_DURATION = 133

logger = logging.getLogger(__name__)


def play_athan() -> None:
    """
    Play the athan audio file using pygame.
    
    Logs an error if the audio file is missing or playback fails.
    """
    if not os.path.exists(AUDIO):
        logger.error(f"Athan audio file missing at {AUDIO}")
        return

    try:
        pygame.init()
        pygame.mixer.Sound(AUDIO).play()
        time.sleep(AUDIO_DURATION)
    except Exception as e:
        logger.error(f"Athan playback failed: {e}")