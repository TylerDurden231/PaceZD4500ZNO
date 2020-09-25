# -*- coding: utf-8 -*-
# Test name = Autodiag
# Test description = Check autodiag tests

from datetime import datetime
from time import gmtime, strftime
import time
import device

import TEST_CREATION_API
import shutil
import os.path
import sys
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')

try:    
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py")) == False) or (str(os.path.getmtime('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py')) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))))):
        shutil.copy2('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py', os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))
except:
    pass

import NOS_API
  
try:
    # Get model
    model_type = NOS_API.get_model()

    # Check if folder with thresholds exists, if not create it
    if(os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds")) == False):
        os.makedirs(os.path.join(os.path.dirname(sys.executable), "Thresholds"))

    # Copy file with threshold if does not exists or if it is updated
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt")) == False) or (str(os.path.getmtime(NOS_API.THRESHOLDS_PATH + model_type + ".txt")) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))))):
        shutil.copy2(NOS_API.THRESHOLDS_PATH + model_type + ".txt", os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))
except Exception as error_message:
    pass

## Number of alphanumeric characters in SN
SN_LENGTH = 16 

## Number of alphanumeric characters in Cas_Id
CASID_LENGTH = 12

## Number of alphanumeric characters in MAC
MAC_LENGTH = 12

## Wait to Autodiag app appears
WAIT_AUTODIAG_START = 10

## Wait first test in autodiag appears
WAIT_AUTODIAG_TEST = 30

## Number of attempts to open Autodiag app
ATTEMPT_OPEN_AUTODIAG = 3

##Set correct grabber for this TestSlot
NOS_API.grabber_type()

##Set correct grabber for this TestSlot
TEST_CREATION_API.grabber_type()

