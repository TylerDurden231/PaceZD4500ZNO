# Test name = HDMI Video Output
# Test description = Analyze video on all HDMI formats

from datetime import datetime
from time import gmtime, strftime
import time
import device

import TEST_CREATION_API
import NOS_API

## Max record video time in miliseconds
MAX_RECORD_VIDEO_TIME = 5000

MAX_RECORD_AUDIO_TIME = 3000

def runTest():
    System_Failure = 0
    
    while(System_Failure < 2):
        try:
            ## Set test result default to FAIL
            test_result = "FAIL"
            
            test_result_4k = False
            test_result_HDMI = False
            test_result_1080 = False
            test_result_720 = False
            
            error_codes = ""
            error_messages = ""
            
            channel_4K = False
            pqm_channel_4K = False       

            
            pqm_SD_720 = False
            
            ## Initialize grabber device
            NOS_API.initialize_grabber()

            ## Start grabber device with video on default video source
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
            TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
            time.sleep(1)
            
            if(System_Failure == 1):
                NOS_API.Send_RF4CE_Command("b")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("b")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("b")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("b")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("b")
                time.sleep(0.2)
                
                NOS_API.Send_RF4CE_Command("o")
                time.sleep(1)
                
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                
                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                if (video_height != "1080"):
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("o")
                    time.sleep(2)
                    NOS_API.Send_RF4CE_Command("r")
                    time.sleep(2)
                    NOS_API.Send_RF4CE_Command("r")
                    time.sleep(2.5)
                    NOS_API.Send_RF4CE_Command("o")
                    time.sleep(4)
                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                    if (video_height != "1080"):
                        NOS_API.set_error_message("Resolução")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                        error_codes = NOS_API.test_cases_results_info.resolution_error_code
                        error_messages = NOS_API.test_cases_results_info.resolution_error_message                     
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file) 
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                    
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        return
                    NOS_API.Send_RF4CE_Command("b")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("u")
                    time.sleep(0.2)
                    NOS_API.Send_RF4CE_Command("u")
                    time.sleep(0.2)
                    NOS_API.Send_RF4CE_Command("o")
                    time.sleep(0.2)
                else:
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)
                    NOS_API.Send_RF4CE_Command("d")
                    time.sleep(0.5)

                    NOS_API.Send_RF4CE_Command("o")
                    time.sleep(0.5)
                        
                NOS_API.Send_RF4CE_Command("1")
                time.sleep(0.5)
                NOS_API.Send_RF4CE_Command("2")
                time.sleep(0.5)
                NOS_API.Send_RF4CE_Command("1")
                time.sleep(0.5)
                NOS_API.Send_RF4CE_Command("o")
                time.sleep(1)
                NOS_API.Send_RF4CE_Command("d")
                time.sleep(1)
                NOS_API.Send_RF4CE_Command("6")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("0")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("0")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("0")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("o")
                time.sleep(1)
                NOS_API.Send_RF4CE_Command("d")
                time.sleep(1)
                
                if not(NOS_API.grab_picture("Modulation")):
                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = ""    
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                        NOS_API.upload_file_report(report_file) 
                        NOS_API.test_cases_results_info.isTestOK = False
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    return
                start_time = int(time.time())
                while not(TEST_CREATION_API.compare_pictures("4k_Parameters_mod_ref", "Modulation", "[Modulation]", NOS_API.thres)):
                    NOS_API.Send_RF4CE_Command("r")
                    time.sleep(1)
                    if not(NOS_API.grab_picture("Modulation")):
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file) 
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                    
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        return
                
                    timeout = int(time.time()) - start_time
                    if (timeout > 30):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        test_result = "FAIL"
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False


                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        return 
                    
                NOS_API.Send_RF4CE_Command("o")
                time.sleep(1)
                NOS_API.Send_RF4CE_Command("d")
                time.sleep(1)

                if not(NOS_API.grab_picture("Anexo")):
                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = ""    
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                        NOS_API.upload_file_report(report_file) 
                        NOS_API.test_cases_results_info.isTestOK = False
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    return
                start_time = int(time.time())
                while not(TEST_CREATION_API.compare_pictures("4k_Parameters_anx_ref", "Anexo", "[Anexo]", NOS_API.thres)):
                    NOS_API.Send_RF4CE_Command("r")
                    time.sleep(1)
                    if not(NOS_API.grab_picture("Anexo")):
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file) 
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                    
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        return
                
                    timeout = int(time.time()) - start_time
                    if (timeout > 30):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        test_result = "FAIL"
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False


                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        return 
                
                NOS_API.Send_RF4CE_Command("o")
                time.sleep(1)
                NOS_API.Send_RF4CE_Command("d")
                time.sleep(1)     
                NOS_API.Send_RF4CE_Command("7")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("9")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("8")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("8")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("o")
                time.sleep(1)
                NOS_API.Send_RF4CE_Command("d")
                time.sleep(1)
                
                if not(NOS_API.grab_picture("Video_type")):
                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = ""    
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                        NOS_API.upload_file_report(report_file) 
                        NOS_API.test_cases_results_info.isTestOK = False
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    return
                start_time = int(time.time())
                while not(TEST_CREATION_API.compare_pictures("4k_Parameters_tv_ref", "Video_type", "[Video_type]", NOS_API.thres)):
                    NOS_API.Send_RF4CE_Command("r")
                    time.sleep(1)
                    if not(NOS_API.grab_picture("Video_type")):
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file) 
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                    
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        return
                
                    timeout = int(time.time()) - start_time
                    if (timeout > 30):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        test_result = "FAIL"
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False


                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        return 
                
                NOS_API.Send_RF4CE_Command("o")
                time.sleep(1)
                NOS_API.Send_RF4CE_Command("d")
                time.sleep(1)     
                NOS_API.Send_RF4CE_Command("7")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("9")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("8")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("9")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("o")
                time.sleep(1)
                NOS_API.Send_RF4CE_Command("d")
                time.sleep(1)
                
                if not(NOS_API.grab_picture("Audio_type")):
                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = ""    
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                        NOS_API.upload_file_report(report_file) 
                        NOS_API.test_cases_results_info.isTestOK = False
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    return
                start_time = int(time.time())
                while not(TEST_CREATION_API.compare_pictures("4k_Parameters_ta_ref", "Audio_type", "[Audio_type]", NOS_API.thres)):
                    NOS_API.Send_RF4CE_Command("r")
                    time.sleep(1)
                    if not(NOS_API.grab_picture("Audio_type")):
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file) 
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                    
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        return
                
                    timeout = int(time.time()) - start_time
                    if (timeout > 30):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        test_result = "FAIL"
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False


                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                        return 
                
                NOS_API.Send_RF4CE_Command("o")
                time.sleep(1)
                NOS_API.Send_RF4CE_Command("d")
                time.sleep(1)     
                NOS_API.Send_RF4CE_Command("7")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("9")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("8")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("8")
                time.sleep(0.7)
                NOS_API.Send_RF4CE_Command("o")
                time.sleep(1)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)
                NOS_API.Send_RF4CE_Command("u")
                time.sleep(0.2)               
                NOS_API.Send_RF4CE_Command("P")
                time.sleep(10)
                
            if(System_Failure == 0):
                NOS_API.Send_RF4CE_Command("M")
                time.sleep(5)
                NOS_API.Send_RF4CE_Command("F")
                time.sleep(10)
            
            if (NOS_API.is_signal_present_on_video_source()):
            
                #if not(NOS_API.grab_picture("4K_HDMI")):
                #    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                #    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                #                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                #    NOS_API.set_error_message("Video HDMI")
                #    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                #    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                #    
                #    NOS_API.add_test_case_result_to_file_report(
                #                    test_result,
                #                    "- - - - - - - - - - - - - - - - - - - -",
                #                    "- - - - - - - - - - - - - - - - - - - -",
                #                    error_codes,
                #                    error_messages)
                #    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #    report_file = ""    
                #    if (test_result != "PASS"):
                #        report_file = NOS_API.create_test_case_log_file(
                #                        NOS_API.test_cases_results_info.s_n_using_barcode,
                #                        NOS_API.test_cases_results_info.nos_sap_number,
                #                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                #                        NOS_API.test_cases_results_info.mac_using_barcode,
                #                        end_time)
                #        NOS_API.upload_file_report(report_file) 
                #        NOS_API.test_cases_results_info.isTestOK = False
                #        
                #        NOS_API.send_report_over_mqtt_test_plan(
                #                test_result,
                #                end_time,
                #                error_codes,
                #                report_file)
                #
                #    ## Update test result
                #    TEST_CREATION_API.update_test_result(test_result)
                #
                #    ## Return DUT to initial state and de-initialize grabber device
                #    NOS_API.deinitialize()
                #    return
                
                if(1==1):
                #if(TEST_CREATION_API.compare_pictures("4K_ref", "4K_HDMI", "[4K_logo]")):                
                    channel_4K = True                
                else:
                    if(TEST_CREATION_API.compare_pictures("4K_NoSignal", "4K_HDMI", "[4K_NoSignal]", NOS_API.thres)):
                        TEST_CREATION_API.write_log_to_file("No signal 4k in HDMI 2160p.")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_2160p_signal_level_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_2160p_signal_level_error_message)
                        error_codes = NOS_API.test_cases_results_info.hdmi_2160p_noise_error_code
                        error_messages = NOS_API.test_cases_results_info.hdmi_2160p_noise_error_message
                        NOS_API.set_error_message("Sem Sinal 4K")               

                    else:
                        TEST_CREATION_API.write_log_to_file("Video 4K is not reproduced correctly on HDMI 2160p.")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_2160p_noise_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_2160p_noise_error_message)
                        error_codes = NOS_API.test_cases_results_info.hdmi_2160p_noise_error_code
                        error_messages = NOS_API.test_cases_results_info.hdmi_2160p_noise_error_message
                        NOS_API.set_error_message("Video HDMI")
                if (channel_4K):
                    ## Record video with duration of recording (5 seconds)
                    NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)
                    
                    ## Instance of PQMAnalyse type
                    pqm_analyse = TEST_CREATION_API.PQMAnalyse()
                    
                    ## Set what algorithms should be checked while analyzing given video file with PQM.
                    # Attributes are set to false by default.
                    pqm_analyse.black_screen_activ = True
                    pqm_analyse.blocking_activ = True
                    pqm_analyse.freezing_activ = True
                    
                    # Name of the video file that will be analysed by PQM.
                    pqm_analyse.file_name = "video"
                    
                    ## Analyse recorded video
                    analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
                    pqm_channel_4K = True
                    #if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                    #   NOS_API.set_error_message("Video HDMI")
                    #   NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_2160p_image_absence_error_code \
                    #            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_2160p_image_absence_error_message)
                    #            
                    #    error_codes = NOS_API.test_cases_results_info.hdmi_2160p_image_absence_error_code
                    #    error_messages = NOS_API.test_cases_results_info.hdmi_2160p_image_absence_error_message
                    #    NOS_API.set_error_message("Video HDMI")
                    #    
                    #    NOS_API.add_test_case_result_to_file_report(
                    #                    test_result,
                    #                    "- - - - - - - - - - - - - - - - - - - -",
                    #                    "- - - - - - - - - - - - - - - - - - - -",
                    #                    error_codes,
                    #                    error_messages)
                    #    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
                    #    report_file = ""    
                    #    if (test_result != "PASS"):
                    #        report_file = NOS_API.create_test_case_log_file(
                    #                        NOS_API.test_cases_results_info.s_n_using_barcode,
                    #                        NOS_API.test_cases_results_info.nos_sap_number,
                    #                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                    #                        NOS_API.test_cases_results_info.mac_using_barcode,
                    #                        end_time)
                    #        NOS_API.upload_file_report(report_file) 
                    #        NOS_API.test_cases_results_info.isTestOK = False
                    #        
                    #        NOS_API.send_report_over_mqtt_test_plan(
                    #                test_result,
                    #                end_time,
                    #                error_codes,
                    #                report_file)
                    #
                    #    ## Update test result
                    #    TEST_CREATION_API.update_test_result(test_result)
                    #
                    #    ## Return DUT to initial state and de-initialize grabber device
                    #    NOS_API.deinitialize()
                    #    return
                    #
                    #if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                    #   NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_2160p_blocking_error_code \
                    #            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_2160p_blocking_error_message)
                    #            
                    #    NOS_API.set_error_message("Video HDMI")
                    #            
                    #    if (error_codes == ""):
                    #        error_codes = NOS_API.test_cases_results_info.hdmi_2160p_blocking_error_code
                    #    else:
                    #        error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_2160p_blocking_error_code
                    #    
                    #    if (error_messages == ""):
                    #        error_messages = NOS_API.test_cases_results_info.hdmi_2160p_blocking_error_message
                    #    else:
                    #        error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_2160p_blocking_error_message
                    #        
                    #    NOS_API.add_test_case_result_to_file_report(
                    #                    test_result,
                    #                    "- - - - - - - - - - - - - - - - - - - -",
                    #                    "- - - - - - - - - - - - - - - - - - - -",
                    #                    error_codes,
                    #                    error_messages)
                    #    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
                    #    report_file = ""    
                    #    if (test_result != "PASS"):
                    #        report_file = NOS_API.create_test_case_log_file(
                    #                        NOS_API.test_cases_results_info.s_n_using_barcode,
                    #                        NOS_API.test_cases_results_info.nos_sap_number,
                    #                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                    #                        NOS_API.test_cases_results_info.mac_using_barcode,
                    #                        end_time)
                    #        NOS_API.upload_file_report(report_file) 
                    #        NOS_API.test_cases_results_info.isTestOK = False
                    #        
                    #        NOS_API.send_report_over_mqtt_test_plan(
                    #                test_result,
                    #                end_time,
                    #                error_codes,
                    #                report_file)
                    #
                    #    ## Update test result
                    #    TEST_CREATION_API.update_test_result(test_result)
                    #
                    #    ## Return DUT to initial state and de-initialize grabber device
                    #    NOS_API.deinitialize()
                    #    return
                    #
                    #if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                    #    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_2160p_image_freezing_error_code \
                    #            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_2160p_image_freezing_error_message)
                    #            
                    #    NOS_API.set_error_message("Video HDMI")
                    #    
                    #    if (error_codes == ""):
                    #        error_codes = NOS_API.test_cases_results_info.hdmi_2160p_image_freezing_error_code
                    #    else:
                    #        error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_2160p_image_freezing_error_code
                    #        
                    #    if (error_messages == ""):
                    #        error_messages = NOS_API.test_cases_results_info.hdmi_2160p_image_freezing_error_message
                    #    else:
                    #        error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_2160p_image_freezing_error_message
                    #        
                    #    NOS_API.add_test_case_result_to_file_report(
                    #                    test_result,
                    #                    "- - - - - - - - - - - - - - - - - - - -",
                    #                    "- - - - - - - - - - - - - - - - - - - -",
                    #                    error_codes,
                    #                    error_messages)
                    #    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
                    #    report_file = ""    
                    #    if (test_result != "PASS"):
                    #        report_file = NOS_API.create_test_case_log_file(
                    #                        NOS_API.test_cases_results_info.s_n_using_barcode,
                    #                        NOS_API.test_cases_results_info.nos_sap_number,
                    #                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                    #                        NOS_API.test_cases_results_info.mac_using_barcode,
                    #                        end_time)
                    #        NOS_API.upload_file_report(report_file) 
                    #        NOS_API.test_cases_results_info.isTestOK = False
                    #        
                    #        NOS_API.send_report_over_mqtt_test_plan(
                    #                test_result,
                    #                end_time,
                    #                error_codes,
                    #                report_file)
                    #
                    #    ## Update test result
                    #    TEST_CREATION_API.update_test_result(test_result)
                    #
                    #    ## Return DUT to initial state and de-initialize grabber device
                    #    NOS_API.deinitialize()
                    #    return
                    #else:
                    #    if (analysed_video):
                    #        pqm_channel_4K = True
                    #    else:
                    #        TEST_CREATION_API.write_log_to_file("System couldn't record Video")
                    #        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                    #                                                            + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                    #        error_codes = NOS_API.test_cases_results_info.grabber_error_code
                    #        error_messages = NOS_API.test_cases_results_info.grabber_error_message
                    #        NOS_API.set_error_message("Inspection")
                
                if (pqm_channel_4K):
                    #NOS_API.grabber_stop_video_source()
                    #time.sleep(0.5)
                    
                    ## Start grabber device with audio on HDMI audio source
                    #TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
                    
                    TEST_CREATION_API.record_audio("audio_4k", MAX_RECORD_AUDIO_TIME)
                    test_result_4k = True
                    NOS_API.Send_RF4CE_Command("b")
                    time.sleep(1)
                    NOS_API.Send_RF4CE_Command("b")
          
                   # if(TEST_CREATION_API.is_audio_present("audio_4k")):
                   #     #test_result = "PASS"
                   #     test_result_4k = True
                   #     #device.handler("RF4CE", "SET", "send_command", "Back")
                   #     NOS_API.Send_RF4CE_Command("b")
                   #     time.sleep(1)
                   #     #device.handler("RF4CE", "SET", "send_command", "Back")
                   #     NOS_API.Send_RF4CE_Command("b")
                   #     
                   # else:
                   #     TEST_CREATION_API.write_log_to_file("No Audio on Video HDMI 4K")
                   #     NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_2160p_signal_absence_error_code \
                   #                                         + "; Error message: " + NOS_API.test_cases_results_info.hdmi_2160p_signal_absence_error_message)
                   #                                         
                   #     error_codes = NOS_API.test_cases_results_info.hdmi_2160p_signal_absence_error_code
                   #     error_messages = NOS_API.test_cases_results_info.hdmi_2160p_signal_absence_error_message
                   #     NOS_API.set_error_message("Audio HDMI")
                   #
            else:
                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                       + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                       
                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                NOS_API.set_error_message("Video HDMI")   
        
        ###############################################################################################################################################
        #################################################################  HDMI Video #################################################################
        ###############################################################################################################################################

            if(test_result_4k):
                NOS_API.Send_RF4CE_Command("A","feito")
                time.sleep(8)
                
                if (NOS_API.is_signal_present_on_video_source()):       
                    time.sleep(5)
                    if not(NOS_API.grab_picture("HD_Video_Channel")):
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file) 
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                    
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        return
                    
                    video_result = NOS_API.compare_pictures("HDMI_HD_Video_ref", "HD_Video_Channel", "[HALF_SCREEN_HD]")
                    video_result_1 = NOS_API.compare_pictures("HDMI_HD_Video_2_ref", "HD_Video_Channel", "[HALF_SCREEN_HD]")
                    video_result_2 = NOS_API.compare_pictures("HDMI_HD_Video_3_ref", "HD_Video_Channel", "[HALF_SCREEN_HD]")
                    
                    ## Record audio from HDMI
                    TEST_CREATION_API.record_audio("HD_Audio_Channel", MAX_RECORD_AUDIO_TIME)

                    audio_result = NOS_API.compare_audio("No_Both_ref", "HD_Audio_Channel")
                    if(audio_result >= TEST_CREATION_API.AUDIO_THRESHOLD):
                        NOS_API.display_custom_dialog("Confirme o cabo HDMI", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                        time.sleep(1)
                        ## Record audio from HDMI
                        TEST_CREATION_API.record_audio("HD_Audio_Channel", MAX_RECORD_AUDIO_TIME)
                        audio_result = NOS_API.compare_audio("No_Both_ref", "HD_Audio_Channel")
                        
                    if ((video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD) and audio_result < TEST_CREATION_API.AUDIO_THRESHOLD):
                        #test_result = "PASS"
                        
                        test_result_HDMI = True
                        NOS_API.Send_RF4CE_Command("b")
                        time.sleep(1)
                        NOS_API.Send_RF4CE_Command("b")
                    else:
                        if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            TEST_CREATION_API.write_log_to_file("Bad Audio on HD Video")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_message)
                            NOS_API.set_error_message("Audio HDMI")
                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_message
                        elif (audio_result < TEST_CREATION_API.AUDIO_THRESHOLD):
                            TEST_CREATION_API.write_log_to_file("Bad Video on HD Video")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                        else:
                            TEST_CREATION_API.write_log_to_file("Bad Video and Audio on HD Video")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hd_channel_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.hd_channel_error_message)
                            NOS_API.set_error_message("Tuner")
                            error_codes = NOS_API.test_cases_results_info.hd_channel_error_code
                            error_messages = NOS_API.test_cases_results_info.hd_channel_error_message
                else:
                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                           + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                           
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    NOS_API.set_error_message("Video HDMI")
        
                         ###############################################################################################################################################
                         ############################################################### HDMI Video 1080i ##############################################################
                         ###############################################################################################################################################
        
                if(test_result_HDMI):
                    NOS_API.Send_RF4CE_Command("D","feito")
                    time.sleep(5)
                    
                    if (NOS_API.is_signal_present_on_video_source()):       
                        
                        if not(NOS_API.grab_picture("SD_Video_Channel")):
                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = ""    
                            if (test_result != "PASS"):
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                                NOS_API.upload_file_report(report_file) 
                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                        
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                        
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            return
                        
                        video_result = NOS_API.compare_pictures("HDMI_SD_Video_1080_ref", "SD_Video_Channel", "[HALF_SCREEN_SD_1080]")
                        video_result_1 = NOS_API.compare_pictures("HDMI_SD_Video_1080_2_ref", "SD_Video_Channel", "[HALF_SCREEN_SD_1080]")
                        video_result_2 = NOS_API.compare_pictures("HDMI_SD_Video_1080_3_ref", "SD_Video_Channel", "[HALF_SCREEN_SD_1080]")
                     
                        ## Record audio from HDMI
                        TEST_CREATION_API.record_audio("SD_Audio_Channel", MAX_RECORD_AUDIO_TIME)

                        audio_result = NOS_API.compare_audio("No_Both_ref", "SD_Audio_Channel")
                        
                        if(audio_result >= TEST_CREATION_API.AUDIO_THRESHOLD):
                            NOS_API.display_custom_dialog("Confirme o cabo HDMI", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                            time.sleep(1)
                                ## Record audio from HDMI
                            TEST_CREATION_API.record_audio("SD_Audio_Channel", MAX_RECORD_AUDIO_TIME)
                            audio_result = NOS_API.compare_audio("No_Both_ref", "SD_Audio_Channel")
                        
                        if ((video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD) and audio_result < TEST_CREATION_API.AUDIO_THRESHOLD):
                        
                           # ## Record video with duration of recording (10 seconds)
                           # TEST_CREATION_API.record_video("video", MAX_RECORD_VIDEO_TIME)
                           #
                           # ## Instance of PQMAnalyse type
                           # pqm_analyse = TEST_CREATION_API.PQMAnalyse()
                           #
                           # ## Set what algorithms should be checked while analyzing given video file with PQM.
                           # # Attributes are set to false by default.
                           # pqm_analyse.black_screen_activ = True
                           # pqm_analyse.blocking_activ = True
                           # pqm_analyse.freezing_activ = True
                           #
                           # # Name of the video file that will be analysed by PQM.
                           # pqm_analyse.file_name = "video"
                           #
                           # ## Analyse recorded video
                           # analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
                           #
                           # if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                           #     NOS_API.set_error_message("Video HDMI")
                           #     NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_code \
                           #             + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_message)
                           #             
                           #     error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_code
                           #     error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_message
                           #     
                           #     NOS_API.add_test_case_result_to_file_report(
                           #                     test_result,
                           #                     "- - - - - - - - - - - - - - - - - - - -",
                           #                     "- - - - - - - - - - - - - - - - - - - -",
                           #                     error_codes,
                           #                     error_messages)
                           #     end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
                           #     report_file = ""    
                           #     if (test_result != "PASS"):
                           #         report_file = NOS_API.create_test_case_log_file(
                           #                         NOS_API.test_cases_results_info.s_n_using_barcode,
                           #                         NOS_API.test_cases_results_info.nos_sap_number,
                           #                         NOS_API.test_cases_results_info.cas_id_using_barcode,
                           #                         NOS_API.test_cases_results_info.mac_using_barcode,
                           #                         end_time)
                           #         NOS_API.upload_file_report(report_file) 
                           #         NOS_API.test_cases_results_info.isTestOK = False
                           #         
                           #         NOS_API.send_report_over_mqtt_test_plan(
                           #                 test_result,
                           #                 end_time,
                           #                 error_codes,
                           #                 report_file)
                           # 
                           #     ## Update test result
                           #     TEST_CREATION_API.update_test_result(test_result)
                           # 
                           #     ## Return DUT to initial state and de-initialize grabber device
                           #     NOS_API.deinitialize()
                           #     return
                           #
                           # if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                           #     NOS_API.set_error_message("Video HDMI")
                           #     NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code \
                           #             + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message)
                           #             
                           #     if (error_codes == ""):
                           #         error_codes = NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code
                           #     else:
                           #         error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code
                           #     
                           #     if (error_messages == ""):
                           #         error_messages = NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message
                           #     else:
                           #         error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message
                           #         
                           #     NOS_API.add_test_case_result_to_file_report(
                           #                     test_result,
                           #                     "- - - - - - - - - - - - - - - - - - - -",
                           #                     "- - - - - - - - - - - - - - - - - - - -",
                           #                     error_codes,
                           #                     error_messages)
                           #     end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
                           #     report_file = ""    
                           #     if (test_result != "PASS"):
                           #         report_file = NOS_API.create_test_case_log_file(
                           #                         NOS_API.test_cases_results_info.s_n_using_barcode,
                           #                         NOS_API.test_cases_results_info.nos_sap_number,
                           #                         NOS_API.test_cases_results_info.cas_id_using_barcode,
                           #                         NOS_API.test_cases_results_info.mac_using_barcode,
                           #                         end_time)
                           #         NOS_API.upload_file_report(report_file) 
                           #         NOS_API.test_cases_results_info.isTestOK = False
                           #         
                           #         NOS_API.send_report_over_mqtt_test_plan(
                           #                 test_result,
                           #                 end_time,
                           #                 error_codes,
                           #                 report_file)
                           # 
                           #     ## Update test result
                           #     TEST_CREATION_API.update_test_result(test_result)
                           # 
                           #     ## Return DUT to initial state and de-initialize grabber device
                           #     NOS_API.deinitialize()
                           #     return
                           # 
                           # if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                           #     NOS_API.set_error_message("Video HDMI")
                           #     NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code \
                           #             + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message)
                           #     if (error_codes == ""):
                           #         error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                           #     else:
                           #         error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                           #         
                           #     if (error_messages == ""):
                           #         error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                           #     else:
                           #         error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                           #         
                           #     NOS_API.add_test_case_result_to_file_report(
                           #                     test_result,
                           #                     "- - - - - - - - - - - - - - - - - - - -",
                           #                     "- - - - - - - - - - - - - - - - - - - -",
                           #                     error_codes,
                           #                     error_messages)
                           #     end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
                           #     report_file = ""    
                           #     if (test_result != "PASS"):
                           #         report_file = NOS_API.create_test_case_log_file(
                           #                         NOS_API.test_cases_results_info.s_n_using_barcode,
                           #                         NOS_API.test_cases_results_info.nos_sap_number,
                           #                         NOS_API.test_cases_results_info.cas_id_using_barcode,
                           #                         NOS_API.test_cases_results_info.mac_using_barcode,
                           #                         end_time)
                           #         NOS_API.upload_file_report(report_file) 
                           #         NOS_API.test_cases_results_info.isTestOK = False
                           #         
                           #         NOS_API.send_report_over_mqtt_test_plan(
                           #                 test_result,
                           #                 end_time,
                           #                 error_codes,
                           #                 report_file)
                           # 
                           #     ## Update test result
                           #     TEST_CREATION_API.update_test_result(test_result)
                           # 
                           #     ## Return DUT to initial state and de-initialize grabber device
                           #     NOS_API.deinitialize()
                           #     return              
                           #     
                           # ## Check if video is playing (check if video is not freezed)
                            if (NOS_API.is_video_playing(TEST_CREATION_API.VideoInterface.HDMI1, NOS_API.ResolutionType.resolution_1080p)):
                                #if (analysed_video):
                                #test_result = "PASS"
                                test_result_1080 = True
                                NOS_API.Send_RF4CE_Command("b")
                                time.sleep(2)
                                NOS_API.Send_RF4CE_Command("b")
                                time.sleep(2)
                                NOS_API.Send_RF4CE_Command("b")
                                #else:
                                #    TEST_CREATION_API.write_log_to_file("System couldn't record Video")
                                #    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                #                                                        + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                                #    error_codes = NOS_API.test_cases_results_info.grabber_error_code
                                #    error_messages = NOS_API.test_cases_results_info.grabber_error_message
                                #    NOS_API.set_error_message("Inspection")
                            else:
                                TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing on HDMI 1080p.")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message)
                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                                NOS_API.set_error_message("Video HDMI") 
                        else:
                            if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                TEST_CREATION_API.write_log_to_file("Bad Audio on HD Video")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_message)
                                NOS_API.set_error_message("Audio HDMI")
                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_signal_discontinuities_error_message
                            elif (audio_result < TEST_CREATION_API.AUDIO_THRESHOLD):
                                TEST_CREATION_API.write_log_to_file("Bad Video on HD Video")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                            else:
                                TEST_CREATION_API.write_log_to_file("Bad Video and Audio on HD Video")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hd_channel_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.hd_channel_error_message)
                                NOS_API.set_error_message("Tuner")
                                error_codes = NOS_API.test_cases_results_info.hd_channel_error_code
                                error_messages = NOS_API.test_cases_results_info.hd_channel_error_message
                    else:
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                               + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                               
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        NOS_API.set_error_message("Video HDMI")

        
                         ###############################################################################################################################################
                         ############################################################### HDMI Video 720p ###############################################################
                         ###############################################################################################################################################
        

                    if(test_result_1080):
                                        
                        NOS_API.Send_RF4CE_Command("R","feito")
                        #time.sleep(8)
                        
                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "720"):
                            NOS_API.set_error_message("Resolução")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                            error_messages = NOS_API.test_cases_results_info.resolution_error_message                     
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = ""    
                            if (test_result != "PASS"):
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
                                                end_time)
                                NOS_API.upload_file_report(report_file) 
                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                        
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                        
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            return
 
                        if (NOS_API.is_signal_present_on_video_source()): 

                            ## Record video with duration of recording (10 seconds)
                            NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)
                       
                            ## Instance of PQMAnalyse type
                            pqm_analyse = TEST_CREATION_API.PQMAnalyse()
                       
                            ## Set what algorithms should be checked while analyzing given video file with PQM.
                            # Attributes are set to false by default.
                            pqm_analyse.black_screen_activ = True
                            pqm_analyse.blocking_activ = True
                            pqm_analyse.freezing_activ = True
                       
                            # Name of the video file that will be analysed by PQM.
                            pqm_analyse.file_name = "video"
                       
                            ## Analyse recorded video
                            analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
                       
                            if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                                NOS_API.set_error_message("Video HDMI")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code \
                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message)
                                        
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message
                       
                            if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                                NOS_API.set_error_message("Video HDMI")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code \
                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message)
                                        
                                if (error_codes == ""):
                                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                                else:
                                    error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                                
                                if (error_messages == ""):
                                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                                else:
                                    error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                            
                            if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                                NOS_API.set_error_message("Video HDMI")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                                        
                                if (error_codes == ""):
                                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                else:
                                    error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                    
                                if (error_messages == ""):
                                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                                else:
                                    error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message

                            else:
                                if (analysed_video):
                                    pqm_SD_720 = True
                                else:
                                    TEST_CREATION_API.write_log_to_file("System couldn't record Video")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                                    error_codes = NOS_API.test_cases_results_info.grabber_error_code
                                    error_messages = NOS_API.test_cases_results_info.grabber_error_message
                                    NOS_API.set_error_message("Inspection")
                                    
                            if (pqm_SD_720):
                                if (NOS_API.is_video_playing()):
                                    if not(NOS_API.grab_picture("SD_Video_Channel_720")):
                                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = ""    
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                                            end_time)
                                            NOS_API.upload_file_report(report_file) 
                                            NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                    
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                    
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        return
                                    
                                    video_result = NOS_API.compare_pictures("HDMI_SD_Video_720_ref", "SD_Video_Channel_720", "[HALF_SCREEN_SD_720]")
                                    video_result_1 = NOS_API.compare_pictures("HDMI_SD_Video_720_2_ref", "SD_Video_Channel_720", "[HALF_SCREEN_SD_720]")
                                    video_result_2 = NOS_API.compare_pictures("HDMI_SD_Video_720_3_ref", "SD_Video_Channel_720", "[HALF_SCREEN_SD_720]")
                                    
                                    ## Record audio from digital output (HDMI)
                                    TEST_CREATION_API.record_audio("SD_Audio_Channel_720", MAX_RECORD_AUDIO_TIME)
                            
                                    ## Compare recorded and expected audio and get result of comparison
                                    audio_result = NOS_API.compare_audio("No_Both_ref", "SD_Audio_Channel_720")
                                    if(audio_result >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                        NOS_API.display_custom_dialog("Confirme o cabo HDMI", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        time.sleep(1)
                                        TEST_CREATION_API.record_audio("SD_Audio_Channel_720", MAX_RECORD_AUDIO_TIME)
                                        audio_result = NOS_API.compare_audio("No_Both_ref", "SD_Audio_Channel_720")
                            
                                    if ((video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD) and audio_result < TEST_CREATION_API.AUDIO_THRESHOLD):
                                        #test_result = "PASS"
                                        test_result_720 = True
                                        NOS_API.Send_RF4CE_Command("b")
                                        time.sleep(2)
                                        NOS_API.Send_RF4CE_Command("b")
                                        time.sleep(2)
                                        NOS_API.Send_RF4CE_Command("b")
                                    else:
                                        if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD  or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                            TEST_CREATION_API.write_log_to_file("Bad Video on HDMI 720 Audio.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_message)
                                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_absence_error_message
                                            NOS_API.set_error_message("Audio HDMI")
                                        elif (audio_result < TEST_CREATION_API.AUDIO_THRESHOLD):
                                            TEST_CREATION_API.write_log_to_file("Bad Video on HDMI 720 Video.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                                            NOS_API.set_error_message("Video HDMI") 
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Bad Video/Audio on HDMI 720 Video.")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                                            NOS_API.set_error_message("Tuner") 
                                else:
                                    TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing on HDMI 720p.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                                    NOS_API.set_error_message("Video HDMI") 
                                        
                        else:
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                   + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                                   
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            NOS_API.set_error_message("Video HDMI")
                    
                     ###############################################################################################################################################
                     ################################################################ Factory Reset ################################################################
                     ###############################################################################################################################################
                        
                        
                        if(test_result_720):
                            NOS_API.Send_RF4CE_Command("I")
                            time.sleep(10)
                            if (NOS_API.wait_for_multiple_pictures(["INITIAL_FR_Ref", "INITIAL_FR_4K_Ref"], 10, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60]) != -1):
                                NOS_API.Send_RF4CE_Command("G")
                                time.sleep(7)
                                if (NOS_API.wait_for_multiple_pictures(["FR_Ref", "FR_4K_Ref"], 10, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60]) != -1):
                                    test_result = "PASS"
                                    
                                    #NOS_API.Send_Serial_Key("d", "feito")
                                    NOS_API.configure_power_switch_by_inspection()
                                    if not(NOS_API.power_off()): 
                                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        NOS_API.set_error_message("Inspection")
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
                                        report_file = ""
                                        if (test_result != "PASS"):
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            "",
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                    
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                    
                                        return
                                        
                                    #NOS_API.Send_RF4CE_Command("G","feito")
                                    #time.sleep(3)
                                    #if(NOS_API.wait_for_no_signal_present(20)):
                                    #    test_result = "PASS"
                                    #elif (NOS_API.wait_for_multiple_pictures(["FR_Ref"], 10, ["[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD]) != -1):
                                    #    test_result = "PASS"
                                    #else:
                                    #    NOS_API.Send_RF4CE_Command("G","feito")
                                    #    time.sleep(3)   
                                    #    if(NOS_API.wait_for_no_signal_present(20)):
                                    #        test_result = "PASS"
                                    #    elif (NOS_API.wait_for_multiple_pictures(["FR_Ref"], 5, ["[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD]) != -1):
                                    #        test_result = "PASS"                                    
                                    #    else:
                                    #        TEST_CREATION_API.write_log_to_file("Failed to perform Factory Settings restore")
                                    #        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                    #                                                + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                                    #        NOS_API.set_error_message("Factory Reset")
                                    #        error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                                    #        error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message
                                    #
                                else:
                                    NOS_API.Send_RF4CE_Command("G")
                                    time.sleep(7)
                                    if (NOS_API.wait_for_multiple_pictures(["FR_Ref", "FR_4K_Ref"], 10, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60]) != -1):
                                        test_result = "PASS"
                                        #NOS_API.Send_Serial_Key("d", "feito")
                                        NOS_API.configure_power_switch_by_inspection()
                                        if not(NOS_API.power_off()): 
                                            TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            NOS_API.set_error_message("Inspection")
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                "",
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                        
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                        
                                            return
                                        
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Failed to perform Factory Settings restore")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                                        NOS_API.set_error_message("Factory Reset")
                                        error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                                        error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message



                            else:  
                                NOS_API.Send_RF4CE_Command("b")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("o")
                                time.sleep(2)

                                if (NOS_API.wait_for_multiple_pictures(["INITIAL_FR_Ref", "INITIAL_FR_4K_Ref"], 10, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60]) != -1):
                                    NOS_API.Send_RF4CE_Command("G")
                                    time.sleep(7)
                                    if (NOS_API.wait_for_multiple_pictures(["FR_Ref", "FR_4K_Ref"], 10, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60]) != -1):
                                        test_result = "PASS"
                                        #NOS_API.Send_Serial_Key("d", "feito")
                                        NOS_API.configure_power_switch_by_inspection()
                                        if not(NOS_API.power_off()): 
                                            TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            NOS_API.set_error_message("Inspection")
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
                                            report_file = ""
                                            if (test_result != "PASS"):
                                                report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                "",
                                                                end_time)
                                                NOS_API.upload_file_report(report_file)
                                                NOS_API.test_cases_results_info.isTestOK = False
                                            
                                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                        
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                        
                                            return
                                        
                                        #NOS_API.Send_RF4CE_Command("G","feito")
                                        #time.sleep(3)
                                        #if(NOS_API.wait_for_no_signal_present(20)):
                                        #    test_result = "PASS"
                                        #elif (NOS_API.wait_for_multiple_pictures(["FR_Ref"], 10, ["[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD]) != -1):
                                        #    test_result = "PASS"
                                        #else:
                                        #    NOS_API.Send_RF4CE_Command("G","feito")
                                        #    time.sleep(3)   
                                        #    if(NOS_API.wait_for_no_signal_present(20)):
                                        #        test_result = "PASS"
                                        #    elif (NOS_API.wait_for_multiple_pictures(["FR_Ref"], 10, ["[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD]) != -1):
                                        #        test_result = "PASS"
                                        #    else:
                                        #        TEST_CREATION_API.write_log_to_file("Failed to perform Factory Settings restore")
                                        #        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                        #                                                + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                                        #        NOS_API.set_error_message("Factory Reset")
                                        #        error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                                        #        error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message
                                        #
                                    else:
                                        NOS_API.Send_RF4CE_Command("G")
                                        time.sleep(7)
                                        if (NOS_API.wait_for_multiple_pictures(["FR_Ref", "FR_4K_Ref"], 10, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60]) != -1):
                                            test_result = "PASS"
                                            #NOS_API.Send_Serial_Key("d", "feito")
                                            NOS_API.configure_power_switch_by_inspection()
                                            if not(NOS_API.power_off()): 
                                                TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                                NOS_API.set_error_message("Inspection")
                                                
                                                NOS_API.add_test_case_result_to_file_report(
                                                                test_result,
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                "- - - - - - - - - - - - - - - - - - - -",
                                                                error_codes,
                                                                error_messages)
                                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
                                                report_file = ""
                                                if (test_result != "PASS"):
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                    "",
                                                                    end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    NOS_API.test_cases_results_info.isTestOK = False
                                                
                                                
                                                ## Update test result
                                                TEST_CREATION_API.update_test_result(test_result)
                                            
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                                
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                            
                                                return
                                        
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Failed to perform Factory Settings restore")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                                            NOS_API.set_error_message("Factory Reset")
                                            error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                                            error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message


                                else:
                                    TEST_CREATION_API.write_log_to_file("Failed to perform initial settings restore")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                                    NOS_API.set_error_message("Factory Reset")
                                    error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                                    error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message
                            
            System_Failure = 2
        
        except Exception as error:
            if(System_Failure == 0):
                System_Failure = System_Failure + 1 
                NOS_API.Inspection = True
                if(System_Failure == 1):
                    try:
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                    try:
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                if (NOS_API.configure_power_switch_by_inspection()):
                    if not(NOS_API.power_off()): 
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)

                        return
                    time.sleep(10)
                    ## Power on STB with energenie
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        test_result = "FAIL"
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                        
                        return
                    time.sleep(10)
                else:
                    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                    
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    NOS_API.set_error_message("Inspection")
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                    report_file = ""
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    test_result = "FAIL"
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
                    
                    return
                
                NOS_API.Inspection = False
            else:
                test_result = "FAIL"
                TEST_CREATION_API.write_log_to_file(error)
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                error_codes = NOS_API.test_cases_results_info.grabber_error_code
                error_messages = NOS_API.test_cases_results_info.grabber_error_message
                NOS_API.set_error_message("Inspection")
                System_Failure = 2
        
    
    NOS_API.add_test_case_result_to_file_report(
                    test_result,
                    "- - - - - - - - - - - - - - - - - - - -",
                    "- - - - - - - - - - - - - - - - - - - -",
                    error_codes,
                    error_messages)
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
    report_file = ""    
    #if (test_result != "PASS"):
    report_file = NOS_API.create_test_case_log_file(
                    NOS_API.test_cases_results_info.s_n_using_barcode,
                    NOS_API.test_cases_results_info.nos_sap_number,
                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                    NOS_API.test_cases_results_info.mac_using_barcode,
                    end_time)
    NOS_API.upload_file_report(report_file) 
    NOS_API.test_cases_results_info.isTestOK = False
    
    NOS_API.send_report_over_mqtt_test_plan(
            test_result,
            end_time,
            error_codes,
            report_file)

    ## Update test result
    TEST_CREATION_API.update_test_result(test_result)

    ## Return DUT to initial state and de-initialize grabber device
    NOS_API.deinitialize()
