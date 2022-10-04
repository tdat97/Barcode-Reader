from utils.logger import logger, switch_logger_level
from run_mode import *
import argparse



def parse_option():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, default=None, help="image path")
    parser.add_argument("--loglevel", type=str, default="DEBUG", 
                        help='["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]')
    return parser.parse_args()
    

def main(opt):
    log_level = opt.__dict__["loglevel"]
    image_path = opt.__dict__["image"]
    
    switch_logger_level(log_level)
    
    if image_path is not None: 
        logger.info("RUN console mode.")
        run_console_mode(image_path)
    else:
        logger.info("RUN GUI mode.")
        run_gui_mode()
        
if __name__ == "__main__":
    opt = parse_option()
    main(opt)