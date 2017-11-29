##################################################################
# Project VisionX App
# Revision 3
# Reference doc: VisionX - OCR and NLP Module Diagram Rev 3.pdf
# Filename: run-nltk-v2.sh 
# VERSION: 2.0
# (Introducted in Revision 3)
# Supervisor: Adnan-ul-Hassan adnan.ulhassan@visionx.io,
# Authors:    Sami-ur-Rehman sami@visionx.io,
#             Adil Usman adil.usman@visionx.io
##################################################################
echo
echo ================================================================
echo Information Extraction using NLTK
echo ================================================================
echo Input: $1_out_ocrlines_word_wbb.json , dictSubjects.txt , my_pwl.txt
echo ----------------------------------------------------------------


python nltk_info_ext_omni_xml2.py $1 # $1_ocr_lines.txt

echo ----------------------------------------------------------------
echo Output: $1_nltk.json
echo ================================================================
echo




echo ----------------------------------------------------------------
echo Highlighting Products
echo ================================================================
echo


#python plotRect.py $2