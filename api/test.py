import logging


def get_unique_words():
    try:
        f = open(r"C:\Users\rohan\OneDrive\Desktop\demo.txt", "r")
        words = []
        unique_list = []

        for line in f:
            temp = line.split(" ")
            words = words + temp

        for word in words:
            if words.count(word) == 1:
                unique_list.append(word)
            if words.count(word) > 1:
                if word in unique_list:
                    pass
                else:
                    unique_list.append(word)



        f.close()
        return unique_list, len(unique_list)
    except Exception as e:
        logging.error(e)

print(get_unique_words())



students = Students.objects.filter(Q(class=xyz) | Q(se=abc))
