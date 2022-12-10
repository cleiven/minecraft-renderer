from colormap import generate_palette
from iso_render import project_2d
import json
import os
from os.path import exists
from PIL import Image
import anvil
import numpy as np
import logging


#def write_colormap(directory):
    #with open(f"colors.json","w") as f:
        #json.dump(generate_palette(directory),f,indent=2)

def main():
    if not exists("colors.json"):
        logging.info("No colors.json file found! You can create one and define colors like so: \n \
        {""block id"":  [r,g,b,a], ... } ")

    with open("colors.json","r") as f:
        colors = json.load(f)
        im = Image.new(size = (1000,1000), mode = "RGB")

        region_files = [file for file in os.listdir() if file.endswith(".mca")]
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
                                    point = project_2d((x+((16*chunk_x)+(32*region_x)),y,z+((16*chunk_z)+(32*region_z))),t=3,center=(100,100)) # Seems to break with angles besides 90deg
                                    im.putpixel(point,color)
                                except Exception as e:
                                    print(e)
                                    continue
                    #im.save(f"2debug-{region_x}.{region_z}mca:{chunk_x}.{chunk_z}-{i}.png")
                #im.save(f"2debug-{region_x}.{region_z}mca:{chunk_x}.{chunk_z}-{i}.png")
        im.save("result.png")
if __name__ == "__main__":
    main()
