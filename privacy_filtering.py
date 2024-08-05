import json
from models.LLaVA_inference import llava_inference
from models.language_model_api import get_response
#from language_model import get_text_response

def privacy_processing(input,output):
    with open(input, 'r') as file:
        data = json.load(file)
    
    
    processed_data = []
    
    for entry in data:
        context = entry.get('context', [])
        processed_context = []
    
        for item in context:
            if 'text' in item:
                #query_text="这句话涉及到作者名或是作者ID吗？请回答是或者不是："+item['text']
                #generate_result = get_response(query_text)
                if '作者' not in item['text'] and 'ID' not in item['text']:
                    processed_context.append(item)
            elif 'image' in item:
                query_image_text="USER: <image>\nAre there any privacy or ethical issues involved in this picture? Please answer with yes or no. ASSISTANT:"
                url=item['image']
                generate_result_image=llava_inference(query_image_text,url)
                if 'Yes' not in generate_result_image and 'yes' not in generate_result_image:
                    processed_context.append(item)
    
        entry['context'] = processed_context
        processed_data.append(entry)
    
    # Save the processed data to a new JSON file
    with open(output, 'w') as file:
        json.dump(processed_data, file, ensure_ascii=False, indent=4)
    
    print('数据已保存到文件中')