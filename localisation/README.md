To run this code, you need to download the file in this link,
https://drive.google.com/file/d/1EUPtbtdF0bjRtNjGv436vDY28EN5DXDH/view?usp=sharing
and add it to the data folder.

If you are using conda, enter those commands in the anaconda command prompt:

For PCs without GPUs:

conda env create -f conda-cpu.yml

conde activate alpd-cpu


For PCs with GPUs:

conda env create -f conda-gpu.yml

conda activate alpd-gpu


Then, run:

python save_model.py


To test the license plate detection code, first, you need to add images to ./data/images. Then, you need to open detect.py and scroll all the way down. You will find 2 lines of code:

crop_one(...)

crop_multiple(...)


If you want to test out one image, comment out line 137 of the code by adding "#" to the start of the line, and then type "./data/images/[image name]" and then run:

python detect.py


If you want to test all the images in the folde, comment out line 136 of the code by adding "#" to the start of the line, then run:

python detect.py
