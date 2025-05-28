# What

**the only QR generator you'll ever need.**  
From basic QR generation to advanced features like:

- Dynamic links  
- Traffic tracking  
- Image integration  

All packed in one seamless tool.


# Why

On **24th May 2025**, I was organizing a tech event.  
During the closing notes, I thought it would be helpful to display the social links of our **speakers and sponsors** on the screen, so the audience could easily access them.

But but — I couldn’t find a **free QR generator** that fit all my needs.

So yaa, here I am **making/made my own**.

# Basic Info 
<p align="right"><sub>26th May 2025</sub></p>

**QR codes** (Quick Response codes) are two-dimensional barcodes that store information in a grid of black and white squares. They are designed to be scanned quickly by digital devices, such as smartphone cameras, and can hold much more data than traditional one-dimensional barcodes. And thre is a catch. There are of two types.

- ### Static Qr
```
They are permanent and uneditable once created. They always point to the same content or URL, making them ideal for simple, one-time use cases.

or

in simple terms the code stores data directly in their pattern—like URLs, text, or contacts. When scanned, they lead straight to the content without redirect link.

    your link -> Qr holds your link in binary form by making patterns.
```
- ### Dynamic Qr
```
it lets you update the content anytime without changing the code itself, making them perfect for evolving or long-term campaigns.

or

in simple terms the qr do not store info directly in the pattern. The code use a short URL that redirects to the final content (like a website, PDF, or app). This makes them editable anytime, unlike static codes that store data directly.


    Your link/data -> some storage -> link of that address in the qr

Think of this like using Google Drive, where you can share the folder link to anyone and have the access to manipulate data lately.
```
## Python Tool
<p align="right"><sub>28th May 2025</sub></p>

- ### tkinter
    tool in Python that helps you build simple desktop applications with a graphical user interface (GUI) — meaning apps with buttons, text boxes, windows, etc. 
    
    - It's like giving your Python program a face that people can interact with, instead of just typing commands in the terminal.

```
Tkinter = Python + GUI elements
```
- ### flask 
    a lightweight and beginner-friendly tool in Python that helps you build web applications — apps that run in your browser.

    - in simple terms, flask lets you turn your python code into a website. It's a web framework, and give you the building blocks to create things.
```
Flask = Python + Web Development
```

## project_under_progress
<p align="right"><sub>26th May 2025</sub></p>

    STARTED on 25th May 2025

Whenever I will be updating my project, I will mention why I did that and when. For example - this section got added on 26th, hence you can see the same under the heading. 25th May 2025 is the 0 of our number line

- ## Timeline(2025)
    - ### 24th May - ran into the problem
    - ### 25th May - writing down the features I have to make
        - a qr generator.
        - should be dynamic - can be edited even when the qr is generated.
        - traffic monitoring.
        - auto-detects link type and suggests optimal display.
        <br>
    - ### 26th May - building basic qr
        <p align="right"><sub>26th May 2025</sub></p>

        ```
        At first I thought it is going to be simple but aahaa, its life.
        Decided to write the logic using python and got into Moral dilemma.

        In order to create the qr there exist two most prominent libraries. 
            1. qrcode -> fast
                         got dependencies (needs [pillow]PIL)
                         output format is PNG
                         and supports logo embedding
            1. segno -> faster
                         no dependencies (pure python)
                         output formats are PNG, SVG and PDF
                         does not support logo embedding

        After doing some study study, I decided to go with segno as for dynamic QR code creation, especially in web apps or any context where you need to generate and serve QR code images on demand, segno offers more flexibility, easier integration, and a broader range of output formats with less overhead.

        Though the most important aspect is not the QR code library itself, but how you design the backend and the way you generate and serve the QR codes. I mentined it because I got carried away while doing so 🙌😗. 

        CONCLUSION :- I decided to go with dynamic qr creation only, wont be thinkinng about the static from now
        ```

    - ### 27th May - making up th Ui
    <p align="right"><sub>27th May 2025</sub></p>
    
    ```
    though the things were working good, still I decided to give it a Ui 
    used tkinter for that (another python library )

    so here are the changes and improvements we made to our QR code generator
        Added Output Format Selection -> Users can now choose the file format
        Added a Scale Slider for QR Size -> its self explanatory I guess
        Improved User Experience and Error Handling -> fixed the collapsing issue 

    enhanced the QR code generator by introducing several user-friendly features and improvements. Most notably, we added the ability for users to choose the output file format—such as PNG, SVG, JPG, or BMP—through a graphical file save dialog, eliminating the need to manually type file extensions and reducing the risk of errors.
    Also replaced the manual entry of the QR code scale with a slider, making it much easier and more intuitive for users to select the desired size visually. Additionally, improved the overall user experience by implementing robust handling and clear feedback messages, ensuring that the application responds to user actions like canceling the file dialog or encountering invalid input.
        
    ```
    - ### 28th May - setting up flask
    <p align="right"><sub>28th May 2025</sub></p>
    
    ```
    as stated above, I started off with a desktop-based QR Code Generator using Python’s tkinter and segno libraries. While it's great locally, I wanted to make something more accessible — something that you can use right from your browser.

    So, I converted the entire app into a web-based QR generator using Flask, 

        Yaaaaaaaa I KNOW, ITS DUMB OF ME
        that I spent my whole yesterday making the tkinter GUI, just to replace.

    But honestly, I saved my time by doing so, else I have to do that later with more no. of features. Though I am not removing the "qr_generator.py" file, instead I will be updating that too.  

    Here is the learning, the quicker you fix your code, the more resources you save.
    ```