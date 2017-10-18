##################################################################
# Project VisionX App
# Revision 3
# Reference doc: VisionX - OCR and NLP Module Diagram Rev 3.pdf
# Filename: run-omni-xml-json-converter.sh 
# VERSION: 2.0
# (Introducted in Revision 3)
# Supervisor: Adnan-ul-Hassan adnan.ulhassan@visionx.io,
# Authors:    Sami-ur-Rehman sami@visionx.io,
#             Adil Usman adil.usman@visionx.io
##################################################################
echo
echo ================================================================
echo Conversion of Omni results from XML format to Json format
echo ================================================================
echo Input: $1_out_omni.xml
echo ----------------------------------------------------------------


python omni-xml-to-json.py $1

echo ----------------------------------------------------------------
echo Output: $1_out_ocrlines_word_wbb.json
echo ================================================================
echo

