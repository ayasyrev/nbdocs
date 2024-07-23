```python
from IPython.display import display, display_jpeg, Image
```


```python
cat_image_filename = "images/cat.jpg"
print("Image output with `Image` from `IPython`.")
Image(cat_image_filename)
```

    Image output with `Image` from `IPython`.





    
![jpeg](output_1_1.jpg)
    




```python
dog_image_filename = "images/dog.jpg"
display(Image(dog_image_filename))
print("Here is output with `display` from `IPython`")
dog_image_filename
```


    
![jpeg](output_2_0.jpg)
    


    Here is output with `display` from `IPython`





    'images/dog.jpg'


