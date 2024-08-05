from PIL import Image
import requests
from transformers import AutoProcessor, LlavaForConditionalGeneration

def llava_inference(prompt,url):
    model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf")
    processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")
    
    #prompt = "USER: <image>\nWhat's the content of the image? ASSISTANT:"
    #url = "https://www.ilankelman.org/stopsigns/australia.jpg"
    image = Image.open(requests.get(url, stream=True).raw)
    
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    
    # Generate
    generate_ids = model.generate(**inputs, max_new_tokens=500)
    res=generate_ids[0][inputs.input_ids.shape[-1] :]
    #output = processor.batch_decode(res, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    output = processor.decode(res, skip_special_tokens=True)
    #output = output.replace("USER:  \nAre there any privacy or ethical issues involved in this picture? Please answer with yes or no. ASSISTANT: ", "")
    return output