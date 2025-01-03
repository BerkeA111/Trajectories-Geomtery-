# -*- coding: utf-8 -*-
"""Trajectoids.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XZ7Lf6pZu6nzEuqt_dUCHormeSbCCMlP

# Trajectoid

Given almost any flat path, this demo computes the 3D shape ("trajectoid") that would exactly follow this path when rolling down a slope.

Watch a [popular explanation on YouTube channel of Nature](https://www.youtube.com/watch?v=2lW9HznqsVY&lc=UgwelVipk0QC7FdNWZV4AaABAg.9tD4YfIcdvc9tI4fvL2fgS):

<a class="youtube" href="http://youtube.com/watch?v=2lW9HznqsVY">
    <img src="http://i3.ytimg.com/vi/2lW9HznqsVY/default.jpg" alt="Trajectoids Video on Nature YouTube channel" />
</a>

For details, see the original research article: Sobolev, Y.I., Dong, R., Tlusty, T. *et al*. Solid-body trajectoids shaped to roll along desired pathways.
*Nature*  **620**, 310–315 (2023). DOI: [10.1038/s41586-023-06306-y](https://rdcu.be/diYqN)

An extended code repository with various examples and additional features is on Github:
https://github.com/yaroslavsobolev/trajectoids

## How this demo works

A Google Colab notebook executes on virtual machine in the Google infrastructure. No installation of any software into your local machine is needed. A Google Colab notebook consists of sections (cells), each containing code to be executed. A section (cell) is executed by pressing black "Play" button at its top left corner. After you press it, wait until execution finishes -- that is, the animation circling around the "Play" buttom will stop and the output will write "Execution finished".

Everything in this demo is open-source. You are free to tweak every piece of all this code as you wish.

This Notebook might only work properly with Google Chrome and Firefox.

# Step 1: Install all the required software into this virtual notebook.
"""

#@title *↓↓↓* click this black "Play" button to install all the software into virtual notebook. Once it's done, hit "restart runtime" like it says (or press Ctrl+M). You'll be asked whether you are sure -- click "yes".

# First we install openscad
!sudo add-apt-repository ppa:openscad/releases -y
!sudo apt-get update
!sudo apt-get install openscad
# Now we install Viewscad
!pip install viewscad trimesh open3d

print("Execution finished.")

#@title *↓↓↓* click this black "Play" button after you've restarted the runtime.

from google.colab import files
import viewscad

!mkdir cut_meshes
!mkdir folder_for_path

url = f"https://raw.githubusercontent.com/yaroslavsobolev/trajectoids/main/compute_trajectoid_in_colab.py"
!wget --no-cache {url}
url = f"https://raw.githubusercontent.com/yaroslavsobolev/trajectoids/main/misc/for_colab/unit_geosphere.stl"
!wget --no-cache {url}

r = viewscad.Renderer()

print("Execution finished.")

"""# Step 2: Find correct relative scale of your path and its trajectoid.

You can provide the path in three alternative ways: by drawing it, by uploading a .CSV file with a list of coordinates, or by randomly generating the path (the default option in this demo).
"""

#@title ## (Optional) You may provide your path by drawing it: {vertical-output: true, run: "auto"}
#@markdown You can optionally draw the path for which a trajectoid will be constructed: press black "Play" button to execute this cell, then draw a black path with mouse going from left to right on white rectangle.
#@markdown After you're done, press "Save" button on the left and then don't forget to **later choose "drawing" in the `source_of_path` parameter below**.
#@markdown
#@markdown Brush color can be swapped from black to white by clicking one of two rectangles on the right. White brush can be used as an eraser. Don't worry if you have white gaps in your path -- that's OK, gaps will be interpolated.
#@markdown
#@markdown
#@markdown For best results, try to keep the left starting point at the same level as right ending point. Self-intersections and double crossings of any vertical line will be ignored. If you want more freedom in path selection, instead of drawing it here you should supply a CSV text file with a list of x,y coordinates.

import ipywidgets as widgets
from ipywidgets import Layout, Button, Box
from IPython.display import display, HTML, Image
from google.colab.output import eval_js
from base64 import b64decode

Square_Size = 256
Brush_Size = 3
filename = "my_drawing"
filename = filename + ".png"

