# Introduction
SpinWiz provides an intuitive interface that enables you to set up camera motion, lighting, and animation for one or more objects in just a few clicks.

Please refer to this video for a quick intro tutorial

# Features Overview

### Quick Turntable Setup:
Use built-in options for object or camera rotation to create a turntable animation in a few clicks. You can define the direction, speed, and duration of the animation.

### Multiple Animation Setups: 
Create and manage multiple animation setups within the same scene. Each setup can have its own unique camera and motion settings, allowing you to capture different views or angles of the same object.

### Stage and Lighting Options:
Quickly add a stage with a preset shader and a basic lighting setup using an HDRI environment. These features are designed to give your models a professional look right out of the box, reducing the time needed for scene preparation.

### Batch Rendering: 
Add multiple setups to an output queue for batch rendering. This feature is ideal for automating the rendering process when you have several setups to render, eliminating the need for manual intervention.

# Installation

Purchase, download and save the .zip file (SpinWiz_1.0) to a location on your computer.

Install in Blender:

Open Blender and go to the Edit menu.
Select Preferences and navigate to the Add-ons tab.
Click on the Install… button located at the top right corner.
Locate the downloaded .zip file for SpinWiz and select it.
Once the add-on is installed, enable it by checking the box next to SpinWiz in the add-on list.

Verify Installation:

After enabling SpinWiz, a new panel named SpinWiz should appear in the 3D Viewport under the N panel (press N to toggle it if it is not visible).

# Update

SpinWiz includes a built-in updater that allows you to keep the add-on up to date with the latest features and bug fixes. 
Update Directly to Main: Instantly download and install the latest version of SpinWiz directly from the main branch.

# Setting up a Turntable Animation

To create a new SpinWiz setup for an object or multiple objects in your scene:

Select the Object(s): In the 3D Viewport, select the object or multiple objects you want to include in the turntable animation. You can select  multiple objects using the Shift key.


Go to the SpinWiz panel located in the N panel (press N to toggle it if it is not visible).

Press the Set up for Selected Object(s) button. This will automatically create a new SpinWiz setup for the selected items, including a camera, keyframes and other default settings. This setup will be created in a new collection that is named based on the active selected object.

