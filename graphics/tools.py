from PIL import Image

# Convert an image to an 8-bit palette image with the OpenTTD palette
# Conventional conversion would be source.quantize(palette=[openttdpalette], dither=False)
# DON'T EVER USE THAT! There is a bug which leads to clipping of r, g or b values to 252 prior to palette index assignment
# ... plus, I think mine looks nicer
def openttd_palettise(source):
	r = [0,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,52,68,88,108,132,156,176,204,48,64,80,96,120,148,176,204,72,88,104,124,152,184,212,244,64,88,112,136,160,188,204,220,236,252,252,252,252,76,96,116,136,156,176,196,68,96,128,156,184,212,232,252,252,252,32,64,84,108,128,148,168,184,196,212,8,16,32,48,64,84,104,128,28,44,60,80,104,128,152,180,16,32,56,76,96,120,152,184,32,56,72,88,104,124,140,160,76,96,116,136,164,184,204,212,224,236,80,100,120,140,160,184,36,48,64,80,100,132,172,212,40,64,88,104,120,140,160,188,0,0,0,0,0,24,56,88,128,188,16,24,40,52,80,116,156,204,172,212,252,252,252,252,252,252,72,92,112,140,168,200,208,232,60,92,128,160,196,224,252,252,252,252,252,252,252,252,204,228,252,252,252,252,8,12,20,28,40,56,72,100,92,108,124,144,224,200,180,132,88,244,245,246,247,248,249,250,251,252,253,254,255,76,108,144,176,210,252,252,252,252,252,252,252,64,255,48,64,80,255,32,36,40,44,48,72,100,216,96,68,255]
	g = [0,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,60,76,96,116,140,160,184,208,44,60,76,92,120,148,176,204,44,60,80,104,132,160,188,220,0,4,16,32,56,84,104,132,156,188,208,232,252,40,60,88,116,136,156,180,24,44,68,96,120,156,184,212,248,252,4,20,28,44,56,72,92,108,128,148,52,64,80,96,112,132,148,168,52,68,88,104,124,148,176,204,52,72,96,116,136,164,192,220,24,28,40,52,64,84,108,128,40,52,68,84,96,112,128,148,168,188,28,40,56,76,100,136,40,52,64,80,100,132,172,212,20,44,64,76,88,104,136,168,24,36,52,72,96,120,144,168,196,224,64,80,96,112,140,172,204,240,52,52,52,100,144,184,216,244,20,44,68,100,136,176,184,208,0,0,0,0,0,0,0,80,108,136,164,192,220,252,136,144,156,176,196,216,24,36,52,68,92,120,152,172,156,176,200,224,244,236,220,188,152,0,0,0,0,0,0,0,0,0,0,0,0,24,44,72,108,146,60,84,104,124,148,172,196,0,0,48,64,80,255,68,72,76,80,84,100,132,244,128,96,255]
	b = [255,16,32,48,64,80,100,116,132,148,168,184,200,216,232,252,72,92,112,132,152,172,196,220,4,12,20,28,64,100,132,168,4,20,44,72,92,120,148,176,4,16,32,52,76,108,124,144,164,192,0,60,128,0,8,28,56,80,108,136,0,4,8,16,24,32,16,0,128,192,0,8,16,28,40,56,76,88,108,128,0,0,4,4,12,20,28,44,24,32,48,60,76,92,108,124,24,44,72,88,108,136,168,200,0,0,4,12,24,44,64,88,16,24,40,56,64,80,96,112,128,148,4,20,40,64,96,136,68,84,100,116,136,164,192,224,112,144,172,196,224,252,252,252,108,132,160,184,212,220,232,240,252,252,96,108,120,132,160,192,220,252,52,52,52,88,124,160,200,236,112,140,168,196,224,248,255,252,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,4,0,48,100,152,88,104,124,140,164,188,216,224,52,64,76,92,252,248,236,216,172,244,245,246,247,248,249,250,251,252,253,254,255,8,24,52,84,126,0,0,0,0,0,0,0,0,0,0,0,0,0,112,116,120,124,128,144,168,252,164,140,255]

	source = source.convert("RGB")
	target = Image.new("P", source.size)
	palette_dict = {}
	palette = []
	for i in range(len(r)):
		key = str(hex(r[i])) + str(hex(g[i])) + str(hex(b[i]))
		palette_dict[key] = i
		palette.append(r[i])
		palette.append(g[i])
		palette.append(b[i])
	target.putpalette(palette)
	for x in range(source.size[0]):
		for y in range(source.size[1]):
			pr, pg, pb = source.getpixel((x, y))
			key = str(hex(pr)) + str(hex(pg)) + str(hex(pb))
			if key in palette_dict:
				target.putpixel((x, y), palette_dict[key])
			else:
				dist = 255 * 255 * 255
				index = 0
				for i in range(len(r)):
					d = (pr - r[i]) * (pr - r[i]) + (pg - g[i]) * (pg - g[i]) + (pb - b[i]) * (pb - b[i])
					if d < dist:
						dist = d
						index = i
				target.putpixel((x, y), index)
	return target