js_code = '''
<style>
  .colors-buttons div {
      width: 30px;
      height: 30px;
      margin: 2px;}
  div {
      display: flex;
  }
  canvas{border:1px solid black !important;}
</style>
<canvas id="myCanvas" width="%d*2" height="%d"></canvas>
<div class="colors-buttons">
  Select brush color:
  <div class="color" style="background-color: #FFFFFF; border:1px solid black;" id-color="#FFFFFF"></div>
  <div class="color" style="background-color: #000000; border:1px solid black;" id-color="#000000"></div>
</div>
<script>
  var canvas = document.querySelector('canvas')
  var ctx = canvas.getContext('2d')
  ctx.fillStyle = 'white';
  ctx.fillRect( 0, 0, canvas.width, canvas.height)
  var Brush_Size = %d
  var button = document.querySelector('button')
  var mouse = {x: 0, y: 0}
  canvas.addEventListener('mousemove', function(e) {
    mouse.x = e.pageX - this.offsetLeft
    mouse.y = e.pageY - this.offsetTop
  ctx.fillStyle = 'black';
  })
  canvas.onmousedown = ()=>{
    ctx.beginPath()
    ctx.moveTo(mouse.x, mouse.y)

    canvas.addEventListener('mousemove', onPaint)
  }
  canvas.onmouseup = ()=>{
    canvas.removeEventListener('mousemove', onPaint)
  }
  var onPaint = ()=>{
    ctx.fillRect(mouse.x-( Brush_Size/2), mouse.y-(Brush_Size/2), Brush_Size, Brush_Size)
    ctx.stroke()
  }
  const colors = document.getElementsByClassName('color');
  Array.from(colors).forEach(color => {
      color.addEventListener('click', (event) => {
          const colorSelected = event.target.getAttribute('id-color');
          ctx.fillStyle = colorSelected;
      });
  });
    // FINISH BUTTON
  var data = new Promise(resolve=>{
    button.onclick = ()=>{
      resolve(canvas.toDataURL('image/jpg'))
    }
  })
</script>
'''


## Function to Appear Image Canvas
def draw(filename=filename,  w=Square_Size, h=Square_Size, Brush_Size=Brush_Size):
  display(HTML(js_code % (w, h, Brush_Size)))
  data = eval_js("data")
  binary = b64decode(data.split(',')[1])
  if AttributeError:
    pass
  with open(filename, 'wb') as f:
    f.write(binary)
  return len(binary)
  if button2.on_click(on_button_clicked2):
    pass


## Action for Reset Button
def on_button_clicked(b):
  with output:
    #display(HTML(canvas_html % ( w=$Square_Size*2, h=$Square_Size, Brush_Size=$Brush_Size)))
    data = eval_js("data")
    binary = b64decode(data.split(',')[1])
    with open(filename, 'wb') as f:
      f.write(binary)
  return len(binary)


## Show Save Button & Save outputs
button = widgets.Button(description="Save")
button.on_click(on_button_clicked)
output = widgets.Output()
display(button, output)

## Show Canvas for the First Time
draw(filename=filename,  w=Square_Size*2, h=Square_Size, Brush_Size=Brush_Size)
print("   Drawing has been saved.")

#@title ## (Optional) You may provide your path as list of coordinates in a CSV file.
#@markdown <--- Click this "Play" button then click "Choose Files" to upload your CSV file
#@markdown
#@markdown This should be a text file with two columns, comma-delimited. First column is
#@markdown X coordinates, second column is Y coordinates. Direction of gravity is assumed
#@markdown to be along the X axis, in the direction if increasing X.
#@markdown
#@markdown Format example showing first 6 lines of CSV file:
#@markdown
#@markdown     1.840776945462769265e-01,-4.440470701774223115e-03
#@markdown     2.121981061754569242e-01,1.430647038434568197e-02
#@markdown     2.403185178046369219e-01,6.730974625118812948e-02
#@markdown     2.684389294338169196e-01,1.169829733724700449e-01
#@markdown     2.965593410629969173e-01,1.523801581863939436e-01
#@markdown     3.246797526921769150e-01,2.590033856137013424e-01
#@markdown
!rm *.csv 2> /dev/null
uploaded = files.upload()

for fn in uploaded.keys():
  csv_filename = fn
  print(f'You have uploaded file "{csv_filename}" with length {len(uploaded[fn])} bytes')
print('Execution finished.')

