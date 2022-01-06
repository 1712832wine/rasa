def name_cap(text):
    tarr = text.split()
    print(tarr)
    for idx in range(len(tarr)):
        tarr[idx] = tarr[idx].capitalize()
    return ' '.join(tarr)


text = 'nguyễn Hửu Trí'
print(name_cap(text))