def runTest():
    System_Failure = 0

    NOS_API.grabber_hour_reboot()
    
    NOS_API.read_thresholds()
    
    NOS_API.reset_test_cases_results_info()      

    FIFO_Id = ""
    Boot_Time = 10
    Upgrade_Start = 45
    Upgrade_Time = 150
    Upgrade_Attempts = 0
    counter_retry = 0
    # Skip this test case if some previous test failed
    # if not(NOS_API.test_cases_results_info.isTestOK):
        # TEST_CREATION_API.update_test_result(TEST_CREATION_API.TestCaseResult.FAIL)
        # TEST_CREATION_API.write_log_to_file("Skip this test case if some previous test failed")
        # return
    while (System_Failure < 2):
        try:      
            FIFO_Id = ""
            SN_LABEL = False
            CASID_LABEL = False
            MAC_LABEL = False  
        
            ## Set test result default to FAIL
            test_result = "FAIL"
            AutoTeste = False
            test_Autodiag = False
            test_AutodiagCM = False
            paired = False
            error_codes = ""
            error_messages = ""
            software_version = ""
            cputemp_threshold = 80
            counter_buttons = 0
            counter = 0
            counter_emparelhamento = 0
            counter_buttons = 0
            nav_counter = 0
            
            timeout = 0
            try:      
                all_scanned_barcodes = NOS_API.get_all_scanned_barcodes()
                NOS_API.test_cases_results_info.s_n_using_barcode = all_scanned_barcodes[1]
                NOS_API.test_cases_results_info.cas_id_using_barcode = all_scanned_barcodes[2]
                NOS_API.test_cases_results_info.mac_using_barcode = all_scanned_barcodes[3]
                NOS_API.test_cases_results_info.nos_sap_number = all_scanned_barcodes[0]
            except Exception as error:
                TEST_CREATION_API.write_log_to_file(error)
                test_result = "FAIL"        
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                                   + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                NOS_API.set_error_message("Leitura de Etiquetas")
                error_codes = NOS_API.test_cases_results_info.scan_error_code
                error_messages = NOS_API.test_cases_results_info.scan_error_message 
             
            test_number = NOS_API.get_test_number(NOS_API.test_cases_results_info.s_n_using_barcode)
            device.updateUITestSlotInfo("Teste N\xb0: " + str(int(test_number)+1))
            
            if ((len(NOS_API.test_cases_results_info.s_n_using_barcode) == SN_LENGTH) and (NOS_API.test_cases_results_info.s_n_using_barcode.isalnum() or NOS_API.test_cases_results_info.s_n_using_barcode.isdigit())):
                SN_LABEL = True

            if ((len(NOS_API.test_cases_results_info.cas_id_using_barcode) == CASID_LENGTH) and (NOS_API.test_cases_results_info.cas_id_using_barcode.isalnum() or NOS_API.test_cases_results_info.cas_id_using_barcode.isdigit())):
                CASID_LABEL = True

            if ((len(NOS_API.test_cases_results_info.mac_using_barcode) == MAC_LENGTH) and (NOS_API.test_cases_results_info.mac_using_barcode.isalnum() or NOS_API.test_cases_results_info.mac_using_barcode.isdigit())):
                MAC_LABEL = True
            
            if not(SN_LABEL and CASID_LABEL and MAC_LABEL):               
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                               + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                NOS_API.set_error_message("Leitura de Etiquetas")
                error_codes = NOS_API.test_cases_results_info.scan_error_code
                error_messages = NOS_API.test_cases_results_info.scan_error_message            
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

            if(System_Failure == 0):
                if not(NOS_API.display_new_dialog("Conectores?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):              
                    test_result = "FAIL"
                    TEST_CREATION_API.write_log_to_file("Conectores NOK")
                    NOS_API.set_error_message("Danos Externos")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.conector_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.conector_nok_error_message)
                    error_codes = NOS_API.test_cases_results_info.conector_nok_error_code
                    error_messages = NOS_API.test_cases_results_info.conector_nok_error_message           
                                   
          
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
            
            cm_modulation = NOS_API.MODULATION_ZD4500NO
           # snr_value_threshold_low = NOS_API.SNR_VALUE_THRESHOLD_LOW_ZD4500NO
            snr_value_threshold_low = 20
            snr_value_threshold_high = NOS_API.SNR_VALUE_THRESHOLD_HIGH_ZD4500NO
            cm_rx_value_threshold_low = NOS_API.RX_THRESHOLD_LOW_ZD4500NO
            cm_rx_value_threshold_high = NOS_API.RX_THRESHOLD_HIGH_ZD4500NO
            cm_tx_value_threshold = NOS_API.TX_THRESHOLD_ZD4500NO
            
            Software_Version_Prod = NOS_API.Firmware_Version_ZD4500ZNO
            scanned_serial_number = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.s_n_using_barcode)
            scanned_casid_number = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.cas_id_using_barcode)
            scanned_mac_number = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.mac_using_barcode)
            NOS_API.test_cases_results_info.cas_id_using_barcode = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.cas_id_using_barcode)
            
            ##Get Slot Number Where Test is Being Executed
            slot_master_fifo = NOS_API.get_test_place_name()
            slot_master_fifo = slot_master_fifo.replace("NOS", "")
            
            ## Initialize grabber device
            NOS_API.initialize_grabber()

            ## Start grabber device with video on default video source
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)        

            NOS_API.Send_Serial_Key("a", "feito")
            
            #FIFO_Id = NOS_API.Put_UMA_FIFO(scanned_serial_number)
            FIFO_Id = NOS_API.master_fifo_PUT_main(slot_master_fifo, scanned_serial_number)
            while (counter < ATTEMPT_OPEN_AUTODIAG):

                if (NOS_API.configure_power_switch_by_inspection()):
                    ## Power off STB
                    if not(NOS_API.power_off()):
                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                            #TEST_CREATION_API.write_log_to_file("")
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
        
                
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                    
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
        
                        return
                    if(NOS_API.Get_Active_UMA(scanned_serial_number)):
                        start_time = time.time()
                        current_time = time.time()
                        NOS_API.display_custom_dialog("Pressione bot\xf5es 'Power' e 'Emparelhar'", 1, ["Continuar"], 60)
                        current_time = time.time()
                        if(current_time - start_time >= 60):
                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                #TEST_CREATION_API.write_log_to_file("")
                            #FIFO_Id = NOS_API.Put_UMA_FIFO(scanned_serial_number)
                            FIFO_Id = NOS_API.master_fifo_PUT_main(slot_master_fifo, scanned_serial_number)
                            continue
                        TEST_CREATION_API.write_log_to_file("Try " + str(counter + 1))
                        ## Power on STB with energenie
                        if not(NOS_API.power_on()):
                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                #TEST_CREATION_API.write_log_to_file("")
                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
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
            
                    
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                        
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
            
                            return
                                            
                        start_time = int(time.time())
                        result = NOS_API.display_custom_dialog("", 1, ["Repetir"], WAIT_AUTODIAG_START)
                        timeout = int(time.time()) - start_time
                        if (result == "Repetir"):
                            if (timeout >= WAIT_AUTODIAG_START):
                                AutoDiag_start = NOS_API.wait_for_multiple_pictures(["First_AutoDiag_ref", "Menu_ref","Paring_ref","UMA_ref","First_AutoDiag_4k_ref","Menu_4K_ref","Paring_4K_ref","UMA_4K_ref","First_AutoDiag_4k_ref1","Menu_4K_ref1","Paring_4K_ref1"], WAIT_AUTODIAG_TEST, ["[AutoDiag]", "[Menu]", "[Paring]", "[FULL_SCREEN_1080]", "[AutoDiag_4k]", "[Menu_4k]", "[Paring_4k]", "[FULL_SCREEN_1080]", "[AutoDiag_4k]", "[Menu_4k]", "[Paring_4k]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60, 60, 60, 60, 60, 60, 60])
                                if (AutoDiag_start != -1 and AutoDiag_start != -2 and AutoDiag_start != 3 and AutoDiag_start != 7):
                                    time.sleep(2)
                                    
                                    if not(NOS_API.grab_picture("Status")):
                                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                            #TEST_CREATION_API.write_log_to_file("")
                                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
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
                                    
                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                    if video_height == "1080":
                                        ref_pic = "Paring_ref"
                                        pic_macro = "[Paring]"
                                    elif video_height == "2160":
                                        ref_pic = "Paring_4K_ref"
                                        pic_macro = "[Paring_4k]"
                                    if(TEST_CREATION_API.compare_pictures(ref_pic, "Status", pic_macro, NOS_API.thres)):
                                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                            #TEST_CREATION_API.write_log_to_file("")
                                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                        TEST_CREATION_API.write_log_to_file("Started in pairing mode")
                                        NOS_API.Send_RF4CE_Command("X","feito")
                                        time.sleep(2)  
                                        NOS_API.Send_RF4CE_Command("e")
                                        time.sleep(1.2)
                                        NOS_API.Send_RF4CE_Command("e")
                                        time.sleep(1.5)                                
                                        NOS_API.Send_RF4CE_Command("1")                                   
                                        time.sleep(5)
                                        if not(NOS_API.grab_picture("Paring_1")):
                                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                #TEST_CREATION_API.write_log_to_file("")
                                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
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
                                                
                                        if(TEST_CREATION_API.compare_pictures(ref_pic, "Paring_1", pic_macro, NOS_API.thres)):
                                            NOS_API.Send_RF4CE_Command("e")
                                            time.sleep(1.5)  
                                            NOS_API.Send_RF4CE_Command("e")
                                            time.sleep(1.5)                                    
                                            NOS_API.Send_RF4CE_Command("1")                                  
                                            time.sleep(5)
                                            
                                            if not(NOS_API.grab_picture("Paring_1")):
                                                #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                    #TEST_CREATION_API.write_log_to_file("")
                                                NOS_API.Remove_UMA_FIFO(FIFO_Id)
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
                                                
                                            if(TEST_CREATION_API.compare_pictures(ref_pic, "Paring_1", pic_macro, NOS_API.thres)):
                                                if(counter_emparelhamento == 0):
                                                    TEST_CREATION_API.write_log_to_file("Pair Try: " + str(counter_emparelhamento + 1))
                                                    counter_emparelhamento += 1
                                                    NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                    #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                        #TEST_CREATION_API.write_log_to_file("")
                                                    #FIFO_Id = NOS_API.Put_UMA_FIFO(scanned_serial_number)
                                                    FIFO_Id = NOS_API.master_fifo_PUT_main(slot_master_fifo, scanned_serial_number)
                                                    continue
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("STB doesn't pair with RF4CE")
                                                    #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                        #TEST_CREATION_API.write_log_to_file("")
                                                    NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.pairing_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.pairing_error_message)
                                                    NOS_API.set_error_message("Emparelhamento")
                                                    error_codes = NOS_API.test_cases_results_info.pairing_error_code
                                                    error_messages = NOS_API.test_cases_results_info.pairing_error_message
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
                                        test_Autodiag = True
                                        paired = True
                                        #counter = 7
                                    if(paired ==False):
                                        NOS_API.display_custom_dialog("Pressione bot\xe3o 'Emparelhar'", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                            #TEST_CREATION_API.write_log_to_file("")
                                        if (NOS_API.wait_for_multiple_pictures(["Paring_ref", "Paring_4K_ref", "Paring_4K_ref1"], WAIT_AUTODIAG_TEST, ["[Paring]", "[Paring_4k]", "[Paring_4k]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60, 60]) != -1):
                                            NOS_API.Send_RF4CE_Command("e")
                                            time.sleep(1.2)
                                            NOS_API.Send_RF4CE_Command("e")
                                            time.sleep(1.5)
                                            NOS_API.Send_RF4CE_Command("1")
                                            time.sleep(1)
                                            NOS_API.Send_RF4CE_Command("9")
                                            
                                            if not(NOS_API.grab_picture("Paring")):
                                                NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                    #TEST_CREATION_API.write_log_to_file("")
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
                                                
                                            if(TEST_CREATION_API.compare_pictures(ref_pic, "Paring", pic_macro, NOS_API.thres)):

                                                NOS_API.Send_RF4CE_Command("X","feito")
                                                time.sleep(2)  
                                                NOS_API.Send_RF4CE_Command("e")
                                                time.sleep(1.2)
                                                NOS_API.Send_RF4CE_Command("e")
                                                time.sleep(1.5)                                    
                                                NOS_API.Send_RF4CE_Command("1")                                  
                                                time.sleep(8)

                                                if not(NOS_API.grab_picture("Paring_1")):
                                                    NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                    #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                        #TEST_CREATION_API.write_log_to_file("")
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

                                                if(TEST_CREATION_API.compare_pictures(ref_pic, "Paring_1", pic_macro, NOS_API.thres)):
                                                    if(counter_emparelhamento == 0):
                                                        counter_emparelhamento += 1
                                                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                            #TEST_CREATION_API.write_log_to_file("")
                                                        #FIFO_Id = NOS_API.Put_UMA_FIFO(scanned_serial_number)
                                                        FIFO_Id = NOS_API.master_fifo_PUT_main(slot_master_fifo, scanned_serial_number)
                                                        continue
                                                    else:
                                                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                            #TEST_CREATION_API.write_log_to_file("")
                                                        TEST_CREATION_API.write_log_to_file("STB doesn't pair with RF4CE")
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.pairing_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.pairing_error_message)
                                                        NOS_API.set_error_message("Emparelhamento")
                                                        error_codes = NOS_API.test_cases_results_info.pairing_error_code
                                                        error_messages = NOS_API.test_cases_results_info.pairing_error_message
                                                        break
                                            test_Autodiag = True  
                                            #counter = 7
                                        else:
                                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                #TEST_CREATION_API.write_log_to_file("")
                                            TEST_CREATION_API.write_log_to_file("Pair Button NOK")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.pairing_button_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.pairing_button_error_message)
                                            NOS_API.set_error_message("Botões")
                                            error_codes = NOS_API.test_cases_results_info.pairing_button_error_code
                                            error_messages = NOS_API.test_cases_results_info.pairing_button_error_message
                                            break 
                                    
                                elif (AutoDiag_start == -1 or AutoDiag_start == 3):
                                    NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                    #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                        #TEST_CREATION_API.write_log_to_file("")
                                    #FIFO_Id = NOS_API.Put_UMA_FIFO(scanned_serial_number)
                                    FIFO_Id = NOS_API.master_fifo_PUT_main(slot_master_fifo, scanned_serial_number)
                                    counter = counter + 1
                                    continue
                                elif (AutoDiag_start == -2):
                                    NOS_API.display_custom_dialog("Confirme o cabo HDMI", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                    AutoDiag_start = NOS_API.wait_for_multiple_pictures(["First_AutoDiag_ref", "Menu_ref","Paring_ref","UMA_ref","First_AutoDiag_4k_ref","Menu_4K_ref","Paring_4K_ref","UMA_4K_ref","First_AutoDiag_4k_ref1","Menu_4K_ref1","Paring_4K_ref1"], WAIT_AUTODIAG_TEST, ["[AutoDiag]", "[Menu]", "[Paring]", "[FULL_SCREEN_1080]", "[AutoDiag_4k]", "[Menu_4k]", "[Paring_4k]", "[FULL_SCREEN_1080]", "[AutoDiag_4k]", "[Menu_4k]", "[Paring_4k]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60, 60, 60, 60, 60, 60, 60])
                                    if (AutoDiag_start != -1 and AutoDiag_start != -2 and AutoDiag_start != 3 and AutoDiag_start != 7):
                                        time.sleep(2)
                                        
                                        if not(NOS_API.grab_picture("Status")):
                                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                #TEST_CREATION_API.write_log_to_file("")
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
                                        
                                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                        if video_height == "1080":
                                            ref_pic = "Paring_ref"
                                            pic_macro = "[Paring]"
                                        elif video_height == "2160":
                                            ref_pic = "Paring_4K_ref"
                                            pic_macro = "[Paring_4k]"
                                        if(TEST_CREATION_API.compare_pictures(ref_pic, "Status", pic_macro, NOS_API.thres)):
                                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                #TEST_CREATION_API.write_log_to_file("")
                                            NOS_API.Send_RF4CE_Command("X","feito")
                                            time.sleep(2)  
                                            NOS_API.Send_RF4CE_Command("e")
                                            time.sleep(1.5)                                    
                                            NOS_API.Send_RF4CE_Command("1")                                   
                                            time.sleep(5)
                                            if not(NOS_API.grab_picture("Paring_1")):
                                                NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                    #TEST_CREATION_API.write_log_to_file("")
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
                                                    
                                            if(TEST_CREATION_API.compare_pictures(ref_pic, "Paring_1", pic_macro, NOS_API.thres)):
                                                NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                    #TEST_CREATION_API.write_log_to_file("")
                                                TEST_CREATION_API.write_log_to_file("STB doesn't pair with RF4CE")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.pairing_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.pairing_error_message)
                                                NOS_API.set_error_message("Emparelhamento")
                                                error_codes = NOS_API.test_cases_results_info.pairing_error_code
                                                error_messages = NOS_API.test_cases_results_info.pairing_error_message
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
                                            test_Autodiag = True
                                            paired = True
                                            #NOS_API.Send_RF4CE_Command("d");  
                                            #NOS_API.Send_RF4CE_Command("d");  
                                            #counter = 7
                                        if(paired ==False):
                                            NOS_API.display_custom_dialog("Pressione bot\xe3o 'Emparelhar'", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                #TEST_CREATION_API.write_log_to_file("")
                                            if (NOS_API.wait_for_multiple_pictures(["Paring_ref", "Paring_4K_ref", "Paring_4K_ref1"], WAIT_AUTODIAG_TEST, ["[Paring]", "[Paring_4k]", "[Paring_4k]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60, 60]) != -1):
                                                NOS_API.Send_RF4CE_Command("e")
                                                time.sleep(1.5)
                                                NOS_API.Send_RF4CE_Command("1")
                                                time.sleep(1)
                                                NOS_API.Send_RF4CE_Command("9")
                                                
                                                if not(NOS_API.grab_picture("Paring")):
                                                    NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                    #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                        #TEST_CREATION_API.write_log_to_file("")
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
                                                    
                                                if(TEST_CREATION_API.compare_pictures(ref_pic, "Paring", pic_macro, NOS_API.thres)):
                                                    
                                                
                                                    NOS_API.Send_RF4CE_Command("X","feito")
                                                    time.sleep(2)  
                                                    NOS_API.Send_RF4CE_Command("e")
                                                    time.sleep(1.5)                                    
                                                    NOS_API.Send_RF4CE_Command("1")                                   
                                                    time.sleep(8)
            
                                                    
                                                    if not(NOS_API.grab_picture("Paring_1")):
                                                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                            #TEST_CREATION_API.write_log_to_file("")
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
                                                        
                                                    
                                                    if(TEST_CREATION_API.compare_pictures(ref_pic, "Paring_1", pic_macro, NOS_API.thres)):
                                                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                            #TEST_CREATION_API.write_log_to_file("")
                                                        TEST_CREATION_API.write_log_to_file("STB doesn't pair with RF4CE")
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.pairing_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.pairing_error_message)
                                                        NOS_API.set_error_message("Emparelhamento")
                                                        error_codes = NOS_API.test_cases_results_info.pairing_error_code
                                                        error_messages = NOS_API.test_cases_results_info.pairing_error_message
                                                        break
                                                test_Autodiag = True
                                                #NOS_API.Send_RF4CE_Command("d");  
                                                #NOS_API.Send_RF4CE_Command("d");  
                                                #counter = 7
                                            else:
                                                NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                                #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                    #TEST_CREATION_API.write_log_to_file("")
                                                TEST_CREATION_API.write_log_to_file("Pair Button NOK")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.pairing_button_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.pairing_button_error_message)
                                                NOS_API.set_error_message("bot\xf5es")
                                                error_codes = NOS_API.test_cases_results_info.pairing_button_error_code
                                                error_messages = NOS_API.test_cases_results_info.pairing_button_error_message
                                                break 
                                        
                                    elif (AutoDiag_start == 3):
                                        if(counter == 1):
                                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                #TEST_CREATION_API.write_log_to_file("")
                                            TEST_CREATION_API.write_log_to_file("Autodiag failed")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.autodiag_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.autodiag_error_message)
                                            NOS_API.set_error_message("AutoDiag")
                                            error_codes = NOS_API.test_cases_results_info.autodiag_error_code
                                            error_messages = NOS_API.test_cases_results_info.autodiag_error_message
                                                                    
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
                                            
                                        else:
                                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                                #TEST_CREATION_API.write_log_to_file("")
                                            #FIFO_Id = NOS_API.Put_UMA_FIFO(scanned_serial_number)
                                            FIFO_Id = NOS_API.master_fifo_PUT_main(slot_master_fifo, scanned_serial_number)
                                            counter += 1
                                            continue
                                    elif (AutoDiag_start == -1):
                                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                            #TEST_CREATION_API.write_log_to_file("")
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
        
        
                                    elif (AutoDiag_start == -2):
                                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                            #TEST_CREATION_API.write_log_to_file("")
                                        if (NOS_API.display_custom_dialog("A STB est\xe1 ligada?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):   
                                            
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI(Não Retestar)")
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
                                        else:
                                            
                                            TEST_CREATION_API.write_log_to_file("No Power")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_power_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.no_power_error_message)
                                            NOS_API.set_error_message("Não Liga")
                                            error_codes = NOS_API.test_cases_results_info.no_power_error_code
                                            error_messages = NOS_API.test_cases_results_info.no_power_error_message
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
                            else:
                                counter = counter + 1
                    else:                  
                        TEST_CREATION_API.write_log_to_file("Cue try " + str(counter + 1) + " failed")
                        counter = counter + 1
            
                            ###############################################################################################################################################
                            ################################################################## AutoDiag CM ################################################################
                            ###############################################################################################################################################

                if(test_Autodiag):
                    TEST_CREATION_API.write_log_to_file("Number of attempts: " + str(counter))
                    Menu_AD = NOS_API.wait_for_multiple_pictures(["Menu_ref", "Menu_4K_ref", "Menu_4K_ref1"], WAIT_AUTODIAG_TEST, ["[Menu]", "[Menu_4k]", "[Menu_4k]"], [80, 60, 60])
                    if (Menu_AD != -1 and Menu_AD != -2):
                        if Menu_AD == 1 or Menu_AD == 2:
                            NOS_API.change_4k_resolution_uma()
                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if video_height != "1080":
                                NOS_API.change_4k_resolution_uma()
                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                if video_height != "1080":
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
                        NOS_API.Send_RF4CE_Command("o")
                        time.sleep(3)
                        
                        if not(NOS_API.grab_picture("Auto_Test")):
                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                #TEST_CREATION_API.write_log_to_file("")
                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
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
                
                        if (TEST_CREATION_API.compare_pictures("Menu_ref", "Auto_Test", "[Menu]", NOS_API.thres)):
                            NOS_API.Send_RF4CE_Command("o")
                            time.sleep(3)
                            if not(NOS_API.grab_picture("Auto_Test")):
                                #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                    #TEST_CREATION_API.write_log_to_file("")
                                NOS_API.Remove_UMA_FIFO(FIFO_Id)
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
                        
                            if (TEST_CREATION_API.compare_pictures("Menu_ref", "Auto_Test", "[Menu]", NOS_API.thres)):
                                test_Autodiag = False
                                paired = False
                                NOS_API.Remove_UMA_FIFO(FIFO_Id)
                                #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                    #TEST_CREATION_API.write_log_to_file("")
                                #FIFO_Id = NOS_API.Put_UMA_FIFO(scanned_serial_number)
                                FIFO_Id = NOS_API.master_fifo_PUT_main(slot_master_fifo, scanned_serial_number)
                                continue
                        
                        counter = 7
                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                            #TEST_CREATION_API.write_log_to_file("")
                        if (NOS_API.wait_for_multiple_pictures(["Audio_Video_ref"], 15, ["[AVRed]"], [NOS_API.thres]) != -1):
                            NOS_API.Send_RF4CE_Command("o")
                            time.sleep(7)
                            if not(NOS_API.grab_picture("Auto_Test")):
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
                            
                            #Button_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Button_OK]", NOS_API.thres)
                            Hardware_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Hardware_OK]", NOS_API.thres)
                            Perif_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Perif_OK]", NOS_API.thres)
                            CM_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[CM_OK]", NOS_API.thres)
                            SC_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[SC_OK]", NOS_API.thres)
                            Flash_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Flash_OK]", NOS_API.thres)
                            HDCP_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[HDCP_OK]",NOS_API.thres)
                            
                            #if(Button_Result and Hardware_Result and Perif_Result and SC_Result and Flash_Result and HDCP_Result):
                            if(Hardware_Result and Perif_Result and SC_Result and Flash_Result and HDCP_Result):
                                NOS_API.Send_RF4CE_Command("b")
                                AutoTeste = True                                               
                                break
                            else:
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Button_OK]", NOS_API.thres)):
                                    AutoTeste = False
                                    NOS_API.Send_RF4CE_Command("b")
                                    NOS_API.Send_RF4CE_Command("B","feito")
                                    time.sleep(3)
                                    NOS_API.display_custom_dialog("Esperar 2seg e pressionar 'Reset' sem segurar", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                    while (counter_buttons < 3):
                                        NOS_API.Send_RF4CE_Command("o")
                                        time.sleep(12)
                                        if not(NOS_API.grab_picture("Buttons")):
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
                                        
                                        if(TEST_CREATION_API.compare_pictures("Buttons_ref", "Buttons", "[Reset_Button]", NOS_API.thres)):    
                                            AutoTeste = True
                                            break
                                        else:
                                            if (counter_buttons < 3):                                                                       
                                                if (NOS_API.display_custom_dialog("Repetir Teste?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):   
                                                    counter_buttons = counter_buttons + 1
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("Reset Button NOK")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.reset_button_error_code  \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.reset_button_error_message)
                                                    NOS_API.set_error_message("Botões")
                                                    error_codes = NOS_API.test_cases_results_info.reset_button_error_code 
                                                    error_messages = NOS_API.test_cases_results_info.reset_button_error_message
                                                    break  
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Reset Button NOK")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.reset_button_error_code  \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.reset_button_error_message)
                                                NOS_API.set_error_message("Botões")
                                                error_codes = NOS_API.test_cases_results_info.reset_button_error_code 
                                                error_messages = NOS_API.test_cases_results_info.reset_button_error_message
                                                break     
                                        
                                    if(counter_buttons == 3):
                                        TEST_CREATION_API.write_log_to_file("Reset Button NOK")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.reset_button_error_code  \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reset_button_error_message)
                                        NOS_API.set_error_message("Botões")
                                        error_codes = NOS_API.test_cases_results_info.reset_button_error_code 
                                        error_messages = NOS_API.test_cases_results_info.reset_button_error_message
                                        
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

                                        
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Hardware_OK]", NOS_API.thres)):
                                    AutoTeste = False
                                    NOS_API.Send_RF4CE_Command("b")
                                    NOS_API.Send_RF4CE_Command("H","feito")
                                    time.sleep(1)
                                    if not(NOS_API.grab_picture("Hardware")):
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
                                    cputemp_result = TEST_CREATION_API.OCR_recognize_text("Hardware", "[HW_CPUT_OK]", "[AUTODIAG_FILTER]", "CPUTemp_Result")
                                    if not(TEST_CREATION_API.compare_pictures("Hardware_ref", "Hardware", "[HW_Sint_OK]", NOS_API.thres)):
                                        TEST_CREATION_API.write_log_to_file("AD tuner test fail")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.tuner_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.tuner_error_message)
                                        NOS_API.set_error_message("Tuner")
                                        error_codes = NOS_API.test_cases_results_info.tuner_error_code
                                        error_messages = NOS_API.test_cases_results_info.tuner_error_message
                                        break 
                                    if not(TEST_CREATION_API.compare_pictures("Hardware_ref", "Hardware", "[HW_RF4CE_OK]", NOS_API.thres)):
                                        TEST_CREATION_API.write_log_to_file("AD RF4CE test fail")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.rf4ce_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.rf4ce_error_message)
                                        NOS_API.set_error_message("RF4CE")
                                        error_codes = NOS_API.test_cases_results_info.rf4ce_error_code
                                        error_messages = NOS_API.test_cases_results_info.rf4ce_error_message
                                        break 
                                    if not(TEST_CREATION_API.compare_pictures("Hardware_ref", "Hardware", "[HW_CM_OK]", NOS_API.thres)):
                                        TEST_CREATION_API.write_log_to_file("Cable Modem Fail")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.cable_modem_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cable_modem_nok_error_message)
                                        NOS_API.set_error_message("IC")
                                        error_codes = NOS_API.test_cases_results_info.cable_modem_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.cable_modem_nok_error_message
        
                                        break 
                                    if not(TEST_CREATION_API.compare_pictures("Hardware_ref", "Hardware", "[HW_Flash_OK]", NOS_API.thres)):
                                        TEST_CREATION_API.write_log_to_file("Flash Fail")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.flash_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.flash_nok_error_message)
                                        NOS_API.set_error_message("IC")
                                        error_codes = NOS_API.test_cases_results_info.flash_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.flash_nok_error_message
                                        break 
                                    if not (cputemp_result > cputemp_threshold):                                                   
                                        TEST_CREATION_API.write_log_to_file("CPU Temperature bigger than threshold")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.cpu_temp_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cpu_temp_nok_error_message)
                                        NOS_API.set_error_message("IC")
                                        error_codes = NOS_API.test_cases_results_info.cpu_temp_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.cpu_temp_nok_error_message
                                        break  
                                    AutoTeste = True
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Perif_OK]", NOS_API.thres)):
                                    AutoTeste = False
                                    NOS_API.Send_RF4CE_Command("b")
                                    NOS_API.Send_RF4CE_Command("J","feito")
                                    time.sleep(3)
                                    if not(NOS_API.grab_picture("Peripherals")):
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
                                    if not(TEST_CREATION_API.compare_pictures("Peripherals_ref", "Peripherals", "[Per_USB_OK]", NOS_API.thres)):
                                        NOS_API.display_custom_dialog("Confirme o cabo USB", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        NOS_API.Send_RF4CE_Command("b")
                                        NOS_API.Send_RF4CE_Command("o")
                                        time.sleep(5)
                                        if not(NOS_API.grab_picture("Peripherals1")):
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
                                    
                                        if not(TEST_CREATION_API.compare_pictures("Peripherals_ref", "Peripherals1", "[Per_USB_OK]", NOS_API.thres)):
                                        
                                            TEST_CREATION_API.write_log_to_file("USB fail")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.usb_nok_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.usb_nok_error_message)
                                            NOS_API.set_error_message("USB")
                                            error_codes = NOS_API.test_cases_results_info.usb_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.usb_nok_error_message
                                            break 
                                        else: 
                                            AutoTeste = True
                                    if not(TEST_CREATION_API.compare_pictures("Peripherals_ref", "Peripherals", "[Per_Eth_OK]", NOS_API.thres)):
                                        AutoTeste = False
                                        NOS_API.display_custom_dialog("Confirme o cabo ETH", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        NOS_API.Send_RF4CE_Command("b")
                                        NOS_API.Send_RF4CE_Command("o")
                                        time.sleep(5)
                                        if not(NOS_API.grab_picture("Peripherals1")):
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
                                    
                                        if not(TEST_CREATION_API.compare_pictures("Peripherals_ref", "Peripherals1", "[Per_Eth_OK]", NOS_API.thres)):
                                            TEST_CREATION_API.write_log_to_file("Eth fail")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ethernet_nok_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.ethernet_nok_error_message)
                                            NOS_API.set_error_message("Eth")
                                            error_codes = NOS_API.test_cases_results_info.ethernet_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.ethernet_nok_error_message
                                            break 
                                        else:
                                            AutoTeste = True
                                    if not(TEST_CREATION_API.compare_pictures("Peripherals_ref", "Peripherals", "[Per_HDMI_OK]", NOS_API.thres)):
                                        TEST_CREATION_API.write_log_to_file("HDMI Test Fail")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_test_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_test_error_message)
                                        NOS_API.set_error_message("HDMI")
                                        error_codes = NOS_API.test_cases_results_info.hdmi_test_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_test_error_message
                                        break 
                                    
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[SC_OK]", NOS_API.thres)):
                                    TEST_CREATION_API.write_log_to_file("AD tuner test fail")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.tuner_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.tuner_error_message)
                                    NOS_API.set_error_message("Tuner")
                                    error_codes = NOS_API.test_cases_results_info.tuner_error_code
                                    error_messages = NOS_API.test_cases_results_info.tuner_error_message
                                    break                                             
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Flash_OK]", NOS_API.thres)):
                                    TEST_CREATION_API.write_log_to_file("Flash Fail")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.flash_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.flash_nok_error_message)
                                    NOS_API.set_error_message("IC")
                                    error_codes = NOS_API.test_cases_results_info.flash_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.flash_nok_error_message
                                    break 
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[HDCP_OK]", NOS_API.thres)):
                                    TEST_CREATION_API.write_log_to_file("HDCP Test Fail")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdcp_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdcp_nok_error_message)
                                    NOS_API.set_error_message("IC")
                                    error_codes = NOS_API.test_cases_results_info.hdcp_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.hdcp_nok_error_message
                                    break
                                AutoTeste = True
                                NOS_API.Send_RF4CE_Command("b")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                counter = 7
                        else:
                            time.sleep(2)
                            if not(NOS_API.grab_picture("Auto_Test")):
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
                            
                            
                            #if(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[CheckResult]")):
                            Button_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Button_OK]", NOS_API.thres)
                            Hardware_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Hardware_OK]", NOS_API.thres)
                            Perif_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Perif_OK]", NOS_API.thres)
                            CM_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[CM_OK]", NOS_API.thres)
                            SC_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[SC_OK]", NOS_API.thres)
                            Flash_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Flash_OK]", NOS_API.thres)
                            HDCP_Result = TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[HDCP_OK]", NOS_API.thres)
                            
                            
                            #if(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[CheckResult]")):
                            if(Button_Result and Hardware_Result and Perif_Result and SC_Result and Flash_Result and HDCP_Result):
                            
                                NOS_API.Send_RF4CE_Command("b")
                                AutoTeste = True                                               
                                break
                            else:
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Button_OK]", NOS_API.thres)):
                                    NOS_API.Send_RF4CE_Command("b")
                                    NOS_API.Send_RF4CE_Command("B","feito")
                                    NOS_API.display_custom_dialog("Esperar 2seg e pressionar 'Reset', 'Emparelhar' e 'Power' alternadamente", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                    while (counter_buttons < 3):
                                        NOS_API.Send_RF4CE_Command("o")
                                        time.sleep(12)
                                        if not(NOS_API.grab_picture("Buttons")):
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
                                        if(TEST_CREATION_API.compare_pictures("Buttons_ref", "Buttons", "[Power_Button]", NOS_API.thres)):
                                            if(TEST_CREATION_API.compare_pictures("Buttons_ref", "Buttons", "[Paring_Button]", NOS_API.thres)):        
                                                if(TEST_CREATION_API.compare_pictures("Buttons_ref", "Buttons", "[Reset_Button]", NOS_API.thres)):    
                                                    TEST_CREATION_API.write_log_to_file("Incosistencias de resultados")
                                                    break
                                                else:
                                                    if (counter_buttons < 2):                                                                       
                                                        if (NOS_API.display_custom_dialog("Repetir Teste?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):   
                                                            counter_buttons = counter_buttons + 1
                                                        else:
                                                            TEST_CREATION_API.write_log_to_file("Reset Button NOK")
                                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.reset_button_error_code  \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.reset_button_error_message)
                                                            NOS_API.set_error_message("Botões")
                                                            error_codes = NOS_API.test_cases_results_info.reset_button_error_code 
                                                            error_messages = NOS_API.test_cases_results_info.reset_button_error_message
                                                            break  
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("Reset Button NOK")
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.reset_button_error_code  \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.reset_button_error_message)
                                                        NOS_API.set_error_message("Botões")
                                                        error_codes = NOS_API.test_cases_results_info.reset_button_error_code 
                                                        error_messages = NOS_API.test_cases_results_info.reset_button_error_message
                                                        break     
                                            else:
                                                if (counter_buttons < 2):
                                                    if (NOS_API.display_custom_dialog("Repetir Teste?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):   
                                                        counter_buttons = counter_buttons + 1
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("Pairing Button NOK")
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.pairing_button_error_code  \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.pairing_button_error_message)
                                                        NOS_API.set_error_message("Botões")
                                                        error_codes = NOS_API.test_cases_results_info.pairing_button_error_code 
                                                        error_messages = NOS_API.test_cases_results_info.pairing_button_error_message
                                                        break  
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("Pairing Button NOK")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.pairing_button_error_code  \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.pairing_button_error_message)
                                                    NOS_API.set_error_message("Botões")
                                                    error_codes = NOS_API.test_cases_results_info.pairing_button_error_code 
                                                    error_messages = NOS_API.test_cases_results_info.pairing_button_error_message
                                                    break     
                                        else:
                                            if (counter_buttons < 2):
                                                if (NOS_API.display_custom_dialog("Repetir Teste?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):  
                                                    counter_buttons = counter_buttons + 1
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("Power Button NOK")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.power_button_nok_error_code  \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_button_nok_error_message)
                                                    NOS_API.set_error_message("Botões")
                                                    error_codes = NOS_API.test_cases_results_info.power_button_nok_error_code 
                                                    error_messages = NOS_API.test_cases_results_info.power_button_nok_error_message
                                                    break
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Power Button NOK")
                                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.power_button_nok_error_code  \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.power_button_nok_error_message)
                                                NOS_API.set_error_message("Botões")
                                                error_codes = NOS_API.test_cases_results_info.power_button_nok_error_code 
                                                error_messages = NOS_API.test_cases_results_info.power_button_nok_error_message
                                                break
                                    break
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Hardware_OK]", NOS_API.thres)):
                                    NOS_API.Send_RF4CE_Command("b")
                                    NOS_API.Send_RF4CE_Command("H","feito")
                                    if not(NOS_API.grab_picture("Hardware")):
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
                                    cputemp_result = TEST_CREATION_API.OCR_recognize_text("Hardware", "[HW_CPUT_OK]", "[AUTODIAG_FILTER]", "CPUTemp_Result")
                                    if not(TEST_CREATION_API.compare_pictures("Hardware_ref", "Hardware", "[HW_Sint_OK]", NOS_API.thres)):
                                        TEST_CREATION_API.write_log_to_file("AD tuner test fail")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.tuner_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.tuner_error_message)
                                        NOS_API.set_error_message("Tuner")
                                        error_codes = NOS_API.test_cases_results_info.tuner_error_code
                                        error_messages = NOS_API.test_cases_results_info.tuner_error_message
                                        break 
                                    if not(TEST_CREATION_API.compare_pictures("Hardware_ref", "Hardware", "[HW_RF4CE_OK]", NOS_API.thres)):
                                        TEST_CREATION_API.write_log_to_file("AD RF4CE test fail")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.rf4ce_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.rf4ce_error_message)
                                        NOS_API.set_error_message("RF4CE")
                                        error_codes = NOS_API.test_cases_results_info.rf4ce_error_code
                                        error_messages = NOS_API.test_cases_results_info.rf4ce_error_message
                                        break 
                                    if not(TEST_CREATION_API.compare_pictures("Hardware_ref", "Hardware", "[HW_CM_OK]", NOS_API.thres)):
                                        TEST_CREATION_API.write_log_to_file("Cable Modem Fail")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.cable_modem_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cable_modem_nok_error_message)
                                        NOS_API.set_error_message("IC")
                                        error_codes = NOS_API.test_cases_results_info.cable_modem_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.cable_modem_nok_error_message
            
                                        break 
                                    if not(TEST_CREATION_API.compare_pictures("Hardware_ref", "Hardware", "[HW_Flash_OK]", NOS_API.thres)):
                                        TEST_CREATION_API.write_log_to_file("Flash Fail")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.flash_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.flash_nok_error_message)
                                        NOS_API.set_error_message("IC")
                                        error_codes = NOS_API.test_cases_results_info.flash_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.flash_nok_error_message
                                        break 
                                    if not (cputemp_result > cputemp_threshold):                                                   
                                        TEST_CREATION_API.write_log_to_file("CPU Temperature bigger than threshold")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.cpu_temp_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.cpu_temp_nok_error_message)
                                        NOS_API.set_error_message("IC")
                                        error_codes = NOS_API.test_cases_results_info.cpu_temp_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.cpu_temp_nok_error_message
                                        break  
                                    
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Perif_OK]", NOS_API.thres)):
                                    NOS_API.Send_RF4CE_Command("b")
                                    NOS_API.Send_RF4CE_Command("J","feito")
                                    if not(NOS_API.grab_picture("Peripherals")):
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
                                    if not(TEST_CREATION_API.compare_pictures("Peripherals_ref", "Peripherals", "[Per_USB_OK]", NOS_API.thres)):
                                        NOS_API.display_custom_dialog("Confirme o cabo USB", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        NOS_API.Send_RF4CE_Command("b")
                                        NOS_API.Send_RF4CE_Command("o")
                                        time.sleep(5)
                                        if not(NOS_API.grab_picture("Peripherals1")):
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
                                    
                                        if not(TEST_CREATION_API.compare_pictures("Peripherals_ref", "Peripherals1", "[Per_USB_OK]", NOS_API.thres)):
                                        
                                            TEST_CREATION_API.write_log_to_file("USB fail")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.usb_nok_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.usb_nok_error_message)
                                            NOS_API.set_error_message("USB")
                                            error_codes = NOS_API.test_cases_results_info.usb_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.usb_nok_error_message
                                            break 
                                        else: 
                                            AutoTeste = True
                                    if not(TEST_CREATION_API.compare_pictures("Peripherals_ref", "Peripherals", "[Per_Eth_OK]", NOS_API.thres)):
                                        AutoTeste = False
                                        NOS_API.display_custom_dialog("Confirme o cabo ETH", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        NOS_API.Send_RF4CE_Command("b")
                                        NOS_API.Send_RF4CE_Command("o")
                                        time.sleep(5)
                                        if not(NOS_API.grab_picture("Peripherals1")):
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
                                    
                                        if not(TEST_CREATION_API.compare_pictures("Peripherals_ref", "Peripherals1", "[Per_Eth_OK]", NOS_API.thres)):
                                            TEST_CREATION_API.write_log_to_file("Eth fail")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ethernet_nok_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.ethernet_nok_error_message)
                                            NOS_API.set_error_message("Eth")
                                            error_codes = NOS_API.test_cases_results_info.ethernet_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.ethernet_nok_error_message
                                            break 
                                        else:
                                            AutoTeste = True
                                    if not(TEST_CREATION_API.compare_pictures("Peripherals_ref", "Peripherals", "[Per_HDMI_OK]", NOS_API.thres)):
                                        TEST_CREATION_API.write_log_to_file("HDMI Test Fail")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_test_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_test_error_message)
                                        NOS_API.set_error_message("HDMI")
                                        error_codes = NOS_API.test_cases_results_info.hdmi_test_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_test_error_message
                                        break 
                                    
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[SC_OK]", NOS_API.thres)):
                                    TEST_CREATION_API.write_log_to_file("AD tuner test fail")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.tuner_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.tuner_error_message)
                                    NOS_API.set_error_message("Tuner")
                                    error_codes = NOS_API.test_cases_results_info.tuner_error_code
                                    error_messages = NOS_API.test_cases_results_info.tuner_error_message
                                    break                                             
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[Flash_OK]", NOS_API.thres)):
                                    TEST_CREATION_API.write_log_to_file("Flash Fail")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.flash_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.flash_nok_error_message)
                                    NOS_API.set_error_message("IC")
                                    error_codes = NOS_API.test_cases_results_info.flash_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.flash_nok_error_message
                                    break 
                                if not(TEST_CREATION_API.compare_pictures("Teste_Auto_ref", "Auto_Test", "[HDCP_OK]", NOS_API.thres)):
                                    TEST_CREATION_API.write_log_to_file("HDCP Test Fail")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdcp_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdcp_nok_error_message)
                                    NOS_API.set_error_message("IC")
                                    error_codes = NOS_API.test_cases_results_info.hdcp_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.hdcp_nok_error_message
                                    break
                                AutoTeste = True
                                NOS_API.Send_RF4CE_Command("b")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                time.sleep(1)
                                NOS_API.Send_RF4CE_Command("u")
                                counter = 7
                    elif(Menu_AD == -1):
                        if(nav_counter == 2):
                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                #TEST_CREATION_API.write_log_to_file("")
                            NOS_API.set_error_message("Navegação")                    
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                            error_codes = NOS_API.test_cases_results_info.navigation_error_code
                            error_messages = NOS_API.test_cases_results_info.navigation_error_message                    
                            
                            NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                            
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = ""    
                            
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            NOS_API.test_cases_results_info.mac_using_barcode,
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            
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
                        else:
                            NOS_API.Remove_UMA_FIFO(FIFO_Id)
                            #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                                #TEST_CREATION_API.write_log_to_file("")
                            #FIFO_Id = NOS_API.Put_UMA_FIFO(scanned_serial_number)
                            FIFO_Id = NOS_API.master_fifo_PUT_main(slot_master_fifo, scanned_serial_number)
                            test_Autodiag = False
                            paired = False
                            nav_counter += 1
                            continue
                    elif(Menu_AD == -2):
                        NOS_API.Remove_UMA_FIFO(FIFO_Id)
                        #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                            #TEST_CREATION_API.write_log_to_file("")
                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                        NOS_API.set_error_message("Reboot")
                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
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
            
            if (counter >= 3 and counter < 7 and test_Autodiag == False):
                NOS_API.Remove_UMA_FIFO(FIFO_Id)
                #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                    #TEST_CREATION_API.write_log_to_file("")
                TEST_CREATION_API.write_log_to_file("Autodiag failed")
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.autodiag_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.autodiag_error_message)
                NOS_API.set_error_message("AutoDiag")
                error_codes = NOS_API.test_cases_results_info.autodiag_error_code
                error_messages = NOS_API.test_cases_results_info.autodiag_error_message                        
            
            
            if(AutoTeste):
                #NOS_API.send_rf4ce_command("[CableModem]")
                NOS_API.Send_RF4CE_Command("C")
                time.sleep(6)
            
                if not(NOS_API.grab_picture("CableModem")):
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
                
                if not(TEST_CREATION_API.compare_pictures("CableModem_ref", "CableModem", "[CABLE_MODEM]", NOS_API.thres)):
                    NOS_API.Send_RF4CE_Command("b")
                    time.sleep(1)
                    NOS_API.Send_RF4CE_Command("u")
                    time.sleep(1)
                    NOS_API.Send_RF4CE_Command("u")
                    time.sleep(1)
                    NOS_API.Send_RF4CE_Command("C")
                    time.sleep(7)
                
                    if not(NOS_API.grab_picture("CableModem")):
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
                
                
                    if not(TEST_CREATION_API.compare_pictures("CableModem_ref", "CableModem", "[CABLE_MODEM]", NOS_API.thres)):
                        NOS_API.set_error_message("Navegação")                    
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
                        error_codes = NOS_API.test_cases_results_info.navigation_error_code
                        error_messages = NOS_API.test_cases_results_info.navigation_error_message                    
                        
                        NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                        
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        NOS_API.test_cases_results_info.mac_using_barcode,
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        
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
                    
                
                cm_ip = TEST_CREATION_API.OCR_recognize_text("CableModem", "[CM_IP]", "[AUTODIAG_FILTER]", "IP_CM")
                NOS_API.test_cases_results_info.ip = cm_ip
                ds_freq = TEST_CREATION_API.OCR_recognize_text("CableModem", "[DS_Freq]", "[AUTODIAG_FILTER]", "DownStream_Freq")
                NOS_API.test_cases_results_info.freq_downstream = ds_freq
                up_freq = TEST_CREATION_API.OCR_recognize_text("CableModem", "[US_Freq]", "[AUTODIAG_FILTER]", "UpStream_Freq")
                NOS_API.test_cases_results_info.freq = up_freq
                modulation = TEST_CREATION_API.OCR_recognize_text("CableModem", "[Modulation]", "[AUTODIAG_FILTER]", "Modulation")
                NOS_API.test_cases_results_info.modulation = modulation
                snr = TEST_CREATION_API.OCR_recognize_text("CableModem", "[SNR]", "[AUTODIAG_FILTER]", "SNR")
                NOS_API.test_cases_results_info.snr = snr
                cm_rx = fix_cm_rx(TEST_CREATION_API.OCR_recognize_text("CableModem", "[DS_CM]", "[AUTODIAG_FILTER]", "CableModem RX"))
                NOS_API.test_cases_results_info.rx = cm_rx
                cm_tx = TEST_CREATION_API.OCR_recognize_text("CableModem", "[US_CM]", "[AUTODIAG_FILTER]", "CableModem TX")
                NOS_API.test_cases_results_info.tx = cm_tx
                
                modulation = NOS_API.fix_modulation(modulation)
                TEST_CREATION_API.write_log_to_file("Modulation: " + modulation)
                TEST_CREATION_API.write_log_to_file("IP: " + cm_ip)
                try:
                    cm_rx = float(cm_rx)
                except:
                    cm_rx = 0
                TEST_CREATION_API.write_log_to_file("RX Value: " + str(cm_rx))
                try:
                    cm_tx = float(cm_tx)
                except:
                    cm_tx = 0
                TEST_CREATION_API.write_log_to_file("TX Value: " + str(cm_tx))
                try:
                    snr = float(snr)
                except: 
                    snr = 0
                TEST_CREATION_API.write_log_to_file("SNR: " + str(snr))
            
                
                if (cm_ip == "0.0.0.0"):
                    TEST_CREATION_API.write_log_to_file("CM DOCSIS IP")
                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ip_error_code  \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.ip_error_message)
                    NOS_API.set_error_message("CM DOCSIS")
                    error_codes = NOS_API.test_cases_results_info.ip_error_code 
                    error_messages = NOS_API.test_cases_results_info.ip_error_message
                else:
                    if (modulation == cm_modulation):
                        if (snr < snr_value_threshold_high and snr >= snr_value_threshold_low):
                            TEST_CREATION_API.write_log_to_file(str(cm_rx > cm_rx_value_threshold_low))
                            TEST_CREATION_API.write_log_to_file(str(cm_rx < cm_rx_value_threshold_high))
                            TEST_CREATION_API.write_log_to_file(str(cm_rx_value_threshold_low))
                            TEST_CREATION_API.write_log_to_file(str(cm_rx_value_threshold_high))
                            if (cm_rx > cm_rx_value_threshold_low and cm_rx < cm_rx_value_threshold_high):
                                if (cm_tx <= cm_tx_value_threshold):
                                    #test_result = "PASS"   
                                    test_AutodiagCM = True
                                    NOS_API.Send_RF4CE_Command("b")
                                else:
                                    TEST_CREATION_API.write_log_to_file("TX value is bigger than threshold")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.tx_fail_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.tx_fail_error_message)
                                    NOS_API.set_error_message("CM Docsis")
                                    error_codes = NOS_API.test_cases_results_info.tx_fail_error_code
                                    error_messages = NOS_API.test_cases_results_info.tx_fail_error_message   
                            else:
                                TEST_CREATION_API.write_log_to_file("RX value is not between threshold parameters")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.rx_fail_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.rx_fail_error_message)
                                NOS_API.set_error_message("CM Docsis")
                                error_codes = NOS_API.test_cases_results_info.rx_fail_error_code
                                error_messages = NOS_API.test_cases_results_info.rx_fail_error_message 
                        else:
                            TEST_CREATION_API.write_log_to_file("SNR value is lower than threshold")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.snr_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.snr_error_message)
                            NOS_API.set_error_message("SNR")
                            error_codes = NOS_API.test_cases_results_info.snr_error_code
                            error_messages = NOS_API.test_cases_results_info.snr_error_message
                    else:
                        TEST_CREATION_API.write_log_to_file("CM Docsis Modulation")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.modulation_error_code  \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.modulation_error_message)
                        NOS_API.set_error_message("CM DOCSIS")
                        error_codes = NOS_API.test_cases_results_info.modulation_error_code 
                        error_messages = NOS_API.test_cases_results_info.modulation_error_message       
                        ###############################################################################################################################################
                        ################################################################ AutoDiag Info ################################################################
                        ###############################################################################################################################################
                         
                if(test_AutodiagCM):
                                      
                    NOS_API.Send_RF4CE_Command("S")
                    time.sleep(3)
                    
                    if not(NOS_API.grab_picture("STB_Info")):
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
                    


                    serial_number = TEST_CREATION_API.OCR_recognize_text("STB_Info", "[Serial_Number]", "[AUTODIAG_FILTER]", "Serial Number")       
                    software_version = TEST_CREATION_API.OCR_recognize_text("STB_Info", "[Software_Version]", "[AUTODIAG_FILTER]", "Software Version")
                    NOS_API.test_cases_results_info.firmware_version = software_version
                    cas_id = TEST_CREATION_API.OCR_recognize_text("STB_Info", "[CASID_Number]", "[AUTODIAG_FILTER]", "CAS ID")
                    NOS_API.test_cases_results_info.cas_id_number = cas_id
                    cm_mac = TEST_CREATION_API.OCR_recognize_text("STB_Info", "[CM_MAC]", "[AUTODIAG_FILTER]", "Cable Modem MAC")        
                    eth_mac = TEST_CREATION_API.OCR_recognize_text("STB_Info", "[Eth_MAC]", "[AUTODIAG_FILTER]", "STB Ethernet MAC")
                    doscsis_mac = TEST_CREATION_API.OCR_recognize_text("STB_Info", "[Docsis_MAC]", "[AUTODIAG_FILTER]", "STB Docsis MAC")
                    
                    cm_mac = NOS_API.fix_mac_stb_uma(cm_mac)
                    eth_mac = NOS_API.fix_mac_stb_uma(eth_mac)
                    doscsis_mac = NOS_API.fix_mac_stb_uma(doscsis_mac)
                    serial_number = NOS_API.remove_whitespaces(serial_number)
                    serial_number = NOS_API.fix_sn_stb_uma(serial_number)
                    
                    NOS_API.test_cases_results_info.s_n = serial_number
                    NOS_API.test_cases_results_info.mac_number = cm_mac
                    
                   
                    cm_mac = NOS_API.fix_mac_stb_pace(NOS_API.remove_whitespaces(cm_mac))
                    
                    TEST_CREATION_API.write_log_to_file(cas_id)
                    TEST_CREATION_API.write_log_to_file(scanned_casid_number)
                    
                    if (NOS_API.ignore_zero_letter_o_during_comparation(serial_number, scanned_serial_number)):
                        
                        if (cm_mac == scanned_mac_number):
                            if (NOS_API.ignore_zero_letter_o_during_comparation(cas_id, scanned_casid_number)):
                                if (software_version.strip() == Software_Version_Prod):
                                    TEST_CREATION_API.write_log_to_file("Serial Number: " + serial_number)
                                    TEST_CREATION_API.write_log_to_file("Software Version: " + software_version)
                                    TEST_CREATION_API.write_log_to_file("CAS ID: " + cas_id)
                                    TEST_CREATION_API.write_log_to_file("CM MAC: " + cm_mac)
                                    TEST_CREATION_API.write_log_to_file("Eth MAC: " + eth_mac)
                                    TEST_CREATION_API.write_log_to_file("Docsis MAC: " + doscsis_mac)
                    
                                    test_result = "PASS"
                                    NOS_API.Send_RF4CE_Command("b")
                                else:
                                    NOS_API.configure_power_switch_by_inspection()
                                    NOS_API.power_off()
                                
                      ############################################################################################################################################################          
                                
                                
                                    while(Upgrade_Attempts < 2):
                                        if(Upgrade_Attempts == 1):
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
                                
                                        
                                                ## Return DUT to initial state and de-initialize grabber device
                                                NOS_API.deinitialize()
                                            
                                                NOS_API.send_report_over_mqtt_test_plan(
                                                        test_result,
                                                        end_time,
                                                        error_codes,
                                                        report_file)
                                
                                                return
                                            NOS_API.display_custom_dialog("Confirme o cabo HDMI", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        
                                        NOS_API.display_custom_dialog("Pressione no bot\xe3o Reset da STB", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        
                                        NOS_API.configure_power_switch_by_inspection()
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
                            
                                    
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                        
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                            
                                            return
                                        time.sleep(1)
                                       
                                        if(NOS_API.wait_for_signal_present(Boot_Time)):
                                            time.sleep(1)
                                            if (NOS_API.wait_for_multiple_pictures(["First_Image_ref", "First_Image_4K_ref"], Boot_Time, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60]) != -1):
                                                time.sleep(1)
                                                NOS_API.display_dialog_without_buttons("Largar bot\xe3o", 2)
                                                Upgrade_State = NOS_API.wait_for_multiple_pictures(["Upgrade_ref", "Upgrade_4K_ref"], Upgrade_Start, ["[Upgrade_Logo]", "[Upgrade_Logo]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60])
                                                if (Upgrade_State != -1 and Upgrade_State != -2):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                                    if(NOS_API.wait_for_no_signal_present(Upgrade_Time)):
                                                        Upgrade_Attempts = 7
                                                        break
                                                       
                                                    
                                                    else:
                                                        NOS_API.grab_picture("Update_after_signal")
                                                        Upgrade_Attempts = 7
                                                        break
                                                        #TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                                        #NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                        #                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                                        #NOS_API.set_error_message("Não Actualiza") 
                                                        #error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                                        #error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                                        #Upgrade_Attempts = Upgrade_Attempts + 1
                                                
                                                elif(Upgrade_State == -1):                                                
                                                    Upgrade_Attempts += 1
                                                elif(Upgrade_State == -2):
                                                    TEST_CREATION_API.write_log_to_file("Continuou sem sinal")
                                                    Upgrade_Attempts = 7
                                                    break
                                                
                                            else:
                                            
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
                    
                                        else:
                                            Upgrade_Attempts += 1
                                            continue
                                    if(Upgrade_Attempts == 2): 
                                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                        NOS_API.set_error_message("Não Actualiza") 
                                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message

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
                                        
                                        
                                    
                                    while(counter_retry < 2):
                                        NOS_API.configure_power_switch_by_inspection()
                                        NOS_API.power_off()
                                        if(counter_retry == 1):
                                            NOS_API.display_custom_dialog("Confirme o cabo HDMI", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                            
                                        NOS_API.display_custom_dialog("Pressione bot\xf5es 'Power' e 'Emparelhar'", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                                        NOS_API.power_on()
                                        result = NOS_API.display_custom_dialog("", 1, ["Repetir"], WAIT_AUTODIAG_START)
                                        #AutoDiag_start = NOS_API.wait_for_multiple_pictures(["Menu_ref", "Paring_ref"], WAIT_AUTODIAG_TEST, ["[Menu]", "[Paring]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD])
                                        AutoDiag_start = NOS_API.wait_for_multiple_pictures(["Menu_ref", "Paring_ref", "Menu_4K_ref", "Paring_4K_ref", "Menu_4K_ref1","Paring_4K_ref1"], WAIT_AUTODIAG_TEST, ["[Menu]", "[Paring]", "[Menu_4k]", "[Paring_4k]", "[Menu_4k]", "[Paring_4k]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD, 60, 60, 60, 60])
                                        if(AutoDiag_start != -1 and AutoDiag_start != -2):
                                            if AutoDiag_start == 2 or AutoDiag_start == 3 or AutoDiag_start == 4 or AutoDiag_start == 5:
                                                NOS_API.change_4k_resolution_uma()
                                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                if video_height != "1080":
                                                    if not(NOS_API.grab_picture("STB_Info")):
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
                                                    NOS_API.change_4k_resolution_uma()
                                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                    if video_height != "1080":
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
                                            NOS_API.Send_RF4CE_Command("d")
                                            time.sleep(1)
                                            NOS_API.Send_RF4CE_Command("d")
                                            time.sleep(1)
                                            NOS_API.Send_RF4CE_Command("d")
                                            time.sleep(1)
                                            
                                            NOS_API.Send_RF4CE_Command("o")
                                            time.sleep(1)
                                            if not(NOS_API.grab_picture("STB_Info1")):
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

                                            software_version1 = TEST_CREATION_API.OCR_recognize_text("STB_Info1", "[Software_Version]", "[AUTODIAG_FILTER]", "Software Version1")
                                            if (software_version1.strip() == Software_Version_Prod):
                                               
                                                TEST_CREATION_API.write_log_to_file("Serial Number: " + serial_number)
                                                TEST_CREATION_API.write_log_to_file("Software Version: " + software_version1)
                                                TEST_CREATION_API.write_log_to_file("CAS ID: " + cas_id)
                                                TEST_CREATION_API.write_log_to_file("CM MAC: " + cm_mac)
                                                TEST_CREATION_API.write_log_to_file("Eth MAC: " + eth_mac)
                                                TEST_CREATION_API.write_log_to_file("Docsis MAC: " + doscsis_mac)               
                                                
                                                test_result = "PASS"                           
                                                NOS_API.Send_RF4CE_Command("b")
                                                break
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)                                        
                                                NOS_API.set_error_message("Não Actualiza") 
                                                error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
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
                                    
                
                                        else:
                                            if(counter_retry == 1):
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
                                            else:
                                                
                                                counter_retry += 1
     
                         ############################################################################################################################################       
                          
                            else:
                                TEST_CREATION_API.write_log_to_file("CAS ID number and CAS ID number previuosly scanned by barcode scanner is not the same")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_cas_id_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.wrong_cas_id_error_message \
                                                                    + "; OCR: " + str(cas_id))
                                NOS_API.set_error_message("CAS ID")
                                error_codes = NOS_API.test_cases_results_info.wrong_cas_id_error_code
                                error_messages = NOS_API.test_cases_results_info.wrong_cas_id_error_message
                        else:
                            TEST_CREATION_API.write_log_to_file("CM MAC number and CM MAC number previuosly scanned by barcode scanner is not the same")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_mac_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.wrong_mac_error_message)
                            NOS_API.set_error_message("MAC")
                            error_codes = NOS_API.test_cases_results_info.wrong_mac_error_code
                            error_messages = NOS_API.test_cases_results_info.wrong_mac_error_message
    
                    else:
                        TEST_CREATION_API.write_log_to_file("Logistic serial number (" + str(serial_number) + ") is not the same as scanned serial number(" + str(scanned_serial_number) + ")")        
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_s_n_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.wrong_s_n_error_message \
                                                                + "; OCR: " + str(serial_number))
                        NOS_API.set_error_message("S/N")
                        error_codes = NOS_API.test_cases_results_info.wrong_s_n_error_code
                        error_messages = NOS_API.test_cases_results_info.wrong_s_n_error_message  
             
            System_Failure = 2
        except Exception as error:
            test_result = "FAIL"
            try:
                NOS_API.Remove_UMA_FIFO(FIFO_Id)
                #if not(NOS_API.Remove_And_Check(FIFO_Id)):
                    #TEST_CREATION_API.write_log_to_file("")
                TEST_CREATION_API.write_log_to_file(error)
            except:
                pass
            if(System_Failure == 0):
                System_Failure = System_Failure + 1 
                NOS_API.Inspection = True
                if(System_Failure == 1):
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
    
def fix_cm_rx(input_text):
    output_text = input_text
    if(output_text[0] == "."):
        output_text = output_text[0].replace('.','-') + output_text[1:]
    if ("z" in output_text):
        output_text = output_text.replace('z','2')
    if ("Z" in output_text):
        output_text = output_text.replace('Z','2')
    return output_text