# Commented out IPython magic to ensure Python compatibility.
from compute_trajectoid_in_colab import *
from bisect import bisect_left
from scipy.interpolate import interp1d
# %matplotlib inline
#@markdown # <-- Press this "Play" button after you've selected the parameters below
#@markdown ### Here you select you path:
#@markdown If you want it to be based on your drawing, select "drawing". If you supplied a CSV file with a list of X,Y coordinates (see above), select "csv file". Otherwise, path will be randomly generated by default.
source_of_path = 'randomly generated' #@param ["csv file", "drawing", "randomly generated"]

# csv_filename = 'path_coordinates.csv'

#@markdown ### Optional settings (you may leave these at default values)
#@markdown When this checkbox is selected, relative scale of path and its trajectoid will be searched automatically.
auto_scale_range = True #@param {type:"boolean"}

#@markdown If `auto_scale_range` parameter is not checked, the following will be the minimum and maximum values of the scales. Only one trajectoid solution must lie between them.
manual_scale_min = 0.5 #@param {type:"number"}
manual_scale_max = 0.7 #@param {type:"number"}

#@markdown If you choose to generate random path, this number will be used as seed for the random number generator. Change it to get different paths.
random_seed = 0 #@param {type:"number"}

def plot_gb_areas(ax, sweeped_scales, gb_areas, mark_one_scale, scale_to_mark, length_of_path, x_limit_of_curve=None):
    ii = np.searchsorted(sweeped_scales, scale_to_mark)
    gb_areas = np.insert(gb_areas, ii, np.pi * np.sign(interpolate.interp1d(sweeped_scales, gb_areas)(scale_to_mark)))
    sweeped_scales = np.insert(sweeped_scales, ii, scale_to_mark)
    xfactor = length_of_path/(2*np.pi)
    if x_limit_of_curve is None:
        ax.plot(sweeped_scales * xfactor, gb_areas)
    else:
        last_index = bisect_left(sweeped_scales, x_limit_of_curve)
        ax.plot(sweeped_scales[:last_index] * xfactor, gb_areas[:last_index])
    ax.axhline(y=np.pi, color='black', alpha=0.5)
    ax.axhline(y=0, color='black', alpha=0.3)
    ax.axhline(y=-1 * np.pi, color='black', alpha=0.5)
    if mark_one_scale:
        value_at_scale_to_mark = interp1d(sweeped_scales, gb_areas, fill_value='extrapolate')(scale_to_mark)
        ax.scatter([scale_to_mark * xfactor], [value_at_scale_to_mark], s=20, color='red')
    ax.set_yticks([-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi])
    ax.set_yticklabels(['-2π', '-π', '0', 'π', '2π'])
    ax.set_ylim(-np.pi * 2 * 1.01, np.pi * 2 * 1.01)
    ax.set_ylabel('Norm. spherical\narea $S(r)/r^2$')
    ax.set_xlabel('Path\'s scale $\sigma = L/(2 \pi r)$')



target_folder = ''
if source_of_path == 'randomly generated':
    input_path_single_section = make_random_path(seed=random_seed, make_ends_horizontal=False,
                                             start_from_zero=True,
                                             end_with_zero=True, amplitude=3)
elif source_of_path == 'drawing':
    input_path_single_section = get_trajectory_from_raster_image('my_drawing.png',
                                                                 do_plotting=False)
    plt.plot(input_path_single_section[:, 0], input_path_single_section[:, 1],
             color='black')
    plt.axis('equal')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.title('Path obtained from your drawing')
    plt.show()
elif source_of_path == 'csv file':
    input_path_single_section = np.genfromtxt(csv_filename, delimiter=',')
    xs = input_path_single_section[:, 0]
    ys = input_path_single_section[:, 1]
    xs = xs - xs[0]
    ys = ys - ys[0]
    ys = ys - xs * (ys[-1] - ys[0]) / (xs[-1] - xs[0])
    input_path_single_section[:, 0] = xs
    input_path_single_section[:, 1] = ys
    plt.plot(input_path_single_section[:, 0], input_path_single_section[:, 1],
             color='black')
    plt.axis('equal')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.title('Path obtained from your CSV file')
    plt.show()

input_path_0 = double_the_path(input_path_single_section, do_plot=False)

do_plot = True
minscale = 0.01
#@markdown Maximum scale attempted by automatic search. Increase only if error indicates so.
upper_limit_of_auto_search = 10 # @param {type:"number"}
nframes = 300

