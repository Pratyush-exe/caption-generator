from PIL import Image
import threading
import keras_ocr
import openai
import os
import dotenv
dotenv.load_dotenv()

prompt = ""

def text_to_image(model, feature_extractor, tokenizer, device, image_paths):
    images = []
    for image_path in image_paths:
        i_image = Image.open(image_path)
        if i_image.mode != "RGB":
            i_image = i_image.convert(mode="RGB")
        images.append(i_image)
    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    gen_kwargs = {"max_length": 16, "num_beams": 4}
    output_ids = model.generate(pixel_values, **gen_kwargs)
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return preds

def extract_text(_, img):
    pipeline=keras_ocr.pipeline.Pipeline()
    output_text = ''
    images=[keras_ocr.tools.read(img)]
    predictions=pipeline.recognize(images)
    first=predictions[0]
    for text, _ in first:
        output_text += ' '+ text
    return output_text

def task(i, body, model, feature_extractor, tokenizer, device, file, pipeline):
    global prompt
    txt2img = text_to_image(model, feature_extractor, tokenizer, device, [file.path])
    prompt += f"Image {i} contains:{txt2img[0]};"
    if body["useImage"]:
        extractText = extract_text(pipeline, file.path)
        prompt += f"and includes text:{extractText}\n"

def get_captions(body, model, feature_extractor, tokenizer, device, pipeline):
    global prompt
    prompt = ""
    threads = []
    
    if body["location"] != "":
        prompt += f"location:{body['location']}\n"  
    if body["occasion"] != "":
        prompt += f"occasion:{body['occasion']}\n"  
    if body["vibe"] != "":
        prompt += f"vibe/feeling:{body['vibe']}\n"
    if body["details"] != "":
        prompt += f"more details:{body['details']}\n"
          
    for i, file in enumerate(os.scandir("temp")):
        t = threading.Thread(target=task, args=(i, body, model, feature_extractor, tokenizer, device, file, pipeline))
        t.start()
        threads.append(t)
        
    for thread in threads:
        thread.join()
    
    prompt += f"\nGiven these details about images, write a combined caption for my social media page. \
                Use {body['person']}-person-perspective. Also generate hashtags and emoji."
    return {"result": chatGPT(prompt)}

def chatGPT(prompt):
    openai.api_key = os.getenv("OPENAI_KEY")
    return openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=250,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1,
        n=5
    )

def empty_temp_folder():
    for file in os.scandir("temp"):
        os.unlink(file.path)
        