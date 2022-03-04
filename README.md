# CarsProject
Software to register, edit and visualize cars in a SQL Server database.

Made in collaboration with Rafael Nascimento (rsdnrafael)

Coded with Python and GUI's made with QtDesigner

The code has some parts in portuguese and others in english because there were two developers. Also, the GUI is in portuguese because the project was developed for a Brazilian customer 

I'm aware that parts of the code could've been written better and smaller but I've learned a lot more during the making of this project than I knew before we started it

Also it's the first real project I've uploaded to github as I am still a beginner programmer

## What the program looks like:

Login Screen with Invalid License:

![image](https://user-images.githubusercontent.com/92460628/156687620-5134011a-46cb-4feb-910b-1f23c5915b06.png)


Normal Login Screen:

![image](https://user-images.githubusercontent.com/92460628/156687746-f5e95b08-c937-4a10-bb09-073dd45f479e.png)


Main Screen, here you can access all the other screens of the program:

![image](https://user-images.githubusercontent.com/92460628/156687821-3dd2b4ad-ea6c-4b68-9989-3c72b249180a.png)


Add Screen, here you can add cars to the database, you can also add multiple images and documents, which have special displays:

![Sem título](https://user-images.githubusercontent.com/92460628/156691168-1b221110-e540-4167-bdc5-5f98fab24f5b.png)


Edit Screen, here you can edit the cars in the database, after inserting them. Once the top input is filled, the rest of the fields are completed with the corresponding information, making it easier to edit. There are special buttons to edit the images, and a special pop-up to edit the documents:

![6](https://user-images.githubusercontent.com/92460628/156691595-94348bc6-a1d2-44fe-87c9-e964b207b233.png)


Consult Screen, here you can search the database, using the rows as filters, displaying all corresponding results, once an item is clicked, the Image and Document fields will be filled with the images and documents attatched to the car. Documents open on double-click and images can be passed with the arrow-buttons.
Also if an item is selected, you can click the pencil button on the bottom-right to open the Edit Screen with all the inputs already filled.
On the bottom-right there are two more buttons, the letter one opens a Pop-up from which emails can be sent containing the data on the table in a PDF, and the donwload button which downloads said PDF

![4](https://user-images.githubusercontent.com/92460628/156690950-ec081b92-f7ba-4d1f-bccf-143e97436a59.png)


Email Pop-up from Consult Screen, here you fill the email field with the emails you want to send to with ';' as the separator, the subject and messages are generated automatically and modified when the check-boxes are clicked, modifying the #conteudo (portugues for content). The subject and message fields can be altered manually:

![5](https://user-images.githubusercontent.com/92460628/156692289-b767c2b5-729f-4905-97c4-f1d1f5dff964.png)


The Config Screen has two tabs, one where you can see information about the logged in user, and other with configurations that can be customized on the program, mainly concerning the email.

![2](https://user-images.githubusercontent.com/92460628/156693099-2c2f3835-483d-40a8-ad72-f42eab216f9d.png)

The customizable configurations include: Wheter the consult screen generates one single PDF with all the information on the table, or one for each line (this was requested by the customer); The automatic subject and message displayed on the email pop-up; The login info for the user email (necessary for the integration with yagmail)

![3](https://user-images.githubusercontent.com/92460628/156693116-a1efb906-c887-4167-b5b7-5d3fc13afc52.png)


Finally, there's the Edit User Screen, where you can edit the username and password for the logged in user

![7](https://user-images.githubusercontent.com/92460628/156693518-956514bd-0795-4ff8-9ad7-686db3a93340.png)


