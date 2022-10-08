# ALPD
> Arabic License Plate Detector
## 📝 Table of Contents

- [Description](#📙-description)
- [Localisation](#localisation)
- [Segmentation](#segmentation)
- [Applications Demo](#📷applications-demo-hr)
    - [Front App](#front-app)
    - [Labling Tool](#labeling-tool)
    - [Streaming App](#streaming-app)

- [Get started](#🏁-getting-started)
  - [Prerequisite](#prerequisite)
  - [Installation](#installation)
  - [Running](#running)
- [Contributers](#contributors)

##  📙 Description 


This projects simulates a smart city's gate to facilitate residents and visitors access using license plate detection. This process is done in three phases. First is localisation, where we get a cropped image of the plate only. Next is segmentation, Where each character is split apart from the other to aperient the character recognition phase. Finally, Character recognition, This phase results in the license plate's characters in the form of string in which you are granted access or not based upon.

## Localisation<hr>

<p align="center">
  <img src="./media/locate.png">

## Segmentation <hr>

<p align="center">
  <img src="./media/segment.jpg">

## Recognition<hr>
A KNN model is trained on recognizing Arabic Chracters and numbers using segmented characters images. The trained model takes segmented characters as input then outputs the plate's string.
<p align="center">
  <img src="./media/rec.png">
  <br><br>

## 📷Applications Demo <hr>
- ## Front App
The front app is used to simulate the smart city's gate, You must have a folder containing cars images with Egyptian license plates. Put the folder's path in Images Folder and the result will look like this. 
<p align="center">
  <img src="./media/front.jpeg">
  <br><br>

- ## Labeling Tool
This tool is used to increase accuracy and help with character labeling, Where you can click on "Incorrect Answer" if the result is incorrect and you'll get the accuracy percentage at the end. You can either choose save or skip, if you click save, an image of each character will be saved in a folder with a number according to its position in arabic alphabet. If a character is wrong you can modify it using the drop down menu, and save it for further improvements.

<p align="center">
  <img src="./media/Label.jpeg">
  <br><br>

- ## Streaming App
The streaming app  allows you to stream a live feed from your mobile phone remotely using IP broadcast. Once you capture an image it goes through the pipeline.

<p align="center">

  <img src="./media/stream.gif">


## 🏁 Getting Started
### Prerequisite 

1. Install Python
2. Install packages in **requirements.txt** using pip
3. Any Python IDE 

### Installation 

1. **_Clone the repository_**

```sh
$ git clone https://github.com/IShamss/Arabic-ALPD.git
```

2. **_Right click on the folder and open it with the IDE_**

### Running 

**_Running program_**

```sh
Run FrontApp.sh or Labeling.sh or Straming.sh
```

# Contributors

<table>
  <tr>
    <td align="center">
    <a href="https://github.com/ZiadSheriif" target="_black">
    <img src="https://avatars.githubusercontent.com/u/76125650?v=4" width="150px;" alt="Zeyad Tarek"/>
    <br />
    <sub><b></b></sub></a>
    </td>
    <td align="center">
    <a href="" target="_black">
    <img src="" width="150px;" alt=""/>
    <br />
    <sub><b>Abdelrahman Mohamed</b></sub></a>
    </td>
    <td align="center">
    <a href="" target="_black">
    <img src="https://avatars.githubusercontent.com/u/82404564?v=4" width="150px;" alt="Beshoy Morad"/>
    <br />
    <sub><b>Beshoy Morad</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/ZiadSheriif" target="_black">
    <img src="https://avatars.githubusercontent.com/u/78238570?v=4" width="150px;" alt="Ziad Sherif"/>
    <br />
    <sub><b>Ziad Sherif</b></sub></a>
    </td>
    
    
  </tr>
 </table>

# License

> This software is licensed under MIT License, See [License]() for more information @OmarRiad.



