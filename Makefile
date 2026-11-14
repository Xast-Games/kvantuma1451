.PHONY: all fonts images clean

all: fonts images

fonts:
	fontforge -lang=py -script scripts/build.py

images:
	python3 scripts/render.py

clean:
	rm -f fonts/*/KVANTUMA1451.* images/*.png
