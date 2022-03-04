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
<img width="960" alt="image" src="https://user-images.githubusercontent.com/35862674/156728967-815f1b05-d583-4b3a-9f9e-689240c46a38.png">
<img width="960" alt="image" src="https://user-images.githubusercontent.com/35862674/156729005-6b8bec4e-5718-4072-9dfd-571527d44be6.png">

-	Thêm dòng sau vào ./engine/recipes/default_components.py
from rasa.nlu.tokenizers.vietnamese_tokenizer import VietnameseTokenizer

- Add vào mảng DEFAULT_COMPONENTS dòng sau
 VietnameseTokenizer,

# RUN
rasa run -m models --enable-api --cors "*"

# RUN IN SHELL
rasa shell
