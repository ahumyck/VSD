import cv2
import os
import glob

def make_template(filename, ext):
    return os.path.splitext(filename)[0] + "{}" + ext

def make_template_jpg(filename):
    return make_template(filename, ".jpg")

# Класс для получения фреймов из видео
class Splitterator:  #создание объекта для разбиения видео на изображения
    def __init__(self, video_name):
        self.__video_name = video_name
        self.__template = make_template_jpg(video_name) #создаем шаблон для сохранения изображений
    
    def save_frames(self, new_size = None) -> (int, float):
        vidcap = cv2.VideoCapture(self.__video_name) # получаем поток видео
        success, image = vidcap.read() # получаем очередное изображение из видео
        count = 0
        while success: # до тех пор, пока есть изображения в видео
            if new_size is not None: # если надо, меняем размер изображения
                image = cv2.resize(image, new_size)
            cv2.imwrite(self.__template.format(count), image) #сохраняем картинку на компьютере
            success, image = vidcap.read() #берем следующее изображение
            count += 1
        fps = vidcap.get(cv2.CAP_PROP_FPS) 
        vidcap.release() # возвращаем ресурсы компьютеру
        return fps #возвращаем (кол-во кадров, длительность видео в секундах)


# Класс для удобной склейки фреймов из видеоряда
class VideoSlicer:
    def __init__(self, video_name): #создание объекта для разбиения видео подвидео
        self.__video_name = video_name
        self.__template = make_template_jpg(video_name) #создаем шаблон для загрузки изображений
        self.__frames, self.__video_length = self.__get_frames_and_length_of_video() # получаем кол-во кадров и длину видео
    
    def __get_frames_and_length_of_video(self):
        vidcap = cv2.VideoCapture(self.__video_name)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        vidcap.release()
        return count, float(count) / float(fps)

    #получение подвидео
    def slice_video(self, start: float, end: float) -> list:
        if start is None and end is None: #если не указано ни начало, ни конец, то возвращаем все видео
            return list(range(0, self.__frames, 1))
        s = int((start / self.__video_length) * self.__frames) # переводим начало (в секундах) в номер кадра
        e = int((end / self.__video_length) * self.__frames) # переводим конец (в секундах) в номер кадра


        if s > e: # если начало больше чем конец, возвращаем индексы кадров в обратном порядке, чтобы видео шло в обратную сторону
            # проверка, чтобы мы не вышли за границы границы длины видео
            s = self.__frames - 1 if s >= self.__frames else s - 1
            e = -1 if e < 0 else e - 1
            return list(range(s, e, -1))
        elif s == e: #если начало и конец совпадают, возвращаем один кадр
            # проверка, чтобы мы не вышли за границы границы длины видео
            s = self.__frames - 1 if s >= self.__frames else s
            s = 0 if s < 0 else s
            return [s]
        else:
            # проверка, чтобы мы не вышли за границы границы длины видео
            s = 0 if s < 0 else s
            e = self.__frames if e >= self.__frames else e
            return list(range(s, e, 1))


# Класс, для создания видео из видеоряда, полученным классом VideoSlier
# todo: сделать так, чтобы он заработал :(
class VideoBuilder:
    def __init__(self, output_video_name, template_images_name, fps = 60, frame_size = (1920, 1080)):
        self.__output_name = output_video_name
        self.__template = template_images_name
        self.__fps = fps
        self.__frame_size = frame_size

    def compile_and_save_video(self, indecies):
        #не работает :(
        codec = cv2.VideoWriter_fourcc(*'MP42')
        out = cv2.VideoWriter(self.__output_name, codec, self.__fps, self.__frame_size)
        for index in indecies:
            filename = self.__template.format(index)
            img = cv2.imread(filename)
            out.write(img)
        out.release()


    