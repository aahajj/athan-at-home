import os
import time
import logging

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

AUDIO = os.path.join(os.path.dirname(__file__), "..", "resources", "athan.mp3")
logger = logging.getLogger(__name__)


def play_athan() -> None:
    if not os.path.exists(AUDIO):
        logger.error("Athan audio file missing")
        return

    try:
        pygame.init()
        pygame.mixer.Sound(AUDIO).play()
        time.sleep(133)
    except Exception as e:
        logger.error(f"Athan playback failed: {e}")