# Social Distancing
This algorithm solves the problem of how many people fit and where they should be placed in a defined space so that a certain distance is kept between them. An approach is to represent each person as a circle, the radius of which is the minimum distance that should be kept.
## Usage
```bash
python social_distancing.py [-i ITEMS]
                            [-r RADIUS]
                            [--min_radius MIN_RADIUS]
                            [--max_radius MAX_RADIUS]
                            [-b BOUNDARY_FILE]
                            [-s SEED]
                            output_file
```
where:
* <b>-i ITEMS, --items ITEMS</b>: Number of circles to be inserted.
* <b>-r RADIUS, --radius RADIUS</b>: A common radius for all circles.
* <b>--min_radius</b>: The minimum radius for pseudorandomly generated circles
* <b>--max_radius</b>: The maximum radius for pseudorandomly generated circles
* <b>-b BOUNDARY_FILE, --boundary_file BOUNDARY_FILE</b>: A file containing coordinations of the boundary of the area.(The .txt files in this repository are some examples).
* <b>-s SEED, --seed SEED</b>: The seed for the pseudorandom numbers generator.
* <b>output_file</b>: The file where the coordinations of circles are saved in form: x y r
## More information
To read the full description of the assignment click [here](https://github.com/dmst-algorithms-course/assignment-2020-3). You can also find 2 scripts with instructions in order to visualize the results.
