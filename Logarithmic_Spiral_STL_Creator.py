import numpy as np
from stl import mesh

# Below code generated by chatGPT using the Question:
# write python code to create a 3d stl file with a logarithmic spiral that is 40 mm tall. with 7 turns and a flat logarithmic spiral that is 40 mm tall. with 7 turns at z = 40 mm and fill in the area between the two. Make both logarithmic spirals go from 5 mm thickness to 1 mm thickness



# Function to generate two sets of 3D logarithmic spiral points with tapering thickness
def generate_tapering_spiral_3d(a, b, height, thickness_start, thickness_end, num_points, turns, flat=False):
    theta = np.linspace(0, 2 * np.pi * turns, num_points)
    r = a * np.exp(b * theta)  # Logarithmic spiral formula in 2D
    
    # Thickness tapers linearly from thickness_start to thickness_end
    thickness = np.linspace(thickness_start, thickness_end, num_points)

    # Outer and inner spirals for thickness
    x_outer = (r + thickness / 2) * np.cos(theta)
    y_outer = (r + thickness / 2) * np.sin(theta)

    x_inner = (r - thickness / 2) * np.cos(theta)
    y_inner = (r - thickness / 2) * np.sin(theta)

    if flat:
        z = np.ones(num_points) * height  # Flat spiral at z = height
    else:
        z = np.linspace(0, height, num_points)  # Spiral growing along z

    return x_outer, y_outer, z, x_inner, y_inner

# Parameters for the logarithmic spiral
a = 0.1              # Scale factor for the spiral
b = 0.15             # Growth rate of the spiral
height = 40          # Height of the spiral in mm
thickness_start = 1  # Starting thickness in mm
thickness_end = 5    # Ending thickness in mm
num_points = 10000    # Number of points on the spiral
turns = 7            # Number of turns in the spiral

# Generate points for the lower spiral (extruding from z = 0 to z = 40 mm)
x_outer_lower, y_outer_lower, z_lower, x_inner_lower, y_inner_lower = generate_tapering_spiral_3d(
    a, b, height, thickness_start, thickness_end, num_points, turns)

# Generate points for the upper flat spiral (at z = 40 mm)
x_outer_upper, y_outer_upper, z_upper, x_inner_upper, y_inner_upper = generate_tapering_spiral_3d(
    a, b, height, thickness_start, thickness_end, num_points, turns, flat=True)

# Prepare the vertices and faces for the STL file
vertices = np.zeros((num_points * 4, 3))  # Outer and inner for both lower and upper spirals

# Lower spiral vertices (outer and inner)
vertices[:num_points, 0] = x_outer_lower
vertices[:num_points, 1] = y_outer_lower
vertices[:num_points, 2] = z_lower

vertices[num_points:num_points * 2, 0] = x_inner_lower
vertices[num_points:num_points * 2, 1] = y_inner_lower
vertices[num_points:num_points * 2, 2] = z_lower

# Upper spiral vertices (outer and inner, at z = 40 mm)
vertices[num_points * 2:num_points * 3, 0] = x_outer_upper
vertices[num_points * 2:num_points * 3, 1] = y_outer_upper
vertices[num_points * 2:num_points * 3, 2] = z_upper

vertices[num_points * 3:num_points * 4, 0] = x_inner_upper
vertices[num_points * 3:num_points * 4, 1] = y_inner_upper
vertices[num_points * 3:num_points * 4, 2] = z_upper

# Creating faces by connecting the lower and upper spirals to fill the area between them
faces = []

# Connect the outer and inner spirals between lower and upper spirals
for i in range(num_points - 1):
    # Outer surface connection between lower and upper spirals
    faces.append([i, i + 1, num_points * 2 + i])  # Lower outer to upper outer
    faces.append([i + 1, num_points * 2 + i + 1, num_points * 2 + i])  # Continue connection

    # Inner surface connection between lower and upper spirals
    faces.append([num_points + i, num_points + i + 1, num_points * 3 + i])  # Lower inner to upper inner
    faces.append([num_points + i + 1, num_points * 3 + i + 1, num_points * 3 + i])  # Continue connection

# Fill the top and bottom
for i in range(num_points - 1):
    # Top cap (at z = 40 mm) between the upper outer and upper inner
    faces.append([num_points * 2 + i, num_points * 2 + i + 1, num_points * 3 + i + 1])
    faces.append([num_points * 2 + i, num_points * 3 + i + 1, num_points * 3 + i])

    # Bottom cap (at z = 0) between the lower outer and lower inner
    faces.append([i, i + 1, num_points + i + 1])
    faces.append([i, num_points + i + 1, num_points + i])

# Convert faces to a numpy array
faces = np.array(faces)

# Create mesh object for STL
spiral_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

for i, face in enumerate(faces):
    for j in range(3):
        spiral_mesh.vectors[i][j] = vertices[face[j], :]

# Save the mesh as an STL file
spiral_mesh.save('logarithmic_spiral_tapered_filled_between.stl')

print("STL file created: logarithmic_spiral_tapered_filled_between.stl")
