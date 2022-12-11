from iso_render import Renderer
import json
import os
from os.path import exists
from PIL import Image
import anvil
import numpy as np
import logging
import argparse


#def write_colormap(directory):
    #with open(f"colors.json","w") as f:
        #json.dump(generate_palette(directory),f,indent=2)

def main():
    if not exists("colors.json"):
        logging.info("No colors.json file found! You can create one and define colors like so: \n \
        {""block id"":  [r,g,b,a], ... } ")


    parser = argparse.ArgumentParser()
    # Main params
    parser.add_argument('--out', type = str, help = 'Path for completed render.', default = 'output.png')
    parser.add_argument('--source', type = str, help = 'Path to region files to render (directory)', default = '.')
    parser.add_argument('--size', type = tuple, help = 'Dimensions of the output image', default = (1000,1000))

    # Renderer params
    parser.add_argument('--theta', type = float, help = 'Y rotation angle for render')
    parser.add_argument('--yscale', type = float, help = 'Y scale', default = -1)
    parser.add_argument('--xscale', type = float, help = 'X scale', default = -1)
    parser.add_argument('--zscale', type = float, help = 'Z scale', default = -0.5)
    parser.add_argument('--center', type = tuple, help = 'Where to center the rendered image (x,y)', default = (200,200))
    args = parser.parse_args()

    render = Renderer(args.theta,args.xscale,args.yscale,args.zscale)

    with open("colors.json","r") as f:
        colors = json.load(f)
        im = Image.new(size = args.size, mode = "RGB")
        print(args.source)
        region_files = [file for file in os.listdir(path=args.source) if file.endswith(".mca")]
        region_files.sort()
        print(region_files)
        for i, region_file in enumerate(region_files):
            print(f"reading {region_file}")
            # Does anvil-parser have built in functionality for this?
            region_x = int(region_file.split(".")[1])
            region_z = int(region_file.split(".")[2])
            region = anvil.Region.from_file(f'r.{region_x}.{region_z}.mca')
            for chunk_x in range(2):
                for chunk_z in range(2):
                    try:
                        chunk = anvil.Chunk.from_region(region,chunk_x,chunk_z)
                    except Exception as e:
                        print(e)
                        continue
                    for x in range(16):
                        for y in range(50,256):
                            for z in range(16):
                                block = chunk.get_block(x,y,z)
                                try:
                                    color = tuple(colors[block.id])
                                    point = render.project_2d((x+((16*chunk_x)+(32*region_x)),y,z+((16*chunk_z)+(32*region_z)))) # Seems to break with angles besides 90deg
                                    im.putpixel(point,color)
                                except Exception as e:
                                    print(e)
                                    continue
                    #im.save(f"2debug-{region_x}.{region_z}mca:{chunk_x}.{chunk_z}-{i}.png")
                #im.save(f"2debug-{region_x}.{region_z}mca:{chunk_x}.{chunk_z}-{i}.png")
        try:
            im.save(args.out)
        except:
            im.save(f"{args.out}.png")
if __name__ == "__main__":
    main()
