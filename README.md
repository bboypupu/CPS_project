# Driving_Skill_Evaluation
### A simple driving skill evaluation system using just smart phone.  
Nowadays, over 90% of families in America own at least one vehicle. Driving has already been a big portion of American’s daily life for decades. Therefore, we want to make a simple system to evaluate the driving skill of the driver. The user will get a score of their driving skill after finishing a tour, and the only thing needed is a smart phone. We believe it can help drivers to evaluate their driving skill and improve their skill to some extent. Furthermore, insurance company can also use the score to evaluate the credit of their clients, while those who has better driving skill should be benefited with lower insurance bill.  
When it comes to the details, we want to build an app in the smart phone (in our case, iPhone). The user can place the device behind the front windscreen, and let it automatically analyze the image and recognize different patterns on the road. In this project, we restrict the targets within the vision to traffic lights, stop signs, speed limit signs, and pedestrians. Besides, we will take advantage of the GPS and accelerometer on the phone to calculate the speed and acceleration of the car. After comparing the speed of the car and patterns gotten by the mobile device, we can evaluate his/her driving score by the information. For example, if the user did not slow down while meeting a pedestrian, he/she would lose some points; if the user drive smoothly for a period of time, he/she would gain some points.  
There are several researches regarding to recognition of traffic signs as listed in the reference. Mainly, we are going to implement Convolutional Neural Network for pattern recognition with the method by Shustanov, A. et al. We want to use the dataset called German Traffic sign benchmark as the training set of traffic signs. On the other hand, we are using cascade classifier by Angelova, A. et al. to detect pedestrians for low latency with Caltech dataset. We will utilize the common tools for implementing computer vision and machine learning with the developer tools like coreML and Metal on iOS, and build virtual machines on AWS with TensorFlow. Meantime, we would also compare the efficiency of computation under different real-time scenario, such as whether compute locally with GPU on the phone, or upload to the cloud via LTE.  