fig, ax = plt.subplots()

sweeped_scales, gb_areas = gb_areas_for_all_scales(input_path_single_section,
                                                   minscale=minscale, maxscale=upper_limit_of_auto_search,
                                                    nframes=nframes, adaptive_sampling=True)
if auto_scale_range:
    print('Automatic search for scale factor...')
    index_where_area_crosses_pi = np.argmax(np.abs(gb_areas) > np.pi)
    if index_where_area_crosses_pi == 0:
        print('Automatic range of scales is too short. Increase the upper limit.')
    range_for_searching_the_roots = [sweeped_scales[index_where_area_crosses_pi - 2],
                                      sweeped_scales[index_where_area_crosses_pi + 1]]
    best_scale = minimize_mismatch_by_scaling(input_path_0, scale_range=range_for_searching_the_roots)
    if not best_scale:
        print('Range of scales is wrong. Try manual range instead of auto.')
    length_of_path = length_of_the_path(input_path_single_section)
    plot_gb_areas(ax, sweeped_scales, gb_areas, mark_one_scale=True,
                          scale_to_mark=best_scale, length_of_path=length_of_path)

else:
    best_scale = minimize_mismatch_by_scaling(input_path_0,
                                              scale_range=[manual_scale_min, manual_scale_max])

print(f'Scale factor σ=L/2πr that yields trajectoid: {best_scale * length_of_path/(2*np.pi)}')

input_path = best_scale * input_path_0

# fig2 = plt.figure(2)
plot_three_path_periods(input_path, plot_midpoints=True, savetofile=target_folder + '/input_path')
plt.gca().set_title('Several periods of the target path')

## Make cut meshes for trajectoid
compute_shape(input_path, kx=1, ky=1,
              folder_for_path=target_folder + 'folder_for_path',
              folder_for_meshes=target_folder + 'cut_meshes',
              core_radius=1, cut_size = 10)

number_of_boxes = input_path.shape[0]

print("Execution finished.")

"""# Step 3. Generate the shape of the trajectoid"""

#@title ## ↓↓↓ Press this button after setting the parameters below. Be patient: execution can take several minutes.

#@markdown ### Parameters of the trajectoid shape to be generated (leave them at default values if you are going to use 1"-diameter steel ball as an insert):

#@markdown Diameter of inner cavity in millimeters (e.g. diameter of your ball bearing):
diameter_of_inner_cavity = '25.4'#@param {type:"string"}

#@markdown Minimum diameter of trajectoid in millimeters (corresponds to value of 2r in the research article):
min_diameter_of_trajectoid = '31.75' #@param {type:"string"}

#@markdown Maximum diameter of trajectoid in millimeters (corresponds to value of 2R in the research article):
max_diameter_of_trajectoid = '41.275' #@param {type:"string"}

cavity_r = float(diameter_of_inner_cavity)/float(min_diameter_of_trajectoid)
outer_geosphere_R = float(max_diameter_of_trajectoid)/float(min_diameter_of_trajectoid)
# print(f'r: {cavity_r}, R: {outer_geosphere_R}')

trajectoid_oscad = """masterscale=$masc;

module cutter_cube(i) {
    import(str("/content/cut_meshes/test_",i,".stl"));
}

module geosphere(radius) {
    scale([radius, radius, radius]) import("/content/unit_geosphere.stl");
}

module cube_for_halving() {
    translate([-10,0,-10]) cube(size = [20, 20, 20], center = false);
}

scale([masterscale, masterscale, masterscale]) difference() {
    geosphere(radius=$outergeorad);
    geosphere(radius=$innergeorad);
    cube_for_halving();
    for (i =[0:$numberofboxes]) cutter_cube(i);
    // cutter_cube(0);
    // cutter_cube(189);
}
""".replace('$numberofboxes', str(number_of_boxes))\
.replace('$innergeorad', str(cavity_r))\
.replace('$outergeorad', str(outer_geosphere_R))\
.replace('$masc', str(float(min_diameter_of_trajectoid)/2))

print('Calculating the left half of the shape...')
r.render(trajectoid_oscad, outfile='trajectoid_half_left.stl')

print('Calculating the right half of the shape...')
r.render(trajectoid_oscad.replace('translate([-10,0,-10])',
                                  'translate([-10,-20,-10])'),
         outfile='trajectoid_half_right.stl')

