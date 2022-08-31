### Steps of segmentation

- remove bluring: `clear un-clear points (using Gaussian filter(low pass filter)) (kernal which has a rectangular of pixel which surrounded by pixel of image)`
- thresholding: `Conversion an image from colour or grayscale into a binary image(make black and white)`
- masking: `taking the region of interest only (ROI)`

## Techniques of thresholding

1. **Otsu’s segmentation**(Set the pixel to white; if they are greater than the threshold else, set it to black.)
2. **Edge-based segmentation algorithms**(It highlights regions of high spatial frequency (excluded))
3. **Clustering-based image segmentation algorithms**
4. **Neural networks for segmentation** (CNN,Deep Learning) (Most efficient and common used)

---

### TODO:

#### LPCS (License plate character segmentation )

1. get-input (image of plate in any side-view)
2. Character Detection
    - Perspective Transform ( (adjust plate)
    - thresholding image
    - detect un-necessary dots
    - character detection
3. output results

---

### Problems

1. image noise
2. plate frame
3. clinch ??
4. rotation and illumination

---

### Algorithms:

- Vertical protection : is based on binary image and good for image that are not heavily but is weak in recognition
  between 2,3 persian digits. '٢' '٣'
- Connected domain:is based on the connectivity of character for letters and numbers ,effect of segmentation are
  perfect,persian character makes mistake with 'ب' ,'پ'
- Template matching: is based on normalization which is to refine the characters into block containing no extra white
  spaces(pixels) in all borders of the characters

### Template matching:

`is a method that detects the characters, comparing the extracted characters and the templates built in the database`
> Template matching is performed after resizing the extracted character into the same size.

> The different styles of characters and numbers are stored as a templates