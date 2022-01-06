from underthesea import word_tokenize
text = '   Thời tiết ấm hơn có thể ngăn chặn việc bùng phát Covid-19 không?   '
text = text.lower().strip()
print(word_tokenize(text))
