from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from splitterator import VideoSlicer, make_template_jpg
import cv2
import numpy as np

class FramesSliceSearcherSSIM:
    def __init__(self, video_name, fps = 60, frame_size = (1920, 1080)): #создание объекта поиска склеек на видео методом SSIM
        self.__video_name = video_name #имя оригинального видео
        self.__template = make_template_jpg(video_name) #шаблон для поиска изображений
        self.fps = fps
        self.frame_size = frame_size

    
    def __calculate_position(self, frame_index, total_frames):
        # зная индекс текущего фрейма и их общее кол-во, мы можем понять на какой секунде произошла склейка
        # с помощью пропорции
        return (frame_index / total_frames) * (total_frames / self.fps)


    def search_for_slices(self, frames):
        """
            Метод для получения оценок
            дальше можно обрабатывать оценки любым удобным нам способом
            например, искать минимумы в массиве оценок и говорить, что в данном месте скорее всего была склейка
            или, все оценки, которые ниже некоторого порогового значения, тоже считать склейками
        """
        prev_image = cv2.imread(self.__template.format(frames[0])) #считываем первое изображение
        scores = [] # массив результатов анализа пар изображений
        for i in range(len(frames) - 1):
            next_image = cv2.imread(self.__template.format(frames[i + 1])) #считываем следующее изображение
            (score, diff) = ssim(prev_image, next_image, full=True, multichannel=True) #считаем меру схожести методом SSIM
            print('{} and {} with score = {}'.format(frames[i], frames[i+1], score)) #выводим результат в консоль
            prev_image = next_image # текущее изображение делаем предыдущим
            scores.append(score) # добававляем результат меры схожести в массив
        return np.array(score)

    def analyze_scores(self, scores):
        mean = np.mean(scores)
        var = np.sqrt(np.var(scores))
        print(mean, var)
        print('threshold = {}'.format(mean - 3 * var))
        indecies = np.where(scores < mean - 3 * var)
        return indecies, scores[indecies]

class FramesSliceSearcherMSE:
    def __init__(self, video_name, fps = 60, frame_size = (1920, 1080)):  #создание объекта поиска склеек на видео методом MSE
        self.__video_name = video_name
        self.__template = make_template_jpg(video_name)
        self.fps = fps
        self.frame_size = frame_size

    def __calculate_position(self, frame_index, total_frames):
        #frame_index / total_frames = current_second / total_seconds
        return (frame_index / total_frames) * (total_frames / self.fps)

    def search_for_slices(self, frames):
        """
            Метод для получения оценок
            дальше можно обрабатывать оценки любым удобным нам способом
            например, искать минимумы в массиве оценок и говорить, что в данном месте скорее всего была склейка
            или, все оценки, которые выше некоторого порогового значения, тоже считать склейками
        """
        prev_image = cv2.imread(self.__template.format(frames[0])) #считываем первое изображение
        scores = []  # массив результатов анализа пар изображений
        for i in range(len(frames) - 1):
            next_image = cv2.imread(self.__template.format(frames[i + 1])) #считываем следующее изображение
            score = mse(prev_image, next_image)  #считаем меру схожести методом MSE
            print('{} and {} with score = {}'.format(frames[i], frames[i+1], score)) #выводим результат в консоль
            prev_image = next_image # текущее изображение делаем предыдущим
            scores.append(score)  # добававляем результат меры схожести в массив
        return np.array(scores)

    def analyze_scores(self, scores):
        mean = np.mean(scores)
        var = np.sqrt(np.var(scores))
        indecies = np.where(scores > mean + 3 * var)
        print("mean = {}, var = {}".format(mean, var))
        print(indecies)
        print('threshold = {}'.format(mean + 3 * var))
        return indecies, scores[indecies]





