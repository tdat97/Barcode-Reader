import stapipy as st
import numpy as np
import cv2
import time

class SentechCam():
    def __init__(self, light_serial=None, logger=None, ExposureTime=10000, AcquisitionMode="SingleFrame"):
        self.light_serial = light_serial
        self.logger = logger
        self.ExposureTime = ExposureTime
        self.AcquisitionMode = AcquisitionMode
        
        st.initialize()
        st_system = st.create_system()
        self.st_device = st_system.create_first_device()
        self.set_configure()
        if self.logger is not None:
            self.logger.debug(f"Device:{self.st_device.info.display_name}")
            
        self.st_datastream = self.st_device.create_datastream()
        self.st_datastream.start_acquisition()
        
    def get_image(self):
        start = time.time()
        
        self.st_device.acquisition_start()
        with self.st_datastream.retrieve_buffer() as st_buffer:
            if not st_buffer.info.is_image_present:
                if self.logger is not None:
                    self.st_device.acquisition_stop()
                    self.logger.error("st_buffer.info.is_image_present : False !!")
                return None
            st_image = st_buffer.get_image()
            st_image = st_buffer.get_image()
            pixel_format = st_image.pixel_format
            pixel_format_info = st.get_pixel_format_info(pixel_format)

            data = st_image.get_image_data()

            if pixel_format_info.each_component_total_bit_count > 8:
                nparr = np.frombuffer(data, np.uint16)
                division = pow(2, pixel_format_info
                               .each_component_valid_bit_count - 8)
                nparr = (nparr / division).astype('uint8')
            else:
                nparr = np.frombuffer(data, np.uint8)

            # Process image for display.
            nparr = nparr.reshape(st_image.height, st_image.width, 1)

            # Perform color conversion for Bayer.
            if pixel_format_info.is_bayer:
                bayer_type = pixel_format_info.get_pixel_color_filter()
                if bayer_type == st.EStPixelColorFilter.BayerRG:
                    nparr = cv2.cvtColor(nparr, cv2.COLOR_BAYER_RG2RGB)
                elif bayer_type == st.EStPixelColorFilter.BayerGR:
                    nparr = cv2.cvtColor(nparr, cv2.COLOR_BAYER_GR2RGB)
                elif bayer_type == st.EStPixelColorFilter.BayerGB:
                    nparr = cv2.cvtColor(nparr, cv2.COLOR_BAYER_GB2RGB)
                elif bayer_type == st.EStPixelColorFilter.BayerBG:
                    nparr = cv2.cvtColor(nparr, cv2.COLOR_BAYER_BG2RGB)
        
        self.st_device.acquisition_stop()
        end = time.time()
        
        if self.logger is not None:
            self.logger.debug(f"Shot Time : {end-start:.4f}")
            
        return nparr
    
    def set_configure(self):
        nodemap = self.st_device.remote_port.nodemap
        node = nodemap.get_node("ExposureTime")
        st.PyIFloat(node).set_value(self.ExposureTime)
        node = nodemap.get_node("AcquisitionMode")
        st.PyIEnumeration(node).set_symbolic_value(self.AcquisitionMode)
        
        if self.logger is not None:
            self.logger.debug(f"ExposureTime:{self.ExposureTime}, AcquisitionMode:{self.AcquisitionMode}")
        
        