print("Execution finished.")

#@title ## ↓↓↓ Press this button to view the trajectoid shape (left half will be opaque, right half -- semitransparent)
import plotly.graph_objects as go
import open3d as o3d
mesh = o3d.io.read_triangle_mesh("trajectoid_half_left.stl")
if mesh.is_empty(): exit()

if not mesh.has_vertex_normals(): mesh.compute_vertex_normals()
if not mesh.has_triangle_normals(): mesh.compute_triangle_normals()

triangles = np.asarray(mesh.triangles)
vertices = np.asarray(mesh.vertices)
colors = None
if mesh.has_triangle_normals():
    colors = (0.5, 0.5, 0.5) + np.asarray(mesh.triangle_normals) * 0.5
    colors = tuple(map(tuple, colors))
else:
    colors = (1.0, 0.0, 0.0)

mesh2 = o3d.io.read_triangle_mesh("trajectoid_half_right.stl")
if mesh2.is_empty(): exit()

if not mesh2.has_vertex_normals(): mesh2.compute_vertex_normals()
if not mesh2.has_triangle_normals(): mesh2.compute_triangle_normals()

triangles2 = np.asarray(mesh2.triangles)
vertices2 = np.asarray(mesh2.vertices)
colors2 = None
if mesh2.has_triangle_normals():
    colors2 = (0.5, 0.5, 0.5) + np.asarray(mesh2.triangle_normals) * 0.5
    colors2 = tuple(map(tuple, colors2))
else:
    colors = (1.0, 0.0, 0.0)

fig = go.Figure(
    data=[
        go.Mesh3d(
            x=vertices[:,0],
            y=vertices[:,1],
            z=vertices[:,2],
            i=triangles[:,0],
            j=triangles[:,1],
            k=triangles[:,2],
            facecolor=colors,
            opacity=1),
        go.Mesh3d(
            x=vertices2[:,0],
            y=vertices2[:,1],
            z=vertices2[:,2],
            i=triangles2[:,0],
            j=triangles2[:,1],
            k=triangles2[:,2],
            facecolor=colors2,
            opacity=0.5)
    ],
    layout=dict(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        )
    )
)
fig.show()
print('Execution finished.')

"""# Step 4. Download .STL files for 3D printing"""

#@title ↓↓↓ press this button to download a .ZIP archive with .STL files of both halves of the trajectoid
import glob
from zipfile import ZipFile

zippydizipzapfile = ZipFile('trajectoid_STL_files_for_3D_printing.zip', 'w')

for name in ['trajectoid_half_left.stl', 'trajectoid_half_right.stl']:
  zippydizipzapfile.write(name)
zippydizipzapfile.close()

files.download('trajectoid_STL_files_for_3D_printing.zip')

"""# Step 5. Use a 3D printer to manufacture the trajectoid.

### Some tips for troubleshooting 3D printing and experiments:

Before you attempt to print trajectoids,
make sure that you are able to 3D print and assemble a sufficiently precise sphere of diameter equal to the `min_diameter_of_trajectoid` parameter (above) and having a concentric spherical cavity housing a steel ball of diameter equal to the `diameter_of_inner_cavity` parameter above (25.4 mm by default for 1-inch ball of a ball bearing). Assemble your test sphere from two halfes, with steel ball inserted into the inner cavity, and test how the assembly rolls. If your test sphere does not roll satisfactorily down a 0.5-degree slope, your trajectoids will not work, either.

If maximum angle `β_max` between gravity projection and your trajectoid's path directions is large -- close to 90 degrees -- then
your test sphere must perform good at even smaller slopes for your trajectoid to perform well.
More specifically, if you intend to run your trajectoid on a slope having angle `α`, then your test sphere must be capable
of performing at slope `γ = α * cos(β_max)`, assuming that α is small.

If your test sphere gets "stuck" at certain orientations instead of rolling down continuously,
your trajectoids will have the same problem too.
Typically, there are two possible reasons of test sphere's poor performance:

* Your ball bearing is not positioned concentrically with the outer 3D printed surface.
* Your outer surface is not spherical -- probably it's an ellipsoid instead.

Make appropriate corrections to your 3D printer calibration (or to scales along X, Y, and Z axes) until you succeed in
manufacturing a test sphere with satisfactory rolling performance.

"""