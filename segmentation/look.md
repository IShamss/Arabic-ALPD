### Algorithms:
- Vertical protection : is based on binary image and good for image that are not heavily but is weak in recognition between 2,3 persian digits. '٢' '٣'
- Connected domain:is based on the connectivity of character for letters and numbers ,effect of segmentation are perfect,persian character makes mistake with 'ب' ,'پ' 
- Template matching: is based on normalization which is to refine the characters into  block containing no extra white spaces(pixels) in all borders of the characters
### Template matching: 
`is a method that detects the characters, comparing the extracted characters and the templates built in the database`
> Template matching is performed after resizing the extracted character into the same size.

> The different styles of characters and numbers are stored as a templates

---
### TODO:
#### LPCS (License plate character segmentation )
1. get-input (image of plate in any side-view)
2. Character Detection
   - Perspective Transform (rotate 90 (adjust plate))
   - adaptive thresholding image (type="Gaussian" ) Or any other algorithm...
   - detect un-necessary dots
   - character detection
3. output results

---
### Problems
 1. image noise 
 2. plate frame 
 3. clinch ??
 4. rotation and illumination