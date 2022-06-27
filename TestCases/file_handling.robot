*** Settings ***

#Libraries
#Library  RequestsLibrary
#Library  Collections
#Library  Dialogs
#Library  OperatingSystem
#Library  String
#Library  JSONLibrary
#Library  os
#Library  SeleniumLibrary
Library  C:\\Users\\alexdinu\\PycharmProjects\\API_Automation\\ProjectCyber\\Python\\FILE.py

*** Variables ***
${pdf_file} =    D:\\files\\sample.pdf
${pdf_file_wrong_path} =    D:\\files\\wrong\\sample.pdf
${expected_message_longest_pdf}=  demonstration
${expected_message_filename_pdf}=  sample
${expected_message_longest_transposed_pdf}=  dottnenrimsao

${wrong_path_error}=    Sorry, the provided file does not exist, check file path or that the file exists!

${csv_file} =    D:\\files\\addresses.csv
${csv_file_wrong_path} =    D:\\files\\adresses.csv
${expected_message_longest_csv}=  Riverside
${expected_message_filename_csv}=  addresses
${expected_message_longest_transposed_csv}=  Reiirdvse

${txt_file} =    D:\\files\\textsamplefile.txt
${txt_file_wrong_path} =    D:\\files\\wrong\\textsamplefile.txt
${expected_message_longest_txt}=  MULTIPLICATION
${expected_message_filename_txt}=  textsamplefile
${expected_message_longest_transposed_txt}=  MTLAOUIITNLPCI


${docx_file} =    D:\\files\\samplefile.docx
${docx_file_wrong_path} =    D:\\files\\wrong\\samplefile.docx
${expected_message_longest_docx}=  professionally
${expected_message_filename_docx}=  samplefile
${expected_message_longest_transposed_docx}=  pfsnlreiayosol



*** Test Cases ***

Test_case_1_pdf_file_handling

    ${message1}=    findlongestwords  ${pdf_file}
    should contain  ${message1}  ${expected_message_longest_pdf}

    ${message2}=    extractbasename    ${pdf_file}
    should contain  ${message2}  ${expected_message_filename_pdf}

    ${message3}=    transposelongest    ${pdf_file}
    should contain  ${message3}  ${expected_message_longest_transposed_pdf}


Test_case_2_pdf_file_handling_negative_scenario_wrong_path
    ${err_msg}=    Run Keyword And Expect Error  *  getallwords   ${pdf_file_wrong_path}

    Should Not Be Empty  ${err_msg}
    Should Contain  ${err_msg}  ${wrong_path_error}


Test_case_3_csv_file_handling

    ${message1}=    findlongestwords  ${csv_file}
    should contain  ${message1}  ${expected_message_longest_csv}

    ${message2}=    extractbasename    ${csv_file}
    should contain  ${message2}  ${expected_message_filename_csv}

    ${message3}=    transposelongest    ${csv_file}
    should contain  ${message3}  ${expected_message_longest_transposed_csv}


Test_case_4_csv_file_handling_negative_scenario_wrong_filename
    ${err_msg}=    Run Keyword And Expect Error  *  getallwords   ${csv_file_wrong_path}

    Should Not Be Empty  ${err_msg}
    Should Contain  ${err_msg}  ${wrong_path_error}


Test_case_5_txt_file_handling

    ${message1}=    findlongestwords  ${txt_file}
    should contain  ${message1}  ${expected_message_longest_txt}

    ${message2}=    extractbasename    ${txt_file}
    should contain  ${message2}  ${expected_message_filename_txt}

    ${message3}=    transposelongest    ${txt_file}
    should contain  ${message3}  ${expected_message_longest_transposed_txt}


Test_case_6_txt_file_handling_negative_scenario_wrong_filename
    ${err_msg}=    Run Keyword And Expect Error  *  getallwords   ${txt_file_wrong_path}

    Should Not Be Empty  ${err_msg}
    Should Contain  ${err_msg}  ${wrong_path_error}

Test_case_7_docx_file_handling

    ${message1}=    findlongestwords  ${docx_file}
    should contain  ${message1}  ${expected_message_longest_docx}

    ${message2}=    extractbasename    ${docx_file}
    should contain  ${message2}  ${expected_message_filename_docx}

    ${message3}=    transposelongest    ${docx_file}
    should contain  ${message3}  ${expected_message_longest_transposed_docx}

Test_case_8_docx_file_handling_negative_scenario_wrong_filename
    ${err_msg}=    Run Keyword And Expect Error  *  getallwords   ${docx_file_wrong_path}

    Should Not Be Empty  ${err_msg}
    Should Contain  ${err_msg}  ${wrong_path_error}