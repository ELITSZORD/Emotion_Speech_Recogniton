
# Library
import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import callback, ctx, State
import PIL.Image as Image
from dash import register_page
import os


# Register
dash.register_page(__name__, path='/')


# Home Page Core Components

## Image 1 - size=750X450
image_directory1 = './asset/'
image_files1 = ["glass1.jpg"]
data1 = []
for image_file in image_files1:
    img1 = Image.open(os.path.join(image_directory1, image_file))
    data1.append(img1)
    
## Image 2 - size=750X450
image_directory2 = './asset/'
image_files2 = ["process.jpg"]  
data2 = []
for image_file2 in image_files2:
    img2 = Image.open(os.path.join(image_directory2, image_file2))
    data2.append(img2)
    
## Image 3 - size=750X450
image_directory3 = './asset/'
image_files3 = ["impact.jpg"]  
data3 = []
for image_file3 in image_files3:
    img3 = Image.open(os.path.join(image_directory3, image_file3))
    data3.append(img3)


## Style
#hstyle7 = {'height': '1400px', 'width':'1300px'}



layout = dbc.Row([
        #dbc.Col([],width=2),
        dbc.Col([
                dbc.Carousel(
                    items=
                    [
                        {"key": "1", "src": data1,"img_style":{"width":"1500px","height":"695px" }, "imgClassName": ""},
                        {"key": "2", "src": data2,"img_style":{"width":"1500px","height":"695px" }, "imgClassName": ""},
                        {"key": "3", "src": data3,"img_style":{"width":"1500px","height":"695px" }, "imgClassName": ""}
                    ]
                    ,
                    controls=True,
                    indicators=True
                )
        ],width=12),
        #dbc.Col([],width=2)
])