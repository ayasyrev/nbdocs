```python
from IPython.display import display, display_jpeg, Image
```


```python
cat_image_filename = 'images/cat.jpg'
print('Image output with `Image` from `IPython`.')
Image(cat_image_filename)
```
!!! output ""  
    Image output with `Image` from `IPython`.





    
![jpeg](images/code_image_files/output_1_1.jpg)
    




```python
dog_image_filename = 'images/dog.jpg'
display(Image(dog_image_filename))
print('Output with `display` from `IPython`')
dog_image_filename
```


    
![jpeg](images/code_image_files/output_2_0.jpg)
!!! output ""  
    Output with `display` from `IPython`
!!! output ""  
    'images/dog.jpg'