![Setup](https://github.com/GrasSoft/360_ez_spinner/blob/main/screenshots/01_setup.png?raw=true)

This collection will then be used as the basis for configuring camera settings, animation options, and output configurations in the subsequent steps. 
The original object(s) will remain intact in the scene, while the setup will include duplicate(s) of it.

# Setting up multiple Turntable Animations

This simple setup process can be applied multiple times to different objects in your scene. Once a new setup is created, it will appear as a separate collection in your scene. 

The visibility of collections is automatically managed by SpinWiz for convenience. The setup you are currently working on is the only one automatically made visible in the viewport.

# Switching between Setups

To switch between multiple setups, you can use the dropdown at the top.

![Switch between selections](https://github.com/GrasSoft/360_ez_spinner/blob/main/screenshots/02_switch.png?raw=true)

You can also simply click on one of the objects from a setup in the Outliner. This will reveal the collection in question and hide the others.

# Copying/Pasting between Setups

SpinWiz makes it easy to apply the same animation and camera settings across multiple setups in your scene using the Copy/Paste functionality:

Copy Settings: The button on the left (with an arrow pointing up) allows you to copy the current setup's configuration, including camera settings, animation parameters, stage options, and lighting settings.

Paste Settings: The button on the right (with an arrow pointing down) lets you paste the copied configuration to another selected setup in the scene. 

Using these buttons, you can quickly transfer settings from one setup to another, streamlining the process of configuring multiple objects or collections with similar animations and camera parameters.

# Camera Options

Current Camera: Displays the name of the active camera that will be used for the current animation setup.

Camera Height
Adjusts the vertical position of the camera relative to the object. 

Target Height
Sets the height of the focus point relative to the object. This determines where the camera is aiming and helps ensure that the object is centered in the frame throughout the animation.


Focal Length
Modifies the focal length of the camera, which affects how zoomed in or out the view appears.

Distance
Defines the distance between the camera and the object. This setting works in conjunction with the focal length to determine how the object is displayed in the frame. A shorter distance brings the camera closer to the object, while a greater distance moves it further away, affecting both perspective and framing.

# Animation Options

The Animation Options panel provides you with control over how the turntable animation is set up and executed. These settings determine the movement type, spin direction, interpolation method, and duration of the animation.

![Animation](https://github.com/GrasSoft/360_ez_spinner/blob/main/screenshots/03_animation.png?raw=true)

Movement Type
Allows you to select the type of movement for the turntable animation:
Object Rotates: The object itself rotates around its axis while the camera remains stationary.
Camera Rotates: The camera rotates around the object, providing a 360° view of the object without changing the object’s position.

Spin Direction
Defines the direction in which the object or camera rotates:
Clockwise: The object or camera spins in a clockwise direction.
Counter-clockwise: The object or camera spins in a counter-clockwise direction.
Interpolation


Determines how the animation transitions between keyframes. Options include:
Smooth/Linear: The object moves at a constant speed.
Slow-Fast-Slow: The object’s speed varies, moving slowly at the beginning, then progressively faster, then slowing down again towards the end of the animation.
Fast-Slow-Fast: The object’s speed varies, moving fast at the beginning, then slowing down, then speeding back up towards the end of the animation.


Length
Specifies the duration of the animation in one of two ways:
By Number of Keyframes: Allows you to manually set the number of frames and the starting frame. This method is ideal when you have a specific number of frames in mind or want to synchronize the animation with other elements in the scene.
By Degrees: Lets you control the animation length based on the number of degrees the object should rotate between two frames. The user can set the number of degrees (e.g., 2, 5, 10) and SpinWiz will automatically calculate the number of frames required for a full 360° rotation based on this value.

# Add Stage

This option in SpinWiz allows you to quickly add a stage beneath the object for which the setup is made. The stage is automatically positioned so that the bottom of the object touches the stage, ensuring the object appears grounded and centered. Also, the shape of the stage changes such that it encompasses both the object and the camera.

![Add stage setup](https://github.com/GrasSoft/360_ez_spinner/blob/main/screenshots/04_addstage.png?raw=true)

Stage Height: Sets the height of the stage. Adjust this value to control the stage’s vertical size, which affects the perceived scale and prominence of the object on the stage.

Subdivisions: Determines the number of subdivisions in the stage geometry. 


Stage Material
Material Color: Defines the base color of the stage. Click on the color swatch to open a color picker and choose the desired color.

Roughness: Controls the roughness of the stage material. Lower values make the stage surface smoother and more reflective, while higher values produce a more matte finish.

Reflection Intensity: Adjusts the intensity of reflections on the stage surface. Higher values result in stronger reflections, which can create a mirror-like effect depending on the roughness setting.

Contact Shadow: Sets the intensity of the contact shadow beneath the object. This shadow helps visually ground the object on the stage, providing a more realistic presentation.

# Add Lighting Setup

This option in SpinWiz allows you to quickly add an HDR environment that is suitable for a turntable type animation.

![Add lighting setup](https://github.com/GrasSoft/360_ez_spinner/blob/main/screenshots/05_addlighting.png?raw=true)

Gradient: Adds a simple gradient as an environment, allowing you control over its position and scale.
Studio HDR: Adds a Studio HDRI map (thanks to PolyHaven!), allowing you control over its rotation and strength.

# Send to Output Queue

Send to Output Queue adds the current Setup to the list of Setups to be batch rendered (the Output Queue).

### Output Setup Tab

Manage and configure the rendering order of your setups, as well as specify the file path where the rendered animations will be saved. This feature helps you organize the output process, ensuring that each setup is rendered in the desired sequence and saved to a location of your choice.

![Output Setup](https://github.com/GrasSoft/360_ez_spinner/blob/main/screenshots/06_outputsetup.png?raw=true)

Setup Order:

- The list displays all the setups that have been created for the current scene.
- Arrow Buttons: Use the up and down arrow buttons on the left side to change the order in which setups are rendered. This is useful for prioritizing certain setups or arranging the sequence of animations.
- Delete Button: Click the trash bin icon on the right to remove a setup from the list if it is no longer needed.

Output Path:

- The Output Path field allows you to set the directory where the rendered animations will be saved.
- Click on the Output Path button to open a file browser and select a directory. This ensures that all your rendered files are saved to a specified location for easy access and management.

Subfolders: SpinWiz creates a subfolder within the Output Path for each setup. The folder receives the same name as the Setup itself.

⚠️ Please note that the Output Setup does not override Blender’s output settings, so frames will also be saved at the location configured in the output tab. Most of the time, you will probably want the standard output to save the frames in the Temp folder.

