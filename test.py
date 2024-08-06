from image_text_getting import image_text_get
from privacy_filtering import privacy_processing
from download_images import images_download
url = 'https://www.digitaling.com/search/articles/?kw=%E6%96%B9%E6%B3%95%E8%AE%BA'
file_image_text_get = 'marketing_image_text.json'
image_text_get(url,file_image_text_get)
input_file = 'marketing_image_text.json'
output_file = 'marketing_image_text_filter.json'
privacy_processing(input_file,output_file)
output_file_download = 'marketing_image_file_text_filter.json'
images_download(output_file,output_file_download )