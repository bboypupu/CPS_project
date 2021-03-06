from PIL import Image, ImageDraw, ImageFont
import os
import argparse
import shutil

parser = argparse.ArgumentParser(description='Mark or crop each annotation.',
			epilog='This program will create a directory called \'annotations\' and save the output there. The directory will be created in the folder where the annotation file is located. If the directory exists already, that will be used, and any existing files will be overwritten.')
parser.add_argument('mode', choices=['copy', 'mark', 'blackout', 'crop'], type=str, help='Copy will copy the frames with no alterations, mark will mark the annotation with a red box, blackout will black out the annotation, and crop will only save the annotation as a small image.')
parser.add_argument('path', metavar='filename.csv', type=str, help='The path to the csv-file containing the annotations.')
parser.add_argument('-f', '--filter', metavar='acceptedTag', type=str, help='If given, only annotations with this tag will be processed.')
parser.add_argument('-c', '--category', metavar='category', type=str, help='If given, the file categories.txt will be loaded and only signs with a tag that belongs to the given category are processed. categories.txt should be formatted with one category on each line in the format categoryName: tag1[, tag2, ... tagN]. It must be placed in the working directory.')
parser.add_argument('-m', '--margin', metavar='5', type=int, default=0, help='Add a margin around the crop/box/blackout equivalent to a percentage of the annotation\'s width/height. Ignored if mode is copy.')
parser.add_argument('-a', '--attributeOn', metavar='occluded', type=str, help='If given, only annotations with this attribute set to true will be processed.')
parser.add_argument('-o', '--attributeOff', metavar='occluded', type=str, help='If given, only annotations with this attribute set to false will be processed.')

args = parser.parse_args()

if not os.path.isfile(args.path):
	print("The given annotation file does not exist.\nSee annotateVisually.py -h for more info.")
	exit()
	
if args.category != None and not os.path.isfile('categories.txt'):
	print("Error: A category was given, but categories.txt does not exist in the working directory.\nTo use this functionality, create the file with a line for each category in the format\ncategoryName: tag1[, tag2, ... tagN]")
	exit()

categories = {}
if args.category != None:
	categories = {k.split(':')[0] : [tag.strip() for tag in k.split(':')[1].split(',')] for k in open('categories.txt', 'r').readlines()}
	if args.category not in categories:
		print("Error: The category '%s' does not exist in categories.txt." % args.category)
		exit()

csv = open(os.path.abspath(args.path), 'r')
header = csv.readline().split(";")
if args.attributeOn != None and args.attributeOn not in header:
        print("Error: The attribute '%s' does not exist in %s." % (args.attributeOn, args.path))
        exit()

if args.attributeOff != None and args.attributeOff not in header:
        print("Error: The attribute '%s' does not exist in %s." % (args.attributeOff, args.path))
        exit()

onAttributes = []
if args.attributeOn != None:
        onAttributes.append(header.index(args.attributeOn))

offAttributes = []
if args.attributeOff != None:
        offAttributes.append(header.index(args.attributeOff))

print args.attributeOn
print header
print onAttributes
        
csv = csv.readlines()
csv.sort()

basePath = os.path.dirname(args.path)
savePath = os.path.join(basePath, 'annotations')
if not os.path.isdir(savePath):
	os.mkdir(savePath)

font = ImageFont.load_default()

im = Image.new('RGB', (1,1))
counter = 0
previousFile = ''
for line in csv:
	fields = line.split(";")
	
	if args.filter != None and args.filter != fields[1]:
		continue
		
	if args.category != None and fields[1] not in categories[args.category]:
		continue

        if len(onAttributes) > 0:
                skipAnnotation = False
                for a in onAttributes:
                        if fields[a] != "1":
                                skipAnnotation = True
                if skipAnnotation:
                        continue

        if len(offAttributes) > 0:
                skipAnnotation = False
                for a in offAttributes:
                        if fields[a] != "0":
                                skipAnnotation = True
                if skipAnnotation:
                        continue
	
	if args.mode == 'copy':
		shutil.copy(os.path.join(basePath, fields[0]), savePath)
		print(os.path.join(savePath, fields[0]))
		counter += 1
		continue
		
	width = int(fields[4])-int(fields[2]);
	height = int(fields[5])-int(fields[3]);
	box = [int(fields[2])-width*args.margin/100, int(fields[3])-height*args.margin/100, int(fields[4])+width*args.margin/100, int(fields[5])+height*args.margin/100]
	
	if fields[0] != previousFile and args.mode != 'crop': # Save the drawn annotations and open the next file (crop opens its own images).
		im = Image.open(os.path.join(basePath, fields[0]))
	
	draw = ImageDraw.Draw(im)
	if args.mode == 'blackout':
		draw.rectangle(box, outline=(0,0,0), fill=(0,0,0));
	elif args.mode == 'mark':
		draw.rectangle(box, outline=(255,0,0));
		
		textSize = font.getsize(fields[1])
		draw.rectangle([int(fields[2]), int(fields[3])-textSize[1]-4, int(fields[2])+textSize[0]+2, int(fields[3])-1], outline=(0,0,0), fill=(0,0,0));
		draw.text((int(fields[2])+2, int(fields[3])-textSize[1]-2), fields[1], font=font)
	elif args.mode == 'crop':
		im = Image.open(os.path.join(basePath, fields[0])) # When cropping, the full image should always be opened.
		im = im.crop(box)
	
	if args.mode == 'crop':
		tag_name = fields[1]
		class_name = -1
		if tag_name == 'speedLimit25':
			class_name = 0
		elif tag_name == 'speedLimit30':
			class_name = 1
		elif tag_name == 'speedLimit35':
			class_name = 2
		elif tag_name == 'speedLimit40':
			class_name = 3
		elif tag_name == 'speedLimit45':
			class_name = 4
		elif tag_name == 'speedLimit50':
			class_name = 5
		elif tag_name == 'speedLimit55':
			class_name = 6
		elif tag_name == 'speedLimit65':
			class_name = 7
		elif tag_name == 'stop':
			class_name = 8
		elif tag_name == 'stopAhead':
			class_name = 9
		elif tag_name == 'slow':
			class_name = 10
		elif tag_name == 'pedestrianCrossing':
			class_name = 11
		elif tag_name == 'school':
			class_name = 12
		elif tag_name == 'schoolSpeedLimit25':
			class_name = 13


		filename = os.path.join(savePath, '$%d$%s' % (class_name, os.path.basename(fields[0])))
	else:
		filename = os.path.join(savePath, os.path.basename(fields[0]))
	im.save(filename)
	print(filename)
	
	previousFile = fields[0]
	counter += 1

print("Done. Processed %d annotations." % (counter+1))
