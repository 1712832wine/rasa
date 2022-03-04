# INSTALL RASA
To install rasa you need to install anaconda, then run these commands below:
conda create --name NAME python==3.8
conda activate NAME
conda install ujson
conda install tensorflow
pip install rasa

# SETUP
-	Ta custom VietnameseTokenizer cho tiếng Việt
-	Vào thư mục rasa đường dẫn của môi trường ảo conda với đường dẫn tương đối sau : C:\Users\ASUS\anaconda3\envs\rasa\Lib\site-packages\rasa
 
-	Copy file vietnamese_tokenizer.py trong ./custom/vietnamese_tokenizer.py của project rasa vào đường dẫn ./nlu/tokenizers

-	 

-	 

-	Thêm dòng sau vào ./engine/recipes/default_components.py

from rasa.nlu.tokenizers.vietnamese_tokenizer import VietnameseTokenizer

 
Add vào mảng DEFAULT_COMPONENTS
 

# RUN
rasa run -m models --enable-api --cors "*"

# RUN IN SHELL
rasa shell