## Inspiration
Today we live in a world that is all online with the pandemic forcing us at home. Due to this, our team and the people around us were forced to rely on video conference apps for school and work. Although these apps function well, there was always something missing and we were faced with new problems we weren't used to facing. Personally, forgetting to mute my mic when going to the door to yell at my dog, accidentally disturbing the entire video conference. For others, it was a lack of accessibility tools that made the experience more difficult. Then for some, simply scared of something embarrassing happening during class while it is being recorded to be posted and seen on repeat! We knew something had to be done to fix these issues.

## What it does
Our app essentially takes over your webcam to give the user more control of what it does and when it does. The goal of the project is to add all the missing features that we wished were available during all our past video conferences.

### Features:
#### Webcam:
1 - Detect when user is away This feature will automatically blur the webcam feed when a User walks away from the computer to ensure the user's privacy

2 - Detect when user is sleeping We all fear falling asleep on a video call and being recorded by others, our app will detect if the user is sleeping and will automatically blur the webcam feed.

3 - Only show registered user Our app allows the user to train a simple AI face recognition model in order to only allow the webcam feed to show if they are present. This is ideal to prevent ones children from accidentally walking in front of the camera and putting on a show for all to see :)

4 - Display Custom Unavailable Image Rather than blur the frame, we give the option to choose a custom image to pass to the webcam feed when we want to block the camera

#### Audio: 
1 - Mute Microphone when video is off This option allows users to additionally have the app mute their microphone when the app changes the video feed to block the camera.

#### Accessibility: 
1- ASL Subtitle Using another AI model, our app will translate your ASL into text allowing mute people another channel of communication

2- Audio Transcriber This option will automatically transcribe all you say to your webcam feed for anyone to read.

#### Concentration Tracker: 
1- Tracks the user's concentration level throughout their session making them aware of the time they waste, giving them the chance to change the bad habbits.

### How we built it
The core of our app was built with Python using OpenCV to manipulate the image feed. The AI's used to detect the different visual situations are a mix of haar_cascades from OpenCV and deep learning models that we built on Google Colab using TensorFlow and Keras.

The UI of our app was created using Electron with React.js and TypeScript using a variety of different libraries to help support our app. The two parts of the application communicate together using WebSockets from socket.io as well as synchronized python thread.

### Challenges we ran into
Dam where to start haha...

Firstly, Python is not a language any of us are too familiar with, so from the start, we knew we had a challenge ahead. Our first main problem was figuring out how to highjack the webcam video feed and to pass the feed on to be used by any video conference app, rather than make our app for a specific one.

The next challenge we faced was mainly figuring out a method of communication between our front end and our python. With none of us having too much experience in either Electron or in Python, we might have spent a bit too much time on Stack Overflow, but in the end, we figured out how to leverage socket.io to allow for continuous communication between the two apps.

Another major challenge was making the core features of our application communicate with each other. Since the major parts (speech-to-text, camera feed, camera processing, socket.io, etc) were mainly running on blocking threads, we had to figure out how to properly do multi-threading in an environment we weren't familiar with. This caused a lot of issues during the development, but we ended up having a pretty good understanding near the end and got everything working together.

### Accomplishments that we're proud of
Our team is really proud of the product we have made and have already begun proudly showing it to all of our friends!

Considering we all have an intense passion for AI, we are super proud of our project from a technical standpoint, finally getting the chance to work with it. Overall, we are extremely proud of our product and genuinely plan to better optimize it in order to use within our courses and work conference, as it is really a tool we need in our everyday lives.

### What we learned
From a technical point of view, our team has learnt an incredible amount the past few days. Each of us tackled problems using technologies we have never used before that we can now proudly say we understand how to use. For me, Jonathan, I mainly learnt how to work with OpenCV, following a 4-hour long tutorial learning the inner workings of the library and how to apply it to our project. For Quan, it was mainly creating a structure that would allow for our Electron app and python program communicate together without killing the performance. Finally, Zhi worked for the first time with the Google API in order to get our speech to text working, he also learned a lot of python and about multi-threadingbin Python to set everything up together. Together, we all had to learn the basics of AI in order to implement the various models used within our application and to finally attempt (not a perfect model by any means) to create one ourselves.

### What's next for Boom. The Meeting Enhancer
This hackathon is only the start for Boom as our team is exploding with ideas!!! We have a few ideas on where to bring the project next. Firstly, we would want to finish polishing the existing features in the app. Then we would love to make a market place that allows people to choose from any kind of trained AI to determine when to block the webcam feed. This would allow for limitless creativity from us and anyone who would want to contribute!!!!
