from skimage.metrics import structural_similarity as ssim
from splitterator import VideoSlicer, Splitterator, VideoBuilder, make_template_jpg
from analyzer import FramesSliceSearcherMSE, FramesSliceSearcherSSIM
import time
import numpy as np


path_to_video = "resources/video/video.mp4"

frame_size = (600, 800)
#fps = 60

spl = Splitterator(path_to_video) # объект для разбития изображения на фреймы
print('Cropping video, may take a while...')
fps = spl.save_frames(frame_size) # сохраняем фреймы в разрешении 600х800, для ускорения работы алгоритма

slicer = VideoSlicer(path_to_video) # создаем объект, для разбиения видео на склейки

# создаем видео из 3 склеек
# первая склейка длится 3 секунды в промежутке 0 - 3 секунды
# третья склейка длится 1 секунду в промежутке от 9 до 7 секунд (она идет в обратном порядке)
r = slicer.slice_video(0, 3) + slicer.slice_video(9, 7) # + slicer.slice_video(5, 4)

builder = VideoBuilder("output.mp4", make_template_jpg(path_to_video), fps, frame_size) # создаем объект для записи видео
builder.compile_and_save_video(r) # сохраняем нашу склейку


slice_searcher = FramesSliceSearcherSSIM(path_to_video, fps, frame_size) # создаем объект для поиска склеек на видео
start = time.time() #таймер
scores = slice_searcher.search_for_slices(r) # получение результатов
end = time.time()
print('it took me {}'.format(end - start))
i, s = slice_searcher.analyze_scores(scores)
print(i, s)




