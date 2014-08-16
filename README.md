# How Fair are Major League Ball Parks?

## About

In the Fall of 2003 I participated in the COMPAPS High School Mathematical Competition in Modeling.  In this competition we told to look at different parks in major league baseball (which are in different location and have different dimensions) and address how fair.  For the compeitition my team addressed this with a model (EXPLAIN).  I have recently recast the orriginal C++ program in Python and have also addressed this same question using data analytic and sabermetric techniques.

> Consider the following major league baseball parks: Atlanta Braves, Colorado Rockies, New York Yankees, California Angles, Minnesota Twins, and Florida Marlins.  Each field is in a different location and has different dimensions. Are all these parks “fair”? Determine how fair or unfair is each park. Determine the optimal baseball “setting” for major league baseball.

## Usage

Simply run `./main <fields.txt` to execute the program.  `fields.txt` cotains  each ballpark the park's name, dimensions, wall heights, and
air resistance. Use `-n` to specify the number of at-bats per ballpark (defaults to 1000).

## Future Work

* When rewritting this program from C++ to Python I found a few errors.  I would like to find a way to debug the program to make sure it is running accurately.

* One interesting project would be to compare the simulation results to satistics.  One simple static is from [park factors][1].  This can be computed using home runs instead of runs.  This can be computed in SQL.

* Write up a summary of the simulation findings as well.