# INSTALL RASA
Để cài đặt rasa trước hết hãy cài đặt anaconda vào máy và thực hiện các lệnh sau:
- conda create --name NAME python==3.8
- conda activate NAME
- conda install ujson
- conda install tensorflow
- pip install rasa

# SETUP
-	Ta custom VietnameseTokenizer cho tiếng Việt

-	Vào thư mục rasa đường dẫn của môi trường ảo conda với đường dẫn tương đối sau : `C:\Users\ASUS\anaconda3\envs\rasa\Lib\site-packages\rasa`

-	Copy file `vietnamese_tokenizer.py` trong `./custom/vietnamese_tokenizer.py` của project rasa vào đường dẫn `./nlu/tokenizers` trong mã nguồn
<img width="960" alt="image" src="https://user-images.githubusercontent.com/35862674/156728967-815f1b05-d583-4b3a-9f9e-689240c46a38.png">
<img width="960" alt="image" src="https://user-images.githubusercontent.com/35862674/156729005-6b8bec4e-5718-4072-9dfd-571527d44be6.png">

-	Thêm dòng sau vào `./engine/recipes/default_components.py`:
`from rasa.nlu.tokenizers.vietnamese_tokenizer import VietnameseTokenizer`

- Add vào mảng `DEFAULT_COMPONENTS` dòng sau
 `VietnameseTokenizer,`

# RUN
Đã có một model được train sẵn, không cần train lại.
để khởi động server rasa, cần chạy các lệnh sau:
- Mở một terminal lên chạy các lệnh sau:
`conda activate NAME`  
`rasa run -m models --enable-api --cors "*"`
- Mở một terminal khác lên chạy lệnh sau để chạy server actions:
`conda activate NAME`  
`rasa run actions`  
## Lưu ý: mở đồng thời 2 terminal trên, sau khi mở thành công, hãy quay lại giao diện chat, bạn đã có thể chat với rasa.

# TRAIN
Nếu bạn muốn train rasa với rasa core và rasa nlu (rasa sẽ response input của bạn), hãy chạy lệnh sau: `rasa train`  
Nếu chỉ muốn train với rasa nlu (rasa sẽ phân tích input của bạn): `rasa train nlu`


# RUN IN SHELL
`rasa shell`


# Test
Validate data `rasa data validate`
Tách data thành tập train và tập test sử dụng `rasa data split nlu`
Test 
`rasa test nlu --nlu train_test_split/test_data.yml`
`rasa test nlu --nlu data/nlu.yml --cross-validation`