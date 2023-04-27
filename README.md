# caption-generator
AI tool that allows user to generate captions for social media using the images. 

Link to [demo video](https://youtu.be/2Gth4SzvYLE)

This is the overall flowchart of the assignment

![flowchart](/flowchart.png)

## Steps to use it
Assuming Node and python is installed on the device.

#### Setup Server
1. Open terminal in ```server``` folder.
2. Type ```pip install -r requirements.txt``` in the terminal and press enter.
3. Create a ```.env``` file in the server folder and write this in it:

    ```OPENAI_KEY=<YOUR KEY>```

You need to generate a key from OpenAI and use it here

4. Type ```python app.py``` in the terminal and press enter
5. It takes some time to initialize the server as it loads the models. Once loaded we can begin setting up client.

#### Setup client (UI)
1. Open terminal in ```client``` folder.
2. Type ```npm i --force``` in the terminal and press enter.
3. Type ```npm run dev``` in the terminal and press enter.
4. Wait for it to run and open the localhost URL
