#RUN command
#bash run.sh bh8msy90-amnb-asdg-5yk3-bmqmmmsdhfo9 sample17.jpeg
#run it in terminal
#the UUID should be different everytime....

clear
echo ================================================================
echo Running OmniPage OCR on $2
echo ================================================================
echo Input: $2
echo ----------------------------------------------------------------

# OMNI call to get OCR results in JSON format
# time curl -F file=@$1.png -o $1_out_omni.json http://35.165.99.224:8091/VisionX2/analyze

# OMNI call to get OCR results in XML format
#time curl -F name=@$1.png -o $1_out_omni.xml http://ec2-35-165-99-224.us-west-2.compute.amazonaws.com/OCRTools/getOmniResults.jsp

#uuid format
#06451143-8863-4909-84c3-189451252f00

# OMNI call to do pre-processing and OCR
time curl -X POST http://52.14.7.109:3000/apis3/omnibb -F uuid=$1 -F imagedata=@$2 -o $1_out_ocrlines_word_wbb.json


echo ----------------------------------------------------------------
time bash run-nltk-v2.sh $1 $2