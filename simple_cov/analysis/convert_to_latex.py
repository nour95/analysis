import os
import subprocess


def to_latex(model_name):
    latex_dir = os.path.join("latex", model_name)
    os.makedirs(latex_dir, exist_ok=True)

    all_images = next(os.walk(f'images/{model_name}'))[2] 
    # print(all_images)

    for image_file in all_images:

        subprocess.run(['inkscape', '-D', f'images/{model_name}/{image_file}', 
                        '-o',  f'{latex_dir}/{image_file[:-4]}.pdf', 
                        '--export-latex'])


model_name = 'JavaNioServerSocket3'
to_latex(model_name)
print(f"Done with {model_name}")

model_name = 'ElevatorModel'
to_latex(model_name)
print(f"Done with {model_name}")

model_name = 'SimpleModel'
to_latex(model_name)
print(f"Done with {model_name}")
